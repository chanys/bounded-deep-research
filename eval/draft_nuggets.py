"""Stage 3.1: draft gold-set nuggets + a reference answer per query (Claude-only).

For each locked query, hand Claude the FULL transcripts of the query's source
videos as one enumerated chunk listing (never the retriever, to keep the H1
dense-vs-hybrid comparison clean) and ask for the atomic facts a correct answer
must contain, each tagged vital / nice-to-have and each citing >=1 supporting
chunk, plus a reference answer synthesized from the cited evidence only.

Single model on purpose (decision with the user): all automated annotation is
Claude, so there is no cross-model agreement signal and the human adjudicates
every core nugget downstream. The random-audit error bound lives on the broad
layer (audit_goldset.py), not here.

Needs the DB up (transcript text): `make up` then the corpus restore.

Usage:
  uv run python -m eval.draft_nuggets --layer core --per-tier 2 --render eval/artifacts/gate_sample.md   # gate
  uv run python -m eval.draft_nuggets --layer core                       # full core
  uv run python -m eval.draft_nuggets --layer core --only-missing        # resume
  uv run python -m eval.draft_nuggets --layer broad                      # broad
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio
from eval.nugget_render import render_query_md

SUMMARIES_DEFAULT = Path("eval/artifacts/summaries_code4AI.jsonl")
INVENTORY_DEFAULT = Path("eval/artifacts/inventory_code4AI.json")
OUT_DIR = Path("eval/artifacts")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 8000    # nuggets + reference answer + adaptive thinking; bump if truncation
CALL_TIMEOUT = 180   # a 6-video longitudinal query is ~26k input tokens; give thinking room
TIERS = ["factual", "comparative", "longitudinal"]


# ---- output schema ---------------------------------------------------------

class Nugget(BaseModel):
    text: str
    importance: Literal["vital", "nice_to_have"]
    evidence_indices: list[int]  # indices into the presented chunk listing


class DraftOut(BaseModel):
    nuggets: list[Nugget]
    reference_answer: str


# ---- prompt (frozen; tied to the run by the git-SHA fingerprint) -----------

DRAFT_SYSTEM = """\
You are building the answer key for an evaluation of a research assistant that answers questions over one AI/ML YouTube creator's video library. For a single question, you are given the FULL transcripts of the source video(s) as a numbered list of ~30-second chunks (each line is "index: text"). Your job is to decompose what a CORRECT answer to the question must contain into atomic "nuggets", and to write a reference answer.

What a nugget is:
- One atomic, self-contained fact. Exactly one idea per nugget; never join two facts with "and". A reader must understand it on its own, without the question or other nuggets.
- A fact the answer needs, stated directly. Not meta-commentary about the video ("the transcript explains X"): state X itself.

Hard rules:
- Grounded: every nugget must be supported by the provided transcript. Cite the index (or indices) of the chunk(s) that state it in `evidence_indices`. Never use outside knowledge; if a fact you would expect is not in the transcript, leave it out. A nugget with no supporting chunk does not belong.
- Relevant: every nugget must directly help answer THIS question. A fact can be true and in the transcript yet off-topic; if it does not belong in a correct answer to the question, omit it.
- Atomic: split compound statements into separate nuggets. "Uses RL and improves accuracy by 12%" becomes two nuggets.
- Importance: tag each nugget `vital` if a correct answer is incomplete or misleading without it, or `nice_to_have` if it adds worthwhile detail but a correct answer could omit it.

Coverage: capture the facts a strong, complete answer genuinely needs, but do not pad. Typical questions need a handful of nuggets; a broad synthesis question (how a topic evolved) needs more, spanning the trajectory. Prefer a few vital nuggets over many marginal ones.

Reference answer: write a concise, correct answer to the question, synthesized ONLY from the cited evidence, in the informed explanatory tone this channel uses. It orients the human adjudicator; it is not scored against, so do not stuff it with every nugget.

