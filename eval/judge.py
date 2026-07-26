"""Phase 4 C2: the alignment judge (one fixed prompt, three directions).

Decides whether a single CLAIM is supported by a given TEXT: binary HIT/MISS + a
one-sentence reason, no middle category. One frozen system prompt serves all three
scoring directions; the user message carries the specifics (text kind, claim type):

- Dir 1 recall:        claim = gold nugget,          text = the agent answer.
- Dir 2 groundedness:  claim = extracted answer-claim, text = the run's retrieved chunk SET.
- Dir 3 attribution:   claim = a MISSED gold nugget,  text = the run's surfaced chunk SET.

Dir 3 is dir-2-shaped (claim vs chunk set), so it reuses the prompt and adds no component;
C3 still calibrates it explicitly because (nugget x transcript-chunk) is a distinct claim/text
combination from dir 2's (answer-claim x transcript-chunk).

Load-bearing details (each would silently bias a number if omitted):
- Chunks are grounded as a SET (evidence combined across chunks), not chunk-by-chunk:
  neighbor_window=0 means lone 30s chunks, and a real claim can span two separately-retrieved
  ones; chunk-by-chunk grounding would false-miss boundary-spanning claims.
- Each chunk carries its video id + PUBLISH DATE as metadata: a dated claim ("early 2026") is
  supported by a chunk's stance whose date lives in metadata, not the transcript text. Text-only
  grounding would false-miss every dated claim and collapse longitudinal groundedness.
- shift / no_change nuggets are judged as CONNECTIONS, not facts (see the system prompt).

The fixed system prompt is prompt-cached (cache_system=True): the judge makes thousands of calls
reusing it, so it is sent once and read from cache after. Sonnet 5, cross-family.

Usage:
  uv run python -m eval.judge --selftest   # crafted pairs; verify mechanics + shift/no-change/metadata
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.db import transaction

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1500
CALL_TIMEOUT = 120


class Verdict(BaseModel):
    hit: bool     # True = HIT (the text supports/states the claim), False = MISS
    reason: str   # one sentence


SYSTEM = """\
You are the alignment judge for an evaluation of a research assistant that answers questions about what one AI/ML YouTube creator said across their videos. You decide whether a single CLAIM is supported by a given TEXT. Output a binary verdict - HIT or MISS - and a one-sentence reason. There is no middle category; when genuinely borderline, choose the more defensible side and say why.

Each request states a TEXT KIND and a CLAIM TYPE. Apply the matching rule.

TEXT KIND:
- "answer": the TEXT is the assistant's full answer. HIT if the answer asserts the claim (paraphrase and rewording are fine); MISS if the answer does not state it, or states something that contradicts it.
- "chunks": the TEXT is a SET of retrieved transcript chunks, each labeled with its video id and publish date. HIT if the chunks TAKEN TOGETHER support the claim - combine evidence across chunks, so a claim may be supported by two chunks jointly even if no single chunk suffices. MISS if the set does not support it. Judge only what the chunks say (plus their date labels); never use outside knowledge.

CLAIM TYPE:
- "fact" or "stance": a single assertion (a fact, a figure, a position the creator held). Support means the same substance; allow paraphrase and the claim's own hedges ("about", "nearly"). A figure matches if it is the same number.
- "shift": the claim asserts the creator's view CHANGED across a period (a trajectory). HIT only if the TEXT conveys a CHANGE over time with a compatible direction and timing - not merely descriptions of separate periods sitting side by side. If the TEXT describes each period but never conveys that the view moved, a shift claim is a MISS.
- "no_change": the claim asserts the creator's view stayed CONSISTENT across a period (no evolution). This is the shift rule inverted. HIT only if the TEXT conveys that the view stayed the same across the period. If the TEXT describes an evolution, or invents a change, it is a MISS - even though it is on the same topic.

TIME WINDOWS (dated claims):
- A time window in the claim (e.g. "in early 2026", "by mid-2025") is PART of the claim.
- For "answer" text: a date in the answer inside the window is HIT; a vaguer but compatible timeframe is HIT; a date that contradicts the window is MISS.
- For "chunks" text: the window can be satisfied by a chunk's PUBLISH DATE (from its label), not only by the transcript words - a chunk published in early 2026 that states the stance supports a claim dated "early 2026" even if the transcript never says the date. Use the metadata dates.

