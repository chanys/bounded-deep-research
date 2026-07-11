"""Stage 2.1: generate candidate evaluation queries, stratified by topic x tier.

Samples generation "cells" against the Stage 1 inventory (one cell = one small
API call over a bounded input), then asks Sonnet 5 for a few queries per cell.
Three tiers:
  - factual:      one source video; specific fact/number questions anchored to it.
  - comparative:  two videos from the same cluster; contrast questions.
  - longitudinal: a time-ordered slice of one cluster; how-did-it-evolve questions.

No DB needed here (generation reads summaries + inventory only); grounding comes
next. Over-generates ~3-4x the keep target; select_queries prunes downstream.

Usage:
  uv run python -m eval.generate_queries --limit 2            # smoke (2 cells/tier)
  uv run python -m eval.generate_queries                      # full run
  uv run python -m eval.generate_queries --tiers factual      # one tier
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured
from core.provenance import PROVENANCE
from eval import corpus_io as cio

SUMMARIES_DEFAULT = Path("eval/artifacts/summaries_code4AI.jsonl")
INVENTORY_DEFAULT = Path("eval/artifacts/inventory_code4AI.json")
OUT_DIR = Path("eval/artifacts")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 3000
CALL_TIMEOUT = 90  # seconds; bound a call (incl. SDK rate-limit backoff) so the batch never appears hung
OTHER = "other"

# Default cell budgets (tunable). Factual/comparative land ~cells * K candidates;
# longitudinal is one slice per qualifying cluster (K each).
DEFAULTS = {"factual_cells": 50, "comparative_cells": 50, "k": 4, "longitudinal_k": 6}
LONG_MONTHS_MIN = 8   # a cluster qualifies for longitudinal if it spans >= this many months
LONG_SLICE_MAX = 6    # videos per time-ordered slice


# ---- output schema ---------------------------------------------------------

class GenQuery(BaseModel):
    query: str
    answer_video_ids: list[str]  # subset of the cell's videos that answer it


class GenBatch(BaseModel):
    queries: list[GenQuery]


# ---- prompts (frozen; tied to the run by the git-SHA fingerprint) ----------

_COMMON = """\
You are helping build an evaluation for a research assistant that answers questions over one AI/ML YouTube creator's video library. Your job is to write the QUESTIONS a user would pose to that assistant.

Model the user as a curious AI practitioner (a researcher, engineer, or enthusiast) who has a general sense of what this channel covers (AI/ML research, model capabilities, techniques, and debates) but has NOT watched any specific video. They are asking to find out whether the library answers something they genuinely wonder about.

Hard rules for every question:
- Standalone: it must make full sense to someone who has watched nothing. NEVER refer to the source: no "this video", "these videos", "the creator", "both papers", "these studies", "each analysis", "as discussed", "across these videos". A reader must not be able to tell the question was written from any particular video.
- Ask about the subject matter directly, never about the video itself (no "what does the video say").
- Substance over trivia: ask about ideas, findings, mechanisms, tradeoffs, and assessments. Do NOT ask about incidental specifics a viewer would not retain or a searcher would not know: exact dates, publication months, author or institution names, precise hyperparameters, or one-off numbers pulled from a slide.
- Analysis, not lookup: prefer questions seeking an explanation, comparison, mechanism, or informed judgment of the kind this channel provides. Avoid bare factoids a general web search answers (user counts, market sizes, release dates, install commands).
- Name a model, method, or paper only if a working practitioner would recognize it unprompted (e.g. GPT-5, GRPO, chain-of-thought, o1). Otherwise describe it generically; never cite an obscure paper or system by name as if the reader already knows it.
- Natural phrasing: write it the way a person would actually type it. Paraphrase; do not copy transcript wording.

The question must be answerable from the material you are given (a later step verifies this), but you write it from the asker's curiosity, not by reverse-engineering the material into a quiz."""

