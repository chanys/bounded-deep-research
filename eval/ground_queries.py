"""Stage 2.1 grounding + post-filters (D10/D12).

For each candidate query, locate the transcript chunks that actually answer it by
handing an LLM the source video's enumerated chunk list (never the pgvector
retriever, which would make retrieval-recall circular). This pins source_chunk_ids
AND verifies answerability: a query no chunk supports is dropped. Then two filters:
leakage (verbatim overlap with the source chunk makes retrieval trivial) and
near-duplicate removal (keeps the human review list clean).

Needs the DB up (chunk text): `make up` then the corpus restore.

Usage:
  uv run python -m eval.ground_queries --tiers factual --limit 20   # smoke
  uv run python -m eval.ground_queries                              # all tiers
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio

OUT_DIR = Path("eval/artifacts")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 1000
CALL_TIMEOUT = 90  # bound a call (incl. rate-limit backoff) so the batch never appears hung
LEAK_MAX = 0.5        # reject a query whose content-trigram overlap with its chunks >= this
DEDUP_JACCARD = 0.8   # token-Jaccard >= this = near-duplicate query

_STOP = set(
    "a an the of to in on for and or is are was were be been being do does did how "
    "what which who whom whose when where why with without from into over under this "
    "that these those it its as at by vs versus compare comparing did does do you your "
    "their his her they them he she we our".split()
)
_WORD = re.compile(r"[a-z0-9]+")


# ---- grounding -------------------------------------------------------------

GROUND_SYSTEM = (
    "You locate supporting evidence in a single video's transcript. Given a question "
    "and the video's transcript as a numbered list of 30-second chunks, return the "
    "indices of the chunks that contain evidence DIRECTLY answering the question. "
    "Return an empty list if no chunk answers it. Do not guess; a chunk merely on the "
    "same topic is not evidence unless it states the answer."
)

# Tier-conditional variant for longitudinal (cc_07 item 4): a trajectory question has no
# single chunk that "directly answers" it, so grounding relaxes to evidence for any part of
# the development. Applied ONLY when explicitly requested and only to the longitudinal tier,
# and recorded as grounding_variant in _meta so the run's grounding condition is auditable.
GROUND_SYSTEM_LONGITUDINAL_V1 = (
    "You locate supporting evidence in a single video's transcript. Given a question about "
    "how something developed over time and the video's transcript as a numbered list of "
    "30-second chunks, return the indices of the chunks that provide evidence for any part "
    "of the development the question asks about. Return an empty list if no chunk provides "
    "such evidence. Do not guess; a chunk merely on the same broad topic is not evidence "
    "unless it states part of the development."
)


def ground_system(tier: str, variant: str | None) -> str:
    if tier == "longitudinal" and variant == "longitudinal_v1":
        return GROUND_SYSTEM_LONGITUDINAL_V1
    return GROUND_SYSTEM


# ---- input/output path resolution ------------------------------------------

# claim-derived inputs; comparative is the frozen Task 5.5 output (post-neutralization),
# not a formula-named file, so it is pinned explicitly.
CLAIM_INPUT = {
    "factual": "query_candidates_factual_claimslice.jsonl",
    "comparative": "query_candidates_comparative_claimslice_v21_final.jsonl",
    "longitudinal": "query_candidates_longitudinal_claimslice.jsonl",
}


def input_path(tier: str, slice_: str) -> Path:
    if slice_ == "claim_derived":
        return OUT_DIR / CLAIM_INPUT[tier]
    return OUT_DIR / f"query_candidates_{tier}.jsonl"


def output_path(tier: str, slice_: str) -> Path:
    suffix = "_claimslice" if slice_ == "claim_derived" else ""
    return OUT_DIR / f"query_grounded_{tier}{suffix}.jsonl"


class Grounded(BaseModel):
    chunk_indices: list[int]


def _chunk_listing(chunks: list[dict]) -> str:
    return "\n".join(f"{i}: {c['text']}" for i, c in enumerate(chunks))


async def ground_in_video(query: str, video_id: str, chunk_cache: dict, sem,
                          system: str = GROUND_SYSTEM) -> tuple[list[str], bool]:
    """Return (chunk_ids answering the query, errored). errored=True on API failure,
    so an empty result from a real 'nothing matches' is not confused with a dropped call."""
    if video_id not in chunk_cache:
        chunk_cache[video_id] = await asyncio.to_thread(cio.video_chunks, video_id)
    chunks = chunk_cache[video_id]
    if not chunks:
        return [], False
    user = (f"Question: {query}\n\nTranscript chunks (index: text):\n{_chunk_listing(chunks)}\n\n"
            "Return the indices of chunks that directly answer the question.")
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(system, user, Grounded, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "disabled"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001
            print(f"  ground fail {video_id}: {type(e).__name__}: {e}")
            return [], True
    return [chunks[i]["chunk_id"] for i in out.chunk_indices if 0 <= i < len(chunks)], False


def observed_shape(chunk_ids: list[str]) -> str:
    videos = {cid.rsplit(":", 1)[0] for cid in chunk_ids}
    if len(videos) > 1:
        return "multi-video"
    return "single" if len(chunk_ids) == 1 else "adjacent"


async def ground_candidate(cand: dict, chunk_cache: dict, sem,
                           system: str = GROUND_SYSTEM) -> tuple[str, dict | None]:
    """Return ('ok', record) | ('unanswerable', None) | ('error', None).

    'error' means a grounding call failed and the union came back empty, so we must
    not record it as a genuine no-answer; it is excluded and reported for a re-run.
    """
    per_video = await asyncio.gather(*(
        ground_in_video(cand["query"], v, chunk_cache, sem, system) for v in cand["answer_video_ids"]
    ))
    chunk_ids = sorted({cid for ids, _ in per_video for cid in ids})
    if chunk_ids:
        return "ok", {**cand, "source_chunk_ids": chunk_ids, "observed_shape": observed_shape(chunk_ids)}
    errored = any(err for _, err in per_video)
    return ("error" if errored else "unanswerable"), None


# ---- filters ---------------------------------------------------------------

def _content_tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall(text.lower()) if w not in _STOP]


def _trigrams(tokens: list[str]) -> set[tuple]:
    return {tuple(tokens[i:i + 3]) for i in range(len(tokens) - 2)}


def leak_score(query: str, chunk_texts: list[str]) -> float:
    """Fraction of the query's content-trigrams that appear verbatim in the source chunks."""
    q = _trigrams(_content_tokens(query))
    if not q:
        return 0.0
    src = _trigrams(_content_tokens(" ".join(chunk_texts)))
    return len(q & src) / len(q)


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a or b) else 0.0


