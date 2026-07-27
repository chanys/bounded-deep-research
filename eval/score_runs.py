"""Phase 4 D: score the A2 runs with the frozen judge + extractors, attribute, and report.

For each scored (question, run) the frozen judge (prompt_sha a7d71e4a, Sonnet 5) produces:
- recall (dir 1): each gold nugget vs the answer -> recall = hits / stance-nuggets.
- groundedness (dir 2): each C1-extracted answer-claim vs the run's retrieved chunk SET -> supported / extracted.
- attribution (dir 3, for MISSED nuggets): missed nugget vs the run's surfaced chunk set -> HIT = supported-but-
  unused = SYNTHESIS failure; MISS = never-surfaced = RETRIEVAL failure. Semantic, judge-based - never
  gold_chunk_id in seen_chunks (that is the chunk-recall metric the gold redesign exists to escape).

Connection nuggets are logged separately, not in the recall denominator: the shift nugget as its own pass
boolean; lc-0130 (the no_change trap) is SEGREGATED entirely and reported apart from the recall average.

Guards at load / run:
- Frozen-instrument assertion: the judge and C1 prompt hashes must equal the calibrated values, else the
  instrument drifted and the numbers are not comparable (fail loud).
- Corpus-drift assertion: recompute corpus_id(channel) and require it equals the corpus_id every run recorded,
  since chunk text is re-fetched at score time (halt on mismatch rather than ground against a shifted corpus).

Resumable: each (question, run) score is cached under eval/artifacts/scores/; a re-run skips existing files.

Usage:
  uv run python -m eval.score_runs --only lc-0011,fc-0001 --runs 3   # first small batch (spot-check gate)
  uv run python -m eval.score_runs                                    # full scored set
  uv run python -m eval.score_runs --report-only                      # re-aggregate from cache
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from app.corpus import corpus_id
from core.claude_llm import call_structured, enable_usage_capture, usage_totals
from eval.calibrate_judge import load_factual, load_longitudinal
from eval.extract_answer_claims import PROMPT_SHA as C1_SHA
from eval.extract_answer_claims import extract_claims
from eval.judge import JUDGE_PROMPT_SHA, format_chunk_set, judge

MODEL = "claude-sonnet-5"

CHANNEL = "code4AI"
RUNS = Path("eval/artifacts/runs")
SCORES = Path("eval/artifacts/scores")
MISS_CLASS = Path("eval/artifacts/miss_class.json")
SEGREGATED = {"lc-0130"}   # no_change presupposition trap: reported apart from the recall average


# ---- longitudinal stance-miss classifier (post-hoc, reason-based diagnostic) ----
# Splits longitudinal stance-nugget MISSes into timing vs stance, so a system that finds the
# right stance but misplaces it in time is distinguished from one that never finds it (a
# plausible pattern given the recency-skewed corpus). Post-hoc over misses only, reusing the
# judge's own reason - no new judge calls. This is an un-calibrated diagnostic split, NOT a
# scored metric, so it is labeled as such in the report and hashed for provenance.

class MissClass(BaseModel):
    category: Literal["timing", "stance"]
    why: str


MISS_CLASS_SYSTEM = """\
A recall MISS on a dated longitudinal stance nugget (a position the creator held, with a time window) can fail two ways. Classify which, given the gold NUGGET, the ANSWER, and the judge's MISS REASON.

- "timing": the answer DOES convey the stance's substance (the position/finding itself), but places it in an incompatible time window, or gives timing the judge found insufficient - right stance, wrong or missing time.
- "stance": the answer does NOT convey the stance's substance at all, or conveys a materially different position - the failure is the stance itself, not its timing.

