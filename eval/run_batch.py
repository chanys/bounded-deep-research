"""Phase 4 Phase A run harness: execute the frozen agent over the gold questions.

Iterates the longitudinal (36, incl. lc-0130) and factual (26) gold questions, runs
each `--runs` times (default 3), and saves each run keyed by (question_id, run_index)
so the batch is resumable: a completed run writes `run.json` last, and a resume skips
any (qid, idx) whose `run.json` already exists.

Each run lands in `eval/artifacts/runs/<question_id>/r<idx>/`:
  - `evidence_<run_id>.json` - the full RunEvidenceState (provenance, seen/cited chunks,
    cited_not_retrieved), dumped by run_agent(dump_dir=...).
  - a markdown trace, also from run_agent's dump.
  - `run.json` - the self-contained scoring record: question, answer, citations, and the
    evidence dict inlined, plus run metadata. Written last as the done-marker.

Retrieval defaults to the production dense pgvector path (RETRIEVAL_BACKEND=pgvector;
mode forced to dense). The hybrid-retrieval ablation arm overrides both: it sets
RETRIEVAL_BACKEND=opensearch and passes --mode hybrid, writing to a separate --out-dir
(runs_hybrid/) so the frozen baseline runs/ are never touched. This does not touch the
/query spend breaker or per-IP quota (those live in app/main.py); concurrency is bounded
only by OpenAI rate limits, so keep it modest.

Integrity halt: if any run reports a non-empty cited_not_retrieved (the agent cited a
chunk no search returned), the batch stops immediately. A provenance defect replicated
across 186 runs is worse than a halted fan-out.

Usage:
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_batch                 # all 62 x 3 (baseline)
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_batch --only lc-0011,lc-0014 --runs 3
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_batch --concurrency 4
  # hybrid ablation (longitudinal only, isolated output dir):
  RETRIEVAL_BACKEND=opensearch uv run python -m eval.run_batch --mode hybrid \
      --out-dir eval/artifacts/runs_hybrid --runs 1
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path

# Import config first so Langfuse keys land in the environment before the SDK initializes.
from core.config import settings  # noqa: F401
from langfuse import get_client

from app.agent import run_agent
from app.retrieval import Mode, aclose

CHANNEL = "code4AI"
ARTIFACTS = Path("eval/artifacts")
GOLD_FILES = [
    ARTIFACTS / "longitudinal_claim_vs_grounder.md",   # 36, incl. lc-0130 (segregated at score time)
    ARTIFACTS / "factual_claim_vs_grounder_kept.md",   # 26 keepers
]
RUNS_DIR = ARTIFACTS / "runs"

_QID_RE = re.compile(r"\*\*question id:\*\*\s*(\S+)")
_QTEXT_RE = re.compile(r"\*\*question:\*\*\s*(.+)")


def parse_questions(path: Path) -> list[tuple[str, str]]:
    """Extract [(question_id, question_text), ...] from a gold worksheet.

    Each entry carries a `**question id:**` line followed by a `**question:**` line;
    the id is captured first and paired with the next question line. Fails loudly
    (raises) if the file is missing, since a partial question set skews the whole run.
    """
    qs: list[tuple[str, str]] = []
    qid: str | None = None
    for line in path.read_text().splitlines():
        m = _QID_RE.match(line)
        if m:
            qid = m.group(1).strip()
            continue
        m = _QTEXT_RE.match(line)
        if m and qid:
            qs.append((qid, m.group(1).strip()))
            qid = None
    return qs


def load_all_questions() -> list[tuple[str, str]]:
    """All gold questions across both worksheets, in file order."""
    out: list[tuple[str, str]] = []
    for f in GOLD_FILES:
        out.extend(parse_questions(f))
    return out


class IntegrityError(RuntimeError):
    """A run cited a chunk no search returned; the fan-out must halt to investigate."""


async def run_one(qid: str, idx: int, question: str, sem: asyncio.Semaphore,
                  runs_dir: Path, mode: Mode) -> str:
    """Run one (question, run_index), persist it, and return a one-line status.

    Skips (returns "skip") when run.json already exists. On success writes the
    self-contained run.json last. Raises IntegrityError on non-empty
    cited_not_retrieved so the caller can stop the whole batch.

    `runs_dir` isolates the output tree (baseline runs/ vs ablation runs_hybrid/);
    `mode` is the requested retrieval mode, honored only under a non-pgvector backend
    (pgvector forces dense regardless - see app/agent.effective_mode).
    """
    out_dir = runs_dir / qid / f"r{idx}"
    done_marker = out_dir / "run.json"
    if done_marker.exists():
        return f"skip {qid} r{idx}"

    async with sem:
        out_dir.mkdir(parents=True, exist_ok=True)
        result = await run_agent(question, CHANNEL, mode=mode, dump_dir=str(out_dir))

    # Read back the evidence run_agent dumped (named by run_id; exactly one per dir).
    evidence_files = list(out_dir.glob("evidence_*.json"))
    if not evidence_files:
        raise RuntimeError(f"{qid} r{idx}: run finished but no evidence_*.json was dumped")
    evidence = json.loads(evidence_files[0].read_text())

    cnr = evidence.get("cited_not_retrieved") or []
    if cnr:
        raise IntegrityError(
            f"{qid} r{idx} (run_id {evidence.get('run_id')}): cited_not_retrieved is non-empty: "
            f"{cnr}. The agent cited chunks no search returned; halting the fan-out."
        )

    record = {
        "question_id": qid,
        "run_index": idx,
        "question": question,
        "channel": CHANNEL,
        "run_id": evidence.get("run_id"),
        "answer": result.answer,
        "citations": [c.model_dump() for c in result.citations],
        "steps_used": result.steps_used,
        "budget_exhausted": result.budget_exhausted,
        "evidence": evidence,
    }
    done_marker.write_text(json.dumps(record, indent=2))
    return f"done {qid} r{idx}  (steps={result.steps_used} cites={len(result.citations)} run_id={evidence.get('run_id')})"


async def main() -> None:
    ap = argparse.ArgumentParser(description="Run the frozen agent over the gold questions.")
    ap.add_argument("--only", default="", help="comma-separated question ids to restrict to (default: all)")
    ap.add_argument("--runs", type=int, default=3, help="runs per question (default 3)")
    ap.add_argument("--concurrency", type=int, default=4, help="max concurrent runs (default 4)")
    ap.add_argument("--mode", default="dense", choices=["dense", "bm25", "hybrid"],
                    help="requested retrieval mode; honored only under a non-pgvector backend (default dense)")
    ap.add_argument("--out-dir", default=str(RUNS_DIR),
                    help="output tree for run artifacts (default eval/artifacts/runs; use runs_hybrid for the ablation)")
    args = ap.parse_args()

    runs_dir = Path(args.out_dir)
    mode: Mode = args.mode

    questions = load_all_questions()
    if args.only:
        wanted = {q.strip() for q in args.only.split(",") if q.strip()}
        questions = [(qid, txt) for qid, txt in questions if qid in wanted]
        missing = wanted - {qid for qid, _ in questions}
        if missing:
            raise SystemExit(f"--only referenced unknown question ids: {sorted(missing)}")

    total = len(questions) * args.runs
    print(f"batch: {len(questions)} questions x {args.runs} runs = {total} runs "
          f"(concurrency={args.concurrency}, backend={settings.retrieval_backend}, "
          f"mode={mode}, out-dir={runs_dir})", flush=True)

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [
        asyncio.create_task(run_one(qid, idx, txt, sem, runs_dir, mode))
        for qid, txt in questions
        for idx in range(args.runs)
    ]

    completed = 0
    try:
        for coro in asyncio.as_completed(tasks):
            status = await coro
            completed += 1
            print(f"[{completed}/{total}] {status}", flush=True)
    except IntegrityError as e:
        print(f"\nHALT: {e}", flush=True)
        for t in tasks:
            t.cancel()
        raise
    finally:
        await aclose()
        get_client().flush()

    print(f"\nbatch complete: {completed}/{total} runs accounted for.", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
