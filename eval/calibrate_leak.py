"""Cheap suite-only calibration loop for the comparative leak/audit instrument.

Runs the full instrument (leak_side + axis + checker + assign) on ONLY the ~14
regression-suite candidates (eval/leak_suite.py), prints a confusion matrix, and
reports whether the instrument reproduces the human labels. The suite gate scores
on the BINARY leak projection (!= none vs none); per-side attribution is shown as a
secondary column for gross-error inspection and never fails the gate.

Cache keys are fingerprinted by the instrument's prompt text: any prompt edit is a
NEW instrument (classifier_version_drift) and must not reuse a prior verdict.

Cap the tuning at four iterations. If it has not converged by then, stop and report
- a prompt hammered into agreeing with 14 known items has memorized the suite, not
learned the boundary; the honest fallback is hybrid (classifier for clear cases,
human read where classifier and deterministic scan disagree).
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path

from eval.finalize_comparative import RESTORE, assign, load
from eval.leak_suite import SUITE, check_case
from eval.repair_comparative_leakage import (AXIS_AUDIT_SYSTEM, CHECK_SYSTEM,
                                             LEAK_SIDE_SYSTEM, axis_audit, check, leak_side)
from eval.text_guards import violation_scan

V1 = Path("eval/artifacts/query_candidates_comparative_claimslice.jsonl")
V21 = Path("eval/artifacts/query_candidates_comparative_claimslice_v21.jsonl")
CACHE = Path("eval/artifacts/comparative_calib_cache.json")
TIER = "comparative"

# Any change to these three prompts is a new instrument; fold their text into the cache key.
PROMPT_FP = hashlib.sha1((LEAK_SIDE_SYSTEM + AXIS_AUDIT_SYSTEM + CHECK_SYSTEM).encode()).hexdigest()[:8]


def _h(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


async def amain(args) -> None:
    v1, v21 = load(V1), load(V21)
    cache: dict = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    sem = asyncio.Semaphore(args.concurrency)

    async def cached(key, factory):
        key = f"{PROMPT_FP}:{key}"
        if key in cache:
            return cache[key]
        cache[key] = (await factory()).model_dump()
        return cache[key]

    async def audit(cid):
        a, b = v21[cid]["gold_draft"]
        orig = v1[cid]["query"]
        final = orig if cid in RESTORE else v21[cid]["final_query"]
        lp = await cached(f"leak:{cid}:{_h(final)}", lambda: leak_side(cid, final, a, b, sem))
        ax = await cached(f"axis:{cid}:{_h(orig)}:{_h(final)}", lambda: axis_audit(cid, orig, final, a, b, sem))
        async with sem:
            cv = await cached(f"chk:{cid}:{_h(final)}",
                              lambda: check(final, ax["comparison_axis"], ax["comparison_axis"], a, b))
        det = violation_scan(final, TIER)
        status = assign(lp["leaked_side"], det, ax, cv["ok"], cv["failure"])
        return cid, {"leaked_side": lp["leaked_side"], "leak_reason": lp["reason"], "status": status,
                     "invalid_axis": ax["invalid_original_axis"], "chk_fail": cv["failure"],
                     "chk_reason": cv["reason"], "final": final}

    results = dict(await asyncio.gather(*(audit(cid) for cid in SUITE)))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False))

    print(f"\n=== leak instrument calibration vs suite (prompt fp {PROMPT_FP}) ===")
    print(f"{'cand':<8} {'label':<26} {'leak(side)':<12} {'status':<18} {'chk_fail':<18} {'inv':<4} {'gate':<5} note")
    n_pass = 0
    for cid, label in SUITE.items():
        r = results[cid]
        ok, detail = check_case(label, leaked_side=r["leaked_side"], status=r["status"], invalid_axis=r["invalid_axis"])
        n_pass += ok
        lbl = next(f"{k}={v}" for k, v in label.items())
        note = r["leak_reason"] if "leak" in lbl else (r["chk_reason"] or detail)
        print(f"{cid:<8} {lbl:<26} {r['leaked_side']:<12} {r['status']:<18} {str(r['chk_fail']):<18} "
              f"{str(r['invalid_axis'])[0]:<4} {'ok' if ok else 'FAIL':<5} {note[:60]}")
    print(f"\nSUITE {n_pass}/{len(SUITE)} {'PASS' if n_pass == len(SUITE) else 'FAIL'}")

    # binary-projection confusion over the leak-labeled cases (the gate's primary signal)
    leak_ids = [c for c, lab in SUITE.items() if "leak_side" in lab]
    fired = [c for c in leak_ids if results[c]["leaked_side"] != "none"]
    clean_status = [c for c, lab in SUITE.items() if lab.get("status") in ("gold_insufficient", "subject_unnameable")]
    clean_leaks = [c for c in clean_status if results[c]["leaked_side"] != "none"]
    print(f"leak-labeled fired (want all): {len(fired)}/{len(leak_ids)} {fired}")
    print(f"status-labeled false leaks (want 0): {len(clean_leaks)}/{len(clean_status)} {clean_leaks}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, default=6)
    asyncio.run(amain(ap.parse_args()))


if __name__ == "__main__":
    main()
