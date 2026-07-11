"""Task 1.3: assemble the creator-posed-question candidate pool (no LLM).

Merges three sources into one deduplicated pool with provenance:
- transcript: the creator_questions already extracted per video in the Stage A summaries.
- title: question-form video titles from the manifest.
- description: '?'-terminated sentences in video descriptions.

Dedup is normalized-exact. No quality filtering beyond dedup; selection happens
downstream. The transcript source rides for free on the Stage A pass, so this
step makes no LLM calls of its own.

Usage:
  uv run python -m eval.mine_questions --summaries eval/artifacts/summaries_code4AI.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from eval import corpus_io as cio

OUT_DEFAULT = Path("eval/artifacts/questions_code4AI.jsonl")

_INTERROGATIVE_LEAD = re.compile(
    r"^\s*(what|why|how|which|who|whom|whose|when|where|is|are|was|were|can|could|do|does|"
    r"did|should|will|would|has|have|had|vs)\b",
    re.IGNORECASE,
)
_DESC_QUESTION = re.compile(r"[^.?!\n]*\?")
_URLISH = re.compile(r"https?://|www\.|\.com/|/watch|\?v=")
_WS = re.compile(r"\s+")


def is_question_title(title: str) -> bool:
    """A title counts as a question if it ends with '?' or opens with an interrogative lead."""
    t = title.strip()
    return t.endswith("?") or bool(_INTERROGATIVE_LEAD.match(t))


def description_questions(description: str) -> list[str]:
    """'?'-terminated multi-word fragments in a description.

    Drops single tokens and URL fragments (e.g. 'com/watch?' from a youtube link):
    those are parse artifacts, not questions. This is data hygiene, not quality
    filtering; genuine questions still pass untouched for downstream selection.
    """
    out = []
    for m in _DESC_QUESTION.finditer(description or ""):
        q = m.group(0).strip()
        if " " in q and not _URLISH.search(q):
            out.append(q)
    return out


def normalize(q: str) -> str:
    """Dedup key: lowercased, trailing '?' dropped, whitespace collapsed."""
    return _WS.sub(" ", q.strip().lower().rstrip("?").strip())


def mine(summaries: dict[str, dict], manifest: dict[str, dict], population: list[str]) -> list[dict]:
    raw: list[tuple[str, str, str]] = []  # (text, video_id, source)
    for vid in population:
        m = manifest.get(vid, {})
        if is_question_title(m.get("title", "")):
            raw.append((m["title"].strip(), vid, "title"))
        for q in description_questions(m.get("description", "")):
            raw.append((q, vid, "description"))
        for q in summaries.get(vid, {}).get("creator_questions", []):
            if q and q.strip():
                raw.append((q.strip(), vid, "transcript"))

    merged: dict[str, dict] = {}
    for text, vid, source in raw:
        key = normalize(text)
        if not key:
            continue
        entry = merged.setdefault(
            key, {"text": text, "normalized": key, "sources": set(), "provenance": []}
        )
        entry["sources"].add(source)
        entry["provenance"].append({"video_id": vid, "source": source})

    records = []
    for i, key in enumerate(sorted(merged), start=1):
        d = merged[key]
        records.append({
            "question_id": f"q{i:04d}",
            "text": d["text"],
            "normalized": d["normalized"],
            "sources": sorted(d["sources"]),
            "provenance": d["provenance"],
            "n_occurrences": len(d["provenance"]),
        })
    return records


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summaries", type=Path, default=Path("eval/artifacts/summaries_code4AI.jsonl"))
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()

    summaries = cio.read_summaries(args.summaries)
    manifest = cio.load_manifest()
    # Title/description questions come from any transcribed video; transcript questions
    # only from videos we have summaries for. Bound to the intersection with a summary.
    population = sorted(set(summaries))

    records = mine(summaries, manifest, population)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_source: dict[str, int] = {}
    for r in records:
        for s in r["sources"]:
            by_source[s] = by_source.get(s, 0) + 1
    print(f"questions={len(records)} by_source={by_source} -> {args.out}")


if __name__ == "__main__":
    main()
