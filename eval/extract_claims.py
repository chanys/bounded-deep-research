"""Stage B: per-video claim inventory extraction (Claude-only).

For each of the 475 answerable code4AI videos, presents the transcript as the
enumerated 30-second chunk listing (the same presentation the grounding script
uses) and extracts EVERY concrete claim the video makes, each anchored to the
DB chunk id(s) that state it. This is the provenance-clean substrate for query
composition (Tasks 4-6) and the coverage statistic (Task 3): unlike Stage A's
salience-filtered summary/key_points, it is exhaustive, chunk-anchored, and
strictly faithful (no interpretive repair of garbled statements).

The model cites chunk *indices* into the presented listing; we map each back to
the real DB chunk_id and drop any claim whose indices do not resolve, so a claim
can never carry an empty or fabricated anchor.

Needs the DB up (transcript chunk text): `make up` then the corpus restore.

Usage:
  uv run python -m eval.extract_claims --limit 3 --out eval/artifacts/_claims_smoke.jsonl --render eval/artifacts/claims_sample.md
  uv run python -m eval.extract_claims                 # full run (475 calls)
  uv run python -m eval.extract_claims --only-missing  # resume failures
"""
from __future__ import annotations

import argparse
import asyncio
import json
import statistics
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio

OUT_DEFAULT = Path("eval/artifacts/claims_code4AI.jsonl")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 16000   # exhaustive extraction of a dense video is many claims; bump if truncation
CALL_TIMEOUT = 240   # a ~60-chunk video is ~15k input tokens; give the call room


# ---- output schema ---------------------------------------------------------

class ExtractedClaim(BaseModel):
    text: str
    evidence_indices: list[int]              # indices into the presented listing
    topics: list[str]
    entities: list[str]
    confidence: Literal["high", "low"]
    confidence_note: str | None = None


class ClaimsOut(BaseModel):
    claims: list[ExtractedClaim]


# ---- prompt (frozen; tied to the run by the git-SHA fingerprint) -----------

