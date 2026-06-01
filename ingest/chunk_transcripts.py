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

        lines = transcript_path.read_text().splitlines()
        segments = [json.loads(line) for line in lines[1:]]

        chunks = [
            (
                f"{video_id}:{int(start):05d}",
                video_id,
                int(start),
                int(end),
                text,
            )
            for start, end, text in chunk_segments(segments, args.window)
        ]
        n = len(chunks)

        with transaction() as conn:
            # conn.executemany does not exist ; only cursor.executemany(...) does ; so you have to get the cursor
            with conn.cursor() as cur:
                # `executemany` runs the same SQL statement N times, once per tuple in the list
                cur.executemany("""
                    INSERT INTO video_chunks (chunk_id, video_id, start_s, end_s, text)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (chunk_id) DO NOTHING
                """, chunks)
                # ON CONFLICT (chunk_id) DO NOTHING: if `chunk_id` already exists in the table, skip this row instead of raising an error

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