FACTUAL_SYSTEM = _COMMON + """

You are given ONE video's summary and key points, which tell you what it can answer. Write questions a practitioner would genuinely ask that this material answers, each targeting a substantive finding, result, mechanism, or claim, not incidental trivia.

Transformations to make:
BAD (transcript quiz / over-specific): "What token size and overlap does Deep GraphRAG use for its sliding-window chunking?"
GOOD (substantive): "How does chunking strategy affect the retrieval quality of a GraphRAG system?"
BAD (bare factoid / metadata): "What research institutions published the March 2025 paper on function-preserving network growing?"
GOOD (substantive): "How can you grow a neural network's size during fine-tuning without causing catastrophic forgetting?" """

COMPARATIVE_SYSTEM = _COMMON + """

You are given TWO videos on the same topic. Do NOT frame the question as "these two videos" or "both papers". Instead ask an approach-space question about the topic itself ("what are the different approaches to X and how do they compare?", "does A or B work better for X, and why?"), where A and B are the actual methods or models, named only if a practitioner would recognize them, else described generically. Write a question only where a genuine, substantive contrast exists across the two; if they do not really contrast, write fewer or none.

Transformations to make:
BAD (insider): "Both these papers claim to beat best-of-N sampling, what mechanism does each use?"
GOOD (approach-space): "What are some approaches that outperform best-of-N sampling for LLM reasoning, and how do their mechanisms differ?"
BAD (insider): "How do the two videos differ on whether adding more agents helps?"
GOOD (natural): "Does adding more communicating agents actually improve a multi-agent system's performance, or can it hurt?" """

LONGITUDINAL_SYSTEM = _COMMON + """

You are given a TIME-ORDERED sequence of videos (oldest first) on one topic. Ask how the topic itself has developed over time ("how have approaches to X evolved over the past year?", "how has thinking on X shifted?"), NOT about "the creator's" views, coverage, or confidence. The question should require synthesizing a trajectory across the period and must stand alone without referencing any video or the channel.

Transformations to make:
BAD (insider): "How has the creator's confidence in models' reasoning shifted from the early Gemini vs DeepSeek test to the later Gemini 3.1 test?"
GOOD (topic trajectory): "How has the reasoning ability of frontier models on hard logic puzzles changed over the past year?"
BAD (insider): "How did the creator's proposed fixes for reasoning failures evolve across these videos?"
GOOD (natural): "How have proposed fixes for LLM reasoning failures evolved recently, from scaling test-time compute to other approaches?" """


def _video_block(vid: str, summ: dict, *, with_key_points: bool, month: str | None = None) -> str:
    head = f"[{month} | {vid}]" if month else f"[{vid}]"
    lines = [f"{head} {summ.get('title', '')}", f"summary: {summ.get('summary', '')}"]
    if with_key_points and summ.get("key_points"):
        lines.append("key_points:")
        lines += [f"- {kp}" for kp in summ["key_points"]]
    return "\n".join(lines)


# ---- sampling --------------------------------------------------------------

def _cluster_members(inventory: dict) -> dict[str, list[dict]]:
    """cluster_id -> list of that cluster's inventory video rows."""
    members: dict[str, list[dict]] = {}
    for v in inventory["videos"]:
        members.setdefault(v["cluster_id"], []).append(v)
    return members


def _richness(v: dict, summaries: dict[str, dict]) -> tuple[int, int]:
    """Rank key: more key_points, then more chunks = more material to ask about."""
    s = summaries.get(v["video_id"], {})
    return (len(s.get("key_points", [])), v.get("chunk_count") or 0)


