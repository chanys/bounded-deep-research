"""Stage A of the corpus inventory: per-video transcript summaries (+ creator questions).

For each of the 475 answerable code4AI videos, asks Claude (Sonnet 5, reasoning
disabled) for a short summary plus the topics, entities, and creator-posed
questions found in the transcript. Cached to a JSONL so the expensive pass runs
once; build_inventory and mine_questions consume it. Writes merge into the
existing file, so a --limit smoke never clobbers a full run.

Usage:
  uv run python -m eval.summarize_transcripts --limit 5 --out eval/artifacts/_smoke.jsonl
  uv run python -m eval.summarize_transcripts                 # full run (475 calls)
  uv run python -m eval.summarize_transcripts --only-missing  # resume failures
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

OUT_DEFAULT = Path("eval/artifacts/summaries_code4AI.jsonl")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 3000

SYSTEM = (
    "You summarize a single YouTube video from its transcript, for a research-corpus "
    "inventory. Be faithful to what is actually said; do not invent facts, and do not "
    "judge quality. Return structured data only."
)

USER_TEMPLATE = (
    "Video title: {title}\n\n"
    "Transcript:\n{text}\n\n"
    "Produce:\n"
    "- summary: 2-4 sentences on what this video actually covers.\n"
    "- key_points: the concrete claims, findings, numbers, or results the video actually "
    "asserts, each a short standalone statement specific enough to build a question from. "
    "Capture the substantive points, not every minor detail.\n"
    "- topics: the main topics/themes discussed, as short phrases.\n"
    "- entities: specific models, techniques, tools, papers, datasets, or people named.\n"
    "- creator_questions: questions the creator explicitly poses or asks aloud in the "
    "transcript, extracted verbatim (light cleanup of ASR errors is fine). Include EVERY "
    "one you find; do not filter for quality or interestingness. Empty list if none."
)


class VideoSummary(BaseModel):
    summary: str
    key_points: list[str]
    topics: list[str]
    entities: list[str]
    creator_questions: list[str]


async def summarize_one(video_id: str, manifest: dict[str, dict], sem: asyncio.Semaphore) -> dict | None:
    """Summarize one video; returns the record, or None on API failure (batch keeps going)."""
    rec = manifest[video_id]
    text = cio.transcript_text(video_id)
    async with sem:
        try:
            out = await call_structured(
                SYSTEM,
                USER_TEMPLATE.format(title=rec.get("title", ""), text=text),
                VideoSummary,
                model=MODEL,
                max_tokens=MAX_TOKENS,
                thinking={"type": "disabled"},
            )
        except Exception as e:  # noqa: BLE001 - one bad call must not kill 475
            print(f"  fail {video_id}: {type(e).__name__}: {e}")
            return None
    return {
        "video_id": video_id,
        "title": rec.get("title", ""),
        "published_at": rec.get("publishedAt"),
        "duration_seconds": rec.get("duration_seconds"),
        "summary": out.summary,
        "key_points": out.key_points,
        "topics": out.topics,
        "entities": out.entities,
        "creator_questions": out.creator_questions,
        "model": MODEL,
    }


def write_all(path: Path, records: dict[str, dict]) -> None:
    """Write a _meta header line then one summary record per line, id-sorted."""
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"_meta": {
        "channel": cio.CHANNEL,
        "model": MODEL,
        "thinking": "disabled",
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
        "count": len(records),
    }}
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for vid in sorted(records):
            f.write(json.dumps(records[vid], ensure_ascii=False) + "\n")


async def amain(args: argparse.Namespace) -> None:
    manifest = cio.load_manifest()
    pop = cio.population()
    if args.limit:
        pop = pop[: args.limit]

    results = cio.read_summaries(args.out)  # merge into whatever is already there
    todo = [v for v in pop if not (args.only_missing and v in results)]
    print(f"population={len(pop)} existing={len(results)} to_summarize={len(todo)}")
    if not todo:
        print("nothing to do")
        return

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [summarize_one(v, manifest, sem) for v in todo]
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="summarize"):
        rec = await coro
        if rec:
            results[rec["video_id"]] = rec

    write_all(args.out, results)
    print(f"done: {len(results)} summaries -> {args.out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--limit", type=int, default=None, help="only the first N videos (smoke)")
    ap.add_argument("--only-missing", action="store_true", help="skip ids already in --out")
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
