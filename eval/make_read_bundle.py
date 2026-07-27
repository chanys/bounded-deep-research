"""Phase 4 D: assemble self-contained human-read bundles for the scoring read.

A score file (eval/artifacts/scores/<qid>__r<idx>.json) holds the chunks, the extracted
answer-claims, and every verdict + reason, but NOT the agent answer, the gold nugget text,
the question, the window, or the [not re-found] status. This joins the score file + the A2
run.json (answer) + the gold worksheet (nugget text / question / window / evidence status)
into one markdown per question - the same shape as the hand-assembled _fc0001_r2_record.md -
so the read opens a single file per question with everything, no database and no cross-file join.

Usage:
  uv run python -m eval.make_read_bundle lc-0011,lc-0027   # named questions
  uv run python -m eval.make_read_bundle --read-sets       # the three read sets (A/B/C) + anchor
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from eval.calibrate_judge import load_factual, load_longitudinal

RUNS = Path("eval/artifacts/runs")
SCORES = Path("eval/artifacts/scores")
OUT = Path("eval/artifacts/read")
WORKSHEET = Path("eval/artifacts/longitudinal_claim_vs_grounder.md")

READ_SETS = {
    "A_lowest_recall": ["fc-0004", "fc-0042", "lc-0087", "lc-0127", "lc-0233",
                        "lc-0388", "lc-0418", "lc-0481", "lc-0497", "lc-0070"],
    "B_n1_violations": ["lc-0011", "lc-0027", "lc-0111", "lc-0251", "lc-0349", "lc-0413"],
    "C_mid_band": ["lc-0014", "lc-0169", "lc-0448", "lc-0337", "lc-0177"],
}


def _win(text: str) -> str:
    m = re.findall(r"\[([^\]]*\d{4}[^\]]*)\]", text)
    return m[-1] if m else ""


def worksheet_extras() -> dict[str, dict]:
    """qid -> {question, original, nug_status: {nugget_id: grounded|not_refound|promoted}}."""
    out: dict[str, dict] = {}
    for b in re.split(r"\n## (?=lc-\d)", WORKSHEET.read_text()):
        m = re.match(r"(lc-\d+)", b)
        if not m:
            continue
        qid = m.group(1)
        q = re.search(r"\*\*question:\*\*\s*(.+)", b)
        orig = re.search(r"\*\*question \(original[^)]*\):\*\*\s*(.+)", b)
        status: dict[str, str] = {}
        for msec in re.split(r"\n### ", b)[1:]:
            sup = re.search(r"supports:\s*(n\d+)", msec)
            if not sup:
                continue
            st = ("grounded" if "[grounded]" in msec or "[promoted from chunk store]" in msec
                  else "not_refound" if "[not re-found]" in msec else "?")
            status.setdefault(sup.group(1), st)
        out[qid] = {"question": q.group(1).strip() if q else "",
                    "original": orig.group(1).strip() if orig else None, "nug_status": status}
    return out


def gold_nuggets() -> dict[str, list[dict]]:
    g: dict[str, list[dict]] = {}
    for n in load_longitudinal():
        g.setdefault(n["question_id"], []).append(
            {"nugget_id": n["nugget_id"], "type": n["type"], "text": n["text"], "window": _win(n["text"])})
    for n in load_factual():
        g.setdefault(n["question_id"], []).append(
            {"nugget_id": n["nugget_id"], "type": "fact", "text": n["text"], "window": ""})
    return g


def bundle(qid: str, gold: dict, extras: dict) -> str:
    ng = {n["nugget_id"]: n for n in gold.get(qid, [])}
    ex = extras.get(qid, {})
    lines = [f"# {qid} - read bundle (all runs, self-contained)", ""]
    if ex.get("question"):
        lines += [f"**question:** {ex['question']}", ""]
    if ex.get("original"):
        lines += [f"**question (original, waypoint-leaked):** {ex['original']}", ""]
    lines += ["## Gold nuggets"]
    for nid, n in ng.items():
        st = ex.get("nug_status", {}).get(nid)
        tag = f"  _[gold evidence: {st}]_" if st else ""
        lines.append(f"- **{nid}** ({n['type']}) {n['text']}{tag}")
    lines.append("")
    for idx in range(3):
        sp = SCORES / f"{qid}__r{idx}.json"
        rp = RUNS / qid / f"r{idx}" / "run.json"
        if not sp.exists() or not rp.exists():
            continue
        s = json.loads(sp.read_text())
        run = json.loads(rp.read_text())
        lines += [f"---\n\n## run r{idx}", "", "### Agent answer", "", run["answer"], "",
                  "### Recall (gold nugget vs answer)"]
        for d in s["recall_details"]:
            lines.append(f"- {'HIT ' if d['hit'] else 'MISS'} {d['nugget_id']}: {d['reason']}")
        lines += ["", "### Attribution / dir-3 (nugget vs retrieved chunks)"]
        for g in s["nugget_grid"]:
            lines.append(f"- {g['nugget_id']}: recall={'HIT' if g['recall_hit'] else 'MISS'}, "
                         f"chunks_support={'YES' if g['supported_in_chunks'] else 'NO'} :: {g['dir3_reason']}")
        lines += ["", "### Groundedness (answer-claim vs retrieved chunks)"]
        for d in s["ground_details"]:
            lines.append(f"- {'HIT ' if d['hit'] else 'MISS'}: {d['claim']}")
        lines += ["", f"### Retrieved chunk set ({len(s['chunks'])} chunks)"]
        for c in s["chunks"]:
            lines.append(f"\n**{c['chunk_id']}** [{c['video_id']} | {c['published_at']}]\n{c['text']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble self-contained human-read bundles.")
    ap.add_argument("questions", nargs="?", default="", help="comma-separated question ids")
    ap.add_argument("--read-sets", action="store_true", help="generate the three read sets A/B/C")
    args = ap.parse_args()
    qids = (sorted({q for ids in READ_SETS.values() for q in ids}) if args.read_sets
            else [q.strip() for q in args.questions.split(",") if q.strip()])
    if not qids:
        ap.error("pass question ids or --read-sets")
    OUT.mkdir(parents=True, exist_ok=True)
    gold, extras = gold_nuggets(), worksheet_extras()
    for qid in qids:
        (OUT / f"{qid}.md").write_text(bundle(qid, gold, extras), encoding="utf-8")
    print(f"wrote {len(qids)} read bundles -> {OUT}/")
    if args.read_sets:
        for name, ids in READ_SETS.items():
            print(f"  {name}: {', '.join(ids)}")


if __name__ == "__main__":
    main()
