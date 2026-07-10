"""End-to-end smoke test for run_agent.

Runs the full ReAct agent on a single query so the Phase 2 step 1 wiring can be
verified in the Langfuse trace:
  - system message contains "Critical Failure Policy" (load_recipe is active)
  - at least one read_video_segment call appears in the tool calls
  - recipe_version in the trace metadata matches the active recipe frontmatter

The run may take 30-60s (multiple searches, reads, then submit). The trace is
flushed to Langfuse on exit; open the Langfuse console to inspect it.

Usage:
  uv run python -m scripts.full_agent_smoke
"""
import asyncio

# Import config first so Langfuse keys land in the environment before the SDK initializes.
from core.config import settings  # noqa: F401
from langfuse import get_client

from app.agent import run_agent
from app.retrieval import aclose

# Trace lands in the Langfuse console; open it there to verify the run.

QUERY = "How does the creator view RAG vs Harness?"
CHANNEL = "code4AI"


async def main():
    print(f"running agent: {QUERY!r} (channel={CHANNEL})\n")
    try:
        result = await run_agent(QUERY, CHANNEL, mode="hybrid")
    finally:
        await aclose()

    print("=== agent result ===")
    print(f"  steps_used: {result.steps_used}")
    print(f"  budget_exhausted: {result.budget_exhausted}")
    print(f"  citations: {len(result.citations)}")
    print(f"\n{result.answer}")


if __name__ == "__main__":
    asyncio.run(main())
    get_client().flush()
