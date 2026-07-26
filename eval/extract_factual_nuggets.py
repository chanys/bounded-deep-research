"""Phase 4 Phase B: extract the scored nuggets from each factual gold claim.

For the 26 kept factual questions (`factual_claim_vs_grounder_kept.md`), decompose the
already-distilled gold CLAIM into atomic nuggets: the independently-checkable facts a
correct answer must contain. Faithfulness and leakage were already ruled at the skips
pass (a "keep" was that ruling), so this stage only atomizes; it does not re-judge.

This is deliberately NOT eval/draft_nuggets.py: that drafter reads full transcripts and
carries the dropped vital/nice-to-have weighting and per-nugget evidence chunks. Here the
input is just (question, claim) and the output is nugget texts. No importance, no chunk
pointers, no reference answer, no date windows, no shift nugget (those are longitudinal).

The extraction rules (in the system prompt): subtract the question (a fact already stated
in the question earns nothing), one independently-checkable fact per nugget (split the
claim's "and"s), keep the fact and drop the claim's framing/phrasing.

Cross-family on purpose: the agent runs on OpenAI, this runs on Claude Sonnet 5.

Needs no DB (works from the worksheet text alone).

Usage:
  uv run python -m eval.extract_factual_nuggets --render eval/artifacts/factual_nuggets_review.md
  uv run python -m eval.extract_factual_nuggets --only-missing        # resume
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.provenance import PROVENANCE

KEPT = Path("eval/artifacts/factual_claim_vs_grounder_kept.md")
OUT = Path("eval/artifacts/factual_nuggets_draft.jsonl")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 2000    # a claim yields a handful of short nuggets + adaptive thinking
CALL_TIMEOUT = 120


# ---- output schema ---------------------------------------------------------

class ExtractOut(BaseModel):
    nuggets: list[str]   # each an atomic, independently-checkable fact; [] if the claim adds nothing to the question


# ---- prompt (frozen; hash recorded in the output _meta) --------------------

SYSTEM = """\
You are building the answer key for an evaluation of a research assistant that answers factual questions over one AI/ML YouTube creator's video library. You are given a QUESTION and a single CLAIM that is the vetted gold answer to it. Decompose the claim into "nuggets": the atomic, independently-checkable facts that a correct answer must state. These nuggets are what a correct answer will be scored against, one hit per nugget - so two "nuggets" that a single sentence would always satisfy together, or that always succeed or fail together, must not be two nuggets, or the score is inflated.

What a nugget is:
- One independently-checkable fact. Exactly one fact per nugget; never join two facts with "and". If the claim asserts two things that could each be right or wrong on their own (two numbers, two findings), make two nuggets.
- Self-contained enough to check, stated as a plain fact, not as commentary about the claim or the paper.

Hard rules:

1. Subtract the question - entities AND predicates. A fact already given in the question earns nothing and is NOT a nugget; nuggets are only the NEW information the claim adds. This covers named entities (a model, a benchmark, a paper) AND the properties/predicates the question already states. If the question already says an update is "fast, temporary, and position-specific" and asks WHY, then "it is fast", "it is temporary", and "it is position-specific" earn nothing - only the new explanation (the mechanism, the cause) is a nugget.

2. No nugget may be entailed by another. If an answer that states nugget B necessarily also states nugget A, they are not two facts - merge them. In particular, a general claim entailed by specific figures is not its own nugget ("performance improves as the dataset grows" is entailed by "16% -> 50% -> 70%", so only the figures earn).

3. A modifier is not a separate fact. An adjective or qualifier that lives inside a fact ("struggling smaller models", "collapse to a single solution") stays inside that fact; it does not become its own nugget.

4. Process enumeration collapses. If the claim lists the steps of a generic process, the nugget is the process as a whole. A single step earns its own nugget only if a correct answer would have to name that specific, distinctive step (not a generic step any description of the process would include).

5. Keep the fact, drop the framing. Phrasings like "the paper's core innovation is...", "the authors demonstrate...", "interestingly..." are framing, not facts - extract the underlying fact. The creator's own evaluation or characterization ("revolutionary", "fascinating", "not a good result") is framing too and earns nothing, UNLESS the question explicitly asks for the creator's judgment.