Be strict about substance and lenient about wording. Do not reward a text that is merely on the same topic; require that it actually supports the specific claim."""

JUDGE_PROMPT_SHA = hashlib.sha1(SYSTEM.encode()).hexdigest()[:8]


def build_user(claim: str, text: str, *, claim_type: str, text_kind: str) -> str:
    return (f"TEXT KIND: {text_kind}\nCLAIM TYPE: {claim_type}\n\n"
            f"CLAIM:\n{claim}\n\nTEXT:\n{text}\n\n"
            "Verdict: is the CLAIM supported by the TEXT? Set hit=true for HIT or "
            "hit=false for MISS, with a one-sentence reason.")


async def judge(claim: str, *, text: str, claim_type: str, text_kind: str) -> Verdict:
    """Judge one (claim, text) pair. claim_type in {fact, stance, shift, no_change};
    text_kind in {answer, chunks}. The system prompt is prompt-cached."""
    user = build_user(claim, text, claim_type=claim_type, text_kind=text_kind)
    return await asyncio.wait_for(
        call_structured(SYSTEM, user, Verdict, model=MODEL, max_tokens=MAX_TOKENS,
                        thinking={"type": "adaptive"}, cache_system=True),
        timeout=CALL_TIMEOUT,
    )


# ---- chunk-set materialization (dirs 2 and 3) ------------------------------

def fetch_chunks(chunk_ids: list[str]) -> dict[str, dict]:
    """chunk_id -> {video_id, published_at (date|None), text} for the given ids."""
    if not chunk_ids:
        return {}
    sql = ("SELECT c.chunk_id, c.video_id, c.text, v.published_at "
           "FROM video_chunks c JOIN videos v USING (video_id) "
           "WHERE c.chunk_id = ANY(%s)")
    with transaction() as conn:
        rows = conn.execute(sql, (list(chunk_ids),)).fetchall()
    return {r["chunk_id"]: dict(r) for r in rows}


def format_chunk_set(chunk_ids: list[str], chunks: dict[str, dict] | None = None) -> str:
    """Render a chunk set as labeled blocks '[video_id | published YYYY-MM-DD] text',
    ordered by chunk_id. Fetches from the DB if a chunk map is not supplied."""
    chunks = chunks if chunks is not None else fetch_chunks(chunk_ids)
    blocks = []
    for cid in sorted(chunk_ids):
        ch = chunks.get(cid)
        if not ch:
            continue
        pub = ch["published_at"]
        date = pub.date().isoformat() if pub else "unknown"
        blocks.append(f"[{ch['video_id']} | published {date}] {ch['text']}")
    return "\n\n".join(blocks)


# ---- self-test (mechanics + special rules; pre-C3 gate) --------------------

_SELFTEST = [
    # (name, claim, text, claim_type, text_kind, expected_hit)
    ("recall_stance_hit",
     "In early 2025 the creator was optimistic about agentic AI's real-world impact.",
     "In February 2025 he described agentic AI as showing breakthroughs and real near-term promise.",
     "stance", "answer", True),
    ("recall_stance_miss",
     "The creator said RAG is obsolete.",
     "He discussed agentic AI benchmarks and reasoning faithfulness across 2025.",
     "stance", "answer", False),
    ("shift_hit",
     "He moved from optimism in early 2025 to concluding by early 2026 that the agentic revolution had stalled.",
     "In early 2025 he was optimistic about agents, but by January 2026 he said the anticipated agentic revolution had stalled.",
     "shift", "answer", True),
    ("shift_miss_describes_separately",
     "He moved from optimism in early 2025 to concluding by early 2026 that the agentic revolution had stalled.",
     "In early 2025 he was optimistic about agents. Separately, agents are useful for coding tasks.",
     "shift", "answer", False),
    ("no_change_hit",
     "Across the period his favorite architecture stayed consistent.",
     "Throughout 2025 and into 2026 he consistently favored the same architecture, without changing his pick.",
     "no_change", "answer", True),
    ("no_change_miss_invents_evolution",
     "Across the period his favorite architecture stayed consistent.",
     "He started favoring transformers, then shifted to state-space models, then moved again by 2026.",
     "no_change", "answer", False),
    ("ground_setwise_hit",
     "Deep-DxSearch outperforms DeepSeek R1 by nearly 20 points on common disease diagnosis.",
     "[vidA | published 2025-09-01] The 14B Deep-DxSearch system was compared against DeepSeek R1.\n\n"
     "[vidA | published 2025-09-01] On common disease diagnosis it beat R1 by close to twenty percentage points.",
     "fact", "chunks", True),
    ("ground_dated_via_metadata_hit",
     "In early 2026 the creator said the agentic revolution had stalled.",
     "[vidX | published 2026-01-15] The anticipated revolution of agentic AI has stalled, developers distrust the code.",
     "stance", "chunks", True),
    ("ground_miss_offtopic",
     "Gemini 3 Deep Think scored 45% on ARC-AGI-2.",
     "[vidY | published 2025-11-01] The video discusses multi-agent consensus time scaling with population size.",
     "fact", "chunks", False),
]


async def _selftest() -> None:
    print(f"judge self-test (prompt_sha {JUDGE_PROMPT_SHA}, model {MODEL})\n", flush=True)
    sem = asyncio.Semaphore(4)

    async def run(case):
        name, claim, text, ct, tk, expected = case
        async with sem:
            v = await judge(claim, text=text, claim_type=ct, text_kind=tk)
        ok = (v.hit == expected)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got hit={v.hit} expected={expected} "
              f":: {v.reason}", flush=True)
        return ok

    results = await asyncio.gather(*(run(c) for c in _SELFTEST))
    print(f"\n{sum(results)}/{len(results)} self-test cases matched expectation.", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Alignment judge (C2).")
    ap.add_argument("--selftest", action="store_true", help="run crafted pairs and report")
    args = ap.parse_args()
    if args.selftest:
        asyncio.run(_selftest())
    else:
        ap.error("nothing to do; pass --selftest (scoring drives judge() from eval.score_runs at D)")


if __name__ == "__main__":
    main()
