"""Stage 2.1c: naturalness filter + core-worthiness scoring, one batched pass.

For each grounded candidate this does two jobs in a single LLM judgment, so no
separate heavy triage call is needed later:
  1. keep-or-drop against a persona floor (drop insider-phrased, transcript-trivia,
     bare-factoid, or obscure-name questions);
  2. score the keepers 1-5 on core-worthiness (exemplary naturalness, trustworthy
     gold, substance, tier-fit), which the deterministic selection then ranks on.

The scorer sees the query, the code-derived signals (tier, observed_shape, chunk
and video counts), and a bounded sample of the actual grounded chunk texts (so it
can judge whether the answer is concretely supported). Chunk texts are resolved
from Postgres by id, so this pass needs the DB up (as grounding did).

Usage:
  uv run python -m eval.screen_queries --tiers factual --limit 30   # smoke
  uv run python -m eval.screen_queries                              # all tiers
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio

OUT_DIR = Path("eval/artifacts")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 8000
CALL_TIMEOUT = 150  # bound a batch call (adaptive thinking + rate-limit backoff) against a hang
BATCH = 15
EVIDENCE_CHUNKS = 4      # sample this many source chunks into the prompt
EVIDENCE_CHARS = 400     # cap each sampled chunk's text

SCREEN_SYSTEM = """\
You are curating evaluation questions for a research assistant that answers over one AI/ML YouTube creator's video library. For each candidate question, do two things.

1) Keep or drop it against a quality floor. DROP if it: references the source as if the reader had seen it ("this/these video(s)", "the creator", "both papers", "each study", "across these videos"); reads as transcript trivia or incidental metadata (exact dates, institution or author names, one-off slide numbers, precise hyperparameters); is a bare web-search factoid (user counts, market sizes, release dates, install commands); or names an obscure paper or system as if the reader already knows it. KEEP if a practitioner who has NOT seen the videos would plausibly type it as a standalone question.

2) If kept, score its core-worthiness from 1 to 5 (5 is best) as a headline, individually-adjudicated evaluation query, judging four things together: exemplary naturalness (reads like a real practitioner question); trustworthy, unambiguous gold (the provided evidence chunks concretely and definitely answer it); substantive and non-trivial (real room for a strong vs weak answer to differ; not trivially answerable, not vague); and tier-fit (genuinely factual, comparative, or longitudinal; for longitudinal, the answer needs a real trajectory across multiple videos). Give dropped items a score of 1.

Return one item per candidate: its id, keep flag, score, and a one-line reason."""


class ScoreItem(BaseModel):
    candidate_id: str
    keep: bool
    core_score: int
    reason: str


class ScoreBatch(BaseModel):
    items: list[ScoreItem]


def read_grounded(tier: str) -> list[dict]:
    path = OUT_DIR / f"query_grounded_{tier}.jsonl"
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in json.loads(ln):
            rows.append(json.loads(ln))
    return rows


def chunk_texts(cands: list[dict]) -> dict[str, str]:
    """chunk_id -> text for every source chunk across candidates (one DB read per video)."""
    needed: dict[str, set[str]] = {}
    for c in cands:
        for cid in c["source_chunk_ids"]:
            needed.setdefault(cid.rsplit(":", 1)[0], set()).add(cid)
    out: dict[str, str] = {}
    for vid, ids in needed.items():
        for ch in cio.video_chunks(vid):
            if ch["chunk_id"] in ids:
                out[ch["chunk_id"]] = ch["text"]
    return out


def _candidate_block(c: dict, ctext: dict[str, str]) -> str:
    videos = {cid.rsplit(":", 1)[0] for cid in c["source_chunk_ids"]}
    head = (f"[{c['candidate_id']}] tier={c['tier']} shape={c['observed_shape']} "
            f"chunks={len(c['source_chunk_ids'])} videos={len(videos)} leak={c.get('leak')}")
    lines = [head, f"Q: {c['query']}", "evidence:"]
    for cid in c["source_chunk_ids"][:EVIDENCE_CHUNKS]:
        lines.append(f"- {(ctext.get(cid, '') or '')[:EVIDENCE_CHARS]}")
    return "\n".join(lines)


async def score_batch(batch: list[dict], ctext: dict[str, str], sem) -> dict[str, ScoreItem]:
    body = "\n\n".join(_candidate_block(c, ctext) for c in batch)
    user = f"Candidates:\n\n{body}\n\nReturn one item per candidate id above."
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(SCREEN_SYSTEM, user, ScoreBatch, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "adaptive"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - a failed batch defaults to keep (below)
            print(f"  screen batch fail ({len(batch)} items): {type(e).__name__}: {e}")
            return {}
    valid = {c["candidate_id"] for c in batch}
    return {it.candidate_id: it for it in out.items if it.candidate_id in valid}


async def run_tier(tier: str, limit: int | None, concurrency: int) -> None:
    cands = read_grounded(tier)
    if limit:
        cands = cands[:limit]
    print(f"{tier}: screening {len(cands)} candidates")
    ctext = chunk_texts(cands)
    batches = [cands[i:i + BATCH] for i in range(0, len(cands), BATCH)]
    sem = asyncio.Semaphore(concurrency)

    scored: dict[str, ScoreItem] = {}
    tasks = [score_batch(b, ctext, sem) for b in batches]
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"screen {tier}"):
        scored.update(await coro)

    kept, n_drop, n_default = [], 0, 0
    drop_reasons = []
    for c in cands:
        it = scored.get(c["candidate_id"])
        if it is None:
            # omitted or whole-batch failure: default-keep at a neutral score (human is the backstop)
            n_default += 1
            kept.append({**c, "core_score": 3, "screen_reason": "(not scored; default-kept)"})
            continue
        if not it.keep:
            n_drop += 1
            if len(drop_reasons) < 20:
                drop_reasons.append({"query": c["query"], "reason": it.reason})
            continue
        kept.append({**c, "core_score": max(1, min(5, it.core_score)), "screen_reason": it.reason})

    kept.sort(key=lambda c: c["candidate_id"])
    path = OUT_DIR / f"query_scored_{tier}.jsonl"
    meta = {"_meta": {"tier": tier, "screen_model": MODEL, "batch": BATCH,
                      "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
                      "input": len(cands), "kept": len(kept),
                      "dropped": n_drop, "default_kept": n_default,
                      "drop_reasons_sample": drop_reasons}}
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for c in kept:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"  kept {len(kept)}/{len(cands)} (dropped {n_drop}, default-kept {n_default}) -> {path}")


async def amain(args: argparse.Namespace) -> None:
    for tier in (args.tiers or ["factual", "comparative", "longitudinal"]):
        await run_tier(tier, args.limit, args.concurrency)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", nargs="*", choices=["factual", "comparative", "longitudinal"])
    ap.add_argument("--limit", type=int, default=None, help="cap candidates per tier (smoke)")
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
