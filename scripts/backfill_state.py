"""Backfill videos table from on-disk state for Phase 1 (code4AI only)."""
import json
from pathlib import Path

from app.db import transaction

CHANNELS = ["code4AI"]
DATA = Path("data")


def pass_1_manifest(conn, channel):
    """Insert a row per video from the channel manifest."""
    manifest = DATA / "channel_manifests" / f"{channel}.jsonl"
    n = 0
    for line in manifest.read_text().splitlines():
        v = json.loads(line)
        # EXCLUDED.x = "the new value I was trying to insert for column x."
        conn.execute("""
            INSERT INTO videos (video_id, channel, title, published_at, duration_s)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO UPDATE SET
              title = EXCLUDED.title,
              published_at = EXCLUDED.published_at,
              duration_s = EXCLUDED.duration_s
        """, (v["id"], channel, v.get("title"), v.get("publishedAt"), v.get("duration_seconds")))
        n += 1
    print(f"  pass 1 ({channel}): {n} manifest rows")


def pass_2_fetched(conn, channel):
    """Mark fetched transcripts."""
    n = 0
    for path in sorted((DATA / "transcripts" / channel).glob("*.jsonl")):
        lines = path.read_text().splitlines()
        meta = json.loads(lines[0])["_meta"]
        n_segments = len(lines) - 1
        conn.execute("""
            UPDATE videos SET
              status = 'fetched',
              fetched_at = NOW(),
              transcript_language = %s,
              transcript_is_generated = %s,
              transcript_n_segments = %s
            WHERE video_id = %s
        """, (meta.get("language"), meta.get("is_generated"), n_segments, path.stem))
        n += 1
    print(f"  pass 2 ({channel}): {n} fetched")


def pass_3_cleaned(conn, channel):
    """Mark cleaned transcripts."""
    n = 0
    for path in sorted((DATA / "transcripts_clean" / channel).glob("*.jsonl")):
        conn.execute("""
            UPDATE videos SET
              cleaned_at = NOW(),
              cleanup_model = 'gpt-5.4-mini',
              cleanup_prompt_version = 'cleanup_v1'
            WHERE video_id = %s
        """, (path.stem,))
        n += 1
    print(f"  pass 3 ({channel}): {n} cleaned")


def pass_4_chunked(conn, channel):
    """Mark chunked videos."""
    n = 0
    for path in sorted((DATA / "chunks" / channel).glob("*.jsonl")):
        n_chunks = len(path.read_text().splitlines())
        conn.execute("""
            UPDATE videos SET
              chunked_at = NOW(),
              chunk_window_s = 30,
              n_chunks = %s
            WHERE video_id = %s
        """, (n_chunks, path.stem))
        n += 1
    print(f"  pass 4 ({channel}): {n} chunked")


def main():
    for channel in CHANNELS:
        print(f"channel: {channel}")
        with transaction() as conn:
            pass_1_manifest(conn, channel)
            pass_2_fetched(conn, channel)
            pass_3_cleaned(conn, channel)
            pass_4_chunked(conn, channel)


if __name__ == "__main__":
    main()