"""Task 6 post-run triage: advisory arc scorer (arc / borderline / collection).

ADVISORY TRIAGE ONLY, same status as the leak-advisory pass (Option 3): it sorts the
human's reading order and NEVER drops a candidate, gates, or has its rate reported as a
finding. Per-candidate calls (one candidate per call, no batching), claude-sonnet-5,
thinking disabled. Verdicts are cached by candidate_id + prompt fingerprint; a prompt or
thinking-setting change invalidates the cache. Standing guards: id-echo, cost print with
flush, truncation counted as an error.

Usage:
  uv run python -m eval.score_arcs --calibrate     # 16-item calibration + confusion table
  uv run python -m eval.score_arcs --score         # score all pass candidates (cached, resumable)
  uv run python -m eval.score_arcs --index         # deterministic clustered markdown index
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from core.claude_llm import call_structured, enable_usage_capture, usage_totals
from eval.compose_comparative_claims import normalize, topic_family

OUT = Path("eval/artifacts/query_candidates_longitudinal_claimslice.jsonl")
CACHE = Path("eval/artifacts/arc_scores_cache.json")
INDEX = Path("eval/artifacts/longitudinal_arc_index.md")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 2000        # adaptive thinking needs room for the reasoning trace
CALL_TIMEOUT = 150       # adaptive calls run longer; guards against the hang mode
THINKING: dict = {"type": "adaptive"}   # pre-registered final-attempt config (user override)
THINKING_TAG = f"thinking={THINKING.get('type')}"

EXAMPLE_IDS = ["lc-0130", "lc-0395", "lc-0320", "lc-0374"]

# Calibration set (worked-example ids excluded). Expected groups:
HARD_ARC = ["lc-0070", "lc-0087", "lc-0143", "lc-0398"]
COLLECTION = ["lc-0041", "lc-0108", "lc-0122", "lc-0139", "lc-0192", "lc-0367", "lc-0492"]
FLEXIBLE = ["lc-0018", "lc-0077", "lc-0125", "lc-0204", "lc-0279"]   # human readers disagreed; report only


# ---- verbatim scorer prompt (worked examples filled from the artifact) -----

_SYSTEM_TEMPLATE = """\
You judge whether an evaluation query candidate describes a genuine ARC or a
COLLECTION. You will see: a question, its trajectory_must_say points (the
required claims of the answer), and dated milestones.

DEFINITIONS

ARC: the must_say points describe a DIRECTIONAL CHANGE in the creator's own
position, or in his own test's results, on ONE CONSISTENT OBJECT. Valid shapes:
a stance reversing or softening, a repeated test's results improving or
worsening, a position hardening with accumulating evidence, the creator
explicitly noting that his view shifted. The points must connect: later points
revise, contradict, extend, or respond to earlier ones. Covering the dates,
you could still say what changed and in which direction.

COLLECTION: separate points that share a topic word but do not form one
directional story. Typical shapes: different facets or definitions of a
concept as it appears in different papers; different applications or usages
of a technique; a sequence of news events; several independent opinions on
related things. The points could be reordered without breaking anything.
The honest summary is "he made several different points about X," not
"his view of X changed."

TRAPS TO AVOID
- A collection is still a collection even when every point is substantive,
  accurate, and chronological. Chronology is not direction.
- Watch for REFERENT SHIFT: the same word used for different objects (e.g.
  "decomposition" of tasks vs of world-models; "vector arithmetic" on
  embeddings vs on hidden states). If the object changes between points,
  the points do not form one arc.
