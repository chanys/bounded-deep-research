"""Task 5.5: semantic-leakage repair on the frozen comparative candidates.

An external review found a wording defect the smokes under-sampled: many comparative
questions disclose the claim content they should probe ("how does A's <what A does>
compare to B's <what B does>"), so the agent can produce a scoreable answer without
retrieving - an instrument-validity bug, distinct from the lexical leak check (chunk
phrasing). This repairs WORDING ONLY on the frozen 40 (pairs unchanged):

  1. semantic-leak check on all 40 (+ an advisory one_sided both-side-necessity flag);
  2. a diagnostic correlating leak with composition order (quartile leak rates primary);
  3. neutral-form recomposition of the leak-flagged ones, sequential with a variety list;
  4. a two-sided checker (leak / underdetermined / one_sided) with retry, then
     neutralization_failed - nothing is ever dropped.

Originals are preserved in every record. Leak verdicts are cached by full composite
identity so re-runs reproduce. Standing guards: truncation-as-error, id-echo on the
check, flushed pre-run cost estimate.

Usage:
  uv run python -m eval.repair_comparative_leakage --checks-only   # classifier + diagnostic, no recompose
  uv run python -m eval.repair_comparative_leakage                 # full repair
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

IN_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice.jsonl")
OUT_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice_v2.jsonl")
RENDER_DEFAULT = Path("eval/artifacts/comparative_claimslice_v2_sample.md")
CACHE_DEFAULT = Path("eval/artifacts/comparative_leak_cache.json")
MODEL = "claude-sonnet-5"
CHECK_MAX_TOKENS = 1500     # adaptive thinking + verdict; the leak check (thinking off) fits easily
RECOMPOSE_MAX_TOKENS = 2500  # adaptive thinking + a two-subject question; avoids truncation
CALL_TIMEOUT = 90
MAX_ATTEMPTS = 2   # recompose attempts before neutralization_failed (Task 5.5: "max 2 attempts")
VARIETY_WINDOW = 40


# ---- prompts (pinned) ------------------------------------------------------

LEAK_CHECK_SYSTEM = """\
You check whether a comparison question discloses the answer it should be probing. You are given a QUESTION comparing two subjects and the TWO CLAIMS that are its gold answer (one per subject). Naming both subjects and stating the comparison axis (the shared dimension being compared) is REQUIRED and is NOT leakage. LEAKAGE is when the question additionally states either subject's mechanism, finding, result, verdict, or design detail - paraphrasing claim content the answer should have to retrieve. Return: leak (true/false) and a one-line reason; one_sided (true if the question could be answered from just ONE of the two claims - advisory); and echo the candidate_id exactly as given."""

RECOMPOSE_SYSTEM = """\
You rewrite a comparison question to remove answer disclosure while keeping it answerable. You are given the two gold claims (one per subject) and possibly questions already written for other candidates. Write ONE natural question that: names BOTH subjects (the specific model/method/system/paper in each claim), states the comparison axis concretely (the shared dimension), and discloses NEITHER side's mechanism, finding, result, or design. The two claims are the gold answer: the question must require both to answer, must not paraphrase either, and must never reveal an outcome. Vary opening and structure; do not resemble the already-written questions. Return the question only."""

CHECKER_SYSTEM = """\
You validate a rewritten comparison question against its two gold claims. REJECT if either: (a) LEAK - it discloses either subject's mechanism/finding/result/design beyond naming the subject and axis; or (b) UNDERDETERMINED - it is too vague for the two claims to determine a right answer (a knowledgeable librarian could not tell which specific comparison is meant). Also require BOTH-SIDE NECESSITY: it must not be answerable from one claim alone. Return ok (true if it passes all three); if not ok, the failure (leak | underdetermined | one_sided) and a one-line reason."""


class LeakVerdict(BaseModel):
    candidate_id: str
    leak: bool
    reason: str
    one_sided: bool


class Recomposed(BaseModel):
    query: str


class CheckVerdict(BaseModel):
    ok: bool
    failure: Literal["leak", "underdetermined", "one_sided"] | None = None
    reason: str = ""


# ---- io / identity ---------------------------------------------------------

def composite_key(c: dict) -> str:
    qh = hashlib.sha1(c["query"].encode("utf-8")).hexdigest()[:12]
    return f"{c['candidate_id']}|{','.join(c['source_claim_ids'])}|{qh}"


def load_candidates(path: Path) -> list[dict]:
    return [json.loads(ln) for ln in path.read_text().splitlines()
            if ln.strip() and '"_meta"' not in ln[:12]]


# ---- LLM steps -------------------------------------------------------------

