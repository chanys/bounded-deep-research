"""Stage 2.2: deterministic core/broad selection, human review, then lock.

--emit: read the scored candidates (from screen_queries), select the deep core by
code (top by core-worthiness score, per-cluster cap for topic spread, minimum-score
floor), default the rest to broad, and write a per-tier review CSV with the verdict
pre-filled, for the user to review and override. No LLM call.

--lock: read the reviewed CSVs and write queryset_core.jsonl / queryset_broad.jsonl,
printing the per-tier rejection rate.

Usage:
  uv run python -m eval.select_queries --emit
  # user edits eval/artifacts/query_review_{tier}.csv
  uv run python -m eval.select_queries --lock
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from core.provenance import PROVENANCE
from eval import corpus_io as cio

OUT_DIR = Path("eval/artifacts")
MODEL = "claude-sonnet-5"
CORE_TARGET = 20         # per tier
PER_CLUSTER_CAP = 3      # at most this many core per topic cluster, to force spread
MIN_CORE_SCORE = 3       # a query below this core-worthiness score is never put in core
BROAD_MIN_SCORE = 4      # a non-core query below this score is dropped (not kept as broad)
TIERS = ["factual", "comparative", "longitudinal"]
CSV_COLS = ["verdict", "id", "tier", "cluster", "observed_shape", "leak", "score", "query",
            "edited_query", "source_chunk_ids", "source_titles", "evidence_snippet", "rationale"]


def read_scored(tier: str) -> list[dict]:
    """Kept, core-scored candidates for a tier (from screen_queries)."""
    path = OUT_DIR / f"query_scored_{tier}.jsonl"
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in json.loads(ln):
            rows.append(json.loads(ln))
    return rows


def select_core(cands: list[dict]) -> set[str]:
    """Pick core ids: highest core_score first, capped per cluster, above the score floor."""
    ranked = sorted(cands, key=lambda c: (-c["core_score"], c["candidate_id"]))
    core: set[str] = set()
    per_cluster: dict[str, int] = {}
    for c in ranked:
        if len(core) >= CORE_TARGET:
            break
        if c["core_score"] < MIN_CORE_SCORE:
            continue
        cl = c["cluster_id"]
        if per_cluster.get(cl, 0) >= PER_CLUSTER_CAP:
            continue
        core.add(c["candidate_id"])
        per_cluster[cl] = per_cluster.get(cl, 0) + 1
    return core


def _titles(video_ids: list[str], summaries: dict) -> str:
    return " || ".join(summaries.get(v, {}).get("title", v) for v in video_ids)


def _chunk_text_for(cands: list[dict]) -> dict[str, str]:
    """chunk_id -> text for every source chunk across candidates (one DB load per video)."""
    needed: dict[str, set[str]] = {}
    for c in cands:
        for cid in c["source_chunk_ids"]:
            needed.setdefault(cid.rsplit(":", 1)[0], set()).add(cid)
    out: dict[str, str] = {}
    for vid, ids in needed.items():
        for ch in cio.video_chunks(vid):
            if ch["chunk_id"] in ids:
                out[ch["chunk_id"]] = ch["text"]
    return out


def emit(args) -> None:
    summaries = cio.read_summaries(args.summaries)
    for tier in (args.tiers or TIERS):
        cands = read_scored(tier)
        if not cands:
            print(f"{tier}: no scored candidates, skipping")
            continue
        core = select_core(cands)
        chunk_text = _chunk_text_for(cands)
        path = OUT_DIR / f"query_review_{tier}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLS)
            w.writeheader()
            # core first (score desc), then broad, then dropped (blank verdict), all score desc
            n_broad = n_drop = 0
            for c in sorted(cands, key=lambda c: (c["candidate_id"] not in core, -c["core_score"])):
                cid = c["candidate_id"]
                if cid in core:
                    verdict = "core"
                elif c["core_score"] >= BROAD_MIN_SCORE:
                    verdict = "broad"
                    n_broad += 1
                else:
                    verdict = ""  # below the broad floor: dropped (kept in the CSV for audit)
                    n_drop += 1
                w.writerow({
                    "verdict": verdict, "id": cid, "tier": tier,
                    "cluster": c["cluster_id"], "observed_shape": c["observed_shape"],
                    "leak": c.get("leak"), "score": c["core_score"], "query": c["query"],
                    "edited_query": "", "source_chunk_ids": " ".join(c["source_chunk_ids"]),
                    "source_titles": _titles(c["answer_video_ids"], summaries),
                    "evidence_snippet": (chunk_text.get(c["source_chunk_ids"][0], "") or "")[:160]
                    if c["source_chunk_ids"] else "",
                    "rationale": c.get("screen_reason", ""),
                })
        short = " SHORT of core target" if len(core) < CORE_TARGET else ""
        print(f"{tier}: {len(cands)} candidates, core={len(core)}/{CORE_TARGET}{short}, "
              f"broad={n_broad}, dropped<{BROAD_MIN_SCORE}={n_drop} -> {path}")


def lock(args) -> None:
    scored = {tier: {c["candidate_id"]: c for c in read_scored(tier)} for tier in TIERS}
    core_rows, broad_rows = [], []
    stats: dict[str, dict] = {}

    for tier in TIERS:
        path = OUT_DIR / f"query_review_{tier}.csv"
        if not path.exists():
            continue
        n_in = n_core = n_broad = 0
        for row in csv.DictReader(path.open(encoding="utf-8")):
            n_in += 1
            verdict = row["verdict"].strip().lower()
            if verdict not in ("core", "broad"):
                continue
            cand = scored[tier].get(row["id"])
            if not cand:
                continue
            query = row["edited_query"].strip() or row["query"].strip()
            rec = {
                "query": query, "tier": tier, "topic_cluster": cand["cluster_id"],
                "layer": verdict, "source_video_ids": cand["answer_video_ids"],
                "source_chunk_ids": cand["source_chunk_ids"],
                "observed_shape": cand["observed_shape"],
                "provenance": {"candidate_id": row["id"], "generated_by": MODEL,
                               "git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
            }
            (core_rows if verdict == "core" else broad_rows).append(rec)
            n_core += verdict == "core"
            n_broad += verdict == "broad"
        kept = n_core + n_broad
        stats[tier] = {"input": n_in, "core": n_core, "broad": n_broad,
                       "rejection_rate": round(1 - kept / n_in, 3) if n_in else None}

    _write_queryset("core", core_rows)
    _write_queryset("broad", broad_rows)
    print(json.dumps(stats, indent=2))
    print(f"locked: core={len(core_rows)} broad={len(broad_rows)}")


def _write_queryset(layer: str, rows: list[dict]) -> None:
    for i, r in enumerate(sorted(rows, key=lambda x: (x["tier"], x["provenance"]["candidate_id"])), 1):
        r["query_id"] = f"q{i:04d}" if layer == "core" else f"b{i:04d}"
    path = OUT_DIR / f"queryset_{layer}.jsonl"
    meta = {"_meta": {"layer": layer, "channel": cio.CHANNEL, "count": len(rows),
                      "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty}}}
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true", help="deterministic core/broad split, write review CSVs")
    ap.add_argument("--lock", action="store_true", help="fold reviewed CSVs into the locked queryset")
    ap.add_argument("--summaries", type=Path, default=Path("eval/artifacts/summaries_code4AI.jsonl"))
    ap.add_argument("--tiers", nargs="*", choices=TIERS)
    args = ap.parse_args()
    if args.emit == args.lock:
        raise SystemExit("pass exactly one of --emit / --lock")
    if args.emit:
        emit(args)
    else:
        lock(args)


if __name__ == "__main__":
    main()
