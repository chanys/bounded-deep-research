"""Chunk cleaned transcripts into fixed 30s windows. Postgres-driven.

Usage:
  uv run python -m ingest.chunk_transcripts --channel code4AI --window 30
"""
import argparse
import json
from pathlib import Path

from app.db import transaction


def chunk_segments(segments, window_seconds):
    """Group segments into fixed-duration windows. Yields (start, end, text)."""
    if not segments:
        return
    chunk_start = segments[0]["start"]
    chunk_end = chunk_start + window_seconds
    buf = []
    for seg in segments:
        if seg["start"] >= chunk_end and buf:
            yield chunk_start, chunk_end, " ".join(buf)
            chunk_start = chunk_end
            chunk_end = chunk_start + window_seconds
            buf = []
            while seg["start"] >= chunk_end:
                chunk_start = chunk_end
                chunk_end = chunk_start + window_seconds
        buf.append(seg["text"])
    if buf:
        yield chunk_start, chunk_end, " ".join(buf)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", required=True, help="channel slug, e.g. code4AI")
    p.add_argument("--window", type=int, default=30, help="chunk window in seconds")
    args = p.parse_args()

    TRANSCRIPTS_DIR = Path(f"data/transcripts_clean/{args.channel}")
    CHUNKS_DIR = Path(f"data/chunks/{args.channel}")
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    # Drive from Postgres: chunk cleaned-but-not-yet-chunked videos.
    # If --source raw, fall back to fetched-but-not-chunked.
    with transaction() as conn:
        rows = conn.execute("""
            SELECT video_id FROM videos
            WHERE channel = %s AND cleaned_at IS NOT NULL AND chunked_at IS NULL
            ORDER BY published_at
        """, (args.channel,)).fetchall()

    if not rows:
        print("nothing to chunk")
        return

    for row in rows:
        video_id = row["video_id"]
        transcript_path = TRANSCRIPTS_DIR / f"{video_id}.jsonl"
        out_path = CHUNKS_DIR / f"{video_id}.jsonl"

        lines = transcript_path.read_text().splitlines()
        meta = json.loads(lines[0])["_meta"]
        segments = [json.loads(line) for line in lines[1:]]

        n = 0
        with out_path.open("w") as f:
            for start, end, text in chunk_segments(segments, args.window):
                chunk = {
                    "video_id": video_id,
                    "title": meta["title"],
                    "start_ts": int(start),
                    "end_ts": int(end),
                    "text": text,
                }
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                n += 1

        with transaction() as conn:
            conn.execute("""
                UPDATE videos SET
                  chunked_at = NOW(),
                  chunk_window_s = %s,
                  n_chunks = %s
                WHERE video_id = %s
            """, (args.window, n, video_id))

        print(f"  ok   {video_id} ({n} chunks)")


if __name__ == "__main__":
    main()