"""Chunk transcripts into fixed 30s windows.

Reads data/transcripts/*.jsonl, writes data/chunks/{video_id}.jsonl.
Skips videos already chunked.
"""
import argparse
import json
from pathlib import Path

TRANSCRIPTS_DIR = Path("data/transcripts")
CHUNKS_DIR = Path("data/chunks")


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
            # If there's a gap larger than window, advance chunk_start to seg
            while seg["start"] >= chunk_end:
                chunk_start = chunk_end
                chunk_end = chunk_start + window_seconds
        buf.append(seg["text"])

    if buf:
        yield chunk_start, chunk_end, " ".join(buf)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--window", type=int, default=30, help="chunk window in seconds")
    args = p.parse_args()

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for transcript_path in sorted(TRANSCRIPTS_DIR.glob("*.jsonl")):
        video_id = transcript_path.stem
        out_path = CHUNKS_DIR / f"{video_id}.jsonl"
        if out_path.exists():
            print(f"  skip {video_id}")
            continue

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

        print(f"  ok   {video_id} ({n} chunks)")


if __name__ == "__main__":
    main()