CLAIM_SYSTEM = """\
You extract the complete set of concrete claims made in a single YouTube video, from its transcript presented as a numbered list of 30-second chunks (each line is "index: text"). This is an exhaustive, faithful inventory for research evaluation - not a summary.

Rules:
- Extract EVERY concrete claim, finding, number, result, comparison, or stated opinion, including minor details (specific counts, dates, names, per-attempt outcomes). Do not filter for importance. When in doubt, extract.
- Each claim is one standalone statement, understandable without the transcript. Resolve pronouns and vague references to the actual subject named in the transcript. One idea per claim; never join two facts with "and".
- Consolidate restatements. When the same claim, assessment, or fact is repeated or rephrased across multiple chunks, extract it ONCE and list every supporting chunk index in evidence_indices. Do not emit near-duplicate claims.
- Outcomes, not play-by-play. When the creator narrates a live demo or a scrolling reasoning trace, extract the outcomes, results, failures, revisions, and the creator's assessments - not the intermediate step-by-step events. Test: would the statement belong in a written summary of the demo after it ended? "The model's reasoning crashed twice" passes; "the model pressed button B on floor 17" does not.
- Attribute opinions and judgments to the creator ("the creator argues that...", "the creator characterizes X as marketing"). These ARE claims.
- For each claim, list in evidence_indices the indices of the chunk(s) that support it. Every claim must have at least one chunk index. Never cite a chunk that does not state the claim.
- Be strictly faithful. Extract what was said. If the transcript is garbled, ambiguous, or self-contradictory, extract the surface claim AS STATED and mark it low confidence with a short confidence_note. NEVER repair, reconcile, or reinterpret a statement into what the speaker probably meant.
- Assign each claim short topic phrases (topics) and the specific entities it names (models, papers, tools, benchmarks, datasets, people). Base these only on this transcript.
- Skip non-content material: greetings, sponsor reads, channel promotion, housekeeping ("like and subscribe"), and meta-narration or production/pacing narration about the video itself ("in this video I will...", "I'll speed up the video here", "let me accelerate this part").
- Consolidation and the outcomes rule remove redundancy and play-by-play only; they do NOT reduce coverage. Every distinct number, date, named entity, concrete finding, and creator judgment must still appear in exactly one claim, including ones that seem unimportant.

Worked example. Transcript chunks:
0: so today I'm testing GPT-5.4 on my elevator puzzle
1: okay it presses button 7, then button 3, now it is heading to floor 12
2: and now it backtracks, tries button 9, and reaches floor 40
3: so that first attempt used 12 button presses and got to floor 40
4: honestly I think the paper's "reasoning" label here is just marketing
5: yeah that reasoning label really is just marketing speak if you ask me
6: the number was either 76 or 67 percent, the audio is unclear
7: alright before we continue smash that subscribe button
8: I'll speed up the video here until the next result
Good claims: {"text": "GPT-5.4's first attempt at the elevator puzzle used 12 button presses and reached floor 40.", "evidence_indices": [3], "topics": ["elevator puzzle benchmark"], "entities": ["GPT-5.4"], "confidence": "high", "confidence_note": null}; {"text": "The creator characterizes the paper's 'reasoning' label as marketing.", "evidence_indices": [4, 5], "topics": ["reasoning terminology"], "entities": [], "confidence": "high", "confidence_note": null}; {"text": "The creator reports a score of 76 percent.", "evidence_indices": [6], "topics": ["benchmark score"], "entities": [], "confidence": "low", "confidence_note": "audio unclear; the number may be 67 rather than 76"}. Chunks 1-2 are the live button-by-button play-by-play of the demo, so they are not claims; only the outcome (chunk 3) is extracted. The marketing opinion is stated twice (chunks 4 and 5) but is ONE claim citing both. Chunk 7 is a subscribe CTA and chunk 8 is video-pacing narration, so neither is a claim.

Return structured data only."""

USER_TEMPLATE = (
    "Video title: {title}\n"
    "Published: {published_at}\n\n"
    "Transcript chunks (index: text):\n{chunk_listing}\n\n"
    "Extract the complete claim inventory per the rules."
)


# ---- listing ---------------------------------------------------------------

def build_listing(chunks: list[dict]) -> tuple[str, list[str]]:
    """Enumerated single-video listing + a parallel index->chunk_id map."""
    lines = [f"{i}: {c['text']}" for i, c in enumerate(chunks)]
    idx_map = [c["chunk_id"] for c in chunks]
    return "\n".join(lines), idx_map


# ---- extraction ------------------------------------------------------------

