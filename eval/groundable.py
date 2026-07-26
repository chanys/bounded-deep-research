"""Shared per-claim groundable filter (Stage B, Task 6 Step 0).

Classifies each high-confidence claim as groundable (states substantive, comparable
content) versus content-free setup/meta, PER CLAIM and batched, with id-echo validation.
The binary content-ful-vs-setup judgment needs no video context, so claims from any
video may share a batch. The cache is keyed by claim id and accumulates across slices;
both the comparative composer and the Task 6 longitudinal composer import this module,
so the two slices share one bar and one cache.

Instrument-drift note: the shared cache is claim-id-keyed and deliberately NOT
prompt-fingerprinted, because it must accumulate across slices and pre-warm from a large
prior investment (~25.5k classifications). Fingerprinting the key would orphan that
pre-warm. Drift is instead controlled by holding the classification CRITERION (the
substantive-property clause below) byte-identical to the prior per-video filter, and by
`instrument_agreement`, which re-classifies a sample of already-cached claims and reports
new-vs-cached agreement before the cache is trusted.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import json
import random
from pathlib import Path

from pydantic import BaseModel

from core.claude_llm import call_structured

MODEL = "claude-sonnet-5"
CALL_TIMEOUT = 90
BATCH_SIZE = 50
MAX_TOKENS = 4000   # 50 echoed ids + verdicts; sized so a full batch does not truncate

# Criterion clause held byte-identical to the prior per-video filter (compose_comparative_
# claims.FILTER_SYSTEM) so cached and new verdicts are the same instrument; only the framing
# and the output contract (per-claim id-echo) changed.
FILTER_SYSTEM = """\
You identify which claims are groundable evaluation material. For EACH claim you are given, decide groundable=true if it states a substantive, comparable property: a concrete result, finding, number, comparison, method or mechanism detail, design choice, behavior, or creator judgment with real content. Decide groundable=false for content-free setup or meta claims (e.g. "the creator tests two models side by side", "a closer look will follow"), moment-by-moment demo narration, and claims too thin or generic to ground against. Return a verdict for EVERY claim id given, echoing each id exactly."""

LEGACY_VIDEO_CACHE = Path("eval/artifacts/groundable_claims_code4AI.json")


class ClaimVerdict(BaseModel):
    claim_id: str
    groundable: bool


class GroundableBatch(BaseModel):
    verdicts: list[ClaimVerdict]


# ---- cache -----------------------------------------------------------------

def _validate_cache(cache: object) -> None:
    """Data-boundary check on read: a dict of non-empty str -> bool. Loud on bad data."""
    if not isinstance(cache, dict):
        raise ValueError(f"groundable cache is not a dict: {type(cache).__name__}")
    for k, v in cache.items():
        if not isinstance(k, str) or not k:
            raise ValueError(f"groundable cache has an empty/non-str key: {k!r}")
        if not isinstance(v, bool):
            raise ValueError(f"groundable cache value for {k!r} is not bool: {v!r}")


def load_cache(path: Path, by_vid: dict[str, list[dict]]) -> dict[str, bool]:
    """Claim-level groundability cache {claim_id: bool}, accumulating across slices.

    Direct load when the claim-keyed file exists; otherwise a one-time pre-warm expanding
    the legacy video-keyed cache into per-claim booleans. The pre-warm count check catches
    a partial key translation (an entry silently lost in the expansion) at warm time,
    loudly, rather than as a mysterious downstream miss.
    """
    if path.exists():
        cache = json.loads(path.read_text())
        _validate_cache(cache)
        return cache
    cache: dict[str, bool] = {}
    if LEGACY_VIDEO_CACHE.exists():
        vc = json.loads(LEGACY_VIDEO_CACHE.read_text())
        expected = 0
        for vid, gids in vc.items():
            g = set(gids)
            for c in by_vid.get(vid, []):
                cache[c["claim_id"]] = c["claim_id"] in g
                expected += 1
        if len(cache) != expected:
            raise AssertionError(
                f"legacy pre-warm lost entries: expanded {expected} claim-video pairs but "
                f"cache has {len(cache)} keys (duplicate claim ids across videos?)")
    return cache


# ---- classification --------------------------------------------------------

async def _classify_batch(batch: list[tuple[str, str]], sem: asyncio.Semaphore) -> dict[str, bool] | None:
    """Classify one batch of (claim_id, text). Returns {claim_id: bool}, or None on an API
    failure (caller falls back to keeping all claims in the batch; the composition checker
    is the backstop). Raises ValueError on an id-echo mismatch, which is a correctness
    failure, not a transient one, and must fail the run loudly."""
    sent = {cid for cid, _ in batch}
    listing = "\n".join(f"[{cid}] {text}" for cid, text in batch)
    user = (f"Claims:\n{listing}\n\nReturn a groundable verdict for EVERY claim id above, "
            f"echoing each id exactly.")
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(FILTER_SYSTEM, user, GroundableBatch, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "disabled"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - transient/truncation -> counted fallback, not silent
            print(f"  groundable filter ERROR (batch of {len(batch)}): {type(e).__name__}", flush=True)
            return None
    got = {v.claim_id for v in out.verdicts}
    if got != sent:
        raise ValueError(f"groundable id-echo mismatch: missing={sorted(sent - got)} "
                         f"extra={sorted(got - sent)}")
    return {v.claim_id: v.groundable for v in out.verdicts}


async def classify_uncached(claim_ids: list[str], text_by_id: dict[str, str],
                            cache: dict[str, bool], *, sem: asyncio.Semaphore,
                            batch_size: int = BATCH_SIZE,
                            cache_path: Path | None = None) -> dict[str, int]:
    """Classify the uncached claim_ids in ~batch_size batches, mutating `cache` in place.

    Batches run concurrently under `sem`. On a batch API failure the batch's claims are
    kept (groundable=true) and counted as a fallback, matching the prior per-video filter.
    Persists once to cache_path after the batches complete. Returns {"calls", "fallbacks"}.
    """
    todo = [cid for cid in claim_ids if cid not in cache]
    if not todo:
        return {"calls": 0, "fallbacks": 0}
    chunks = [todo[i:i + batch_size] for i in range(0, len(todo), batch_size)]
    results = await asyncio.gather(
        *(_classify_batch([(c, text_by_id[c]) for c in ch], sem) for ch in chunks))
    fallbacks = 0
    for ch, verdicts in zip(chunks, results):
        if verdicts is None:
            for cid in ch:
                cache[cid] = True   # fallback: keep all; the checker backstops
            fallbacks += 1
        else:
            cache.update(verdicts)
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False))
    return {"calls": len(chunks), "fallbacks": fallbacks}


async def instrument_agreement(cache: dict[str, bool], text_by_id: dict[str, str], *,
                               sem: asyncio.Semaphore, sample_n: int = 60,
                               seed: int = 20260714) -> dict:
    """Re-classify a deterministic sample of already-cached claims with the current
    per-claim prompt and compare to the cached verdicts. Controls classifier drift without
    fingerprinting the shared cache. Report before trusting the pre-warm."""
    ids = sorted(cid for cid in cache if cid in text_by_id)
    sample = random.Random(seed).sample(ids, min(sample_n, len(ids)))
    chunks = [sample[i:i + BATCH_SIZE] for i in range(0, len(sample), BATCH_SIZE)]
    results = await asyncio.gather(
        *(_classify_batch([(c, text_by_id[c]) for c in ch], sem) for ch in chunks))
    fresh: dict[str, bool] = {}
    for v in results:
        if v:
            fresh.update(v)
    agree = sum(1 for cid in fresh if fresh[cid] == cache[cid])
    return {
        "sample": len(fresh),
        "agree": agree,
        "agreement": round(agree / len(fresh), 3) if fresh else None,
        "disagreements": [{"claim_id": c, "cached": cache[c], "fresh": fresh[c]}
                          for c in fresh if fresh[c] != cache[c]][:15],
    }


# ---- standalone CLI (instrument-agreement check for the human gate) ---------

def load_claim_texts(path: Path) -> tuple[dict[str, str], dict[str, list[dict]]]:
    """High-confidence claim text_by_id and video->claims map, for the CLI and pre-warm."""
    text_by_id: dict[str, str] = {}
    by_vid: dict[str, list[dict]] = collections.defaultdict(list)
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        if "_meta" in rec or not rec.get("published_at"):
            continue
        for c in rec["claims"]:
            if c["confidence"] != "high":
                continue
            text_by_id[c["claim_id"]] = c["text"]
            by_vid[rec["video_id"]].append({"claim_id": c["claim_id"]})
    return text_by_id, dict(by_vid)


async def _cli(args: argparse.Namespace) -> None:
    text_by_id, by_vid = load_claim_texts(args.claims)
    cache = load_cache(args.cache, by_vid)
    print(f"[groundable] cache entries: {len(cache)}", flush=True)
    if args.validate:
        sem = asyncio.Semaphore(args.concurrency)
        print(f"[cost estimate] instrument-agreement re-classifies {args.validate} cached "
              f"claims ~ {(args.validate + BATCH_SIZE - 1) // BATCH_SIZE} calls "
              f"~ ${((args.validate + BATCH_SIZE - 1) // BATCH_SIZE) * 0.01:.2f}", flush=True)
        rep = await instrument_agreement(cache, text_by_id, sem=sem, sample_n=args.validate)
        print(f"[instrument agreement] {rep['agree']}/{rep['sample']} = {rep['agreement']}", flush=True)
        for d in rep["disagreements"]:
            print(f"  DISAGREE {d['claim_id']}: cached={d['cached']} fresh={d['fresh']}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Shared per-claim groundable filter / drift check.")
    ap.add_argument("--claims", type=Path, default=Path("eval/artifacts/claims_code4AI.jsonl"))
    ap.add_argument("--cache", type=Path, default=Path("eval/artifacts/groundable_claims.json"))
    ap.add_argument("--validate", type=int, default=0,
                    help="re-classify N already-cached claims and report new-vs-cached agreement")
    ap.add_argument("--concurrency", type=int, default=8)
    args = ap.parse_args()
    asyncio.run(_cli(args))


if __name__ == "__main__":
    main()
