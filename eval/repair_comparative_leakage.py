"""Task 5.5 v2.1: audit-first semantic-leakage repair on the comparative candidates.

Builds on the v2 output (does not restart from v1). For every candidate it audits the
current final wording, re-repairs only audit failures with a stricter neutral-form
prompt + named-status checker, and on a double failure falls back to the ORIGINAL v1
wording (a question that traded leakage for axis-drift is not an improvement worth
keeping). Nothing is dropped. A completeness invariant (output ids == input ids) is a
hard assertion before rendering.

Audit per candidate: per-side leak on the original (pre) and final (post) wording; an
axis analysis (original axis, validity fields - advisory, neutralizability, and whether
the final wording drifted from the original axis); and the deterministic wording scan
(eval/text_guards). Re-repair checker returns a named failure: leak, axis_drift,
gold_insufficient, two_factuals, subject_unnameable, underdetermined; deterministic
meta_reference / stilted_opener come from text_guards.

Usage:
  uv run python -m eval.repair_comparative_leakage
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval.text_guards import completeness_assert, violation_scan

V1_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice.jsonl")
V2_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice_v2.jsonl")
OUT_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice_v21.jsonl")
RENDER_DEFAULT = Path("eval/artifacts/comparative_claimslice_v21_sample.md")
CACHE_DEFAULT = Path("eval/artifacts/comparative_repair_v21_cache.json")
MODEL = "claude-sonnet-5"
LEAK_MAX_TOKENS = 700
AXIS_MAX_TOKENS = 2500   # adaptive thinking + 9 fields; 1200 truncated
RECOMPOSE_MAX_TOKENS = 2500
CHECK_MAX_TOKENS = 1500
CALL_TIMEOUT = 120
MAX_ATTEMPTS = 2
VARIETY_WINDOW = 40
TIER = "comparative"

FINAL_STATUS = {"pass", "leak", "axis_drift", "invalid_original_axis", "meta_reference",
                "gold_insufficient", "two_factuals", "subject_unnameable", "stilted_opener",
                "unneutralizable", "repair_error"}


# ---- prompts ---------------------------------------------------------------

LEAK_SIDE_SYSTEM = """\
You classify which side's SPECIFIC CONTENT a comparison question discloses. You are given the QUESTION and the two gold CLAIMS (one per subject).

A side is LEAKED only when the question states or paraphrases what that subject specifically DOES, FOUND, ACHIEVED, or CONCLUDED - its mechanism, result, metric, verdict, or design choice - so that the answer for that side is already in the question. This holds even when the content is embedded as framing or a subordinate clause.

A side is NOT leaked when the question merely names the subject and the shared comparison AXIS - the dimension along which the two are compared - even a technical-sounding axis. Naming WHAT is compared is not disclosing what each side did.

Setup vs content: stating a subject's SETUP, CONDITION, or CONTEXT is NOT a leak; stating its BEHAVIOR, FINDING, or OUTCOME is. "How did Gemini tackle the puzzle when code execution was enabled" names a condition (not a leak). "Gemini's strategy of redefining the task as math functions" states the behavior (leak).

Named method is content: naming the SPECIFIC method, algorithm, or training technique a subject uses (e.g. "continual pre-training", "Monte Carlo tree search"), or describing what that method accomplishes for it, discloses that side. The axis is the shared QUESTION the two sides answer (e.g. "how each adapts to new data without forgetting"), not the named technique that IS one side's answer.

Tiebreak when unsure whether a phrase is an axis or a disclosed mechanism: ask "could the agent produce a scoreable answer from the QUESTION TEXT ALONE?" If NO (a correct answer still requires reading the claims), it is an axis - not a leak. If YES (the question already carries the answer), it is a leak. Judge by this harm model, not by how technical the wording sounds.

