"""Render an agent run's transcript to readable markdown for behavioral analysis.

The flow. As run_agent works, it keeps appending to one list called input_items.
That list is the running conversation: the system prompt, your question, and then
for each turn the model's reasoning, the tool calls it made, and the tool results
that came back. When the run succeeds, _finish is called, and if you passed a
dump_dir it hands that list (plus a few other things) to write_trace_dump. That
function calls render_markdown, which builds the file in three parts: a header,
the transcript, and the final answer. Then it writes the text to
traces/dumps/<timestamp>_<slug>.md.

How the transcript gets built. input_items is a flat list, not grouped by turn.
So _group_turns walks it and chops it into turns. The rule is simple: every model
turn begins with a reasoning item, so a new turn starts whenever it sees one.
Within a turn it collects the function_call items (the calls) and the
function_call_output items (the results). It skips the system prompt and your
original question (those go in the header instead), and any mid-run injected
message (like the budget-exhausted nudge) becomes a quoted note. Then for each
turn the renderer prints the reasoning summary, each tool call's arguments, and
each tool result, paired up call-with-result. Helper functions shape tool results
by type (search hits become a bulleted list, a read segment shows its chunk text,
errors show the message). Nothing is truncated: dumps carry full text so no detail
is lost during analysis.

On reasoning specifically: a reasoning item carries both an encrypted_content blob
and a human-readable summary. _reasoning_text reads only the summary and ignores
the encrypted blob, which is why the dumps are clean.
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def _slug(query: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
    return s[:max_len].rstrip("-") or "query"


def _render_args(name: str, raw_args: str) -> str:
    """Render a tool call's arguments. submit_answer's args (the full answer +
    citations) are shown in the Final Answer section instead, so we summarize."""
    try:
        args = json.loads(raw_args)
    except (json.JSONDecodeError, TypeError):
        return str(raw_args)

    if name == "submit_answer":
        n = len(args.get("citations", []))
        return f"(final answer with {n} citation(s) — see Final Answer below)"
    return json.dumps(args, ensure_ascii=False)


def _render_output(raw_output: str) -> str:
    """Render a function_call_output, shaped by which tool produced it."""
    try:
        out = json.loads(raw_output)
    except (json.JSONDecodeError, TypeError):
        return str(raw_output)

    if "hits" in out:
        hits = out["hits"]
        lines = [f"{len(hits)} hit(s)"]
        for h in hits:
            lines.append(
                f"  - [{h.get('video_id')} @ {h.get('start_ts')}-{h.get('end_ts')}] "
                f"({h.get('published_at')}) "
                f"{h.get('title', '')}: {h.get('text', '')}"
            )
        return "\n".join(lines)

    if "status" in out:  # submit_answer accepted
        return f"status: {out['status']}"

    if "error" in out:
        return f"error: {out['error']}"

    return json.dumps(out, ensure_ascii=False)


def _reasoning_text(item: dict) -> str:
    """Pull the readable summary out of a reasoning item, ignoring encrypted_content."""
    parts = [s.get("text", "") for s in item.get("summary", []) if s.get("text")]
    return "\n\n".join(parts).strip()


def _group_turns(input_items: list[dict]) -> list[dict]:
    """Group the flat item list into turns.

    A turn starts at a reasoning item (each model response begins with reasoning)
    and collects the tool calls it made plus the tool results that followed.
    Returns dicts shaped {"reasoning", "calls": [(name, args)], "outputs": [str],
    "messages": [str]} for model turns, or {"note": str} for injected user messages.
    The leading system prompt and the initial user query are skipped (shown in the
    header instead).
    """
    turns: list[dict] = []
    cur: dict | None = None
    seen_query = False

    def flush():
        nonlocal cur
        if cur is not None:
            turns.append(cur)
            cur = None

    def fresh() -> dict:
        return {"reasoning": "", "calls": [], "outputs": [], "messages": []}

    for item in input_items:
        role = item.get("role")
        itype = item.get("type")

        if role == "system":
            continue
        if role == "user":
            if not seen_query:  # the original question, already in the header
                seen_query = True
                continue
            flush()
            turns.append({"note": item.get("content", "")})
            continue

        if itype == "reasoning":
            flush()
            cur = fresh()
            cur["reasoning"] = _reasoning_text(item)
        elif itype == "function_call":
            if cur is None:
                cur = fresh()
            cur["calls"].append((item.get("name", "?"), item.get("arguments", "{}")))
        elif itype == "function_call_output":
            if cur is None:
                cur = fresh()
            cur["outputs"].append(item.get("output", ""))
        elif role == "assistant":
            if cur is None:
                cur = fresh()
            content = item.get("content", "")
            if isinstance(content, list):  # responses API content blocks
                content = " ".join(b.get("text", "") for b in content if isinstance(b, dict))
            if content:
                cur["messages"].append(content)

    flush()
    return turns


def render_markdown(
    *,
    query: str,
    channel: str,
    mode: str,
    recipe_version: str,
    trace_id: str | None,
    trace_url: str | None,
    input_items: list[dict],
    result: Any,
) -> str:
    lines: list[str] = []

    lines.append(f"# Agent run: {query}")
    lines.append("")
    lines.append(f"- **query:** {query}")
    lines.append(f"- **channel:** {channel}")
    lines.append(f"- **mode:** {mode}")
    lines.append(f"- **recipe_version:** {recipe_version}")
    lines.append(f"- **steps_used:** {result.steps_used}")
    lines.append(f"- **budget_exhausted:** {result.budget_exhausted}")
    if trace_id:
        lines.append(f"- **trace_id:** {trace_id}")
    if trace_url:
        lines.append(f"- **trace_url:** {trace_url}")
    lines.append("")

    lines.append("## Transcript")
    lines.append("")
    turn_no = 0
    for turn in _group_turns(input_items):
        if "note" in turn:
            lines.append(f"> **Injected message:** {turn['note']}")
            lines.append("")
            continue

        turn_no += 1
        lines.append(f"### Turn {turn_no}")
        if turn["reasoning"]:
            lines.append("**Reasoning summary:**")
            lines.append("")
            lines.append(turn["reasoning"])
            lines.append("")
        for msg in turn["messages"]:
            lines.append(f"**Assistant:** {msg}")
            lines.append("")

        # Pair each call with its result (gather preserves call order).
        outputs = turn["outputs"]
        for i, (name, raw_args) in enumerate(turn["calls"]):
            lines.append(f"**Tool call:** `{name}`")
            lines.append("")
            lines.append("```json")
            lines.append(_render_args(name, raw_args))
            lines.append("```")
            if i < len(outputs):
                lines.append("**Tool result:**")
                lines.append("")
                lines.append("```")
                lines.append(_render_output(outputs[i]))
                lines.append("```")
            lines.append("")

    lines.append("## Final Answer")
    lines.append("")
    lines.append(result.answer)
    lines.append("")
    lines.append("### Citations")
    if result.citations:
        for c in result.citations:
            lines.append(f"- {c.video_id} @ {c.start_ts}-{c.end_ts}")
    else:
        lines.append("- (none)")
    lines.append("")

    return "\n".join(lines)


def write_trace_dump(
    dump_dir: str | Path,
    *,
    query: str,
    channel: str,
    mode: str,
    recipe_version: str,
    trace_id: str | None,
    trace_url: str | None,
    input_items: list[dict],
    result: Any,
) -> Path:
    """Render the run to markdown and write it to dump_dir. Returns the path."""
    md = render_markdown(
        query=query,
        channel=channel,
        mode=mode,
        recipe_version=recipe_version,
        trace_id=trace_id,
        trace_url=trace_url,
        input_items=input_items,
        result=result,
    )
    out_dir = Path(dump_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{ts}_{_slug(query)}.md"
    path.write_text(md, encoding="utf-8")
    return path