def _allocate(sizes: dict[str, int], total: int, cap: dict[str, int]) -> dict[str, int]:
    """Proportional allocation of `total` cells across clusters by size, floor 1,
    capped per cluster. Largest-remainder rounding."""
    keys = [k for k in sizes if cap.get(k, 0) >= 1]
    if not keys or total <= 0:
        return {}
    # floor of 1 each, then distribute the remainder proportional to size
    alloc = {k: 1 for k in keys}
    remaining = total - len(alloc)
    if remaining > 0:
        denom = sum(sizes[k] for k in keys) or 1
        frac = {k: remaining * sizes[k] / denom for k in keys}
        base = {k: int(frac[k]) for k in keys}
        for k in keys:
            alloc[k] += base[k]
        leftover = remaining - sum(base.values())
        for k in sorted(keys, key=lambda k: frac[k] - base[k], reverse=True)[:leftover]:
            alloc[k] += 1
    # cap and drop excess
    return {k: min(alloc[k], cap[k]) for k in keys}


def factual_cells(inventory, summaries, n_cells, limit) -> list[dict]:
    members = _cluster_members(inventory)
    sizes = {c: len(vs) for c, vs in members.items() if c != OTHER}
    alloc = _allocate(sizes, n_cells, cap=sizes)
    cells = []
    for c, n in alloc.items():
        ranked = sorted(members[c], key=lambda v: _richness(v, summaries), reverse=True)
        for v in ranked[:n]:
            cells.append({"cluster_id": c, "video_ids": [v["video_id"]]})
    return cells[:limit] if limit else cells


def comparative_cells(inventory, summaries, n_cells, limit) -> list[dict]:
    members = _cluster_members(inventory)
    sizes = {c: len(vs) for c, vs in members.items() if c != OTHER and len(vs) >= 2}
    cap = {c: sizes[c] // 2 for c in sizes}
    alloc = _allocate(sizes, n_cells, cap=cap)
    cells = []
    for c, n in alloc.items():
        ranked = sorted(members[c], key=lambda v: _richness(v, summaries), reverse=True)
        for i in range(n):
            a, b = ranked[2 * i], ranked[2 * i + 1]
            cells.append({"cluster_id": c, "video_ids": [a["video_id"], b["video_id"]]})
    return cells[:limit] if limit else cells


def longitudinal_cells(inventory, summaries, limit) -> list[dict]:
    matrix = inventory["time_axis"]["matrix"]
    members = _cluster_members(inventory)
    cells = []
    for c in sorted(members):
        if c == OTHER:
            continue
        n_months = len(matrix.get(c, {}))
        if n_months < LONG_MONTHS_MIN:
            continue
        ordered = sorted(
            (v for v in members[c] if v.get("published_at")),
            key=lambda v: v["published_at"],
        )
        if len(ordered) < 3:
            continue
        # evenly sample up to LONG_SLICE_MAX videos across the time span
        if len(ordered) <= LONG_SLICE_MAX:
            slice_vids = ordered
        else:
            step = (len(ordered) - 1) / (LONG_SLICE_MAX - 1)
            idx = sorted({round(i * step) for i in range(LONG_SLICE_MAX)})
            slice_vids = [ordered[i] for i in idx]
        cells.append({"cluster_id": c, "video_ids": [v["video_id"] for v in slice_vids]})
    return cells[:limit] if limit else cells


# ---- generation ------------------------------------------------------------

def _build_user(tier: str, cell: dict, summaries: dict, inv_by_id: dict, k: int) -> str:
    vids = cell["video_ids"]
    if tier == "factual":
        block = _video_block(vids[0], summaries[vids[0]], with_key_points=True)
        return f"{block}\n\nWrite {k} such questions. For each, list the video ids that answer it."
    if tier == "comparative":
        blocks = "\n\n".join(_video_block(v, summaries[v], with_key_points=True) for v in vids)
        return (f"{blocks}\n\nWrite up to {k} contrast questions. For each, list which of the "
                "two video ids answer it (usually both).")
    # longitudinal: summaries only, time-ordered, with month labels
    blocks = "\n\n".join(
        _video_block(v, summaries[v], with_key_points=False, month=inv_by_id[v].get("month"))
        for v in vids
    )
    return (f"Videos in time order (oldest first):\n\n{blocks}\n\nWrite {k} evolution "
            "questions. For each, list which video ids answer it.")


SYSTEMS = {"factual": FACTUAL_SYSTEM, "comparative": COMPARATIVE_SYSTEM,
           "longitudinal": LONGITUDINAL_SYSTEM}


async def generate_cell(tier, cell, summaries, inv_by_id, k, sem) -> list[dict]:
    user = _build_user(tier, cell, summaries, inv_by_id, k)
    provided = set(cell["video_ids"])
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(
                    SYSTEMS[tier], user, GenBatch, model=MODEL, max_tokens=MAX_TOKENS,
                    thinking={"type": "adaptive"},
                ),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001 - one bad/slow cell must not stall or kill the batch
            print(f"  fail {tier} {cell['cluster_id']} {cell['video_ids']}: {type(e).__name__}: {e}")
            return []
    rows = []
    for q in out.queries:
        answers = [v for v in q.answer_video_ids if v in provided]
        if not q.query.strip() or not answers:
            continue  # a query that names no provided video is not grounded to this cell
        rows.append({
            "tier": tier,
            "cluster_id": cell["cluster_id"],
            "cell_video_ids": cell["video_ids"],
            "answer_video_ids": answers,
            "query": q.query.strip(),
            "model": MODEL,
        })
    return rows


async def run_tier(tier, cells, summaries, inv_by_id, k, concurrency) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)
    tasks = [generate_cell(tier, c, summaries, inv_by_id, k, sem) for c in cells]
    out: list[dict] = []
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"gen {tier}"):
        out.extend(await coro)
    prefix = tier[0]
    for i, r in enumerate(out, start=1):
        r["candidate_id"] = f"{prefix}{i:04d}"
    return out