async def extract_one(video_id: str, manifest: dict[str, dict],
                      sem: asyncio.Semaphore) -> tuple[dict | None, int]:
    """Extract one video's claims. Returns (record | None, n_dropped).

    None means the API call failed (never recorded as 'no claims'), so
    --only-missing can recover it later.
    """
    rec = manifest[video_id]
    chunks = await asyncio.to_thread(cio.video_chunks, video_id)
    listing, idx_map = build_listing(chunks)
    user = USER_TEMPLATE.format(title=rec.get("title", ""),
                                published_at=rec.get("publishedAt"),
                                chunk_listing=listing)
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(CLAIM_SYSTEM, user, ClaimsOut, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "disabled"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - one bad/slow video must not kill the batch
            print(f"  fail {video_id}: {type(e).__name__}: {e}")
            return None, 0

    # Resolve indices -> chunk_ids; drop claims with no valid pointer.
    surviving: list[tuple[int, ExtractedClaim, list[int]]] = []
    n_dropped = 0
    for c in out.claims:
        valid = [i for i in c.evidence_indices if 0 <= i < len(idx_map)]
        if not valid:
            n_dropped += 1
            continue
        surviving.append((min(valid), c, valid))

    # claim_id numbered by first supporting chunk index (stable ordering rule).
    surviving.sort(key=lambda t: t[0])
    claims = []
    for n, (_first, c, valid) in enumerate(surviving, 1):
        note = c.confidence_note if c.confidence == "low" else None
        claims.append({
            "claim_id": f"{video_id}#c{n:03d}",
            "text": c.text.strip(),
            "chunk_ids": sorted({idx_map[i] for i in valid}),
            "topics": c.topics,
            "entities": c.entities,
            "confidence": c.confidence,
            "confidence_note": note,
        })

    record = {
        "video_id": video_id,
        "title": rec.get("title", ""),
        "published_at": rec.get("publishedAt"),
        "duration_seconds": rec.get("duration_seconds"),
        "n_chunks": len(chunks),
        "claims": claims,
        "model": MODEL,
    }
    return record, n_dropped


# ---- io --------------------------------------------------------------------

def write_all(path: Path, records: dict[str, dict]) -> None:
    """Write a _meta header then one claim record per line, id-sorted.

    Called after each completed video, so the on-disk file is always a valid,
    sorted, resumable checkpoint (a --limit smoke never clobbers a full run).
    """
    counts = [len(r["claims"]) for r in records.values()]
    cpv = {"min": min(counts), "median": statistics.median(counts), "max": max(counts)} if counts else {}
    meta = {"_meta": {
        "channel": cio.CHANNEL,
        "model": MODEL,
        "thinking": "disabled",
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
        "count": len(records),
        "claims_per_video": cpv,
    }}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for vid in sorted(records):
            f.write(json.dumps(records[vid], ensure_ascii=False) + "\n")


def render_md(records: dict[str, dict]) -> str:
    """Human-readable sample: each video's claims with anchors and metadata."""
    out: list[str] = []
    for vid in sorted(records):
        r = records[vid]
        out.append(f"# {r['title']}\n\n`{vid}` - {r['published_at']} - "
                   f"{r['n_chunks']} chunks, {len(r['claims'])} claims\n")
        for c in r["claims"]:
            flag = "" if c["confidence"] == "high" else f"  [LOW: {c['confidence_note']}]"
            out.append(f"- **{c['claim_id']}**{flag} {c['text']}\n"
                       f"    - anchors: {', '.join(c['chunk_ids'])}\n"
                       f"    - topics: {c['topics']} | entities: {c['entities']}")
        out.append("")
    return "\n".join(out)


# ---- driver ----------------------------------------------------------------

async def amain(args: argparse.Namespace) -> None:
    manifest = cio.load_manifest()
    pop = cio.population()
    if args.limit:
        pop = pop[: args.limit]

    results = cio.read_summaries(args.out)  # merge into whatever is already there
    todo = [v for v in pop if not (args.only_missing and v in results)]
    print(f"population={len(pop)} existing={len(results)} to_extract={len(todo)}")
    if not todo:
        print("nothing to do")
        return

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [extract_one(v, manifest, sem) for v in todo]
    n_ok = n_err = n_drop = 0
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="extract"):
        rec, dropped = await coro
        n_drop += dropped
        if rec is None:
            n_err += 1
            continue
        results[rec["video_id"]] = rec
        write_all(args.out, results)  # crash-safe checkpoint per completed video
        n_ok += 1

    total_claims = sum(len(r["claims"]) for r in results.values())
    err = f", ERRORS {n_err} (resume with --only-missing)" if n_err else ""
    print(f"done: {n_ok} videos this run, {len(results)} total, "
          f"{total_claims} claims ({n_drop} dropped, no evidence){err} -> {args.out}")

    if args.render:
        Path(args.render).write_text(render_md(results), encoding="utf-8")
        print(f"  rendered {len(results)} videos -> {args.render}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--limit", type=int, default=None, help="only the first N videos (smoke)")
    ap.add_argument("--only-missing", action="store_true", help="skip ids already in --out")
    ap.add_argument("--render", type=Path, default=None, help="also write a markdown reader of this run")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
