"""Stage B+C of the corpus inventory: taxonomy induction, classification, aggregation.

Consumes the Stage A summaries. Induces a flat, emergent topic taxonomy (no fixed
cluster count) from the per-video topics, freezes it, classifies every video into
it, then aggregates per-cluster video counts / durations / DB chunk counts, a
cluster x month time-axis, and a per-video chapter-timestamp flag. Emits a
machine-readable inventory JSON and a human-readable markdown summary, both
stamped with the provenance fingerprint.

Usage:
  # smoke on the 5-video summaries, no DB (chunk counts null):
  uv run python -m eval.build_inventory --summaries eval/artifacts/_smoke.jsonl \
      --no-require-db --out-json eval/artifacts/_inv.json --out-md eval/artifacts/_inv.md
  # full run (needs the full summaries + DB up with the corpus restored):
  uv run python -m eval.build_inventory
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio

SUMMARIES_DEFAULT = Path("eval/artifacts/summaries_code4AI.jsonl")
OUT_JSON_DEFAULT = Path("eval/artifacts/inventory_code4AI.json")
OUT_MD_DEFAULT = Path("eval/artifacts/inventory_code4AI.md")
MODEL = "claude-sonnet-5"
OTHER = "other"

# A chapter list is per-line "[H:]MM:SS  Label"; treat as chapters at >=min_hits
# lines with the first timestamp at 0:00 (the observed convention).
_CHAPTER_LINE = re.compile(r"^\s*(?:(\d{1,2}):)?([0-5]?\d):([0-5]\d)\s+\S")


# ---- taxonomy induction (Stage B) ------------------------------------------

TAXONOMY_SYSTEM = (
    "You organize a single AI/ML YouTube creator's video catalog into an interpretable "
    "topic taxonomy that will be used to stratify evaluation-query sampling. Induce a FLAT "
    "set of topics that naturally emerge from the videos; choose the granularity yourself "
    "and do NOT force a target count. Merge near-duplicate or tiny topics. If one genre "
    "dominates (e.g. model-benchmark tests), split it by a meaningful sub-axis so no single "
    "topic swallows the corpus. Each topic: a short human-readable label, a one-line "
    "definition, and 3-5 example video ids drawn from the input."
)


class ProposedCluster(BaseModel):
    label: str
    definition: str
    example_video_ids: list[str]


class Taxonomy(BaseModel):
    clusters: list[ProposedCluster]


def _video_line(vid: str, rec: dict) -> str:
    topics = "; ".join(rec.get("topics", []))
    return f"{vid} | {rec.get('title', '')} | topics: {topics}"


async def propose_taxonomy(summaries: dict[str, dict]) -> list[dict]:
    """One induction call over (id, title, topics). Returns frozen clusters with ids c01.."""
    body = "\n".join(_video_line(v, summaries[v]) for v in sorted(summaries))
    user = (
        "Here is the catalog, one line per video as `id | title | topics`:\n\n"
        f"{body}\n\n"
        "Induce the topic taxonomy per the instructions."
    )
    # Reasoning disabled: over 475 videos, adaptive thinking is unbounded and blew past
    # max_tokens (thinking counts against the output budget). Grouping topic-lists is
    # well within Sonnet 5's no-thinking ability; 8000 is ample for the taxonomy JSON.
    tax = await call_structured(
        TAXONOMY_SYSTEM, user, Taxonomy, model=MODEL, max_tokens=8000,
        thinking={"type": "disabled"},
    )
    return [
        {"cluster_id": f"c{i:02d}", "label": c.label, "definition": c.definition,
         "example_video_ids": c.example_video_ids}
        for i, c in enumerate(tax.clusters, start=1)
    ]


# ---- classification (Stage C) ----------------------------------------------

CLASSIFY_SYSTEM = (
    "You assign each video to exactly one topic from a fixed taxonomy, by its best fit. "
    f"If none fits, use the id '{OTHER}'. Judge from the title and topics."
)


class ClassifiedVideo(BaseModel):
    video_id: str
    cluster_id: str
    confidence: str  # high | medium | low


class Classification(BaseModel):
    items: list[ClassifiedVideo]


def _taxonomy_block(taxonomy: list[dict]) -> str:
    lines = [f"{c['cluster_id']}: {c['label']} - {c['definition']}" for c in taxonomy]
    lines.append(f"{OTHER}: none of the above")
    return "\n".join(lines)


async def classify_videos(taxonomy: list[dict], summaries: dict[str, dict], batch: int) -> dict[str, str]:
    """Batched classification of every video into a frozen cluster_id."""
    tax_block = _taxonomy_block(taxonomy)
    valid = {c["cluster_id"] for c in taxonomy} | {OTHER}
    vids = sorted(summaries)
    assigned: dict[str, str] = {}

    async def one_batch(chunk_vids: list[str]) -> Classification:
        body = "\n".join(_video_line(v, summaries[v]) for v in chunk_vids)
        user = (
            f"Taxonomy:\n{tax_block}\n\n"
            f"Videos (`id | title | topics`):\n{body}\n\n"
            "Return one item per video with its cluster_id and your confidence."
        )
        return await call_structured(
            CLASSIFY_SYSTEM, user, Classification, model=MODEL, max_tokens=4000,
            thinking={"type": "disabled"},
        )

    sem = asyncio.Semaphore(6)

    async def guarded(chunk_vids: list[str]) -> Classification:
        async with sem:
            return await one_batch(chunk_vids)

    batches = [vids[i:i + batch] for i in range(0, len(vids), batch)]
    results = await asyncio.gather(*(guarded(b) for b in batches))
    for res in results:
        for item in res.items:
            # A hallucinated cluster_id falls back to OTHER rather than corrupting counts.
            assigned[item.video_id] = item.cluster_id if item.cluster_id in valid else OTHER
    # Any video the model omitted defaults to OTHER (never silently dropped).
    for v in vids:
        assigned.setdefault(v, OTHER)
    return assigned


# ---- aggregation (Stage C) -------------------------------------------------

def detect_chapters(description: str, min_hits: int) -> tuple[bool, int]:
    """(has_chapters, n_chapter_lines): >=min_hits timestamped lines, first one at 0:00."""
    hits = [m for m in (_CHAPTER_LINE.match(ln) for ln in (description or "").splitlines()) if m]
    if len(hits) < min_hits:
        return False, len(hits)
    h, mm, ss = hits[0].groups()
    first_zero = (int(h or 0) * 3600 + int(mm) * 60 + int(ss)) == 0
    return first_zero, len(hits)


def month_of(published_at: str | None) -> str | None:
    return published_at[:7] if published_at else None


def build_inventory(summaries, manifest, cluster_by_vid, taxonomy, chunk_counts, chapter_min_hits):
    """Assemble the machine-readable inventory dict."""
    videos = []
    for vid in sorted(summaries):
        rec = summaries[vid]
        m = manifest.get(vid, {})
        has_ch, n_ch = detect_chapters(m.get("description", ""), chapter_min_hits)
        videos.append({
            "video_id": vid,
            "title": rec.get("title") or m.get("title", ""),
            "published_at": rec.get("published_at") or m.get("publishedAt"),
            "month": month_of(rec.get("published_at") or m.get("publishedAt")),
            "duration_seconds": rec.get("duration_seconds") or m.get("duration_seconds"),
            "chunk_count": chunk_counts.get(vid),
            "cluster_id": cluster_by_vid.get(vid, OTHER),
            "has_chapters": has_ch,
            "n_chapter_lines": n_ch,
        })

    clusters = taxonomy + [{"cluster_id": OTHER, "label": "other", "definition": "unclassified",
                            "example_video_ids": []}]
    summaries_by_cluster = []
    for c in clusters:
        members = [v for v in videos if v["cluster_id"] == c["cluster_id"]]
        summaries_by_cluster.append({
            "cluster_id": c["cluster_id"],
            "label": c["label"],
            "video_count": len(members),
            "total_duration_s": sum(v["duration_seconds"] or 0 for v in members),
            "chunk_count": sum((v["chunk_count"] or 0) for v in members) if chunk_counts else None,
        })

    months = sorted({v["month"] for v in videos if v["month"]})
    matrix: dict[str, dict[str, int]] = {}
    for v in videos:
        if v["month"]:
            matrix.setdefault(v["cluster_id"], {}).setdefault(v["month"], 0)
            matrix[v["cluster_id"]][v["month"]] += 1

    n_with_ch = sum(1 for v in videos if v["has_chapters"])
    return {
        "channel": cio.CHANNEL,
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
        "models": {"taxonomy_model": MODEL},
        "counts": {
            "manifest_total": len(manifest),
            "in_inventory": len(videos),
            "with_db_chunks": sum(1 for v in videos if v["chunk_count"] is not None),
        },
        "chapter_detector": {"min_hits": chapter_min_hits, "n_with_chapters": n_with_ch},
        "taxonomy": clusters,
        "cluster_summaries": summaries_by_cluster,
        "time_axis": {"months": months, "matrix": matrix},
        "videos": videos,
    }


def render_markdown(inv: dict) -> str:
    lines = [f"# Corpus inventory: {inv['channel']}", ""]
    prov = inv["provenance"]
    lines += [f"git_sha `{prov['git_sha'][:12]}` (dirty={prov['git_dirty']}) | "
              f"taxonomy model `{inv['models']['taxonomy_model']}`", ""]
    c = inv["counts"]
    lines += ["## Population", "",
              f"- manifest total: {c['manifest_total']}",
              f"- in inventory: {c['in_inventory']}",
              f"- with DB chunk counts: {c['with_db_chunks']}",
              f"- chapter coverage: {inv['chapter_detector']['n_with_chapters']} videos "
              f"(>= {inv['chapter_detector']['min_hits']} lines)", ""]

    lines += ["## Clusters", "", "| cluster | label | videos | % | hours | chunks |",
              "|---|---|---:|---:|---:|---:|"]
    total = max(c["in_inventory"], 1)
    for cs in sorted(inv["cluster_summaries"], key=lambda x: -x["video_count"]):
        hours = f"{cs['total_duration_s'] / 3600:.1f}"
        chunks = cs["chunk_count"] if cs["chunk_count"] is not None else "-"
        pct = f"{100 * cs['video_count'] / total:.0f}%"
        lines.append(f"| {cs['cluster_id']} | {cs['label']} | {cs['video_count']} | {pct} | {hours} | {chunks} |")
    lines.append("")

    lines += ["## Cluster definitions", ""]
    for cl in inv["taxonomy"]:
        if cl["cluster_id"] == OTHER:
            continue
        lines.append(f"- **{cl['label']}** (`{cl['cluster_id']}`): {cl['definition']}")
    lines.append("")

    months = inv["time_axis"]["months"]
    if months:
        lines += ["## Time axis (videos per cluster per month)", "",
                  "| cluster | " + " | ".join(months) + " |",
                  "|---|" + "---|" * len(months)]
        for cl in inv["taxonomy"]:
            row = inv["time_axis"]["matrix"].get(cl["cluster_id"], {})
            cells = " | ".join(str(row.get(m, "")) for m in months)
            lines.append(f"| {cl['cluster_id']} | {cells} |")
        lines.append("")
    return "\n".join(lines)


async def amain(args: argparse.Namespace) -> None:
    summaries = cio.read_summaries(args.summaries)
    if not summaries:
        raise SystemExit(f"no summaries in {args.summaries}; run summarize_transcripts first")
    manifest = cio.load_manifest()

    chunk_counts = cio.db_chunk_counts() if args.require_db else {}

    if args.taxonomy and args.taxonomy.exists():
        taxonomy = json.loads(args.taxonomy.read_text())
        print(f"reusing frozen taxonomy: {len(taxonomy)} clusters")
    else:
        print(f"inducing taxonomy from {len(summaries)} videos ...")
        taxonomy = await propose_taxonomy(summaries)
        print(f"induced {len(taxonomy)} clusters")

    print("classifying ...")
    cluster_by_vid = await classify_videos(taxonomy, summaries, args.classify_batch)

    inv = build_inventory(summaries, manifest, cluster_by_vid, taxonomy,
                          chunk_counts, args.chapter_min_hits)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(inv, ensure_ascii=False, indent=2))
    args.out_md.write_text(render_markdown(inv))
    print(f"done: inventory -> {args.out_json} and {args.out_md}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summaries", type=Path, default=SUMMARIES_DEFAULT)
    ap.add_argument("--out-json", type=Path, default=OUT_JSON_DEFAULT)
    ap.add_argument("--out-md", type=Path, default=OUT_MD_DEFAULT)
    ap.add_argument("--taxonomy", type=Path, default=None, help="reuse a frozen taxonomy JSON")
    ap.add_argument("--classify-batch", type=int, default=30)
    ap.add_argument("--chapter-min-hits", type=int, default=2)
    ap.add_argument("--require-db", action=argparse.BooleanOptionalAction, default=True)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