def write_candidates(tier: str, rows: list[dict]) -> Path:
    path = OUT_DIR / f"query_candidates_{tier}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"_meta": {"tier": tier, "model": MODEL, "thinking": "adaptive",
                      "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
                      "count": len(rows)}}
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return path


async def amain(args: argparse.Namespace) -> None:
    summaries = cio.read_summaries(args.summaries)
    inventory = cio.read_inventory(args.inventory)
    inv_by_id = {v["video_id"]: v for v in inventory["videos"]}
    if not summaries or not inventory.get("videos"):
        raise SystemExit("missing summaries or inventory; run Stage 1 first")

    tiers = args.tiers or ["factual", "comparative", "longitudinal"]
    builders = {
        "factual": lambda: factual_cells(inventory, summaries, args.factual_cells, args.limit),
        "comparative": lambda: comparative_cells(inventory, summaries, args.comparative_cells, args.limit),
        "longitudinal": lambda: longitudinal_cells(inventory, summaries, args.limit),
    }
    for tier in tiers:
        cells = builders[tier]()
        k = args.longitudinal_k if tier == "longitudinal" else args.k
        print(f"{tier}: {len(cells)} cells, k={k}")
        rows = await run_tier(tier, cells, summaries, inv_by_id, k, args.concurrency)
        path = write_candidates(tier, rows)
        print(f"  {len(rows)} candidates -> {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summaries", type=Path, default=SUMMARIES_DEFAULT)
    ap.add_argument("--inventory", type=Path, default=INVENTORY_DEFAULT)
    ap.add_argument("--tiers", nargs="*", choices=["factual", "comparative", "longitudinal"])
    ap.add_argument("--factual-cells", type=int, default=DEFAULTS["factual_cells"])
    ap.add_argument("--comparative-cells", type=int, default=DEFAULTS["comparative_cells"])
    ap.add_argument("--k", type=int, default=DEFAULTS["k"])
    ap.add_argument("--longitudinal-k", type=int, default=DEFAULTS["longitudinal_k"])
    ap.add_argument("--limit", type=int, default=None, help="cap cells per tier (smoke)")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