async def leak_check(c: dict, sem: asyncio.Semaphore) -> LeakVerdict:
    a, b = c["gold_draft"]
    user = (f"candidate_id: {c['candidate_id']}\n\nQUESTION: {c['query']}\n\n"
            f"CLAIM A: {a}\nCLAIM B: {b}\n\nDoes the question disclose either side's content?")
    async with sem:
        out = await asyncio.wait_for(
            call_structured(LEAK_CHECK_SYSTEM, user, LeakVerdict, model=MODEL,
                            max_tokens=CHECK_MAX_TOKENS, thinking={"type": "disabled"}),
            timeout=CALL_TIMEOUT,
        )
    if out.candidate_id != c["candidate_id"]:          # id-echo guard
        raise ValueError(f"id echo mismatch: sent {c['candidate_id']} got {out.candidate_id}")
    return out


async def recompose(c: dict, priors: list[str]) -> str:
    a, b = c["gold_draft"]
    lines = [f"Claim A (subject 1): {a}", f"Claim B (subject 2): {b}",
             f"Comparison axis (tag): {c['pair_key']}"]
    if priors:
        lines.append("\nAlready written (do not resemble these):")
        lines += [f"- {q}" for q in priors[-VARIETY_WINDOW:]]
    lines.append("\nWrite one neutral comparison question naming both subjects and the axis.")
    out = await asyncio.wait_for(
        call_structured(RECOMPOSE_SYSTEM, "\n".join(lines), Recomposed, model=MODEL,
                        max_tokens=RECOMPOSE_MAX_TOKENS, thinking={"type": "adaptive"}),
        timeout=CALL_TIMEOUT,
    )
    return out.query.strip()


async def check(q: str, a: str, b: str) -> CheckVerdict:
    user = f"QUESTION: {q}\n\nCLAIM A: {a}\nCLAIM B: {b}\n\nDoes it pass all three tests?"
    return await asyncio.wait_for(
        call_structured(CHECKER_SYSTEM, user, CheckVerdict, model=MODEL,
                        max_tokens=CHECK_MAX_TOKENS, thinking={"type": "adaptive"}),
        timeout=CALL_TIMEOUT,
    )


# ---- diagnostic ------------------------------------------------------------

def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs) ** 0.5
    vy = sum((y - my) ** 2 for y in ys) ** 0.5
    return round(cov / (vx * vy), 3) if vx and vy else 0.0


