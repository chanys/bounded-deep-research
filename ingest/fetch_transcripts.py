"""Fetch transcripts for videos in a channel manifest, optionally filtered by month.

Usage:
  uv run python -m ingest.fetch_transcripts --channel code4AI
  uv run python -m ingest.fetch_transcripts --channel code4AI --month 2026-04
"""
import random
import argparse
import json
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", help="channel slug, e.g. code4AI")
    p.add_argument("--month", help="filter by YYYY-MM prefix on publishedAt")
    p.add_argument("--lang", default="en")
    p.add_argument("--delay", type=float, default=90)
    p.add_argument("--jitter", type=float, default=15)
    args = p.parse_args()

    manifest = Path(f"data/channel_manifests/{args.channel}.jsonl")
    out_dir = Path(f"data/transcripts/{args.channel}")
    out_dir.mkdir(parents=True, exist_ok=True)

    videos = [json.loads(line) for line in manifest.read_text().splitlines()]
    if args.month:
        videos = [v for v in videos if v["publishedAt"].startswith(args.month)]
    print(f"{len(videos)} videos")

    api = YouTubeTranscriptApi()

    for v in videos:
        out_path = out_dir / f"{v['id']}.jsonl"
        if out_path.exists():
            print(f"  skip {v['id']}")
            continue

        try:
            # t — a Transcript object (metadata + a handle to fetch).
            # Key attributes:
            #   .language_code (e.g. "en"),
            #   .is_generated (bool, auto vs manual),
            #   .video_id,
            #   .language (human name).
            # It hasn't fetched the actual text yet — it's a pointer.
            t = api.list(v["id"]).find_transcript([args.lang])
            fetched = t.fetch()

            # segments — a list of dicts, one per caption line, after .fetch() actually pulls the transcript. Shape:
            # [
            #   {"text": "hello everyone welcome back", "start": 0.0,  "duration": 3.2},
            #   {"text": "today we're talking about",    "start": 3.2,  "duration": 2.8},
            #   ...
            # ]
            segments = fetched.to_raw_data()  # list of {"text", "start", "duration"} dicts
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            print(f"  FAIL {v['id']}: {type(e).__name__}")
            continue

        meta = {**v, "language": t.language_code, "is_generated": t.is_generated}
        with out_path.open("w") as f:
            f.write(json.dumps({"_meta": meta}, ensure_ascii=False) + "\n")
            for seg in segments:
                f.write(json.dumps(seg, ensure_ascii=False) + "\n")

        print(f"  ok   {v['id']} ({len(segments)} segs, gen={t.is_generated})")
        sleep_for = args.delay + random.uniform(-args.jitter, args.jitter)
        time.sleep(sleep_for)


if __name__ == "__main__":
    main()