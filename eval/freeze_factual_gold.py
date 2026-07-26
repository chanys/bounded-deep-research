"""Phase 4 B3: freeze the reviewed factual nuggets as factual-gold-v1.0.

Snapshots the human-approved generation (`eval/extract_factual_nuggets.py` at extract
prompt_sha 910a6696) with the two edits the second-read ruling directed, and writes the
versioned gold. This is a DETERMINISTIC freeze - no model call. It reads the approved
draft and applies documented edits, so the result is auditable and reproducible from the
draft, even though the draft itself came from a non-deterministic LLM pass.

The frozen artifact IS this approved generation, not a regenerable output: re-running the
prompt would not reproduce it. The prompt_sha identifies the behavior that produced the
artifact; the artifact is the gold.

Applied edits (human ruling, 2026-07-26):
- fc-0009: cut nugget 1 ("the evidence is presented as a graph") - it is entailed by the
  word-frequency-graph nugget (the entailment audit's one true positive).
- fc-0036: drop the question entirely - 0 nuggets after subtraction, the plan's zero-nugget
  rule; a 25th instance of the question/claim-overlap class the manual skips pass missed.
  Its three A2 runs go unused, so scoring covers 61 of 62 run questions.

Usage:
  uv run python -m eval.freeze_factual_gold
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from core.provenance import PROVENANCE
from eval.extract_factual_nuggets import (
    AUDIT_PROMPT_SHA, MODEL, OUT, PROMPT_SHA, read_records,
)

VERSION = "factual-gold-v1.0"
GOLD_JSONL = Path("eval/artifacts/factual_gold_v1.0.jsonl")
GOLD_MD = Path("eval/artifacts/factual_gold_v1.0.md")

# Human-adjudicated edits applied at freeze (documented, auditable).
DROP: dict[str, str] = {
    "fc-0036": "0 nuggets after subtraction (plan zero-nugget rule); question/claim overlap, "
               "25th instance the skips pass missed; its 3 A2 runs go unused at scoring",
}
CUT_NUGGET: dict[str, int] = {
    "fc-0009": 1,   # 1-based index of the nugget to remove (entailed by the word-frequency-graph nugget)
}


def build_gold() -> list[dict]:
    """Apply the documented edits to the approved draft and return the frozen records."""
    records = read_records(OUT)
    gold: list[dict] = []
    for r in sorted(records, key=lambda r: r["question_id"]):
        qid = r["question_id"]
        if qid in DROP:
            continue
        nuggets = list(r["nuggets"])
        if qid in CUT_NUGGET:
            i = CUT_NUGGET[qid] - 1
            if not (0 <= i < len(nuggets)):
                raise ValueError(f"{qid}: cut index {CUT_NUGGET[qid]} out of range for {len(nuggets)} nuggets")
            nuggets.pop(i)
        gold.append({
            "question_id": qid,
            "question": r["question"],
            "claim": r["claim"],
            "nuggets": [{"nugget_id": f"{qid}_n{i}", "text": t} for i, t in enumerate(nuggets, 1)],
        })
    return gold


def render_gold_md(gold: list[dict]) -> str:
    """Human-readable frozen gold sheet."""
    n_nug = sum(len(g["nuggets"]) for g in gold)
    counts = Counter(len(g["nuggets"]) for g in gold)
    lines = [f"# Factual gold - {VERSION} ({len(gold)} questions, {n_nug} nuggets)", "",
             f"Frozen approved generation. Model {MODEL}, extract prompt_sha `{PROMPT_SHA}`, "
             f"entailment-audit prompt_sha `{AUDIT_PROMPT_SHA}`.", "",
             "This artifact is the frozen generation itself, not a regenerable output: LLM "
             "extraction is non-deterministic, so re-running the prompt would not reproduce it.", "",
             "## Nugget-count distribution", ""]
    for k in sorted(counts):
        lines.append(f"- {k} nugget(s): {counts[k]} question(s)")
    lines += ["", "## Applied freeze edits", ""]
    for qid, why in DROP.items():
        lines.append(f"- DROP {qid}: {why}")
    for qid, idx in CUT_NUGGET.items():
        lines.append(f"- CUT {qid} nugget {idx}: entailed by another nugget (entailment audit true positive)")
    lines += ["", "---", ""]
    for g in gold:
        lines += [f"## {g['question_id']}  ({len(g['nuggets'])} nuggets)", "",
                  f"**question:** {g['question']}", "",
                  f"**claim:** {g['claim']}", "", "**nuggets:**"]
        lines += [f"{i}. {n['text']}" for i, n in enumerate(g["nuggets"], 1)]
        lines += ["", "---", ""]
    return "\n".join(lines)


def main() -> None:
    gold = build_gold()
    n_nug = sum(len(g["nuggets"]) for g in gold)
    meta = {"_meta": {
        "version": VERSION,
        "stage": "factual_nuggets_frozen",
        "model": MODEL,
        "extract_prompt_sha": PROMPT_SHA,
        "audit_prompt_sha": AUDIT_PROMPT_SHA,
        "frozen_git_sha": PROVENANCE.git_sha,
        "frozen_git_dirty": PROVENANCE.git_dirty,
        "n_questions": len(gold),
        "n_nuggets": n_nug,
        "scored_of_run": "61 of 62 run questions (fc-0036 dropped; its 3 A2 runs unused)",
        "edits": {"drop": DROP, "cut_nugget": CUT_NUGGET},
        "note": "frozen approved generation; non-reproducible - the prompt_sha identifies the "
                "behavior that produced this artifact, the artifact is the gold",
    }}
    with GOLD_JSONL.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta) + "\n")
        for g in gold:
            f.write(json.dumps(g) + "\n")
    GOLD_MD.write_text(render_gold_md(gold), encoding="utf-8")
    print(f"{VERSION}: {len(gold)} questions, {n_nug} nuggets -> {GOLD_JSONL}")
    print(f"  extract_prompt_sha={PROMPT_SHA} audit_prompt_sha={AUDIT_PROMPT_SHA} "
          f"git_sha={PROVENANCE.git_sha[:8]} dirty={PROVENANCE.git_dirty}")
    print(f"  edits: dropped {list(DROP)}, cut {CUT_NUGGET}")
    print(f"  rendered -> {GOLD_MD}")


if __name__ == "__main__":
    main()