- A change in WHICH PAPERS he covers is not a change in HIS position.
- Do not reward an arc-shaped narrative sentence ("his framing shifted from
  narrow to systemic") unless the individual points actually show the
  creator's own position moving on one object.

DECISIVE SIGNAL (overrides the paper-survey trap)
If even one point explicitly reports the creator's OWN position changing on the
object - he "shifted from X to Y", "moved from", "no longer holds", "revised his
earlier view", or the answer states his view at one date contradicts or
supersedes his view at an earlier date - that is arc evidence and it outweighs
the mere presence of several papers or systems. Label arc or borderline, not
collection. A genuine collection contains no point in which the creator's own
position moves; it only reports what different papers say or applies a technique
in different places.

LEXICAL SIGNALS (attention aids, not deterministic rules)
ARC signals - phrases showing the creator's OWN position or his OWN test's
results moving on one consistent object; if present, lean arc or borderline:
- temporal-shift framing on one object: "initially" / "at first" ... "later" /
  "by [date]" / "ultimately" / "eventually" / "came to"
- explicit self-revision: "shifted from", "moved from X to Y", "no longer",
  "reversed", "revised his earlier view", "hardened", "softened", "abandoned
  his earlier", "began by ... culminated in", "contradicts his earlier"
COLLECTION signals - enumeration/survey language with no position-move; if these
dominate and no ARC signal is present, lean collection:
- "different papers", "across systems", "in several/various contexts", "each",
  "separate", "distinct", "as it appears in", "applied to different"
- referent shift: the same term on different objects ("X on embeddings" vs
  "X on hidden states")
- "characterization of the concept", "engagement with the concept"
Decision aid: an ARC signal on ONE consistent object OUTRANKS collection signals.
The hard case - a genuine self-shift point buried among survey language - is arc
or borderline, never collection, because the creator's own position is the thing
that moved. A true collection has no self-shift point at all.
These phrases are hints from a small human-labeled sample. An arc can contain
none of the ARC phrases, and a collection can lack all COLLECTION phrases - the
DEFINITIONS above always decide. Absence of an ARC phrase is never, by itself,
evidence of collection.

WORKED EXAMPLES

Example 1 - ARC (stance reversal):
[[EX_lc-0130]]
Why: he repeatedly concluded there is no emergent intelligence, then by Feb
2026 shifted to a conditional view. One object (emergent intelligence in
LLMs), one direction (denial -> conditional acceptance). Reordering breaks it.

Example 2 - ARC (results evolution):
[[EX_lc-0395]]
Why: the creator's own recurring puzzle test; the puzzle grows more complex
and models' results change across generations. One object (his elevator
test), measurable direction over time.

Example 3 - COLLECTION (definition collection):
[[EX_lc-0320]]
Why: four different papers' usages of the word "policy." No stance of his
changes; the points are independent and reorderable. "He explained policy
in several contexts" is the honest summary.

Example 4 - COLLECTION (the hard case - looks like an arc):
[[EX_lc-0374]]
Why: the points feel progressive (advantage -> hidden -> fake -> business
motive), but they are four separate observations about transparency; nothing
states his own position on one object moving in a direction (no better/worse,
no reversal, no hardening he himself draws). Substantive, chronological -
still a collection.

