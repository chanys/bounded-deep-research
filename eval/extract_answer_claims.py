"""Phase 4 C1: extract the groundable assertions an agent answer makes.

Input is one A2 agent answer; output is the factual assertions it makes about what the
creator said/held, each phrased to be checkable against a single retrieved chunk. These
answer-claims are the groundedness side of scoring (judge dir 2): each is checked against
the run's retrieved chunk set.

The load-bearing rule is longitudinal: a cross-video SHIFT ("he moved from optimism to
skepticism", "his view evolved") is not groundable against any single chunk, so a shift
statement must NOT become an extracted claim - it would guarantee a false groundedness
miss. The extractor decomposes a shift into its per-period stances (each groundable) and
drops the shift itself. The shift is scored on the recall side (a gold nugget), never here.
Getting this wrong silently deflates groundedness.

Distinct from eval/extract_factual_nuggets.py (that decomposes a gold CLAIM into scored
nuggets; this decomposes an agent ANSWER into groundable assertions). Sonnet 5, cross-family.

Usage:
  uv run python -m eval.extract_answer_claims --eyeball --render eval/artifacts/answer_claims_eyeball.md
  uv run python -m eval.extract_answer_claims --runs lc-0011:0,fc-0001:0 --render out.md
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path

from pydantic import BaseModel

from core.claude_llm import call_structured

RUNS_DIR = Path("eval/artifacts/runs")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 4000
CALL_TIMEOUT = 150

# Default eyeball set: mixed tiers (3 longitudinal where shift-skipping bites, 2 factual).
EYEBALL_RUNS = ["lc-0011:0", "lc-0014:0", "lc-0024:0", "fc-0001:0", "fc-0032:0"]


class ClaimsOut(BaseModel):
    claims: list[str]   # each a standalone groundable assertion the answer makes; [] if none


SYSTEM = """\
You extract the factual assertions a research assistant's ANSWER makes, so each can later be checked against the evidence the assistant retrieved. The answer is about what one YouTube creator (an AI/ML explainer) said or held across their videos. Extract the assertions the answer makes about what the creator said, holds, or claimed, and the concrete facts it reports.

What to extract:
- Each standalone assertion about what the creator said or held, or a concrete fact the answer states (a number, a finding, a comparison, a dated stance). One assertion per claim, understandable on its own.
- For a dated stance in a longitudinal answer, keep the stance as its own claim, with its time marker if the answer gives one ("In early 2025 the creator was optimistic about agentic AI's real-world impact").

What to SKIP:
- Pure connective framing that asserts nothing checkable: "in summary", "overall", "to answer the question", "so the evolution was...". These organize the answer; they are not facts.
- CRUCIAL - do not extract a cross-video SHIFT or TRAJECTORY statement. "He moved from optimism to skepticism", "his assessment evolved", "the arc went from X to Y" describe a change ACROSS videos, which no single retrieved chunk can support. Do NOT extract the shift itself. Instead extract the individual period stances it is built from (the early "optimism" stance and the later "skepticism" stance, each as its own claim). The shift is checked elsewhere; here we want only the groundable stances.
- Ignore the bracketed timestamp citation markers like [990-1020]; they are references, not content.

Rules:
- One assertion per claim; never join two facts with "and".
- Deduplicate restatements only. If the SAME fact is asserted in two places - typically an intro thesis and its restatement in a body section - keep the more complete one and drop the other. This applies ONLY to genuine restatements of one fact; it NEVER overrides atomicity. Two DISTINCT facts remain two claims even when they share a subject and period, and even when a single sentence states both (never merge distinct facts into one "and"-joined claim). Examples that stay separate: "scored at best 30%" and "most systems below 30%"; "the model doesn't always say what it thinks" and "the model will blatantly lie". When unsure whether two assertions are one fact restated or two related facts, keep them separate.
- Do not invent assertions the answer does not make, and never add outside knowledge. Extract only what the answer states.
- If the answer makes no groundable assertion (pure framing), return an empty list.

