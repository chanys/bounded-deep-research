"""One-off: run the agent and print the per-turn token breakdown.

Shows how input grows turn over turn (the stateless re-send cost), how much is
cached, and the reasoning/output split, so we can see which lever matters.

Usage: uv run python -m scripts.token_breakdown
"""
import asyncio

from core.config import settings  # noqa: F401  (loads Langfuse env before SDK init)
from langfuse import get_client

from app.agent import run_agent, SYSTEM_PROMPT
from app.retrieval import aclose

QUERY = "How has the creator's view of LLM reasoning evolved over 2025-2026?"


async def main():
    turns: list[dict] = []
    searches = reads = 0

    def sink(e: dict):
        nonlocal searches, reads
        if e["type"] == "turn_complete":
            turns.append(e["usage"])
        elif e["type"] == "search_start":
            searches += 1
        elif e["type"] == "read_start":
            reads += 1

    result = await run_agent(QUERY, "code4AI", mode="hybrid", event_sink=sink)
    await aclose()

    print(f"\nsystem prompt: ~{len(SYSTEM_PROMPT) // 4} tokens ({len(SYSTEM_PROMPT)} chars)")
    print(f"{'turn':>4} {'input':>8} {'cached':>8} {'output':>8} {'reason':>7} {'total':>8}")
    sin = sout = scached = sreason = 0
    for i, u in enumerate(turns):
        print(f"{i:>4} {u['input_tokens']:>8} {u['cached_input_tokens']:>8} "
              f"{u['output_tokens']:>8} {u['reasoning_tokens']:>7} {u['total_tokens']:>8}")
        sin += u["input_tokens"]; sout += u["output_tokens"]
        scached += u["cached_input_tokens"]; sreason += u["reasoning_tokens"]
    print(f"\nturns={len(turns)} searches={searches} reads={reads} citations={len(result.citations)}")
    print(f"sum: input={sin} (cached={scached}) output={sout} (reasoning={sreason})")
    uncached = sin - scached
    print(f"uncached input={uncached}  -> billed at full input rate")


if __name__ == "__main__":
    asyncio.run(main())
    get_client().flush()
