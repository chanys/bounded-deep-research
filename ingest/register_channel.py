"""Register a channel's manifest and on-disk transcripts in the videos table.

Channel-generic successor to scripts/backfill_state.py (which is Phase-1,
code4AI-only). Three passes, same idea: manifest rows in, fetched marks from
data/transcripts/{channel}, cleaned marks from data/transcripts_clean/{channel}.

--manual-clean is for channels whose transcripts are human-made captions and
skip the ASR cleanup model entirely (e.g. TransGlobalTV): copy the raw files
into data/transcripts_clean/{channel} first, then this stamps
cleanup_model='manual' (no prompt version) so chunk_transcripts picks them up
without pretending a cleanup model ran.

Usage:
  uv run python -m ingest.register_channel --channel TransGlobalTV --manual-clean
"""
import argparse
import json
from pathlib import Path

from app.db import transaction

DATA = Path("data")


def pass_1_manifest(conn, channel):
    """Insert a row per video from the channel manifest (re-runnable upsert)."""
    manifest = DATA / "channel_manifests" / f"{channel}.jsonl"
    n = 0
    for line in manifest.read_text().splitlines():
        v = json.loads(line)
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
    """Mark fetched transcripts, with language/is_generated from each file's _meta header."""
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


def pass_3_cleaned(conn, channel, manual: bool):
    """Mark cleaned transcripts from the files present in transcripts_clean.

    manual=True stamps cleanup_model='manual' with no prompt version: the
    transcripts were never run through the cleanup model, they arrived clean.
    """
    clean_dir = DATA / "transcripts_clean" / channel
    if not clean_dir.is_dir():
        raise SystemExit(f"{clean_dir} does not exist; copy the transcripts there first")
    model = "manual" if manual else "gpt-5.4-mini"
    prompt_version = None if manual else "cleanup_v1"
    n = 0
    for path in sorted(clean_dir.glob("*.jsonl")):
        conn.execute("""
            UPDATE videos SET
              cleaned_at = NOW(),
              cleanup_model = %s,
              cleanup_prompt_version = %s
            WHERE video_id = %s
        """, (model, prompt_version, path.stem))
        n += 1
    print(f"  pass 3 ({channel}): {n} cleaned ({model})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", required=True, help="channel slug, e.g. TransGlobalTV")
    p.add_argument("--manual-clean", action="store_true",
                   help="transcripts are human-made; mark them cleaned without a cleanup model")
    args = p.parse_args()

    with transaction() as conn:
        pass_1_manifest(conn, args.channel)
        pass_2_fetched(conn, args.channel)
        pass_3_cleaned(conn, args.channel, manual=args.manual_clean)


if __name__ == "__main__":
    main()