Worked example 1 (longitudinal: drop the shift, keep the stances).
Answer: "The creator moved from qualified optimism in early 2025 to deep skepticism by early 2026: in February 2025 he described agentic AI as showing breakthroughs in autonomous reasoning [990-1020], but by January 2026 he said the anticipated agentic revolution had stalled [90-120]. So the evolution was from excitement to disappointment."
Claims: ["In February 2025 the creator described agentic AI as showing breakthroughs in autonomous reasoning.", "By January 2026 the creator said the anticipated agentic-AI revolution had stalled."]
(NOT extracted: "moved from qualified optimism to deep skepticism" - a cross-video shift; "So the evolution was from excitement to disappointment" - connective framing.)

Worked example 2 (factual: the assertion, marker stripped).
Answer: "Gemini 3 Deep Think scored 45% on the ARC-AGI-2 benchmark [30-60]."
Claims: ["Gemini 3 Deep Think scored 45% on the ARC-AGI-2 benchmark."]"""

PROMPT_SHA = hashlib.sha1(SYSTEM.encode()).hexdigest()[:8]


async def extract_claims(answer: str, sem: asyncio.Semaphore) -> list[str]:
    """Extract the groundable assertions from one answer; [] on failure (logged)."""
    user = f"Answer:\n\n{answer}\n\nExtract the groundable assertions, following the rules."
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(SYSTEM, user, ClaimsOut, model=MODEL,
                                max_tokens=MAX_TOKENS, thinking={"type": "adaptive"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - one bad answer must not kill the batch
            print(f"  extract fail: {type(e).__name__}: {e}", flush=True)
            return []
    return [c.strip() for c in out.claims if c.strip()]


def load_run(spec: str) -> dict:
    """spec 'qid:idx' -> the run.json record."""
    qid, idx = spec.split(":")
    path = RUNS_DIR / qid / f"r{idx}" / "run.json"
    return json.loads(path.read_text())


def render(results: list[dict]) -> str:
    """Eyeball sheet: per run the question, answer, and extracted claims."""
    lines = [f"# Answer-claim extraction - eyeball ({len(results)} runs)", "",
             f"Model {MODEL}, prompt_sha `{PROMPT_SHA}`. Groundable assertions only; "
             "cross-video shift/trajectory statements and pure framing are dropped.", "", "---", ""]
    for r in results:
        lines += [f"## {r['question_id']} r{r['run_index']}  ({len(r['claims'])} claims)", "",
                  f"**question:** {r['question']}", "",
                  "**answer:**", "", r["answer"], "",
                  "**extracted claims:**"]
        lines += [f"{i}. {c}" for i, c in enumerate(r["claims"], 1)] or ["_(none)_"]
        lines += ["", "---", ""]
    return "\n".join(lines)


async def amain(args: argparse.Namespace) -> None:
    specs = EYEBALL_RUNS if args.eyeball else [s.strip() for s in args.runs.split(",") if s.strip()]
    runs = [load_run(s) for s in specs]
    print(f"extracting answer-claims for {len(runs)} run(s) (prompt_sha {PROMPT_SHA})", flush=True)
    sem = asyncio.Semaphore(args.concurrency)

    async def one(run):
        claims = await extract_claims(run["answer"], sem)
        print(f"  {run['question_id']} r{run['run_index']}: {len(claims)} claims", flush=True)
        return {"question_id": run["question_id"], "run_index": run["run_index"],
                "question": run["question"], "answer": run["answer"], "claims": claims}

    results = await asyncio.gather(*(one(r) for r in runs))
    results.sort(key=lambda r: (r["question_id"], r["run_index"]))
    if args.render:
        Path(args.render).write_text(render(results), encoding="utf-8")
        print(f"rendered -> {args.render}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract groundable assertions from agent answers.")
    ap.add_argument("--eyeball", action="store_true", help=f"use the default mixed-tier set: {EYEBALL_RUNS}")
    ap.add_argument("--runs", default="", help="comma-separated qid:idx to extract (e.g. lc-0011:0,fc-0001:0)")
    ap.add_argument("--render", type=Path, default=None, help="write the eyeball markdown")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    if not args.eyeball and not args.runs:
        ap.error("pass --eyeball or --runs")
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
