"""Phase 4 C3: draw a stratified two-sided calibration set for the alignment judge.

Builds real (claim, text) pairs from the A2 runs + frozen gold across all three judge
directions and both tiers, runs the judge to get its (hidden) verdicts, selects a
stratified two-sided ~60-pair set, and emits a blind human-labeling sheet plus a hidden
answer key. After the human labels, `--score` computes raw agreement + Cohen's kappa.

Directions:
- recall (dir 1):        claim = gold nugget,           text = the run's answer.
- groundedness (dir 2):  claim = extracted answer-claim, text = the run's retrieved chunk set.
- attribution (dir 3):   claim = gold nugget,            text = the run's retrieved chunk set.

Stratification (plan + human additions, 2026-07-26):
- both tiers (longitudinal, factual); all three directions; two-sided (judge-HIT and judge-MISS
  present in each cell, so kappa is not degenerate).
- oversample two hard cells: dir-3 nugget x raw ASR chunk, and window-compatibility calls.
- factual dir-1 claims come from the frozen factual-gold-v1.0, not any earlier generation.
- force-include several bundled compound answer-claims ("X and Y"), the partial-support case the
  crafted self-test never exercised.
- force-include dir-3 pairs whose gold evidence was flagged [not re-found] by the grounder.

Verdicts are hidden in the labeling sheet; the answer key is written separately. Seeded, so the
draw reproduces.

Usage:
  uv run python -m eval.calibrate_judge --dry-run          # build pool, print cell counts, no judge
  uv run python -m eval.calibrate_judge --draw             # full: judge pool, select, emit sheet + key
  uv run python -m eval.calibrate_judge --score labels.md  # after labeling: raw agreement + kappa
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import re
from pathlib import Path

from eval.extract_answer_claims import extract_claims
from eval.judge import format_chunk_set, judge
from eval.stats import cohen_kappa

ARTIFACTS = Path("eval/artifacts")
RUNS = ARTIFACTS / "runs"
LON_WORKSHEET = ARTIFACTS / "longitudinal_claim_vs_grounder.md"
FACTUAL_GOLD = ARTIFACTS / "factual_gold_v1.0.jsonl"
CLAIMS_CACHE = ARTIFACTS / "answer_claims_calib.jsonl"
SHEET = ARTIFACTS / "judge_calibration_sheet.md"
KEY = ARTIFACTS / "judge_calibration_key.json"
SEED = 20260726
TARGET = 60


# ---- gold loaders ----------------------------------------------------------

_NUG_RE = re.compile(r"^- \*\*(shift|no-change)?\s*\(?(n\d+)\)?\*\*\s*(.+?)\s*$")
_WIN_RE = re.compile(r"\[([^\]]*\d{4}[^\]]*)\]\s*$")   # trailing [ ... YYYY ... ] window


def load_longitudinal() -> list[dict]:
    """Parse the worksheet -> nugget dicts: question_id, nugget_id, text, type
    (stance|shift|no_change), has_window, and question-level has_not_refound."""
    text = LON_WORKSHEET.read_text()
    blocks = re.split(r"\n## (?=lc-\d)", text)
    out: list[dict] = []
    for b in blocks:
        m = re.match(r"(lc-\d+)", b)
        if not m:
            continue
        qid = m.group(1)
        has_nrf = "[not re-found]" in b
        in_nuggets = False
        for line in b.splitlines():
            if line.startswith("**nuggets"):
                in_nuggets = True
                continue
            if in_nuggets:
                nm = _NUG_RE.match(line)
                if nm:
                    kind = {"shift": "shift", "no-change": "no_change"}.get(nm.group(1), "stance")
                    body = nm.group(3)
                    out.append({"question_id": qid, "nugget_id": nm.group(2), "text": body,
                                "type": kind, "tier": "longitudinal",
                                "has_window": bool(_WIN_RE.search(body)),
                                "has_not_refound": has_nrf})
                elif line.startswith(("**", "### ")):
                    in_nuggets = False
    return out


def load_factual() -> list[dict]:
    """Frozen factual-gold-v1.0 nuggets -> nugget dicts (type fact)."""
    out: list[dict] = []
    for ln in FACTUAL_GOLD.read_text().splitlines():
        o = json.loads(ln)
        if "_meta" in o:
            continue
        for n in o["nuggets"]:
            out.append({"question_id": o["question_id"], "nugget_id": n["nugget_id"],
                        "text": n["text"], "type": "fact", "tier": "factual",
                        "has_window": False, "has_not_refound": False})
    return out


def load_run(qid: str, idx: int = 0) -> dict | None:
    p = RUNS / qid / f"r{idx}" / "run.json"
    return json.loads(p.read_text()) if p.exists() else None


# ---- answer-claim cache (dir 2) --------------------------------------------

async def answer_claims_for(runs: list[dict], concurrency: int) -> dict[str, list[str]]:
    """Extract (and cache) answer-claims for the given runs -> question_id -> claims."""
    cache: dict[str, list[str]] = {}
    if CLAIMS_CACHE.exists():
        for ln in CLAIMS_CACHE.read_text().splitlines():
            o = json.loads(ln)
            cache[o["question_id"]] = o["claims"]
    todo = [r for r in runs if r["question_id"] not in cache]
    if todo:
        sem = asyncio.Semaphore(concurrency)
        results = await asyncio.gather(*(extract_claims(r["answer"], sem) for r in todo))
        with CLAIMS_CACHE.open("a", encoding="utf-8") as f:
            for r, claims in zip(todo, results):
                cache[r["question_id"]] = claims
                f.write(json.dumps({"question_id": r["question_id"], "claims": claims}) + "\n")
    return cache


def is_compound(claim: str) -> bool:
    """Heuristic: a claim joining two independently-checkable parts with 'and'."""
    return bool(re.search(r"\w\s+and\s+\w", claim)) and len(claim.split()) >= 12


# ---- pool construction -----------------------------------------------------

def build_pool(claims_by_q: dict[str, list[str]], lon_q: list[str], fac_q: list[str],
               dir2_q: list[str], rng: random.Random) -> list[dict]:
    """All candidate pairs across the three directions, tagged for stratification.
    Chunk-set text is fetched once per run. No judge yet."""
    lon = {n["question_id"]: [] for n in load_longitudinal()}
    for n in load_longitudinal():
        lon[n["question_id"]].append(n)
    fac = {}
    for n in load_factual():
        fac.setdefault(n["question_id"], []).append(n)
    nuggets_by_q = {**lon, **fac}

    pool: list[dict] = []
    chunkset_cache: dict[str, str] = {}

    def chunkset(run: dict) -> str:
        qid = run["question_id"]
        if qid not in chunkset_cache:
            chunkset_cache[qid] = format_chunk_set(list(run["evidence"]["seen_chunks"]))
        return chunkset_cache[qid]

    # dir 1 recall: STANCE/FACT nugget x answer. shift and no_change get dedicated builders
    # below (their judge rule needs two-sided pairs and the window tag would dilute them here).
    for qid in lon_q + fac_q:
        run = load_run(qid)
        if not run:
            continue
        for n in nuggets_by_q.get(qid, []):
            if n["type"] in ("shift", "no_change"):
                continue
            pool.append({"direction": "recall", "tier": n["tier"], "claim": n["text"],
                         "text": run["answer"], "text_kind": "answer", "claim_type": n["type"],
                         "question_id": qid, "ref": n["nugget_id"],
                         "compound": False, "not_refound": False, "window": n["has_window"],
                         "negative_control": False})

    # dir 3 attribution: stance/fact nugget x chunk set
    for qid in lon_q + fac_q:
        run = load_run(qid)
        if not run:
            continue
        for n in nuggets_by_q.get(qid, []):
            if n["type"] in ("shift", "no_change"):
                continue   # connection nuggets are not grounded against chunks
            pool.append({"direction": "attribution", "tier": n["tier"], "claim": n["text"],
                         "text": chunkset(run), "text_kind": "chunks", "claim_type": n["type"],
                         "question_id": qid, "ref": n["nugget_id"],
                         "compound": False, "not_refound": n["has_not_refound"], "window": n["has_window"],
                         "negative_control": False})

    # dir 2 groundedness: answer-claim x chunk set
    for qid in dir2_q:
        run = load_run(qid)
        if not run:
            continue
        tier = "longitudinal" if qid.startswith("lc") else "factual"
        for i, claim in enumerate(claims_by_q.get(qid, [])):
            pool.append({"direction": "groundedness", "tier": tier, "claim": claim,
                         "text": chunkset(run), "text_kind": "chunks", "claim_type": "fact",
                         "question_id": qid, "ref": f"claim{i + 1}",
                         "compound": is_compound(claim), "not_refound": False, "window": False,
                         "negative_control": False})

    # Groundedness negative controls: real answer-claims are ~all self-grounded (the agent
    # asserts what it retrieved), so a naturalistic dir-2 draw is one-sided HIT and kappa would
    # be degenerate. Pair each dir-2 run's first two claims with a DIFFERENT run's chunk set - a
    # clean MISS control that gives the judge something to correctly reject. Tagged so provenance
    # shows they are constructed, not naturalistic.
    runs = [load_run(q) for q in dir2_q]
    runs = [r for r in runs if r]
    for run in runs:
        others = [r for r in runs if r["question_id"] != run["question_id"]]
        if not others:
            continue
        tier = "longitudinal" if run["question_id"].startswith("lc") else "factual"
        for i, claim in enumerate(claims_by_q.get(run["question_id"], [])[:2]):
            tgt = rng.choice(others)
            pool.append({"direction": "groundedness", "tier": tier, "claim": claim,
                         "text": chunkset(tgt), "text_kind": "chunks", "claim_type": "fact",
                         "question_id": run["question_id"], "ref": f"negctl{i + 1}->{tgt['question_id']}",
                         "compound": is_compound(claim), "not_refound": False, "window": False,
                         "negative_control": True})

    # shift (dir 1): every longitudinal score depends on the shift rule, so draw a dedicated
    # two-sided pool - shift nugget x its own answers across runs r0/r1/r2 (natural HIT, and
    # weaker/budget-exhausted runs give natural MISS), plus cross-question controls (shift nugget
    # x a DIFFERENT question's answer = a clean MISS the judge must reject).
    shift_by_q = {n["question_id"]: n for n in load_longitudinal() if n["type"] == "shift"}
    shift_qs = [q for q in lon_q if q in shift_by_q]
    for q in shift_qs:
        n = shift_by_q[q]
        for idx in (0, 1, 2):
            r = load_run(q, idx)
            if not r:
                continue
            pool.append({"direction": "recall", "tier": "longitudinal", "claim": n["text"],
                         "text": r["answer"], "text_kind": "answer", "claim_type": "shift",
                         "question_id": q, "ref": f"{n['nugget_id']}:r{idx}",
                         "compound": False, "not_refound": n["has_not_refound"],
                         "window": n["has_window"], "negative_control": False})
    for q in rng.sample(shift_qs, min(6, len(shift_qs))):
        n = shift_by_q[q]
        others = [o for o in shift_qs if o != q]
        if not others:
            continue
        tgt = rng.choice(others)
        r = load_run(tgt, 0)
        if r:
            pool.append({"direction": "recall", "tier": "longitudinal", "claim": n["text"],
                         "text": r["answer"], "text_kind": "answer", "claim_type": "shift",
                         "question_id": q, "ref": f"{n['nugget_id']}->ctl:{tgt}",
                         "compound": False, "not_refound": False, "window": n["has_window"],
                         "negative_control": True})

    # no_change (dir 1): only lc-0130 n2 exists in the gold, so exactly one real pair is drawable.
    nc = next((n for n in load_longitudinal() if n["type"] == "no_change"), None)
    if nc and (r := load_run(nc["question_id"], 0)):
        pool.append({"direction": "recall", "tier": "longitudinal", "claim": nc["text"],
                     "text": r["answer"], "text_kind": "answer", "claim_type": "no_change",
                     "question_id": nc["question_id"], "ref": nc["nugget_id"],
                     "compound": False, "not_refound": nc["has_not_refound"],
                     "window": nc["has_window"], "negative_control": False})

    for i, p in enumerate(pool):
        p["pair_id"] = f"p{i + 1:03d}"
    return pool


# ---- selection -------------------------------------------------------------

# (direction, tier) -> target count for STANCE/FACT nuggets and claims; dir-3 longitudinal
# oversampled (hard cell). shift (~9) and no_change (1) are drawn separately below.
CELL_TARGETS = {
    ("recall", "longitudinal"): 10, ("recall", "factual"): 8,
    ("groundedness", "longitudinal"): 10, ("groundedness", "factual"): 8,
    ("attribution", "longitudinal"): 12, ("attribution", "factual"): 8,
}
SHIFT_TARGET = 9


def select(pool: list[dict], rng: random.Random) -> list[dict]:
    """Stratified two-sided selection: within each (direction,tier) cell, interleave
    judge-HIT and judge-MISS candidates up to the target, prioritizing forced-include
    tags (compound / not_refound / shift / no_change / window)."""
    chosen: list[dict] = []
    for cell, target in CELL_TARGETS.items():
        cands = [p for p in pool if (p["direction"], p["tier"]) == cell
                 and p["claim_type"] not in ("shift", "no_change")]
        hits = [p for p in cands if p["judge_hit"]]
        misses = [p for p in cands if not p["judge_hit"]]

        def prio(p):   # forced-include tags first, then random
            return (not (p["compound"] or p["not_refound"] or p["window"]
                         or p["claim_type"] in ("shift", "no_change")), rng.random())
        hits.sort(key=prio)
        misses.sort(key=prio)
        picked, hi, mi = [], 0, 0
        while len(picked) < target and (hi < len(hits) or mi < len(misses)):
            if hi < len(hits) and (len(picked) % 2 == 0 or mi >= len(misses)):
                picked.append(hits[hi])
                hi += 1
            elif mi < len(misses):
                picked.append(misses[mi])
                mi += 1
        chosen.extend(picked)

    # Dedicated two-sided shift draw (SHIFT_TARGET): interleave judge-HIT and judge-MISS shift
    # pairs; de-dup on (question_id, judge_hit) so we do not pick the same nugget's 3 runs when
    # they all agree, but keep both a HIT run and a MISS run of the same nugget when they differ.
    shift = [p for p in pool if p["claim_type"] == "shift"]
    s_hits = [p for p in shift if p["judge_hit"]]
    s_miss = [p for p in shift if not p["judge_hit"]]
    rng.shuffle(s_hits)
    rng.shuffle(s_miss)

    def dedup(ps):
        seen, out = set(), []
        for p in ps:
            k = (p["question_id"], p["negative_control"])
            if k not in seen:
                seen.add(k)
                out.append(p)
        return out
    s_hits, s_miss = dedup(s_hits), dedup(s_miss)
    picked, hi, mi = [], 0, 0
    while len(picked) < SHIFT_TARGET and (hi < len(s_hits) or mi < len(s_miss)):
        if hi < len(s_hits) and (len(picked) % 2 == 0 or mi >= len(s_miss)):
            picked.append(s_hits[hi])
            hi += 1
        elif mi < len(s_miss):
            picked.append(s_miss[mi])
            mi += 1
    chosen.extend(picked)

    # no_change: the single lc-0130 n2 pair (only one exists in the gold).
    nc = next((p for p in pool if p["claim_type"] == "no_change"), None)
    if nc:
        chosen.append(nc)
    return chosen


# ---- emit + score ----------------------------------------------------------

def cell_counts(pairs: list[dict]) -> str:
    from collections import Counter
    lines = []
    stance = [p for p in pairs if p["claim_type"] not in ("shift", "no_change")]
    c = Counter((p["direction"], p["tier"]) for p in stance)
    for (d, t), n in sorted(c.items()):
        nhit = sum(1 for p in stance if (p["direction"], p["tier"]) == (d, t) and p.get("judge_hit"))
        lines.append(f"  {d:13s} {t:12s}: {n:2d}  (judge HIT {nhit}, MISS {n - nhit})")
    for ct in ("shift", "no_change"):
        ps = [p for p in pairs if p["claim_type"] == ct]
        if ps:
            nhit = sum(1 for p in ps if p.get("judge_hit"))
            lines.append(f"  {ct:13s} {'(recall)':12s}: {len(ps):2d}  (judge HIT {nhit}, MISS {len(ps) - nhit})")
    tags = {"compound": sum(p["compound"] for p in pairs),
            "not_refound": sum(p["not_refound"] for p in pairs),
            "window": sum(p["window"] for p in pairs),
            "negative_control": sum(p["negative_control"] for p in pairs),
            "shift": sum(p["claim_type"] == "shift" for p in pairs),
            "no_change": sum(p["claim_type"] == "no_change" for p in pairs)}
    lines.append(f"  forced-include tags: {tags}")
    return "\n".join(lines)


def write_sheet(pairs: list[dict]) -> None:
    pairs = sorted(pairs, key=lambda p: len(p["text"]))   # shortest-text-first: quick pairs early, long chunk sets batched at the end
    lines = [f"# Judge calibration - blind labeling sheet ({len(pairs)} pairs)", "",
             "For each pair decide HIT or MISS and write it in the blank. HIT = the TEXT supports/states "
             "the CLAIM under the stated CLAIM TYPE and TEXT KIND (same rules the judge uses). "
             "The judge's own verdict is withheld until you finish. Pairs are ordered shortest-text-first, "
             "so the long chunk-set pairs are batched at the end.", "",
             "DIRECTION: recall = gold nugget vs the answer; groundedness (dir 2) = an answer-claim vs the "
             "retrieved chunk set; attribution (dir 3) = a gold nugget vs the retrieved chunk set. "
             "The HIT/MISS rule is the same for groundedness and attribution (does the chunk set support "
             "the claim); the label distinguishes them for the record. Some pairs are constructed mismatches "
             "(a claim paired with an unrelated chunk set or answer) - label them on their merits.", "",
             "TEXT KIND answer = the assistant's answer; chunks = retrieved transcript chunks (each labeled "
             "[video | published date]). CLAIM TYPE shift = must convey a change over time; no_change = must "
             "convey the view stayed consistent; fact/stance = a single assertion.", "", "---", ""]
    for p in pairs:
        lines += [f"## {p['pair_id']}", "",
                  f"- direction: **{p['direction']}**   text kind: **{p['text_kind']}**   "
                  f"claim type: **{p['claim_type']}**   ({len(p['text']):,} chars)", "",
                  f"**CLAIM:** {p['claim']}", "",
                  "**TEXT:**", "", p["text"], "",
                  "**your verdict (HIT / MISS):** [    ]", "", "---", ""]
    SHEET.write_text("\n".join(lines), encoding="utf-8")


def write_key(pairs: list[dict]) -> None:
    key = {p["pair_id"]: {k: p[k] for k in ("direction", "tier", "claim_type", "text_kind",
           "question_id", "ref", "compound", "not_refound", "window", "negative_control",
           "judge_hit", "judge_reason")}
           for p in pairs}
    KEY.write_text(json.dumps(key, indent=2))


async def draw(dry_run: bool, concurrency: int) -> None:
    rng = random.Random(SEED)
    lon_all = sorted({n["question_id"] for n in load_longitudinal()})
    fac_all = sorted({n["question_id"] for n in load_factual()})
    # prioritize longitudinal questions with not-re-found evidence + variety; seeded.
    nrf = sorted({n["question_id"] for n in load_longitudinal() if n["has_not_refound"]})
    # lc-0130 forced in: it carries the only no_change (presupposition-trap) nugget.
    lon_q = list(dict.fromkeys(["lc-0130"] + nrf + rng.sample(lon_all, len(lon_all))))[:14]
    fac_q = rng.sample(fac_all, min(12, len(fac_all)))
    dir2_q = rng.sample(lon_q, 4) + rng.sample(fac_q, 4)

    runs = [r for qid in set(lon_q + fac_q + dir2_q) if (r := load_run(qid))]
    claims_by_q = {} if dry_run else await answer_claims_for(
        [load_run(q) for q in dir2_q if load_run(q)], concurrency)
    pool = build_pool(claims_by_q, lon_q, fac_q, dir2_q, rng)
    print(f"pool: {len(pool)} candidate pairs "
          f"(lon_q={len(lon_q)} fac_q={len(fac_q)} dir2_q={len(dir2_q)} runs={len(runs)})", flush=True)
    from collections import Counter
    print("pool by cell:", dict(Counter((p["direction"], p["tier"]) for p in pool)), flush=True)
    print("pool tags:", {"compound": sum(p["compound"] for p in pool),
                         "not_refound": sum(p["not_refound"] for p in pool),
                         "window": sum(p["window"] for p in pool)}, flush=True)
    if dry_run:
        print("\n[dry-run] pool built; skipping judge + selection.", flush=True)
        return

    sem = asyncio.Semaphore(concurrency)

    async def jr(p):
        async with sem:
            try:
                v = await judge(p["claim"], text=p["text"], claim_type=p["claim_type"], text_kind=p["text_kind"])
            except Exception as e:  # noqa: BLE001 - one bad pair must not kill the 235-call draw
                print(f"  judge fail {p['pair_id']} ({p['direction']}/{p['tier']}): {type(e).__name__}: {e}", flush=True)
                p["judge_hit"] = None
                return p
        p["judge_hit"], p["judge_reason"] = v.hit, v.reason
        return p
    await asyncio.gather(*(jr(p) for p in pool))
    n_fail = sum(1 for p in pool if p["judge_hit"] is None)
    pool = [p for p in pool if p["judge_hit"] is not None]
    if n_fail:
        print(f"  ({n_fail} pairs dropped on judge failure)", flush=True)

    chosen = select(pool, rng)
    write_sheet(chosen)   # sorts shortest-text-first internally
    write_key(chosen)
    print(f"\nselected {len(chosen)} pairs -> {SHEET} (+ hidden key {KEY})", flush=True)
    print("per-cell counts (what you are labeling):", flush=True)
    print(cell_counts(chosen), flush=True)
    chars = sorted(len(p["text"]) for p in chosen)
    total = sum(chars)
    longest = sorted(chosen, key=lambda p: -len(p["text"]))[:5]
    print(f"text size: total {total:,} chars; median {chars[len(chars) // 2]:,}; "
          f"min {chars[0]:,}; max {chars[-1]:,}", flush=True)
    print("  longest 5:", [(p["pair_id"], len(p["text"])) for p in longest], flush=True)


def score(labels_path: Path) -> None:
    """Compute raw agreement + Cohen's kappa from a filled labeling sheet vs the key."""
    key = json.loads(KEY.read_text())
    text = labels_path.read_text()
    labels: dict[str, bool] = {}
    for pid, block in re.findall(r"## (p\d+)\b(.*?)(?=\n## p\d|\Z)", text, re.S):
        m = re.search(r"your verdict \(HIT / MISS\):\*\*\s*\[\s*(HIT|MISS)\s*\]", block, re.I)
        if m:
            labels[pid] = (m.group(1).upper() == "HIT")
    common = [pid for pid in key if pid in labels]
    if not common:
        raise SystemExit("no filled verdicts parsed; write HIT or MISS inside the [ ] blanks")
    human = [labels[pid] for pid in common]
    machine = [key[pid]["judge_hit"] for pid in common]
    agree = sum(1 for h, m in zip(human, machine) if h == m)
    print(f"labeled {len(common)}/{len(key)} pairs", flush=True)
    print(f"raw agreement: {agree}/{len(common)} = {agree / len(common):.1%}", flush=True)
    print(f"Cohen's kappa: {cohen_kappa(human, machine):.3f}  (HEADLINE)", flush=True)
    print("\ndisagreements (read every one -> judge-error / my-error / gold-defect):", flush=True)
    for pid in common:
        if labels[pid] != key[pid]["judge_hit"]:
            k = key[pid]
            print(f"  {pid} [{k['direction']}/{k['tier']}/{k['claim_type']}] "
                  f"human={'HIT' if labels[pid] else 'MISS'} judge={'HIT' if k['judge_hit'] else 'MISS'}"
                  f" :: {k['judge_reason']}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Calibrate the alignment judge (C3).")
    ap.add_argument("--dry-run", action="store_true", help="build pool + print cell counts, no judge")
    ap.add_argument("--draw", action="store_true", help="judge pool, select, emit sheet + key")
    ap.add_argument("--score", type=Path, help="compute agreement + kappa from a filled sheet")
    ap.add_argument("--concurrency", type=int, default=6)
    args = ap.parse_args()
    if args.score:
        score(args.score)
    elif args.dry_run or args.draw:
        asyncio.run(draw(args.dry_run, args.concurrency))
    else:
        ap.error("pass --dry-run, --draw, or --score")


if __name__ == "__main__":
    main()