Return leaked_side: "none", "claim_a", "claim_b", or "both", a one-line reason, and echo the candidate_id."""

AXIS_AUDIT_SYSTEM = """\
You audit a comparison-question pair. You are given the ORIGINAL question, the CURRENT (possibly rewritten) question, and the two gold claims. Return, echoing candidate_id:
- comparison_axis: the shared dimension the ORIGINAL question intends to compare (a short phrase).
- axis_supported_by_claim_a / axis_supported_by_claim_b: does each claim actually speak to that axis?
- same_conceptual_level: are the two sides at the same conceptual level (method vs method, evaluation vs evaluation), not apples-to-oranges?
- both_sides_required: does a correct answer require both claims (not answerable from one alone)?
- invalid_original_axis: true if the original axis is not a valid, commensurable comparison at all (advisory).
- neutralizable: default TRUE. Set FALSE ONLY when the pair is structurally impossible to neutralize: a subject whose claim gives only a generic descriptor ("the paper", "the study", "the world-generation framework") with no real proper name - the test is whether the claim supplies a real name, not whether the word "unnamed" appears - OR a pair with no substantive comparable content (pure availability/metadata, e.g. where a model can be downloaded). A merely weak, broad, low-value, or number-driven pair is still neutralizable (TRUE). Do NOT use this to drop weak pairs; when in doubt, TRUE.
- final_axis_drift: does the CURRENT question compare a DIFFERENT axis than the ORIGINAL intended (its comparison changed)?"""

RECOMPOSE_SYSTEM = """\
You rewrite a comparison question so it names both subjects and their comparison axis but discloses NEITHER side's content, and reads like a real practitioner's question. You are given the two gold claims (one per subject) and the intended comparison axis (preserve it).

Rules:
- Name BOTH subjects (the specific model/method/system/paper in each claim) and state the comparison axis concretely.
- Disclose NEITHER side's mechanism, finding, result, verdict, or design, and never reveal an outcome. The two claims are the gold answer: the question must require both and must not paraphrase either.
- Preserve the intended comparison axis - do not shift to a different comparison.
- Standalone practitioner phrasing: NO "the creator", "creator's", "this video", "these videos", "previous video", "earlier", "the second paper", "unnamed", or any reference to the corpus or videos. Public entity names are fine; a creator-specific construct is described by what it is (e.g. "an elevator-style causal-reasoning puzzle"), never as "the creator's".
- Integrate the axis INTO the question body; do NOT front-load it as a topic-marker preamble. GOOD: "How do A and B differ in <axis>?" or "How did A's <axis> compare to B's?". BANNED: opening with "In terms of", "When it comes to", "Regarding", "With respect to", "As for" followed by a comma.
- Vary sentence STRUCTURE across questions (not a rotation of preamble phrases); do not resemble the already-written questions.

Test before you answer: would a practitioner watching this channel actually type this question? If the question needs a preamble to state its axis, fold the axis into the question instead.

