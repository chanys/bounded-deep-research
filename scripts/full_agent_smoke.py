"""End-to-end smoke test for run_agent.

Runs the full ReAct agent on a single query so the Phase 2 step 1 wiring can be
verified in the Langfuse trace:
  - system message contains "Critical Failure Policy" (load_recipe is active)
  - at least one read_video_segment call appears in the tool calls
  - recipe_version: "0.1.0" is in the trace metadata

The run may take 30-60s (multiple searches, reads, then submit). The trace is
flushed to Langfuse on exit; open the Langfuse console to inspect it.

Usage:
  uv run python -m scripts.full_agent_smoke
"""
# Import config first so Langfuse keys land in the environment before the SDK initializes.
from app.config import settings  # noqa: F401
from langfuse import get_client

from app.agent import run_agent

# Trace lands in the Langfuse console; open it there to verify the run.

QUERY = "How does the creator view RAG vs Harness?"
CHANNEL = "code4AI"


def main():
    print(f"running agent: {QUERY!r} (channel={CHANNEL})\n")
    result = run_agent(QUERY, CHANNEL, mode="hybrid")

    print("=== agent result ===")
    print(f"  steps_used: {result.steps_used}")
    print(f"  budget_exhausted: {result.budget_exhausted}")
    print(f"  citations: {len(result.citations)}")
    print(f"\n{result.answer}")


if __name__ == "__main__":
    main()
    get_client().flush()
