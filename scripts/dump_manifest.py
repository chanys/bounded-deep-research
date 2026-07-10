# scripts/dump_manifest.py
"""Dump the videos table to a JSON manifest. Reproducibility artifact.

Run after any ingest/clean/chunk/embed/index changes. Commit the output.
"""
import argparse
import json
from pathlib import Path

from core.config import settings
from core.db import transaction


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", required=True)
    p.add_argument("--out", default=None,
                   help="output path; default: data/manifest_<channel>.json")
    args = p.parse_args()

    out_path = Path(args.out or f"data/manifest_{args.channel}.json")

    with transaction() as conn:
        rows = conn.execute("""
            SELECT
              video_id,
              title,
              published_at,
              duration_s,
              transcript_language,
              transcript_is_generated,
              status,
              excluded_reason,
              chunk_window_s,
              n_chunks,
              cleanup_model,
              cleanup_prompt_version
            FROM videos
            WHERE channel = %s
            ORDER BY published_at
        """, (args.channel,)).fetchall()

    manifest = {
        "channel": args.channel,
        "embedding_model": settings.embedding_model,
        "n_videos": len(rows),
        "n_processed": sum(1 for r in rows if r["status"] == "fetched"),
        "n_excluded": sum(1 for r in rows if r["status"] == "excluded"),
        "videos": [
            {**r, "published_at": r["published_at"].isoformat() if r["published_at"] else None}
            for r in rows
        ],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, default=str))
    print(f"wrote {out_path}: {manifest['n_videos']} videos "
          f"({manifest['n_processed']} processed, {manifest['n_excluded']} excluded)")


if __name__ == "__main__":
    main()