6. Do not invent. Only use facts present in the claim. Never add outside knowledge or infer facts the claim does not state.

7. No date windows and no "how it changed over time" nugget: this is a single-point factual claim, not a trajectory.

8. If the claim adds no checkable fact beyond what the question already states, return an empty list.

Beware over-collapsing. Rules 2-4 remove redundancy; they do NOT merge genuinely distinct facts. A list of per-model scores, or several distinct mathematical scaling relations, are independent facts - each is its own nugget even though they are parallel in form, because getting one right says nothing about the others.

Worked examples.

Example 1 (subtraction leaves one nugget).
Question: "What score did Gemini 3 Deep Think achieve on the ARC-AGI-2 benchmark?"
Claim: "Gemini 3 Deep Think scores 45% on the ARC-AGI-2 benchmark."
The question already names the model and the benchmark, so those earn nothing. The only new fact is the score.
Nuggets: ["Gemini 3 Deep Think scored 45% on the ARC-AGI-2 benchmark."]

Example 2 (split the "and" into two independent figures).
Question: "How does the 14B Deep-DxSearch model compare in performance to the much larger 671B DeepSeek R1 system on common versus rare disease diagnosis tasks?"
Claim: "The 14B Deep-DxSearch model outperforms a 671B DeepSeek R1 system by nearly 20 percentage points on common disease diagnosis and nearly 30 percentage points on rare disease diagnosis."
The models, their sizes, and the common-vs-rare split are all in the question. The two margin figures are independently checkable (one can be right while the other is wrong), so they are two nuggets. This is NOT over-collapsing territory.
Nuggets: ["Deep-DxSearch outperforms DeepSeek R1 by nearly 20 percentage points on common disease diagnosis.", "Deep-DxSearch outperforms DeepSeek R1 by nearly 30 percentage points on rare disease diagnosis."]

Example 3 (framing dropped, one real fact).
Question: "What did the VLM4VA paper's ablation study find about the correlation between a vision-language model's performance on standard visual question-answering benchmarks and its success rate in robotic manipulation tasks?"
Claim: "The VLM4VA paper's core innovation is a systematic ablation demonstrating the visual-semantic gap in real AI systems, finding zero correlation between a vision-language model's performance on standard vision question-answering benchmarks and its success rate in robotic manipulation."
"The core innovation is a systematic ablation" and "the visual-semantic gap" are framing; the ablation itself is presupposed by the question. The only earned fact is the finding.
Nuggets: ["The study found zero correlation between the vision-language model's visual-question-answering benchmark performance and its robotic-manipulation success rate."]

Example 4 (rule 2: a general claim entailed by the figures is not its own nugget).
Question: "How does performance change as the supervised fine-tuning dataset size increases from 20,000 samples to 1 million samples?"
Claim: "Scaling the supervised fine-tuning dataset size improves performance: with 20,000 data samples performance rises from about 16% to 50%, and with 1 million data samples it reaches about 70%."
"Scaling improves performance" is entailed by the figures (16% -> 50% -> 70% already shows improvement), so it is NOT its own nugget. Only the specific data points earn.
Nuggets: ["With about 20,000 samples, performance is about 16%.", "With about 20,000 samples, performance rises to about 50%.", "With about 1 million samples, performance reaches about 70%."]

Example 5 (rule 1: subtract predicates the question already states; only the explanation earns).
Question: "How does the rank of the weight update differ between standard fine-tuning and in-context learning (ICL), and why does this make ICL's update fast, temporary, and specific to the current token position?"
Claim: "Standard fine-tuning updates the whole weight matrix (rank N), making it expensive and slow, whereas ICL uses only a rank-one update, making it fast, temporary, and hyper-specific to the current token position due to non-linearity."
The question already states ICL's update is fast, temporary, and position-specific, and asks WHY - so those three properties earn nothing. The rank contrast is the requested "how", and non-linearity is the requested "why".
Nuggets: ["Standard fine-tuning updates the whole weight matrix (rank N).", "ICL uses only a rank-one update.", "The position-specificity comes from non-linearity."]

