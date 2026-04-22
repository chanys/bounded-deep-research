"""ReAct agent loop over the transcript corpus."""
import json
from langfuse import observe, get_client

from app.config import settings
from app.llm import respond, to_input_item
from app.tools import TOOLS, dispatch, SubmittedAnswer


SYSTEM_PROMPT = """\
You are a research agent answering questions about a corpus of video \
transcripts. You have two tools:

- search_transcripts(query, k): returns up to k transcript chunks \
matching the query, with video_id, title, timestamps, and a snippet.
- submit_answer(answer, citations): submits your final answer with \
supporting citations.

How to work:

1. Start by searching with concise, specific queries. Run multiple \
searches with different phrasings when the question has multiple \
aspects or when initial results are thin — this corpus is bounded, \
so a missed chunk is unrecoverable.
2. Base your answer only on what you find in the transcripts. If the \
corpus does not contain enough evidence to answer, say so in the \
answer rather than guessing.
3. Every factual claim in your answer should be supported by at least \
one citation. Citations reference chunks by (video_id, start_ts, \
end_ts) — you do not need to quote chunk text in the citation itself.
4. Call submit_answer exactly once, when you have sufficient evidence. \
Do not emit plain text as your final reply; always go through \
submit_answer.
"""


class AgentResult(SubmittedAnswer):
    """The final agent output: answer + citations + run metadata."""

    steps_used: int
    budget_exhausted: bool


def _finalize(submitted: SubmittedAnswer, steps_used: int, budget_exhausted: bool) -> AgentResult:
    result = AgentResult(
        answer=submitted.answer,
        citations=submitted.citations,
        steps_used=steps_used,
        budget_exhausted=budget_exhausted,
    )
    langfuse = get_client()
    langfuse.update_current_span(
        output={
            "answer": result.answer,
            "citation_count": len(result.citations),
        },
        metadata={"steps_used": steps_used, "budget_exhausted": budget_exhausted},
    )
    return result


@observe(name="run_agent")
def run_agent(query: str) -> AgentResult:
    """Run the ReAct loop for a single query.

    Returns AgentResult on success. Raises RuntimeError if the agent
    emits text without calling any tool (unexpected state) or if the
    forced submit_answer on budget exhaustion also fails.
    """
    langfuse = get_client()
    langfuse.update_current_span(
        input={"query": query},
        metadata={"agent_model": settings.agent_model,
                  "reasoning_effort": settings.reasoning_effort,
                  "max_steps": settings.agent_max_steps},
    )

    input_items: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": query},
    ]

    for step in range(settings.agent_max_steps):
        # import json
        # print(f"--- turn {step + 1} input_items ---")
        # for i, it in enumerate(input_items):
        #     print(i, json.dumps(it, indent=2, default=str))

        response = respond(input_items, tools=TOOLS, tool_choice="required")

        # 1. Append every emitted item verbatim (reasoning, function_calls, messages).
        for item in response.output:
            input_items.append(to_input_item(item))

        # 2. Dispatch every function_call; append each output.
        terminal = None
        any_function_call = False
        for item in response.output:
            if item.type == "function_call":
                any_function_call = True
                result = dispatch(to_input_item(item))
                input_items.append(result.output_item)
                if result.terminal:
                    terminal = result

        # 3. Exit on successful submit_answer.
        if terminal is not None:
            return _finalize(terminal.submitted, step + 1, False)

        # 4. Model emitted text with no tool call — unexpected in this loop.
        if not any_function_call:
            raise RuntimeError(
                f"Agent emitted text without calling any tool at step {step + 1}. "
                f"Output: {response.output_text!r}"
            )

    # 5. Budget exhausted — force submit_answer.
    input_items.append({
        "role": "user",
        "content": (
            "Step budget exhausted. Call submit_answer now with the best "
            "answer you can construct from evidence gathered so far. If "
            "evidence is insufficient, say so in the answer."
        ),
    })
    response = respond(
        input_items,
        tools=TOOLS,
        tool_choice={"type": "function", "name": "submit_answer"},
    )
    for item in response.output:
        input_items.append(to_input_item(item))
    for item in response.output:
        if item.type == "function_call":
            result = dispatch(to_input_item(item))
            input_items.append(result.output_item)
            if result.terminal:
                return _finalize(result.submitted, settings.agent_max_steps, True)

    raise RuntimeError("Forced submit_answer on budget exhaustion failed.")