If both are arguably wrong, pick the more fundamental: if the substance is absent or different, that is "stance"; only call it "timing" when the substance is clearly present and just mis-dated."""

MISS_CLASS_SHA = hashlib.sha1(MISS_CLASS_SYSTEM.encode()).hexdigest()[:8]


async def classify_miss(nugget_text: str, answer: str, reason: str) -> MissClass:
    user = (f"NUGGET (gold stance + time window):\n{nugget_text}\n\nANSWER:\n{answer}\n\n"
            f"JUDGE'S MISS REASON:\n{reason}\n\nClassify this miss: timing or stance.")
    return await call_structured(MISS_CLASS_SYSTEM, user, MissClass, model=MODEL,
                                 max_tokens=1500, thinking={"type": "adaptive"})

# Frozen instruments (must match the calibrated/frozen values or the numbers are not comparable).
FROZEN_JUDGE_SHA = "a7d71e4a"
FROZEN_C1_SHA = "c7cbc275"
SCORE_PROVENANCE = {
    "judge_model": "claude-sonnet-5",
    "judge_prompt_sha": JUDGE_PROMPT_SHA,
    "judge_calibration": {"kappa": 0.879, "raw_agreement": 0.939, "n_pairs": 66, "seed": 20260726},
    "answer_claim_extractor_sha": C1_SHA,
    "factual_nugget_extractor_sha": "910a6696",
    "entailment_audit_sha": "ddfc49a9",
    "miss_classifier_sha": MISS_CLASS_SHA,   # un-calibrated diagnostic split, not a scored metric
    "factual_gold": "factual-gold-v1.0",
    "longitudinal_gold": "gold-v0.2.2",
}


def _assert_frozen() -> None:
    if JUDGE_PROMPT_SHA != FROZEN_JUDGE_SHA:
        raise SystemExit(f"judge prompt drifted: {JUDGE_PROMPT_SHA} != frozen {FROZEN_JUDGE_SHA}; re-calibrate before scoring")
    if C1_SHA != FROZEN_C1_SHA:
        raise SystemExit(f"C1 extractor drifted: {C1_SHA} != frozen {FROZEN_C1_SHA}")


def load_gold() -> dict[str, list[dict]]:
    """question_id -> [{nugget_id, text, type}] for both tiers (longitudinal + factual v1.0)."""
    gold: dict[str, list[dict]] = defaultdict(list)
    for n in load_longitudinal():
        gold[n["question_id"]].append({"nugget_id": n["nugget_id"], "text": n["text"], "type": n["type"]})
    for n in load_factual():
        gold[n["question_id"]].append({"nugget_id": n["nugget_id"], "text": n["text"], "type": "fact"})
    return gold


def load_run(qid: str, idx: int) -> dict | None:
    p = RUNS / qid / f"r{idx}" / "run.json"
    return json.loads(p.read_text()) if p.exists() else None


async def score_run(run: dict, nuggets: list[dict], sem: asyncio.Semaphore) -> dict:
    """Score one (question, run): recall, groundedness, attribution. All judge calls under `sem`."""
    qid, idx = run["question_id"], run["run_index"]
    tier = "longitudinal" if qid.startswith("lc") else "factual"
    answer = run["answer"]
    seen = list(run["evidence"]["seen_chunks"])
    chunkset = format_chunk_set(seen)   # one DB fetch + render per run

    async def j(claim, text, ct, tk):
        async with sem:
            v = await judge(claim, text=text, claim_type=ct, text_kind=tk)
        return v

    # recall (dir 1): every nugget vs the answer
    recall = await asyncio.gather(*(j(n["text"], answer, n["type"], "answer") for n in nuggets))
    recall_details = [{"nugget_id": n["nugget_id"], "type": n["type"], "hit": v.hit, "reason": v.reason}
                      for n, v in zip(nuggets, recall)]

    # groundedness (dir 2): C1 answer-claims vs the retrieved chunk set
    claims = await extract_claims(answer, sem)
    ground = await asyncio.gather(*(j(c, chunkset, "fact", "chunks") for c in claims))
    ground_details = [{"claim": c, "hit": v.hit, "reason": v.reason} for c, v in zip(claims, ground)]

    # dir 3 on ALL stance/fact nuggets (not just missed): gives the full recall x supported 2x2,
    # so one pass yields the retrieval ceiling, synthesis conversion, inequality violations, and
    # the missed-nugget attribution split. shift/no_change are connections, not grounded here.
    gradeable = [(n, d) for n, d in zip(nuggets, recall_details) if n["type"] not in ("shift", "no_change")]
    dir3 = await asyncio.gather(*(j(n["text"], chunkset, n["type"], "chunks") for n, _ in gradeable))
    nugget_grid = [{"nugget_id": n["nugget_id"], "type": n["type"], "recall_hit": d["hit"],
                    "supported_in_chunks": v.hit, "dir3_reason": v.reason}
                   for (n, d), v in zip(gradeable, dir3)]

    return {
        "question_id": qid, "run_index": idx, "tier": tier,
        "segregated": qid in SEGREGATED,
        "recall_details": recall_details,
        "ground_details": ground_details,
        "nugget_grid": nugget_grid,
        "corpus_id": run["evidence"]["provenance"]["corpus_id"],
    }


# ---- aggregation + report --------------------------------------------------

def _stance_recall(rec: dict) -> tuple[int, int]:
    """(hits, total) over stance/fact nuggets only (shift + no_change excluded)."""
    ns = [d for d in rec["recall_details"] if d["type"] not in ("shift", "no_change")]
    return sum(d["hit"] for d in ns), len(ns)


def _miss_key(qid: str, idx: int, nugget_id: str) -> str:
    return f"{qid}|r{idx}|{nugget_id}"


async def classify_longitudinal_misses(scores: list[dict], gold: dict[str, list[dict]],
                                       concurrency: int) -> dict[str, str]:
    """timing/stance category for every longitudinal stance MISS. Resumable via MISS_CLASS cache."""
    cache: dict[str, str] = json.loads(MISS_CLASS.read_text()) if MISS_CLASS.exists() else {}
    gold_text = {(qid, n["nugget_id"]): n["text"] for qid in gold for n in gold[qid]}
    todo = []
    for s in scores:
        if s["tier"] != "longitudinal":
            continue
        for d in s["recall_details"]:
            if d["type"] == "stance" and not d["hit"]:
                k = _miss_key(s["question_id"], s["run_index"], d["nugget_id"])
                if k not in cache:
                    todo.append((k, s["question_id"], s["run_index"], d["nugget_id"], d["reason"]))
    if todo:
        sem = asyncio.Semaphore(concurrency)

        async def one(k, qid, idx, nid, reason):
            run = load_run(qid, idx)
            async with sem:
                mc = await classify_miss(gold_text[(qid, nid)], run["answer"], reason)
            return k, mc.category
        for k, cat in await asyncio.gather(*(one(*t) for t in todo)):
            cache[k] = cat
        MISS_CLASS.write_text(json.dumps(cache, indent=2))
    return cache


def aggregate(scores: list[dict], miss_class: dict[str, str] | None = None) -> str:
    miss_class = miss_class or {}
    lines = ["# Phase 4 scoring report", "", "Score-time provenance:", "```",
             json.dumps(SCORE_PROVENANCE, indent=2), "```", ""]

    scored = [s for s in scores if not s["segregated"]]
    for tier in ("longitudinal", "factual"):
        ts = [s for s in scored if s["tier"] == tier]
        if not ts:
            continue
        # per run_index: macro-average recall / groundedness over that index's questions
        rec_by_idx, grd_by_idx = {}, {}
        for idx in sorted({s["run_index"] for s in ts}):
            si = [s for s in ts if s["run_index"] == idx]
            recs = [h / t for s in si for (h, t) in [_stance_recall(s)] if t]
            grds = [sum(d["hit"] for d in s["ground_details"]) / len(s["ground_details"])
                    for s in si if s["ground_details"]]
            rec_by_idx[idx] = sum(recs) / len(recs) if recs else 0.0
            grd_by_idx[idx] = sum(grds) / len(grds) if grds else 0.0
        rv, gv = list(rec_by_idx.values()), list(grd_by_idx.values())
        lines += [f"## {tier} ({len({s['question_id'] for s in ts})} questions x {len(rv)} runs)", "",
                  f"- recall:       mean {sum(rv) / len(rv):.1%}   range [{min(rv):.1%}, {max(rv):.1%}] across runs",
                  f"- groundedness: mean {sum(gv) / len(gv):.1%}   range [{min(gv):.1%}, {max(gv):.1%}] across runs"]
        if tier == "longitudinal":
            shifts = [d["hit"] for s in ts for d in s["recall_details"] if d["type"] == "shift"]
            if shifts:
                lines.append(f"- shift-nugget pass rate: {sum(shifts) / len(shifts):.1%} ({sum(shifts)}/{len(shifts)})")
            # stance-miss breakdown: timing (right stance, wrong window) vs stance (not conveyed)
            cats = [miss_class.get(_miss_key(s["question_id"], s["run_index"], d["nugget_id"]))
                    for s in ts for d in s["recall_details"] if d["type"] == "stance" and not d["hit"]]
            if cats:
                nt = cats.count("timing")
                ns = cats.count("stance")
                lines.append(f"- stance-miss breakdown: {nt} timing (right stance, wrong/missing window), "
                             f"{ns} stance (not conveyed) [un-calibrated reason-based diagnostic]")
        # dir-3-on-all-nuggets: the recall x supported 2x2 across every stance/fact nugget-run
        grid = [g for s in ts for g in s["nugget_grid"]]
        if grid:
            supported = [g for g in grid if g["supported_in_chunks"]]
            ceiling = len(supported) / len(grid)
            conversion = (sum(1 for g in supported if g["recall_hit"]) / len(supported)) if supported else 0.0
            missed = [g for g in grid if not g["recall_hit"]]
            syn = sum(1 for g in missed if g["supported_in_chunks"])
            violations = [g for g in grid if g["recall_hit"] and not g["supported_in_chunks"]]
            lines += [
                f"- retrieval ceiling:    {ceiling:.1%}  ({len(supported)}/{len(grid)} gold nuggets had supporting evidence in the retrieved set)",
                f"- synthesis conversion: {conversion:.1%}  (of retrieved-evidence nuggets, fraction expressed in the answer)",
                f"- missed-nugget attribution: {syn}/{len(missed)} synthesis (surfaced-but-unused), "
                f"{len(missed) - syn}/{len(missed)} retrieval (never-surfaced)",
                f"- inequality violations (answer HIT, chunks MISS): {len(violations)} - each is parametric leakage or a judge artifact, listed below",
            ]
        lines.append("")

    # Inequality violations listed individually (they need reading, not counting)
    viols = [(s["question_id"], s["run_index"], g) for s in scored for g in s["nugget_grid"]
             if g["recall_hit"] and not g["supported_in_chunks"]]
    lines += ["## Inequality violations (answer states it, retrieved chunks do not support it)", "",
              "Each is either parametric leakage (agent stated gold content it did not retrieve) or a "
              "judge artifact (clean answer prose easier to confirm than garbled ASR). Read each.", ""]
    if viols:
        for qid, idx, g in sorted(viols):
            lines.append(f"- {qid} r{idx} {g['nugget_id']} ({g['type']}): dir-3 said no support :: {g['dir3_reason']}")
    else:
        lines.append("- (none)")
    lines.append("")

    # lc-0130 reported separately
    seg = [s for s in scores if s["segregated"]]
    if seg:
        lines += ["## lc-0130 (SEGREGATED - no_change trap, excluded from recall average)", ""]
        for s in seg:
            nc = [d for d in s["recall_details"] if d["type"] == "no_change"]
            st = [d for d in s["recall_details"] if d["type"] == "stance"]
            lines.append(f"- r{s['run_index']}: no_change {'HIT' if nc and nc[0]['hit'] else 'MISS'}; "
                         f"stance {sum(d['hit'] for d in st)}/{len(st)}")
        lines.append("")

    # 10 lowest-scoring questions by mean stance-recall across runs
    by_q: dict[str, list[dict]] = defaultdict(list)
    for s in scored:
        by_q[s["question_id"]].append(s)
    q_recall = {}
    for qid, ss in by_q.items():
        vals = [h / t for s in ss for (h, t) in [_stance_recall(s)] if t]
        q_recall[qid] = sum(vals) / len(vals) if vals else 0.0
    worst = sorted(q_recall.items(), key=lambda kv: kv[1])[:10]
    lines += ["## 10 lowest-recall questions (for the human read)", ""]
    for qid, r in worst:
        ss = by_q[qid]
        missed_ids = sorted({d["nugget_id"] for s in ss for d in s["recall_details"]
                             if not d["hit"] and d["type"] not in ("shift", "no_change")})
        missed = [g for s in ss for g in s["nugget_grid"] if not g["recall_hit"]]
        syn = sum(1 for g in missed if g["supported_in_chunks"])
        lines.append(f"- {qid}: recall {r:.0%}; missed nuggets {missed_ids or '-'}; "
                     f"attribution {syn} synthesis / {len(missed) - syn} retrieval")
    return "\n".join(lines)


# ---- driver ----------------------------------------------------------------

def _cache_path(qid: str, idx: int) -> Path:
    return SCORES / f"{qid}__r{idx}.json"


def _read_cached() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(SCORES.glob("*.json"))]


# Sonnet 5 standard rate (assumption; token counts are measured, rate is the only estimate).
_SONNET_IN_PER_TOK = 3.0 / 1_000_000
_SONNET_OUT_PER_TOK = 15.0 / 1_000_000


def _report_cost(n_scored_runs: int) -> None:
    u = usage_totals()
    if not u:
        return
    cost = u["input_tokens"] * _SONNET_IN_PER_TOK + u["output_tokens"] * _SONNET_OUT_PER_TOK
    print(f"\ntoken usage over {n_scored_runs} scored runs: {u}", flush=True)
    print(f"est cost: ${cost:.2f} at Sonnet $3/$15 per M (output incl. thinking)", flush=True)
    if n_scored_runs:
        print(f"per-run: ${cost / n_scored_runs:.3f}  ->  extrapolated to 183 scored runs: "
              f"${cost / n_scored_runs * 183:.2f}", flush=True)


async def amain(args: argparse.Namespace) -> None:
    _assert_frozen()
    enable_usage_capture()
    if args.report_only:
        cached = _read_cached()
        mc = await classify_longitudinal_misses(cached, load_gold(), args.concurrency)
        report = aggregate(cached, mc)
        Path("eval/artifacts/scoring_report.md").write_text(report, encoding="utf-8")
        print(report)
        return

    gold = load_gold()
    qids = [q.strip() for q in args.only.split(",")] if args.only else sorted(gold)
    qids = [q for q in qids if q in gold]   # scored set excludes fc-0036 (not in gold)

    # corpus-drift guard: current corpus must match what the runs recorded.
    current = corpus_id(CHANNEL)
    sample = next((load_run(q, 0) for q in qids if load_run(q, 0)), None)
    if sample and sample["evidence"]["provenance"]["corpus_id"] != current:
        raise SystemExit(f"corpus drift: runs stamped {sample['evidence']['provenance']['corpus_id']} "
                         f"but current corpus is {current}; scoring would ground against a different corpus")

    SCORES.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(args.concurrency)
    todo = [(q, i) for q in qids for i in range(args.runs) if not _cache_path(q, i).exists()]
    print(f"scoring {len(todo)} (question, run) pairs (concurrency {args.concurrency}); "
          f"judge {JUDGE_PROMPT_SHA}, C1 {C1_SHA}", flush=True)

    async def one(qid, idx):
        run = load_run(qid, idx)
        if not run:
            return
        rec = await score_run(run, gold[qid], sem)
        _cache_path(qid, idx).write_text(json.dumps(rec, indent=2))
        h, t = _stance_recall(rec)
        print(f"  scored {qid} r{idx}: recall {h}/{t}, "
              f"grounded {sum(d['hit'] for d in rec['ground_details'])}/{len(rec['ground_details'])}", flush=True)

    await asyncio.gather(*(one(q, i) for q, i in todo))
    _report_cost(len(todo))
    cached = _read_cached()
    mc = await classify_longitudinal_misses(cached, gold, args.concurrency)
    report = aggregate(cached, mc)
    Path("eval/artifacts/scoring_report.md").write_text(report, encoding="utf-8")
    print("\n" + report, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Score the A2 runs (Phase D).")
    ap.add_argument("--only", default="", help="comma-separated question ids (default: full scored set)")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--report-only", action="store_true", help="re-aggregate from cached scores, no judging")
    asyncio.run(amain(ap.parse_args()))


if __name__ == "__main__":
    main()