Example 6 (rule 4: a generic process collapses; keep only the distinctive steps).
Question: "In the context of an AI system built for laser fusion experiments, what is it actually designed to do if its purpose goes beyond just writing code?"
Claim: "The creator explains that the system is not about writing code but about automating the scientific method itself: experiment, discover, reason about results, form new hypotheses, formulate new experiments with new parameters, run a digital twin simulation, and if successful, run the real laser fusion experiment, then repeat the loop."
Experiment / discover / reason / hypothesize / formulate are the generic steps of the scientific method and collapse into "automates the scientific method". The distinctive, must-name steps are the digital-twin gate on the real experiment, and the loop.
Nuggets: ["The system automates the scientific method itself, rather than just writing code.", "It runs a digital-twin simulation and, only if that succeeds, runs the real laser-fusion experiment, then repeats the loop."]

Example 7 (rule 5: the creator's evaluation is a nugget only when the question asks for it).
Contrast two questions. If the question asks "...and was that considered a good result?", then the creator's judgment IS the requested answer, so "the creator says this is not a good result" is a nugget. But if the question asks only what a technique IS and how it works, then a characterization like "the creator calls it a revolutionary unification" is evaluative framing the question did not ask for, and earns nothing."""

PROMPT_SHA = hashlib.sha1(SYSTEM.encode()).hexdigest()[:8]


# ---- worksheet parsing -----------------------------------------------------

_QID_RE = re.compile(r"\*\*question id:\*\*\s*(\S+)")
_Q_RE = re.compile(r"\*\*question:\*\*\s*(.+)")
_CLAIM_RE = re.compile(r"\*\*claim:\*\*\s*(.+)")


def parse_kept(path: Path) -> list[dict]:
    """[{question_id, question, claim}, ...] from the kept-set worksheet.

    Each entry carries `**question id:**`, then `**question:**`, then `**claim:**`.
    Fails loudly if a started entry is missing its question or claim, since a
    silently-dropped keeper would shrink the gold below 26.
    """
    entries: list[dict] = []
    cur: dict = {}
    for line in path.read_text().splitlines():
        if m := _QID_RE.match(line):
            if cur:
                _require(cur)
                entries.append(cur)
            cur = {"question_id": m.group(1).strip()}
        elif m := _Q_RE.match(line):
            if cur:
                cur["question"] = m.group(1).strip()
        elif m := _CLAIM_RE.match(line):
            if cur:
                cur["claim"] = m.group(1).strip()
    if cur:
        _require(cur)
        entries.append(cur)
    return entries


def _require(entry: dict) -> None:
    if "question" not in entry or "claim" not in entry:
        raise ValueError(f"kept entry {entry.get('question_id', '?')} is missing question or claim")


# ---- extraction ------------------------------------------------------------

async def extract_one(entry: dict, sem: asyncio.Semaphore) -> tuple[str, dict | None]:
    """Return ('ok', record) | ('error', None). 'error' means the call failed and
    the entry is left unrecorded so --only-missing can retry it."""
    user = (f"Question: {entry['question']}\n\n"
            f"Claim (gold answer): {entry['claim']}\n\n"
            "Extract the nuggets a correct answer must contain, following the rules.")
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(SYSTEM, user, ExtractOut, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "adaptive"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - one bad call must not kill the batch
            print(f"  extract fail {entry['question_id']}: {type(e).__name__}: {e}", flush=True)
            return "error", None

    nuggets = [n.strip() for n in out.nuggets if n.strip()]
    record = {
        "question_id": entry["question_id"],
        "question": entry["question"],
        "claim": entry["claim"],
        "nuggets": nuggets,
        "provenance": {"generated_by": MODEL, "thinking": "adaptive", "prompt_sha": PROMPT_SHA,
                       "git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }
    return "ok", record


# ---- entailment audit (review-side QC, not part of extraction) -------------
# The >=5-count flag is a proxy that missed entailed nuggets in 2-/3-/4-nugget
# questions (B2 review, 2026-07-26). This is the real detector: a semantic check,
# because the defect (a general claim entailed by specific figures) has no lexical
# signal. It annotates the review sheet for the human; it is not a scored instrument.

class EntailmentPair(BaseModel):
    entailed: int       # 1-based index of the redundant nugget
    entailed_by: int    # 1-based index of the nugget that entails it
    why: str            # one short phrase


class EntailmentReport(BaseModel):
    pairs: list[EntailmentPair]


AUDIT_SYSTEM = """\
You audit a list of gold "nuggets" (atomic facts extracted for one question) for redundancy before a human review. Two nuggets are redundant when one ENTAILS the other: an answer that states nugget B necessarily also states nugget A. Report every ordered pair (entailed, entailed_by) where the first is entailed by the second.

Count as entailment:
- a general claim entailed by specific figures ("performance improves" is entailed by "16% -> 70%");
- a modifier or qualifier that is already contained inside another nugget;
- a generic step of a process that any statement of the whole process would include.

Do NOT flag two facts that merely share a subject or topic but can each be independently right or wrong (per-model scores, distinct scaling relations). If you are not sure that stating one truly forces the other, do not flag it. Return an empty list when the nuggets are mutually independent."""

AUDIT_PROMPT_SHA = hashlib.sha1(AUDIT_SYSTEM.encode()).hexdigest()[:8]


async def audit_one(record: dict, sem: asyncio.Semaphore) -> tuple[str, list[str]]:
    """Return (question_id, [human-readable entailment flags]); [] if independent or <2 nuggets."""
    nuggets = record["nuggets"]
    if len(nuggets) < 2:
        return record["question_id"], []
    listing = "\n".join(f"{i}. {n}" for i, n in enumerate(nuggets, 1))
    user = f"Question: {record['question']}\n\nNuggets:\n{listing}\n\nReport any entailment pairs."
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(AUDIT_SYSTEM, user, EntailmentReport, model=MODEL,
                                max_tokens=1500, thinking={"type": "adaptive"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - an audit miss must not kill the render
            print(f"  audit fail {record['question_id']}: {type(e).__name__}: {e}", flush=True)
            return record["question_id"], []
    n = len(nuggets)
    flags = [f"n{p.entailed} entailed by n{p.entailed_by}: {p.why.strip()}"
             for p in out.pairs
             if 1 <= p.entailed <= n and 1 <= p.entailed_by <= n and p.entailed != p.entailed_by]
    return record["question_id"], flags


async def audit_all(records: list[dict], concurrency: int) -> dict[str, list[str]]:
    """Run the entailment audit over all records concurrently -> {question_id: flags}."""
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*(audit_one(r, sem) for r in records))
    return dict(results)


# ---- render (B2 hand-over) -------------------------------------------------

def render_review(records: list[dict], audits: dict[str, list[str]] | None = None) -> str:
    """Human review sheet: per question the claim + numbered nuggets, the nugget-count
    distribution, the >=5-nugget count flag, and (if `audits` is given) the LLM
    entailment audit - the real redundancy detector the count flag proxies for."""
    audits = audits or {}
    records = sorted(records, key=lambda r: r["question_id"])
    lines = [f"# Factual nugget extraction - review ({len(records)} questions)", "",
             f"Model {MODEL}, prompt_sha `{PROMPT_SHA}`"
             + (f", entailment-audit prompt_sha `{AUDIT_PROMPT_SHA}`" if audits else "")
             + ". Each nugget is one independently-checkable fact subtracted from the claim "
             "(facts already in the question earn nothing).", ""]

    counts = Counter(len(r["nuggets"]) for r in records)
    lines += ["## Nugget-count distribution", ""]
    for k in sorted(counts):
        lines.append(f"- {k} nugget(s): {counts[k]} question(s)")
    total = sum(len(r["nuggets"]) for r in records)
    lines += ["", f"Total nuggets: {total} across {len(records)} questions "
              f"(mean {total / len(records):.1f}).", ""]

    if audits:
        flagged = [(r["question_id"], audits.get(r["question_id"], [])) for r in records]
        flagged = [(q, fs) for q, fs in flagged if fs]
        lines += ["## Entailment audit (LLM-checked; the real redundancy detector)", ""]
        if flagged:
            lines.append("Questions where a nugget is entailed by another (candidate over-splits):")
            for q, fs in flagged:
                lines.append(f"- **{q}**: " + "; ".join(fs))
        else:
            lines.append("No entailment flagged: no nugget is entailed by another in any question.")
        lines.append("")

    heavy = [r for r in records if len(r["nuggets"]) >= 5]
    lines += ["## Count flag: >=5 nuggets (proxy only - see the entailment audit above)", ""]
    lines += [f"- {r['question_id']}: {len(r['nuggets'])} nuggets" for r in heavy] or ["- (none)"]
    lines.append("")

    lines += ["---", ""]
    for r in records:
        qid = r["question_id"]
        lines += [f"## {qid}  ({len(r['nuggets'])} nuggets)", "",
                  f"**question:** {r['question']}", "",
                  f"**claim:** {r['claim']}", "",
                  "**nuggets:**"]
        if r["nuggets"]:
            lines += [f"{i}. {n}" for i, n in enumerate(r["nuggets"], 1)]
        else:
            lines.append("_(none - claim adds nothing beyond the question)_")
        if audits.get(qid):
            lines += ["", "_entailment audit:_ " + "; ".join(audits[qid])]
        lines += ["", "---", ""]
    return "\n".join(lines)


# ---- io + driver -----------------------------------------------------------

def read_done_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in (o := json.loads(ln)):
            done.add(o["question_id"])
    return done


def read_records(path: Path) -> list[dict]:
    out = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln and "_meta" not in (o := json.loads(ln)):
            out.append(o)
    return out


async def amain(args: argparse.Namespace) -> None:
    entries = parse_kept(KEPT)
    resuming = args.only_missing and OUT.exists()
    if resuming:
        done = read_done_ids(OUT)
        todo = [e for e in entries if e["question_id"] not in done]
        sink = OUT.open("a", encoding="utf-8")
    else:
        todo = entries
        sink = OUT.open("w", encoding="utf-8")
        sink.write(json.dumps({"_meta": {"stage": "factual_nuggets", "model": MODEL,
                   "thinking": "adaptive", "prompt_sha": PROMPT_SHA,
                   "provenance": {"git_sha": PROVENANCE.git_sha,
                                  "git_dirty": PROVENANCE.git_dirty}}}) + "\n")

    print(f"extracting {len(todo)}/{len(entries)} factual claims "
          f"(concurrency {args.concurrency}, prompt_sha {PROMPT_SHA}) -> {OUT}", flush=True)
    sem = asyncio.Semaphore(args.concurrency)
    n_ok = n_err = 0
    tasks = [extract_one(e, sem) for e in todo]
    for coro in asyncio.as_completed(tasks):
        status, rec = await coro
        if status == "ok":
            sink.write(json.dumps(rec) + "\n")
            sink.flush()   # crash-safe: each completed extraction hits disk immediately
            n_ok += 1
            print(f"  [{n_ok + n_err}/{len(todo)}] {rec['question_id']}: {len(rec['nuggets'])} nuggets", flush=True)
        else:
            n_err += 1
    sink.close()

    err = f", ERRORS {n_err} (resume with --only-missing)" if n_err else ""
    print(f"done: {n_ok} extracted{err}", flush=True)

    if args.render:
        records = read_records(OUT)
        print(f"running entailment audit over {len(records)} questions "
              f"(prompt_sha {AUDIT_PROMPT_SHA})...", flush=True)
        audits = await audit_all(records, args.concurrency)
        n_flagged = sum(1 for fs in audits.values() if fs)
        print(f"entailment audit: {n_flagged} question(s) with a flagged pair", flush=True)
        Path(args.render).write_text(render_review(records, audits), encoding="utf-8")
        print(f"rendered {len(records)} questions -> {args.render}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract factual gold nuggets from the kept claims.")
    ap.add_argument("--only-missing", action="store_true", help="resume: skip already-extracted questions")
    ap.add_argument("--render", type=Path, default=None, help="also write the human review markdown")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