def diagnostic(cands: list[dict], leak: dict[str, bool]) -> dict:
    """Leak rate by composition-order quartile (primary); point-biserial r (descriptive)."""
    order = sorted(cands, key=lambda c: c["candidate_id"])   # cc-NNNN = accept order
    n = len(order)
    quartiles = {}
    for qi in range(4):
        grp = order[qi * n // 4:(qi + 1) * n // 4]
        hits = sum(1 for c in grp if leak[c["candidate_id"]])
        quartiles[f"Q{qi + 1}"] = f"{hits}/{len(grp)}"
    ranks = [i for i, _ in enumerate(order)]
    flags = [1.0 if leak[c["candidate_id"]] else 0.0 for c in order]
    return {"leak_rate_by_order_quartile": quartiles, "point_biserial_r_descriptive": _pearson(flags, ranks)}


# ---- driver ----------------------------------------------------------------

async def amain(args: argparse.Namespace) -> None:
    cands = load_candidates(args.in_path)
    cache: dict = json.loads(args.cache.read_text()) if args.cache.exists() else {}
    todo = [c for c in cands if composite_key(c) not in cache]
    upper_calls = len(todo) + len(cands) * MAX_ATTEMPTS * 2   # checks + worst-case recompose+check
    print(f"[cost estimate] rough upper bound: {len(todo)} leak checks + up to "
          f"{len(cands)} recompositions (x{MAX_ATTEMPTS} attempts, 2 calls each) "
          f"~ ${upper_calls * 0.01:.2f}", flush=True)

    # ---- step 2: leak check (concurrent, cached, id-echo + truncation guards) ----
    sem = asyncio.Semaphore(args.concurrency)
    n_err = 0
    errors: list[dict] = []

    async def _check(c):
        nonlocal n_err
        try:
            v = await leak_check(c, sem)
            cache[composite_key(c)] = {"leak": v.leak, "reason": v.reason, "one_sided": v.one_sided}
        except Exception as e:  # noqa: BLE001 - truncation/mismatch counted, never silent
            n_err += 1
            errors.append({"candidate_id": c["candidate_id"], "error": f"{type(e).__name__}: {str(e)[:80]}"})
    await asyncio.gather(*(_check(c) for c in todo))
    args.cache.parent.mkdir(parents=True, exist_ok=True)
    args.cache.write_text(json.dumps(cache, ensure_ascii=False))

    leak = {c["candidate_id"]: cache.get(composite_key(c), {}).get("leak", False) for c in cands}
    one_sided = {c["candidate_id"]: cache.get(composite_key(c), {}).get("one_sided", False) for c in cands}
    reason = {c["candidate_id"]: cache.get(composite_key(c), {}).get("reason", "") for c in cands}
    diag = diagnostic(cands, leak)
    flagged = [c for c in cands if leak[c["candidate_id"]]]
    print(f"leak-flagged {len(flagged)}/{len(cands)}, one_sided {sum(one_sided.values())}, "
          f"check errors {n_err}; diagnostic {diag}", flush=True)

    records = []
    n_recomposed = n_failed = 0
    if not args.checks_only:
        # ---- steps 4-5: recompose flagged, sequential with variety list + two-sided checker ----
        priors: list[str] = []
        final_q: dict[str, str] = {}
        status: dict[str, str] = {}
        for c in sorted(flagged, key=lambda c: c["candidate_id"]):
            a, b = c["gold_draft"]
            q = None
            for _ in range(MAX_ATTEMPTS):
                try:
                    cand_q = await recompose(c, priors)
                    v = await check(cand_q, a, b)
                except Exception as e:  # noqa: BLE001
                    n_err += 1
                    errors.append({"candidate_id": c["candidate_id"], "error": f"recompose {type(e).__name__}"})
                    continue
                if v.ok:
                    q = cand_q
                    break
            if q:
                final_q[c["candidate_id"]], status[c["candidate_id"]] = q, "recomposed"
                priors.append(q)
                n_recomposed += 1
            else:
                status[c["candidate_id"]] = "neutralization_failed"
                n_failed += 1

        for c in cands:
            cid = c["candidate_id"]
            st = status.get(cid, "unchanged")
            records.append({**c, "original_query": c["query"],
                            "final_query": final_q.get(cid, c["query"]),
                            "semantic_leak": {"leak": leak[cid], "reason": reason[cid], "one_sided": one_sided[cid]},
                            "status": st})
            records[-1]["query"] = records[-1]["final_query"]   # `query` carries the wording Task 7 grounds

    meta = {"_meta": {
        "tier": "comparative", "slice": "claim_derived", "model": MODEL, "seed": args.seed,
        "task": "5.5_semantic_leakage_repair", "max_attempts": MAX_ATTEMPTS,
        "counts": {"total": len(cands), "leak_flagged": len(flagged),
                   "one_sided_advisory": sum(one_sided.values()),
                   "recomposed": n_recomposed, "neutralization_failed": n_failed, "errors": n_err},
        "diagnostic": diag, "errors_sample": errors[:10],
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }}
    if not args.checks_only:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as f:
            f.write(json.dumps(meta, ensure_ascii=False) + "\n")
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"wrote {len(records)} v2 candidates ({n_recomposed} recomposed, {n_failed} failed, "
              f"{n_err} errors) -> {args.out}", flush=True)
        args.render.write_text(render_md(meta["_meta"], cands, records, leak, reason, one_sided), encoding="utf-8")
        print(f"  rendered -> {args.render}", flush=True)
    else:
        print(f"checks-only: {json.dumps(meta['_meta']['counts'])}  diag={diag}", flush=True)


def render_md(meta: dict, cands: list[dict], records: list[dict],
              leak: dict, reason: dict, one_sided: dict) -> str:
    by_id = {r["candidate_id"]: r for r in records}
    out = [f"# Comparative semantic-leakage repair (Task 5.5): {meta['counts']}\n",
           f"diagnostic (leak rate by composition-order quartile; r descriptive): {meta['diagnostic']}\n",
           "## Recomposed candidates (original -> final)"]
    for c in sorted(cands, key=lambda c: c["candidate_id"]):
        r = by_id[c["candidate_id"]]
        if r["status"] != "recomposed":
            continue
        a, b = c["gold_draft"]
        out.append(f"\n### {c['candidate_id']}  [{c['pair_key']}]  (leak: {reason[c['candidate_id']]})")
        out.append(f"  OLD: {r['original_query']}")
        out.append(f"  NEW: {r['final_query']}")
        out.append(f"  A: {a}\n  B: {b}")
    fails = [r for r in records if r["status"] == "neutralization_failed"]
    if fails:
        out.append("\n## neutralization_failed (kept original, for human review)")
        for r in fails:
            out.append(f"  [{r['candidate_id']}] {r['original_query']}")
    out.append("\n## 3 unflagged candidates (spot-check the classifier is not mis-firing)")
    for c in [c for c in sorted(cands, key=lambda c: c["candidate_id"]) if not leak[c["candidate_id"]]][:3]:
        a, b = c["gold_draft"]
        out.append(f"\n### {c['candidate_id']}  (unflagged{'; one_sided' if one_sided[c['candidate_id']] else ''})")
        out.append(f"  Q: {c['query']}\n  A: {a}\n  B: {b}")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-path", type=Path, default=IN_DEFAULT, dest="in_path")
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--render", type=Path, default=RENDER_DEFAULT)
    ap.add_argument("--cache", type=Path, default=CACHE_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260714)
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--checks-only", action="store_true", help="leak check + diagnostic, no recomposition")
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