Return the question and the comparison_axis it uses (a short phrase)."""

CHECK_SYSTEM = """\
You validate a rewritten comparison question against its two gold claims and the intended comparison axis (given). Return ok=true only if it passes ALL of the following; otherwise ok=false with the single most important failure:
- leak: it states or paraphrases what a subject specifically DOES, FOUND, or ACHIEVED (mechanism/result/verdict/design), so that side's answer is already in the question - even when embedded as framing or a subordinate clause. NOT a leak: merely naming a subject and the shared comparison axis (even a technical axis), or naming a subject's setup/condition/context. Tiebreak: if the agent could NOT produce a scoreable answer from the question text alone, it is an axis, not a leak.
- axis_drift: its comparison changed from the intended axis to a different comparison.
- gold_insufficient: fully answering it would need information beyond the two gold claims (the claims must contain the whole answer). Check EACH side: if the question asks for a property (approach, structure, mechanism, result, quality) that EITHER claim does not actually contain, it is gold_insufficient - even if the other claim does. E.g. it asks for a side's "approach" or "structure" but that claim carries only a step count, a bare label ("is an agent framework"), or a metadata fact.
- two_factuals: it staples two unrelated facts with "compared to" and has no genuine shared axis.
- subject_unnameable: a side's subject is only a generic descriptor ("the paper", "the world-generation framework") with no real proper name in its claim - the test is whether the claim supplies a real name, not whether the word "unnamed" appears. Never a valid neutralization.
- underdetermined: it is too vague for the two claims to determine a right answer (librarian test).
Return ok, failure (one of those or null), and a one-line reason."""


class LeakSide(BaseModel):
    candidate_id: str
    leaked_side: Literal["none", "claim_a", "claim_b", "both"]
    reason: str


class AxisAudit(BaseModel):
    candidate_id: str
    comparison_axis: str
    axis_supported_by_claim_a: bool
    axis_supported_by_claim_b: bool
    same_conceptual_level: bool
    both_sides_required: bool
    invalid_original_axis: bool
    neutralizable: bool
    final_axis_drift: bool


class Recomposed(BaseModel):
    query: str
    comparison_axis: str


class CheckV21(BaseModel):
    ok: bool
    failure: Literal["leak", "axis_drift", "gold_insufficient", "two_factuals",
                     "subject_unnameable", "underdetermined"] | None = None
    reason: str = ""


# ---- identity / cache ------------------------------------------------------

def _h(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(ln) for ln in path.read_text().splitlines()
            if ln.strip() and '"_meta"' not in ln[:12]]


# ---- LLM steps -------------------------------------------------------------

async def leak_side(cid: str, q: str, a: str, b: str, sem) -> LeakSide:
    user = f"candidate_id: {cid}\n\nQUESTION: {q}\n\nCLAIM A: {a}\nCLAIM B: {b}"
    async with sem:
        out = await asyncio.wait_for(
            call_structured(LEAK_SIDE_SYSTEM, user, LeakSide, model=MODEL,
                            max_tokens=LEAK_MAX_TOKENS, thinking={"type": "disabled"}), timeout=CALL_TIMEOUT)
    if out.candidate_id != cid:
        raise ValueError(f"id echo mismatch {cid} != {out.candidate_id}")
    return out


async def axis_audit(cid: str, original: str, final: str, a: str, b: str, sem) -> AxisAudit:
    user = (f"candidate_id: {cid}\n\nORIGINAL question: {original}\n\nCURRENT question: {final}\n\n"
            f"CLAIM A: {a}\nCLAIM B: {b}")
    async with sem:
        out = await asyncio.wait_for(
            call_structured(AXIS_AUDIT_SYSTEM, user, AxisAudit, model=MODEL,
                            max_tokens=AXIS_MAX_TOKENS, thinking={"type": "adaptive"}), timeout=CALL_TIMEOUT)
    if out.candidate_id != cid:
        raise ValueError(f"id echo mismatch {cid} != {out.candidate_id}")
    return out


async def recompose(a: str, b: str, axis: str, priors: list[str]) -> Recomposed:
    lines = [f"Claim A (subject 1): {a}", f"Claim B (subject 2): {b}",
             f"Intended comparison axis (preserve this): {axis}"]
    if priors:
        lines.append("\nAlready written (vary structure, do not resemble):")
        lines += [f"- {q}" for q in priors[-VARIETY_WINDOW:]]
    lines.append("\nWrite one neutral, natural comparison question.")
    return await asyncio.wait_for(
        call_structured(RECOMPOSE_SYSTEM, "\n".join(lines), Recomposed, model=MODEL,
                        max_tokens=RECOMPOSE_MAX_TOKENS, thinking={"type": "adaptive"}), timeout=CALL_TIMEOUT)


async def check(q: str, declared_axis: str, intended_axis: str, a: str, b: str) -> CheckV21:
    user = (f"INTENDED axis: {intended_axis}\nDECLARED axis of this question: {declared_axis}\n\n"
            f"QUESTION: {q}\n\nCLAIM A: {a}\nCLAIM B: {b}")
    return await asyncio.wait_for(
        call_structured(CHECK_SYSTEM, user, CheckV21, model=MODEL,
                        max_tokens=CHECK_MAX_TOKENS, thinking={"type": "adaptive"}), timeout=CALL_TIMEOUT)


def _det_status(violations: list[str]) -> str:
    return "stilted_opener" if violations == ["stilted_opener"] else "meta_reference"


# ---- driver ----------------------------------------------------------------

async def amain(args: argparse.Namespace) -> None:
    v1 = {c["candidate_id"]: c for c in load_jsonl(args.v1)}
    v2 = load_jsonl(args.v2)                       # build on v2 output
    input_ids = list(v1)                           # canonical 40; output must equal these exactly
    cache: dict = json.loads(args.cache.read_text()) if args.cache.exists() else {}

    def cached(key, coro_factory):
        async def run():
            if key in cache:
                return cache[key]
            cache[key] = (await coro_factory()).model_dump()
            return cache[key]
        return run()

    print(f"[cost estimate] rough upper bound: audit ~{len(v2) * 3} calls + re-repair up to "
          f"{len(v2)} x {MAX_ATTEMPTS} x2 ~ ${(len(v2) * 3 + len(v2) * MAX_ATTEMPTS * 2) * 0.01:.2f}", flush=True)

    sem = asyncio.Semaphore(args.concurrency)
    n_err = 0
    errors: list[dict] = []

    # ---- audit (concurrent, cached) ----
    audit: dict[str, dict] = {}

    async def _audit(c):
        nonlocal n_err
        cid, a, b = c["candidate_id"], c["gold_draft"][0], c["gold_draft"][1]
        orig, fin = c["original_query"], c["final_query"]
        try:
            post = await cached(f"leak:{cid}:{_h(fin)}", lambda: leak_side(cid, fin, a, b, sem))
            pre = post if fin == orig else await cached(f"leak:{cid}:{_h(orig)}", lambda: leak_side(cid, orig, a, b, sem))
            ax = await cached(f"axis:{cid}:{_h(orig)}:{_h(fin)}", lambda: axis_audit(cid, orig, fin, a, b, sem))
        except Exception as e:  # noqa: BLE001
            n_err += 1
            errors.append({"candidate_id": cid, "error": f"audit {type(e).__name__}"})
            return
        det = violation_scan(fin, TIER)
        audit[cid] = {"leak_pre": pre["leaked_side"], "leak_post_audit": post["leaked_side"],
                      "axis": ax, "det": det,
                      "fail": post["leaked_side"] != "none" or ax["final_axis_drift"] or bool(det)}
    await asyncio.gather(*(_audit(c) for c in v2))
    args.cache.parent.mkdir(parents=True, exist_ok=True)
    args.cache.write_text(json.dumps(cache, ensure_ascii=False))

    # ---- re-repair (sequential, only audit failures, cached) ----
    priors: list[str] = []
    result: dict[str, dict] = {}
    for c in v2:
        cid, a, b = c["candidate_id"], c["gold_draft"][0], c["gold_draft"][1]
        au = audit.get(cid)
        if au is None:                                # audit errored: keep v1 original, repair_error
            result[cid] = {"final": v1[cid]["query"], "source": "original_after_repair_failure",
                           "status": "repair_error", "attempts": 0, "violations": [], "post": "none"}
            continue
        if not au["fail"]:                            # unflagged: keep v2 final wording
            src = "v2_recomposed" if c["final_query"] != c["original_query"] else "original_unflagged"
            result[cid] = {"final": c["final_query"], "source": src, "status": "pass",
                           "attempts": 0, "violations": [], "post": au["leak_post_audit"]}
            continue
        if not au["axis"]["neutralizable"]:           # structurally unneutralizable: skip spend
            result[cid] = {"final": v1[cid]["query"], "source": "original_after_repair_failure",
                           "status": "unneutralizable", "attempts": 0,
                           "violations": au["det"], "post": au["leak_pre"]}
            continue
        # re-repair up to MAX_ATTEMPTS
        intended = au["axis"]["comparison_axis"]
        viols: list[str] = list(au["det"])
        final_q = last = None
        attempts = 0
        for attempts in range(1, MAX_ATTEMPTS + 1):
            key = f"repair:{cid}:{attempts}"
            try:
                if key in cache:
                    rc = Recomposed(**cache[key])
                else:
                    rc = await recompose(a, b, intended, priors)
                    cache[key] = rc.model_dump()
                dv = violation_scan(rc.query, TIER)
                if dv:
                    viols += dv
                    last = _det_status(dv)
                    continue
                cv = await check(rc.query, rc.comparison_axis, intended, a, b)
            except Exception as e:  # noqa: BLE001 - truncation/parse counted, retried, never silent
                n_err += 1
                errors.append({"candidate_id": cid, "error": f"repair {type(e).__name__}"})
                last = "repair_error"
                continue
            if cv.ok:
                final_q = rc.query
                break
            viols.append(cv.failure or "underdetermined")
            last = cv.failure or "underdetermined"
        if final_q:
            priors.append(final_q)
            result[cid] = {"final": final_q, "source": "v2_recomposed", "status": "pass",
                           "attempts": attempts, "violations": viols, "post": "none"}
        else:                                          # double failure: fall back to ORIGINAL v1 wording
            result[cid] = {"final": v1[cid]["query"], "source": "original_after_repair_failure",
                           "status": last or "leak", "attempts": attempts, "violations": viols,
                           "post": au["leak_pre"]}
    args.cache.write_text(json.dumps(cache, ensure_ascii=False))

    # ---- assemble records ----
    records = []
    for c in v2:
        cid = c["candidate_id"]
        r, au = result[cid], audit.get(cid, {})
        ax = au.get("axis", {})
        rec = {k: c[k] for k in ("candidate_id", "tier", "slice", "answer_video_ids",
                                 "source_claim_ids", "pair_key", "gold_draft", "date_gap_days") if k in c}
        rec.update({
            "original_query": v1[cid]["query"], "final_query": r["final"], "query": r["final"],
            "final_query_source": r["source"], "repair_attempts": r["attempts"],
            "final_status": r["status"], "violations": r["violations"],
            "leaked_side": {"pre": au.get("leak_pre", "none"), "post": r["post"]},
            "axis": {"comparison_axis": ax.get("comparison_axis", ""),
                     "supported_by_claim_a": ax.get("axis_supported_by_claim_a"),
                     "supported_by_claim_b": ax.get("axis_supported_by_claim_b"),
                     "same_conceptual_level": ax.get("same_conceptual_level"),
                     "both_sides_required": ax.get("both_sides_required")},
            "invalid_original_axis": ax.get("invalid_original_axis", False),
        })
        assert rec["final_status"] in FINAL_STATUS, rec["final_status"]
        records.append(rec)

    # ---- completeness invariant (hard, before render) ----
    completeness_assert(sorted(input_ids), [r["candidate_id"] for r in records])

    leak_pre_n = sum(1 for r in records if r["leaked_side"]["pre"] != "none")
    leak_post_n = sum(1 for r in records if r["leaked_side"]["post"] != "none")
    from collections import Counter
    status_counts = Counter(r["final_status"] for r in records)
    meta = {"_meta": {
        "tier": "comparative", "slice": "claim_derived", "model": MODEL, "task": "5.5_v2.1_audit",
        "leak_rate": {"pre": f"{leak_pre_n}/{len(records)}", "post": f"{leak_post_n}/{len(records)}"},
        "final_status_counts": dict(status_counts),
        "source_counts": dict(Counter(r["final_query_source"] for r in records)),
        "errors": n_err, "errors_sample": errors[:10],
        "invalid_original_axis_advisory": [r["candidate_id"] for r in records if r["invalid_original_axis"]],
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"leak pre {leak_pre_n}/{len(records)} -> post {leak_post_n}/{len(records)}; "
          f"statuses {dict(status_counts)}; errors {n_err} -> {args.out}", flush=True)
    args.render.write_text(render_md(meta["_meta"], records), encoding="utf-8")
    print(f"  rendered -> {args.render}", flush=True)


def render_md(meta: dict, records: list[dict]) -> str:
    out = ["# Comparative leakage repair v2.1 (audit-first)\n",
           f"leak rate: pre {meta['leak_rate']['pre']} -> post {meta['leak_rate']['post']}",
           f"final_status: {meta['final_status_counts']}",
           f"sources: {meta['source_counts']} | errors: {meta['errors']} | "
           f"invalid_original_axis (advisory): {meta['invalid_original_axis_advisory']}\n",
           "## Audit table (candidate | leak_pre -> leak_post | axis | status | source)"]
    for r in records:
        out.append(f"  {r['candidate_id']}  {r['leaked_side']['pre']:>7} -> {r['leaked_side']['post']:<5}  "
                   f"axis={r['axis']['comparison_axis'][:34]:<34}  {r['final_status']:<18} {r['final_query_source']}"
                   + (f"  viol={r['violations']}" if r['violations'] else ""))
    out.append("\n## Changed wordings (original -> final)")
    for r in records:
        if r["final_query"] != r["original_query"]:
            out.append(f"\n### {r['candidate_id']}  [{r.get('pair_key','')}]  status={r['final_status']}")
            out.append(f"  OLD: {r['original_query']}")
            out.append(f"  NEW: {r['final_query']}")
    out.append("\n## Kept original after repair failure (status shown)")
    for r in records:
        if r["final_query_source"] == "original_after_repair_failure":
            out.append(f"  [{r['candidate_id']}] ({r['final_status']}) {r['original_query'][:110]}")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", type=Path, default=V1_DEFAULT)
    ap.add_argument("--v2", type=Path, default=V2_DEFAULT)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--render", type=Path, default=RENDER_DEFAULT)
    ap.add_argument("--cache", type=Path, default=CACHE_DEFAULT)
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
