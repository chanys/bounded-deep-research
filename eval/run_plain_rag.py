"""Plain single-shot RAG baseline over the factual gold questions (no ReAct loop).

The no-ReAct ablation: for each factual question, retrieve once (dense kNN on the RAW
question, top-k) and synthesize an answer in a single gpt-5.4 call over exactly those
chunks. No search reformulation, no mark_ready, no iteration - the whole ReAct loop is
replaced by one retrieve-then-answer pass. Scored later with the FROZEN Phase 4
instrument (judge a7d71e4a, C1 c7cbc275, factual-gold-v1.0) so the recall/groundedness
numbers are directly comparable to the agent's factual 86.9%.

The comparison this arm makes: agent (multi-search, LLM-generated queries, ~40 chunks
accumulated) vs plain RAG (one raw-question search, k chunks). The gap prices the loop.

Writes scorer-compatible run.json files to eval/artifacts/runs_plainrag/<qid>/r0/ so the
existing score_runs (with --runs-dir/--scores-dir) consumes them unchanged. The record
carries only what the scorer reads - answer, evidence.seen_chunks, provenance.corpus_id -
plus provenance for auditability. Resumable: a completed (qid) writes run.json last.

Usage:
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_plain_rag                 # all factual
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_plain_rag --only fc-0001  # smoke
  RETRIEVAL_BACKEND=pgvector uv run python -m eval.run_plain_rag --k 10 --concurrency 4
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from core.config import settings  # noqa: F401 - front-loads env before SDK init
from core.llm import call_text_llm
from core.provenance import PROVENANCE

from app.corpus import corpus_id
from app.retrieval import aclose, search
from eval.run_batch import ARTIFACTS, parse_questions

CHANNEL = "code4AI"
FACTUAL_GOLD = ARTIFACTS / "factual_claim_vs_grounder_kept.md"
LONGITUDINAL_GOLD = ARTIFACTS / "longitudinal_claim_vs_grounder.md"
OUT_DIR = ARTIFACTS / "runs_plainrag"  # shared; fc-/lc- ids do not collide

# Closed-book synthesis: answer ONLY from the provided excerpts. Deliberately minimal -
# a plain RAG baseline is retrieve-then-answer, not the ReAct recipe (which is written for
# the search/mark_ready loop and would not apply here).
SYNTH_SYSTEM = (
    "You answer a question using ONLY the provided transcript excerpts from one "
    "AI/ML YouTube creator's videos. Be specific and factual, and ground every claim in "
    "the excerpts - do not add outside knowledge. Cite the video id and timestamp inline "
    "where relevant. If the excerpts do not contain the answer, say so plainly. "
    "Answer in markdown."
)


def _chunk_id(hit: dict) -> str:
    """Match the seen_chunks format the scorer resolves: video_id:<5-digit start>."""
    return f"{hit['video_id']}:{int(hit['start_ts']):05d}"


def _format_chunks(hits: list[dict]) -> str:
    lines = []
    for h in hits:
        date = h.get("published_at") or "unknown date"
        lines.append(f"[{h['video_id']} @ {int(h['start_ts'])}s | published {date}]\n{h['text']}")
    return "\n\n".join(lines)


async def run_one(qid: str, question: str, k: int, sem: asyncio.Semaphore) -> str:
    """Retrieve once, synthesize once, persist a scorer-compatible run.json."""
    out_dir = OUT_DIR / qid / "r0"
    done = out_dir / "run.json"
    if done.exists():
        return f"skip {qid}"

    async with sem:
        hits = await search(question, channel=CHANNEL, k=k, mode="dense")
        seen = sorted({_chunk_id(h) for h in hits})
        if not hits:
            answer = "No relevant transcript excerpts were retrieved."
        else:
            user = f"Question: {question}\n\nTranscript excerpts:\n\n{_format_chunks(hits)}\n\nAnswer:"
            answer = await call_text_llm(SYNTH_SYSTEM, user)

    out_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "question_id": qid,
        "run_index": 0,
        "question": question,
        "channel": CHANNEL,
        "arm": f"plain_rag_k{k}",
        "answer": answer,
        "citations": [],  # plain RAG does no structured citation; scorer grounds on seen_chunks
        "evidence": {
            "seen_chunks": seen,
            "seen_count": len(seen),
            "retrieval_mode": "dense",
            "retrieval_k": k,
            "model": settings.agent_model,
            "cited_not_retrieved": [],
            "provenance": {
                "git_sha": PROVENANCE.git_sha,
                "git_dirty": PROVENANCE.git_dirty,
                "recipe_version": "plain_rag",  # no ReAct recipe; synthesis prompt is inline above
                "corpus_id": corpus_id(CHANNEL),
            },
        },
    }
    done.write_text(json.dumps(record, indent=2))
    return f"done {qid}  (retrieved={len(seen)} answer_chars={len(answer)})"


async def main() -> None:
    ap = argparse.ArgumentParser(description="Plain single-shot RAG baseline over factual gold.")
    ap.add_argument("--only", default="", help="comma-separated question ids (default: all in the gold file)")
    ap.add_argument("--gold-file", default=str(FACTUAL_GOLD),
                    help="gold worksheet to read questions from (factual default; pass the longitudinal worksheet for that tier)")
    ap.add_argument("--k", type=int, default=settings.retrieval_k, help="chunks retrieved per question (default retrieval_k=10)")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()

    questions = parse_questions(Path(args.gold_file))
    if args.only:
        wanted = {q.strip() for q in args.only.split(",") if q.strip()}
        questions = [(q, t) for q, t in questions if q in wanted]

    print(f"plain RAG: {len(questions)} factual questions, k={args.k}, backend={settings.retrieval_backend}, "
          f"out={OUT_DIR}", flush=True)
    sem = asyncio.Semaphore(args.concurrency)
    tasks = [asyncio.create_task(run_one(qid, txt, args.k, sem)) for qid, txt in questions]
    done = 0
    try:
        for coro in asyncio.as_completed(tasks):
            status = await coro
            done += 1
            print(f"[{done}/{len(questions)}] {status}", flush=True)
    finally:
        await aclose()
    print(f"\nplain RAG complete: {done}/{len(questions)}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