OUTPUT FORMAT (exactly this, nothing else):
label: arc | borderline | collection
reason: <one sentence naming the object and the direction if arc; or why the
points are separate if collection; borderline only if you can state the
specific unresolved doubt in that one sentence>"""


class ArcVerdict(BaseModel):
    candidate_id: str
    label: Literal["arc", "borderline", "collection"]
    reason: str


def load_candidates(path: Path = OUT) -> list[dict]:
    return [r for r in (json.loads(ln) for ln in path.open()) if "candidate_id" in r]


def render_candidate(c: dict) -> str:
    g = c["gold_draft"]
    lines = [f"Question: {c['query']}", "trajectory_must_say:"]
    lines += [f"- {p}" for p in g["trajectory_must_say"]]
    lines.append("Milestone dates: " + ", ".join(s["date"] for s in g["milestone_slots"]))
    return "\n".join(lines)


def build_system(by_id: dict[str, dict]) -> str:
    system = _SYSTEM_TEMPLATE
    for eid in EXAMPLE_IDS:
        system = system.replace(f"[[EX_{eid}]]", render_candidate(by_id[eid]))
    return system


async def score_one(system: str, c: dict) -> ArcVerdict:
    user = (f"CANDIDATE TO JUDGE:\nCandidate id: {c['candidate_id']}\n{render_candidate(c)}\n\n"
            f"Return label and reason, echoing the candidate id.")
    out = await asyncio.wait_for(
        call_structured(system, user, ArcVerdict, model=MODEL, max_tokens=MAX_TOKENS,
                        thinking=THINKING),
        timeout=CALL_TIMEOUT,
    )
    if out.candidate_id != c["candidate_id"]:
        raise ValueError(f"arc id-echo mismatch: sent {c['candidate_id']} got {out.candidate_id}")
    return out


def _load_cache() -> dict:
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


async def _score_ids(ids: list[str], by_id: dict, system: str, fp: str, cache: dict,
                     persist: bool) -> tuple[dict, int]:
    """Score the given ids (skipping cached), mutating cache. Returns (verdicts_by_id, errors)."""
    n_err = 0
    for cid in ids:
        key = f"{fp}:{cid}"
        if key in cache:
            continue
        try:
            v = await score_one(system, by_id[cid])
            cache[key] = {"label": v.label, "reason": v.reason}
        except Exception as e:  # noqa: BLE001 - truncation/parse counted, never silent
            n_err += 1
            print(f"  arc score ERROR {cid}: {type(e).__name__}: {str(e)[:80]}", flush=True)
            continue
        if persist:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(cache, ensure_ascii=False))
    return {cid: cache.get(f"{fp}:{cid}") for cid in ids}, n_err


# ---- calibration -----------------------------------------------------------

async def _score_retry(system: str, c: dict, attempts: int = 3):
    """Score one candidate, retrying transient failures (timeout/hang) so a spurious
    error does not fail the gate. Final failure returns None (counted as an error)."""
    for k in range(attempts):
        try:
            return await score_one(system, c)
        except Exception as e:  # noqa: BLE001 - transient retried; final counted, never silent
            if k == attempts - 1:
                print(f"  arc ERROR {c['candidate_id']}: {type(e).__name__} (after {attempts})", flush=True)
                return None
            await asyncio.sleep(2)


async def _score_fresh(ids: list[str], by_id: dict, system: str) -> dict:
    """Score every id fresh (no cache) so calibration runs are independent."""
    out = {}
    for cid in ids:
        v = await _score_retry(system, by_id[cid])
        out[cid] = (v.label, v.reason) if v else ("ERROR", "")
    return out


def _report_run(run: int, labels: dict) -> bool:
    def lab(cid: str) -> str:
        return labels[cid][0]

    groups = [("hard-arc", HARD_ARC), ("collection", COLLECTION), ("flexible", FLEXIBLE)]
    print(f"\n=== run {run}: confusion table (expected group -> predicted) ===")
    print(f"{'group':<12} {'arc':>4} {'border':>7} {'coll':>5} {'err':>4}")
    for name, ids in groups:
        row = {k: sum(1 for cid in ids if lab(cid) == k) for k in ("arc", "borderline", "collection", "ERROR")}
        print(f"{name:<12} {row['arc']:>4} {row['borderline']:>7} {row['collection']:>5} {row['ERROR']:>4}")
    for name, ids in groups:
        for cid in ids:
            print(f"  [{name:<10}] {cid} -> {lab(cid):<11} {labels[cid][1][:80]}")
    hard_coll = [cid for cid in HARD_ARC if lab(cid) == "collection"]
    hard_ok = sum(1 for cid in HARD_ARC if lab(cid) in ("arc", "borderline"))
    coll_ok = sum(1 for cid in COLLECTION if lab(cid) in ("collection", "borderline"))
    passed = not hard_coll and hard_ok == 4 and coll_ok >= 5
    print(f"  run {run}: hard-arc->coll={hard_coll or 'none'}  hard_ok={hard_ok}/4  "
          f"coll_ok={coll_ok}/7  -> {'PASS' if passed else 'FAIL'}")
    return passed


async def calibrate() -> None:
    """Pre-registered double-pass gate: two independent fresh runs, both must pass."""
    cands = load_candidates()
    by_id = {c["candidate_id"]: c for c in cands}
    system = build_system(by_id)
    fp = hashlib.sha1((system + THINKING_TAG).encode()).hexdigest()[:8]
    test_ids = HARD_ARC + COLLECTION + FLEXIBLE
    print(f"[arc calibrate DOUBLE-PASS] fp={fp} {THINKING_TAG}; 2 fresh runs x {len(test_ids)} items "
          f"~ ${2 * len(test_ids) * (1900 * 2 + 800 * 10) / 1e6:.2f} (intro pricing)", flush=True)
    enable_usage_capture()
    results = [_report_run(r, await _score_fresh(test_ids, by_id, system)) for r in (1, 2)]
    print(f"\n=== DOUBLE-PASS GATE (both runs must pass): {'PASS' if all(results) else 'FAIL'} ===")
    u = usage_totals()
    if u:
        print(f"  usage: {u['calls']} calls, ${u['input_tokens'] * 2 / 1e6 + u['output_tokens'] * 10 / 1e6:.2f}")


# ---- score all + index (Steps 2-3) -----------------------------------------

async def score_all() -> None:
    cands = load_candidates()
    by_id = {c["candidate_id"]: c for c in cands}
    system = build_system(by_id)
    fp = hashlib.sha1((system + THINKING_TAG).encode()).hexdigest()[:8]
    passes = [c["candidate_id"] for c in cands if c["composition_checks"]["status"] == "pass"]
    cache = _load_cache()
    todo = [cid for cid in passes if f"{fp}:{cid}" not in cache]
    print(f"[arc score] fp={fp} {THINKING_TAG}; {len(passes)} pass candidates, {len(todo)} uncached "
          f"~ ${len(todo) * (1800 * 2 + 60 * 10) / 1e6:.2f} (intro pricing)", flush=True)
    enable_usage_capture()
    _, n_err = await _score_ids(passes, by_id, system, fp, cache, persist=True)
    scored = sum(1 for cid in passes if f"{fp}:{cid}" in cache)
    print(f"[arc score] scored {scored}/{len(passes)}, errors {n_err}", flush=True)
    u = usage_totals()
    if u:
        print(f"  usage: {u['calls']} calls, ${u['input_tokens'] * 2 / 1e6 + u['output_tokens'] * 10 / 1e6:.2f}",
              flush=True)


def _span_days(c: dict) -> int:
    import datetime as dt
    ds = sorted(s["date"] for s in c["gold_draft"]["milestone_slots"])
    return (dt.date.fromisoformat(ds[-1]) - dt.date.fromisoformat(ds[0])).days


def _label(cache: dict, fp: str, cid: str) -> str:
    return (cache.get(f"{fp}:{cid}") or {}).get("label", "unrated")


# Fallback lexical sort keys (deterministic render-sort hint only; NOT a label/verdict).
# The LLM arc scorer was abandoned after failing the pre-registered double-pass gate.
ARC_LEX = ["shifted", "moved from", "no longer", "reversed", "revised", "hardened",
           "softened", "abandoned", "began by", "culminated", "contradicts", "came to",
           "initially", "at first", "ultimately", "eventually"]
COLL_LEX = ["different paper", "across system", "various context", "several context",
            "separate", "distinct", "as it appears", "applied to different",
            "characterization of the concept", "engagement with the concept", "each"]


def _lex(c: dict) -> tuple[int, int]:
    text = " ".join(c["gold_draft"]["trajectory_must_say"]).lower()
    return (sum(text.count(p) for p in ARC_LEX), sum(text.count(p) for p in COLL_LEX))


def build_index() -> None:
    import collections
    cands = load_candidates()
    passes = [c for c in cands if c["composition_checks"]["status"] == "pass"]
    clusters: dict[str, list[dict]] = collections.defaultdict(list)
    for c in passes:
        clusters[topic_family(normalize(c["thread_key"].split(":", 1)[-1]))].append(c)
    order = sorted(clusters, key=lambda k: (-len(clusters[k]), k))

    n_span_viol = sum(1 for c in passes if _span_days(c) < 90)
    out = [f"# Longitudinal cluster index (fallback): {len(passes)} pass candidates, {len(clusters)} clusters",
           "LLM arc scorer ABANDONED (failed the pre-registered double-pass gate). The lex(arc/coll)",
           "hint is a DETERMINISTIC keyword-list render-sort aid ONLY - not a label, not a verdict,",
           "never gates or drops. Clusters by topic (size desc); within a cluster, higher (arc-coll)",
           "lexical score first, then milestone span desc. Read these as reading order, not judgment.",
           f"milestone-span violations (<90 days): {n_span_viol}/{len(passes)}\n"]
    for k in order:
        members = clusters[k]
        members.sort(key=lambda c: (-(_lex(c)[0] - _lex(c)[1]), -_span_days(c)))
        out.append(f"\n## {k}  ({len(members)})")
        for c in members:
            a, kk = _lex(c)
            span = _span_days(c)
            adv = c.get("advisory", {}).get("hint", "?")
            flag = "  SPAN<90" if span < 90 else ""
            out.append(f"\n### {c['candidate_id']}  lex(arc{a}/coll{kk})  span={span}d{flag}  "
                       f"advisory={adv}  milestones={len(c['gold_draft']['milestone_slots'])}")
            out.append(f"**Q:** {c['query']}")
            out.append("must_say:")
            out += [f"- {p}" for p in c["gold_draft"]["trajectory_must_say"]]
    INDEX.write_text("\n".join(out))
    print(f"wrote {INDEX} ({len(passes)} candidates, {len(clusters)} clusters, "
          f"{n_span_viol} span<90 flags)", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--index", action="store_true")
    args = ap.parse_args()
    if args.calibrate:
        asyncio.run(calibrate())
    elif args.score:
        asyncio.run(score_all())
    elif args.index:
        build_index()
    else:
        ap.error("one of --calibrate / --score / --index required")


if __name__ == "__main__":
    main()
