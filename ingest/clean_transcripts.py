"""Clean ASR errors in raw transcripts using gpt-5.4-mini.

Async version: ~5 videos concurrent via asyncio.Semaphore. Within each video,
batches are processed sequentially (~20 segments/call) to keep neighbor-context
ordering simple.

Usage:
  uv run python -m ingest.clean_transcripts
  uv run python -m ingest.clean_transcripts --batch-size 20 --concurrency 5
  uv run python -m ingest.clean_transcripts --video-id zlGDEE64DDM
"""
import argparse
import asyncio
import json
from pathlib import Path

from pydantic import BaseModel
from langfuse.openai import AsyncOpenAI

from app.config import settings
from app.db import transaction
from prompts import CLEANUP_VERSION, load

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

TRANSCRIPTS_DIR = Path("data/transcripts")
CLEAN_DIR = Path("data/transcripts_clean")
MODEL = "gpt-5.4-mini"
REASONING_EFFORT = "low"

client = AsyncOpenAI(api_key=settings.openai_api_key)


class CleanedSegment(BaseModel):
    i: int
    text: str


class CleanedBatch(BaseModel):
    segments: list[CleanedSegment]


PROMPT_VERSION = CLEANUP_VERSION
SYSTEM_PROMPT_TEMPLATE = load(PROMPT_VERSION)


def format_segment_list(segs: list[dict], indexed: bool) -> str:
    if indexed:
        return "\n".join(f'{{"i": {s["i"]}, "text": {json.dumps(s["text"])}}}' for s in segs)
    return "\n".join(json.dumps(s["text"]) for s in segs)


async def clean_batch(
    targets: list[dict],
    before: list[dict],
    after: list[dict],
    title: str,
    description: str,
    log_prefix: str,
) -> list[str] | None:
    """Returns cleaned text list aligned to targets, or None on failure."""
    system = SYSTEM_PROMPT_TEMPLATE.format(title=title, description=description[:500])

    parts = []
    if before:
        parts.append(f"CONTEXT BEFORE (read-only, do not output):\n{format_segment_list(before, indexed=False)}\n\n")
    parts.append(f"CLEAN THESE SEGMENTS:\n{format_segment_list(targets, indexed=True)}")
    if after:
        parts.append(f"\n\nCONTEXT AFTER (read-only, do not output):\n{format_segment_list(after, indexed=False)}")
    user = "".join(parts)

    try:
        # why isn't the following using llm.py call_structured_llm
        response = await client.responses.parse(
            model=MODEL,
            reasoning={"effort": REASONING_EFFORT},
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            text_format=CleanedBatch,
            store=False,
        )
        parsed = response.output_parsed
        if parsed is None:
            return None
    except Exception as e:
        print(f"{log_prefix}    LLM error: {type(e).__name__}: {e}")
        return None

    expected = {s["i"] for s in targets}
    got = {s.i for s in parsed.segments}
    if got != expected or len(parsed.segments) != len(targets):
        print(f"{log_prefix}    index mismatch: expected {sorted(expected)}, got {sorted(got)}")
        return None

    by_idx = {s.i: s.text for s in parsed.segments}
    out = []
    for t in targets:
        cleaned = by_idx[t["i"]]
        in_len = len(t["text"])
        out_len = len(cleaned)
        if in_len > 0 and not (0.7 * in_len <= out_len <= 1.3 * in_len):
            print(f"{log_prefix}    seg {t['i']}: length {in_len}->{out_len}, keeping raw")
            out.append(t["text"])
        else:
            out.append(cleaned)
    return out


async def clean_video(
    transcript_path: Path,
    out_path: Path,
    batch_size: int,
    neighbors: int,
    log_prefix: str,
):
    lines = transcript_path.read_text().splitlines()
    meta = json.loads(lines[0])["_meta"]
    segments = [json.loads(line) for line in lines[1:]]

    title = meta.get("title", "")
    description = meta.get("description", "")

    cleaned_texts: list[str] = [None] * len(segments)  # type: ignore

    n_batches = (len(segments) + batch_size - 1) // batch_size
    for b in range(n_batches):
        lo = b * batch_size
        hi = min(lo + batch_size, len(segments))

        targets = [{"i": i, "text": segments[i]["text"]} for i in range(lo, hi)]
        before = [{"text": segments[i]["text"]} for i in range(max(0, lo - neighbors), lo)]
        after = [{"text": segments[i]["text"]} for i in range(hi, min(len(segments), hi + neighbors))]

        result = await clean_batch(targets, before, after, title, description, log_prefix)
        if result is None:
            print(f"{log_prefix}    batch {b+1}/{n_batches} failed, retrying")
            result = await clean_batch(targets, before, after, title, description, log_prefix)
        if result is None:
            print(f"{log_prefix}    batch {b+1}/{n_batches} failed twice, keeping raw")
            result = [t["text"] for t in targets]

        for offset, text in enumerate(result):
            cleaned_texts[lo + offset] = text

    with out_path.open("w") as f:
        f.write(json.dumps({"_meta": meta}, ensure_ascii=False) + "\n")
        for seg, cleaned_text in zip(segments, cleaned_texts):
            new_seg = {**seg, "text": cleaned_text}  # will replace the original "text" value in seg
            f.write(json.dumps(new_seg, ensure_ascii=False) + "\n")


# NOTE: the semaphore is a counter that caps how many coroutines can run within `async with sem` block at once
async def process_one(row: dict, batch_size: int, neighbors: int, sem: asyncio.Semaphore):
    """Clean one video under the semaphore, then mark it cleaned in Postgres."""
    video_id = row["video_id"]
    channel = row["channel"]
    log_prefix = f"[{video_id}]"

    async with sem:
        transcript_path = TRANSCRIPTS_DIR / channel / f"{video_id}.jsonl"
        out_path = CLEAN_DIR / channel / f"{video_id}.jsonl"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"{log_prefix} clean")
        try:
            await clean_video(transcript_path, out_path, batch_size, neighbors, log_prefix)
        except Exception as e:
            print(f"{log_prefix} FAILED: {type(e).__name__}: {e}")
            return

        # DB update is sync but cheap; run in default thread.
        def _mark_cleaned():
            with transaction() as conn:
                conn.execute("""
                    UPDATE videos SET
                      cleaned_at = NOW(),
                      cleanup_model = %s,
                      cleanup_prompt_version = %s
                    WHERE video_id = %s
                """, (MODEL, PROMPT_VERSION, video_id))

        await asyncio.to_thread(_mark_cleaned)
        print(f"{log_prefix} ok")


async def amain(args):
    with transaction() as conn:
        if args.video_id:
            rows = conn.execute("""
                SELECT video_id, channel FROM videos WHERE video_id = %s
            """, (args.video_id,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT video_id, channel FROM videos
                WHERE status = 'fetched' AND cleaned_at IS NULL
                ORDER BY published_at
            """).fetchall()

    if not rows:
        print("nothing to clean")
        return

    print(f"cleaning {len(rows)} videos at concurrency={args.concurrency}")
    sem = asyncio.Semaphore(args.concurrency)
    tasks = [
        asyncio.create_task(process_one(row, args.batch_size, args.neighbors, sem))
        for row in rows
    ]
    await asyncio.gather(*tasks)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batch-size", type=int, default=20)
    p.add_argument("--neighbors", type=int, default=3, help="read-only neighbor segments per side")
    p.add_argument("--concurrency", type=int, default=5, help="concurrent videos")
    p.add_argument("--video-id", help="clean a single video (for smoke testing)")
    args = p.parse_args()

    asyncio.run(amain(args))


if __name__ == "__main__":
    main()