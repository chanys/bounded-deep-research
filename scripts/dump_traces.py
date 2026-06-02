"""Batch-run trial queries through run_agent and dump a markdown trace per query.

Edit QUERIES (and CHANNEL/MODE) below as you iterate on the recipe. Each run
writes traces/dumps/<timestamp>_<slug>.md, which you can open, skim, or paste
into chat for behavioral analysis.

Usage:
  uv run python -m scripts.dump_traces
"""
import asyncio
from pathlib import Path

# Import config first so Langfuse keys land in the environment before the SDK initializes.
from app.config import settings  # noqa: F401
from langfuse import get_client

from app.agent import run_agent
from app.retrieval import aclose

# --- edit me as I iterate ---------------------------------------------------
# Spans the recipe's three tiers, grounded in the indexed code4AI corpus
# (Jan 2025 - Apr 2026).
QUERIES = [
    # single-topic factual
    "What two techniques does Llama 4 Scout use to achieve its 10 million token context length?",
    "What does the creator mean by 'Potemkin understanding', and why does he say it matters for AI safety?",
    # multi-topic comparative
    "How does the creator distinguish RAG from the broader 'AI harness', and what role does each play in an agent system?",
    "How does the creator compare the reasoning quality of GPT-5 and GPT-5.4 for scientific tasks?",
    # longitudinal
    "How has the creator's view of LLM reasoning evolved over 2025-2026, from 'the reasoning lie' to the GPT-5.4 reasoning decline?",
]
CHANNEL = "code4AI"
MODE = "hybrid"
DUMP_DIR = Path("traces/dumps")
# ----------------------------------------------------------------------------


async def main():
    try:
        for i, query in enumerate(QUERIES, 1):
            print(f"[{i}/{len(QUERIES)}] {query!r}")
            result = await run_agent(query, CHANNEL, mode=MODE, dump_dir=DUMP_DIR)
            print(f"    steps={result.steps_used} "
                  f"budget_exhausted={result.budget_exhausted} "
                  f"citations={len(result.citations)}")
    finally:
        await aclose()

    print(f"\ndumps written to {DUMP_DIR}/")


if __name__ == "__main__":
    asyncio.run(main())
    get_client().flush()
