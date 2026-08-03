"""Read a channel's summaries: url, summary, key points, newest first.

The reading end of eval.summarize_channel. Wraps long key points to the terminal
width, which the equivalent jq one-liner cannot do:

  jq -r 'select(._meta|not) | "\\(.url)\\n\\(.summary)"' data/summaries/<channel>.jsonl

Usage:
  uv run python -m eval.show_summaries --channel starterstory
  uv run python -m eval.show_summaries --channel starterstory --limit 10
  uv run python -m eval.show_summaries --channel starterstory --grep tiktok
  uv run python -m eval.show_summaries --channel starterstory | less -R
"""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path


def load(channel: str) -> list[dict]:
    """Summary records for a channel, newest first. Skips the _meta header line."""
    path = Path(f"data/summaries/{channel}.jsonl")
    if not path.exists():
        raise SystemExit(f"no summaries at {path}; run eval.summarize_channel --channel {channel}")
    recs = []
    for ln in path.read_text().splitlines():
        if ln.strip():
            obj = json.loads(ln)
            if "_meta" not in obj:
                recs.append(obj)
    return sorted(recs, key=lambda r: r.get("published_at") or "", reverse=True)


def render(rec: dict, width: int) -> str:
    """One record as url + summary + key points."""
    mins = (rec.get("duration_seconds") or 0) // 60
    out = [
        "=" * width,
        f"{rec['title']}  [{mins}m, {(rec.get('published_at') or '')[:10]}]",
        rec["url"],
        "",
        textwrap.fill(rec["summary"], width=width, initial_indent="  ", subsequent_indent="  "),
        "",
    ]
    out += [
        textwrap.fill(k, width=width, initial_indent="  - ", subsequent_indent="    ")
        for k in rec["key_points"]
    ]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True)
    ap.add_argument("--limit", type=int, default=None, help="only the first N (newest first)")
    ap.add_argument("--grep", help="case-insensitive filter on title, summary, and key points")
    ap.add_argument("--width", type=int, default=96)
    args = ap.parse_args()

    recs = load(args.channel)
    if args.grep:
        needle = args.grep.lower()
        recs = [r for r in recs
                if needle in (r["title"] + r["summary"] + " ".join(r["key_points"])).lower()]
    if args.limit:
        recs = recs[: args.limit]

    for rec in recs:
        print(render(rec, args.width))
        print()
    print(f"({len(recs)} videos)")


if __name__ == "__main__":
    main()