def dedup(cands: list[dict]) -> tuple[list[dict], int]:
    """Greedy near-duplicate removal by token-Jaccard, keeping the first seen."""
    kept, kept_tok, dropped = [], [], 0
    for c in cands:
        toks = set(_content_tokens(c["query"]))
        if any(_jaccard(toks, t) >= DEDUP_JACCARD for t in kept_tok):
            dropped += 1
            continue
        kept.append(c)
        kept_tok.append(toks)
    return kept, dropped


# ---- driver ----------------------------------------------------------------

def read_candidates(tier: str, slice_: str) -> list[dict]:
    path = input_path(tier, slice_)
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        o = json.loads(ln)
        if "_meta" not in o:
            rows.append(o)
    return rows


def _load_ids(ids_file: str | None) -> set[str] | None:
    """Optional allow-list of candidate_ids restricting grounding to a subset.

    Accepts either a bare JSON list or a provenance-stamped object with an "ids" list.
    """
    if not ids_file:
        return None
    obj = json.loads(Path(ids_file).read_text())
    ids = obj["ids"] if isinstance(obj, dict) else obj
    if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
        raise ValueError(f"{ids_file}: expected a JSON list of candidate_id strings (or {{'ids': [...]}})")
    return set(ids)


async def run_tier(tier: str, limit: int | None, concurrency: int, slice_: str,
                   variant: str | None, ids: set[str] | None) -> None:
    cands = read_candidates(tier, slice_)
    if ids is not None:
        before = len(cands)
        cands = [c for c in cands if c["candidate_id"] in ids]
        matched = {c["candidate_id"] for c in cands}
        missing = ids - matched
        print(f"  {tier}: ids-filter kept {len(cands)}/{before}"
              + (f"; {len(missing)} requested ids not in this tier" if missing else ""))
    if limit:
        cands = cands[:limit]
    system = ground_system(tier, variant)
    n_calls = sum(len(c["answer_video_ids"]) for c in cands)
    # Pre-spend estimate (standing guard): grounding sends ~a full transcript per call, tiny output.
    est_in_tok = n_calls * 4500
    print(f"[cost estimate] {tier}: {len(cands)} candidates, ~{n_calls} ground calls, "
          f"~{est_in_tok/1e6:.2f}M input tok, ~${est_in_tok/1e6*2:.2f} at Sonnet 5 intro in-price",
          flush=True)
    print(f"{tier}: grounding {len(cands)} candidates"
          + (f" [variant={variant}]" if variant and tier == "longitudinal" else ""), flush=True)
    sem = asyncio.Semaphore(concurrency)
    chunk_cache: dict[str, list[dict]] = {}

    grounded: list[dict] = []
    n_unanswerable = n_error = 0
    tasks = [ground_candidate(c, chunk_cache, sem, system) for c in cands]
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"ground {tier}"):
        status, r = await coro
        if status == "ok":
            grounded.append(r)
        elif status == "unanswerable":
            n_unanswerable += 1
        else:
            n_error += 1

    # leakage
    n_leak = 0
    survivors = []
    for c in grounded:
        texts = [ct["text"] for v in {cid.rsplit(":", 1)[0] for cid in c["source_chunk_ids"]}
                 for ct in chunk_cache.get(v, []) if ct["chunk_id"] in set(c["source_chunk_ids"])]
        c["leak"] = round(leak_score(c["query"], texts), 3)
        if c["leak"] >= LEAK_MAX:
            n_leak += 1
            continue
        survivors.append(c)

    survivors.sort(key=lambda c: c["candidate_id"])
    survivors, n_dup = dedup(survivors)

    path = output_path(tier, slice_)
    meta = {"_meta": {"tier": tier, "slice": slice_,
                      "grounding_variant": (variant if variant and tier == "longitudinal" else None),
                      "grounding_model": MODEL, "leak_max": LEAK_MAX,
                      "dedup_jaccard": DEDUP_JACCARD,
                      "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
                      "input": len(cands), "kept": len(survivors),
                      "dropped": {"unanswerable": n_unanswerable, "leakage": n_leak, "near_dup": n_dup},
                      "grounding_errors": n_error}}
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for c in survivors:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    err = f", ERRORS {n_error} (re-run to recover)" if n_error else ""
    print(f"  kept {len(survivors)}/{len(cands)} "
          f"(unanswerable {n_unanswerable}, leakage {n_leak}, near_dup {n_dup}{err}) -> {path}")


async def amain(args: argparse.Namespace) -> None:
    ids = _load_ids(args.ids_file)
    for tier in (args.tiers or ["factual", "comparative", "longitudinal"]):
        await run_tier(tier, args.limit, args.concurrency, args.slice, args.grounding_variant, ids)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", nargs="*", choices=["factual", "comparative", "longitudinal"])
    ap.add_argument("--limit", type=int, default=None, help="cap candidates per tier (smoke)")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--slice", choices=["legacy", "claim_derived"], default="legacy",
                    help="legacy = original summary-derived files (default, unchanged); "
                         "claim_derived = the Task 4/5.5/6 *_claimslice inputs")
    ap.add_argument("--grounding-variant", choices=["longitudinal_v1"], default=None,
                    help="longitudinal-only relaxed grounding prompt; recorded in _meta")
    ap.add_argument("--ids-file", default=None,
                    help="optional JSON list of candidate_ids to restrict grounding to")
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