Worked example. Question: "Why can adding more agents to a multi-agent system hurt performance?" Transcript chunks:
0: so when we add more agents each one introduces its own errors and those errors compound across the pipeline
1: and we found the coordination overhead grows faster than the benefit once you pass about five agents
2: the models were all evaluated on the standard reasoning benchmark suite
Good nuggets: {"text": "Each additional agent introduces its own errors, which compound across the system's pipeline.", "importance": "vital", "evidence_indices": [0]}; {"text": "Past roughly five agents, coordination overhead grows faster than the added benefit.", "importance": "vital", "evidence_indices": [1]}. Chunk 2 (which benchmark was used) is true but off-topic for a "why does it hurt" question, so it is NOT a nugget. Note the two facts in chunks 0 and 1 are kept as separate atomic nuggets, not merged."""


# ---- listing ---------------------------------------------------------------

def _ordered_videos(video_ids: list[str], inv_by_id: dict) -> list[str]:
    """Order source videos oldest-first (matters for longitudinal); stable otherwise."""
    return sorted(video_ids, key=lambda v: inv_by_id.get(v, {}).get("published_at") or "")


def build_listing(video_ids: list[str], chunk_cache: dict, summaries: dict,
                  inv_by_id: dict) -> tuple[str, list[str]]:
    """Enumerated chunk listing across the videos + a parallel index->chunk_id map."""
    lines: list[str] = []
    idx_map: list[str] = []
    idx = 0
    for v in video_ids:
        title = summaries.get(v, {}).get("title", v)
        month = inv_by_id.get(v, {}).get("month")
        lines.append(f"=== Video: {title} ({month}) ===" if month else f"=== Video: {title} ===")
        for c in chunk_cache[v]:
            lines.append(f"{idx}: {c['text']}")
            idx_map.append(c["chunk_id"])
            idx += 1
    return "\n".join(lines), idx_map


# ---- drafting --------------------------------------------------------------

async def draft_one(q: dict, chunk_cache: dict, summaries: dict, inv_by_id: dict,
                    sem) -> tuple[str, dict | None]:
    """Return ('ok', record) | ('error', None). 'error' means the API call failed
    (never recorded as 'no nuggets'), so --only-missing can recover it later."""
    vids = _ordered_videos(q["source_video_ids"], inv_by_id)
    for v in vids:
        if v not in chunk_cache:
            chunk_cache[v] = await asyncio.to_thread(cio.video_chunks, v)
    listing, idx_map = build_listing(vids, chunk_cache, summaries, inv_by_id)
    user = (f"Question: {q['query']}\n\n"
            f"Transcripts ({len(idx_map)} chunks across {len(vids)} video(s)); "
            f"each line is 'index: text':\n\n{listing}\n\n"
            "Produce the nuggets a correct answer to the question must contain, with "
            "evidence_indices citing the chunk(s) that support each, and a reference answer.")
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(DRAFT_SYSTEM, user, DraftOut, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "adaptive"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - one bad/slow query must not kill the batch
            print(f"  draft fail {q['query_id']}: {type(e).__name__}: {e}")
            return "error", None

    nuggets: list[dict] = []
    n_dropped = 0
    for n in out.nuggets:
        cids = [idx_map[i] for i in n.evidence_indices if 0 <= i < len(idx_map)]
        if not cids:
            n_dropped += 1  # a nugget with no valid evidence pointer does not exist
            continue
        nuggets.append({"nugget_id": f"{q['query_id']}_n{len(nuggets) + 1}",
                        "text": n.text.strip(), "importance": n.importance,
                        "evidence_chunk_ids": sorted(set(cids))})
    record = {
        "query_id": q["query_id"], "query": q["query"], "tier": q["tier"],
        "topic_cluster": q["topic_cluster"], "source_video_ids": q["source_video_ids"],
        "source_chunk_ids": q["source_chunk_ids"], "observed_shape": q["observed_shape"],
        "nuggets": nuggets, "reference_answer": out.reference_answer.strip(),
        "n_dropped": n_dropped,
        "provenance": {"generated_by": MODEL, "thinking": "adaptive",
                       "git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }
    return "ok", record


# ---- io + driver -----------------------------------------------------------

def read_queryset(layer: str) -> list[dict]:
    path = OUT_DIR / f"queryset_{layer}.jsonl"
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in json.loads(ln):
            rows.append(json.loads(ln))
    return rows


def read_done_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in (o := json.loads(ln)):
            done.add(o["query_id"])
    return done


def _select(queryset: list[dict], tiers: list[str] | None, per_tier: int | None) -> list[dict]:
    picked = [q for q in queryset if not tiers or q["tier"] in tiers]
    if per_tier:
        seen: dict[str, int] = {}
        out = []
        for q in sorted(picked, key=lambda q: (q["tier"], q["query_id"])):
            if seen.get(q["tier"], 0) < per_tier:
                out.append(q)
                seen[q["tier"]] = seen.get(q["tier"], 0) + 1
        return out
    return picked


async def amain(args: argparse.Namespace) -> None:
    summaries = cio.read_summaries(args.summaries)
    inventory = cio.read_inventory(args.inventory)
    inv_by_id = {v["video_id"]: v for v in inventory["videos"]}

    queryset = read_queryset(args.layer)
    todo = _select(queryset, args.tiers, args.per_tier)
    out_path = OUT_DIR / f"nuggets_draft_{args.layer}.jsonl"

    resuming = args.only_missing and out_path.exists()
    if resuming:
        done = read_done_ids(out_path)
        todo = [q for q in todo if q["query_id"] not in done]
        sink = out_path.open("a", encoding="utf-8")
    else:
        sink = out_path.open("w", encoding="utf-8")
        sink.write(json.dumps({"_meta": {"layer": args.layer, "model": MODEL,
                   "thinking": "adaptive", "channel": cio.CHANNEL,
                   "provenance": {"git_sha": PROVENANCE.git_sha,
                                  "git_dirty": PROVENANCE.git_dirty}}}, ensure_ascii=False) + "\n")

    print(f"{args.layer}: drafting {len(todo)} queries (concurrency {args.concurrency}) -> {out_path}")
    sem = asyncio.Semaphore(args.concurrency)
    chunk_cache: dict[str, list[dict]] = {}
    records: list[dict] = []
    n_ok = n_err = 0
    tasks = [draft_one(q, chunk_cache, summaries, inv_by_id, sem) for q in todo]
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"draft {args.layer}"):
        status, rec = await coro
        if status == "ok":
            sink.write(json.dumps(rec, ensure_ascii=False) + "\n")
            sink.flush()  # crash-safe: each completed query hits disk immediately
            records.append(rec)
            n_ok += 1
        else:
            n_err += 1
    sink.close()

    n_nug = sum(len(r["nuggets"]) for r in records)
    n_drop = sum(r["n_dropped"] for r in records)
    err = f", ERRORS {n_err} (resume with --only-missing)" if n_err else ""
    print(f"  drafted {n_ok} queries, {n_nug} nuggets ({n_drop} dropped, no evidence){err}")

    if args.render:
        chunk_text = {c["chunk_id"]: c["text"] for chs in chunk_cache.values() for c in chs}
        md = "\n".join(render_query_md(r, chunk_text)
                       for r in sorted(records, key=lambda r: (r["tier"], r["query_id"])))
        Path(args.render).write_text(md, encoding="utf-8")
        print(f"  rendered {len(records)} queries -> {args.render}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", choices=["core", "broad"], required=True)
    ap.add_argument("--tiers", nargs="*", choices=TIERS)
    ap.add_argument("--per-tier", type=int, default=None, help="cap queries per tier (gate/smoke)")
    ap.add_argument("--only-missing", action="store_true", help="resume: skip already-drafted queries")
    ap.add_argument("--render", type=Path, default=None, help="also write a markdown reader of this run")
    ap.add_argument("--summaries", type=Path, default=SUMMARIES_DEFAULT)
    ap.add_argument("--inventory", type=Path, default=INVENTORY_DEFAULT)
    ap.add_argument("--concurrency", type=int, default=3)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
