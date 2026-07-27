"""Nugget-level dir-3 support overlap between two scored arms (zero-cost, no model calls).

Answers "same 40% or a different 40%?": when two retrieval arms land on the same aggregate
retrieval ceiling, do they surface evidence for the SAME gold nuggets, or a DIFFERENT slice?
The answer decides the recommendation - a largely-overlapping YES-set means the material is
structurally unreachable by single-query retrieval (decomposition is the fix), while a
substantially different slice means a union of retrievers would lift the ceiling (ensembling
is the fix). The aggregate ceiling cannot distinguish these; the per-nugget overlap can.

Reads each arm's score files (`<scores_dir>/<qid>__r<idx>.json`) and uses the frozen dir-3
verdict `nugget_grid[*].supported_in_chunks` (whether the run's retrieved chunk SET supports
the gold nugget). Nuggets are keyed (question_id, nugget_id); both arms must share the same
gold version for the ids to align. lc-0130 (segregated no_change trap) is excluded.

Two cuts:
- Fair 1v1: arm-B's run vs arm-A's matching run index (default r0 vs r0), the honest
  single-run-vs-single-run comparison; reports the four-way split + Jaccard of the YES-sets.
- Union test: does arm B reach any nugget arm A NEVER supported across ALL its runs? This is
  deliberately biased toward arm A (its multiple stochastic runs vs arm B's one), so a nugget
  B finds outside A's whole union is a strong "genuinely different evidence" signal. Also
  reports arm A's own multi-run union ceiling, which isolates the query-variety headroom.

Usage:
  uv run python -m eval.analyze_arm_overlap
  uv run python -m eval.analyze_arm_overlap --a-scores eval/artifacts/scores \
      --b-scores eval/artifacts/scores_hybrid --b-run 0
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

SEGREGATED = {"lc-0130"}


def load_support(scores_dir: Path) -> dict[int, dict[tuple[str, str], bool]]:
    """run_index -> {(question_id, nugget_id): supported_in_chunks} over stance/fact nuggets."""
    per_run: dict[int, dict[tuple[str, str], bool]] = defaultdict(dict)
    for p in sorted(scores_dir.glob("*.json")):
        d = json.loads(p.read_text())
        if d["question_id"] in SEGREGATED:
            continue
        idx = d["run_index"]
        for g in d["nugget_grid"]:   # nugget_grid already excludes shift/no_change connections
            per_run[idx][(d["question_id"], g["nugget_id"])] = g["supported_in_chunks"]
    return per_run


def main() -> None:
    ap = argparse.ArgumentParser(description="Per-nugget dir-3 support overlap between two arms.")
    ap.add_argument("--a-scores", default="eval/artifacts/scores", help="arm A score dir (baseline)")
    ap.add_argument("--b-scores", default="eval/artifacts/scores_hybrid", help="arm B score dir (hybrid)")
    ap.add_argument("--a-run", type=int, default=0, help="arm A run index for the 1v1 cut (default 0)")
    ap.add_argument("--b-run", type=int, default=0, help="arm B run index for the 1v1 cut (default 0)")
    ap.add_argument("--a-name", default="baseline", help="label for arm A")
    ap.add_argument("--b-name", default="hybrid", help="label for arm B")
    args = ap.parse_args()

    a = load_support(Path(args.a_scores))
    b = load_support(Path(args.b_scores))
    if args.a_run not in a:
        raise SystemExit(f"arm A has no run index {args.a_run} (found {sorted(a)})")
    if args.b_run not in b:
        raise SystemExit(f"arm B has no run index {args.b_run} (found {sorted(b)})")
    a0, b0 = a[args.a_run], b[args.b_run]
    # Compare only on questions present in BOTH arms. The arms need not cover the same
    # question set (e.g. baseline scores both tiers, the hybrid ablation is longitudinal-only);
    # a nugget whose question one arm never ran is not a "loss", so restrict to the shared
    # question ids or the four-way split is silently confounded by coverage mismatch.
    a_qids = {k[0] for run in a.values() for k in run}
    b_qids = {k[0] for run in b.values() for k in run}
    common_qids = a_qids & b_qids
    dropped = (a_qids | b_qids) - common_qids
    nugs = {k for k in (set(a0) | set(b0)) if k[0] in common_qids}
    tot = len(nugs)
    print(f"questions: {args.a_name}={len(a_qids)}, {args.b_name}={len(b_qids)}, "
          f"shared={len(common_qids)}"
          + (f" (dropped {len(dropped)} not in both: {sorted(dropped)[:5]}...)" if dropped else ""))
    print(f"gradeable stance/fact nuggets on shared questions (per run): "
          f"{args.a_name}={sum(1 for k in a0 if k[0] in common_qids)}, "
          f"{args.b_name}={sum(1 for k in b0 if k[0] in common_qids)}, universe={tot}")

    # ---- fair 1v1 ----
    both_y = a_only = b_only = both_n = 0
    for k in nugs:
        av, bv = a0.get(k, False), b0.get(k, False)
        if av and bv:
            both_y += 1
        elif av:
            a_only += 1
        elif bv:
            b_only += 1
        else:
            both_n += 1
    union1 = both_y + a_only + b_only
    print(f"\n=== FAIR 1v1: {args.b_name}(r{args.b_run}) vs {args.a_name}(r{args.a_run}), "
          f"support = dir-3 supported_in_chunks YES ===")
    print(f"  both YES:            {both_y:3d}  ({both_y / tot:.0%})")
    print(f"  {args.a_name}-only:  {a_only:3d}  ({args.a_name} had, {args.b_name} lost)")
    print(f"  {args.b_name}-only:  {b_only:3d}  ({args.b_name} found, {args.a_name} missed)")
    print(f"  both NO:             {both_n:3d}")
    print(f"  ceilings: {args.a_name} r{args.a_run} {(both_y + a_only) / tot:.1%}  |  "
          f"{args.b_name} {(both_y + b_only) / tot:.1%}")
    print(f"  Jaccard of the two YES-sets: {both_y / union1:.2f}  (intersection {both_y} / union {union1})")

    # ---- union test: does B reach nuggets A NEVER did (any A run)? ----
    a_any = {k: any(a[i].get(k, False) for i in a) for k in nugs}
    n_a_any = sum(a_any.values())
    b_yes = {k for k in nugs if b0.get(k, False)}
    new_from_b = sorted(k for k in b_yes if not a_any[k])
    combined = n_a_any + len(new_from_b)
    print(f"\n=== UNION TEST: does {args.b_name} reach nuggets {args.a_name} NEVER did "
          f"(any of {len(a)} runs)? ===")
    print(f"  {args.a_name} multi-run UNION ceiling: {n_a_any}/{tot} = {n_a_any / tot:.1%}")
    print(f"  {args.b_name} single-run ceiling:      {len(b_yes)}/{tot} = {len(b_yes) / tot:.1%}")
    print(f"  {args.b_name} YES that {args.a_name} NEVER supported: {len(new_from_b)}")
    for k in new_from_b:
        print(f"     + {k[0]} {k[1]}")
    print(f"  combined ({args.a_name}-union + {args.b_name} new): {combined}/{tot} = {combined / tot:.1%} "
          f"(+{len(new_from_b) / tot:.1%}pt over {args.a_name}-union)")


if __name__ == "__main__":
    main()
