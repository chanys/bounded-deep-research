"""Shared human-readable rendering of a drafted nugget record.

Used by the Stage 3 content gate (draft_nuggets --render) and the adjudication
emit (adjudicate_nuggets), so the reading view is defined once. A record is one
query's draft: query text, nuggets (each with importance + evidence chunk ids),
and a reference answer. `chunk_text` maps chunk_id -> transcript text so evidence
can be shown inline.
"""
from __future__ import annotations


def render_query_md(record: dict, chunk_text: dict[str, str]) -> str:
    """Return a markdown block for one drafted query record."""
    head = (f"## {record['query_id']} "
            f"[{record['tier']} | {record.get('topic_cluster', '?')} | "
            f"{record.get('observed_shape', '?')}]")
    lines = [head, "", f"**Query:** {record['query']}", "",
             f"### Nuggets ({len(record['nuggets'])})", ""]
    for i, n in enumerate(record["nuggets"], 1):
        lines.append(f"{i}. **[{n['importance']}]** {n['text']}")
        for cid in n["evidence_chunk_ids"]:
            snippet = chunk_text.get(cid, "(chunk text unavailable)")
            lines.append(f"    - `{cid}` — {snippet}")
        lines.append("")
    lines += ["### Reference answer", "", record.get("reference_answer", ""), ""]
    return "\n".join(lines)
