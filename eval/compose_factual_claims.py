"""Task 4: factual query candidates composed from single Stage B claims.

A temporally stratified two-stage sample, frozen before any system runs (selection
blind to system performance): the 475 videos are cut into 5 equal-count strata by
publish date, 10 videos are sampled per stratum, one substantive claim is selected
per sampled video by a small LLM judgment, and one natural practitioner question is
composed per claim behind a lexical firewall (the composer sees the claim text and
its tags, never the transcript, summary, or key points).

Randomness is seeded and keyed by stable ids, so the same --seed reproduces the same
sample regardless of async completion order. Output is the candidate file the
existing grounding script consumes (its {**cand} spread carries the extra fields
through to query_grounded_*); wiring ground_queries to read this file by name is
deferred to Task 7 and should be a `--candidates <path>` option.

Usage:
  uv run python -m eval.compose_factual_claims --per-stratum 2 --render eval/artifacts/factual_claimslice_sample.md   # gate
  uv run python -m eval.compose_factual_claims                                                                        # full (50)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.provenance import PROVENANCE

CLAIMS_DEFAULT = Path("eval/artifacts/claims_code4AI.jsonl")
OUT_DEFAULT = Path("eval/artifacts/query_candidates_factual_claimslice.jsonl")
MODEL = "claude-sonnet-5"
SELECT_MAX_TOKENS = 400
COMPOSE_MAX_TOKENS = 800
CALL_TIMEOUT = 90
N_STRATA = 5


# ---- prompts (frozen; tied to the run by the git-SHA fingerprint) ----------

SELECT_SYSTEM = """\
You select evaluation-worthy claims from one video's claim inventory. Return the ids of the 2 claims a practitioner who never saw the video would most plausibly ask a substantive question about: concrete results, findings, comparisons, technical explanations, or creator judgments with real content. Do not select video setup or meta claims, moment-by-moment demo narration, or claims too thin to yield a non-trivial question. Do not select claims with unresolved references ("the paper", "the study", "the model") that only sibling claims resolve - the downstream composer sees the claim alone and cannot recover the referent; prefer a claim that names its subject. If fewer than 2 qualify, return fewer. Return ONLY claim ids."""

COMPOSE_SYSTEM = """\
You write evaluation questions for a research assistant that answers questions over one AI/ML YouTube creator's video library. You are given ONE standalone claim (with topic and entity tags), and possibly a list of questions already written for other claims. Write ONE natural question that the claim answers.

Rules:
- The question must be fully answerable by the claim alone.
- Anchor it: include at least one identifying specific from the claim (a named system, org, paper, benchmark, technique, or figure) so the question points at this content and no other across hundreds of videos. If the claim offers no such anchor, return skip.
- Never include the part of the claim the question ASKS FOR (the finding, verdict, reason, or outcome). DO include the claim's factual frame: for a why/how question, the phenomenon being explained belongs in the question.
- Never presuppose context the asker could not have: no definite references to unnamed things ("the study", "the given constraints", "its reported performance level"). Name it or describe it self-containedly. If the CLAIM itself contains such an unresolved reference ("the paper proves...") and you cannot name the referent from the claim alone, return skip - do not inherit the reference into the question.
- Write it as a practitioner who has NOT seen any video would type it: standalone, no "this video" / "the creator" / "as mentioned" phrasing.
- Public entities (model names, papers, benchmarks) may be named. Creator-specific constructs must be described naturally instead of assumed known.
- Vary opening and structure; avoid resembling the previously written questions, if any are provided.
- If the claim cannot yield a natural standalone question, return skip with a short reason.

Example (good): "How does Intrinsic Reward Policy Optimization address the noisy-TV problem, where an agent gets fooled by high intrinsic reward from meaningless random observations?" - named method, self-contained problem description, asks for the mechanism without revealing it.
Example (bad): "Why did the model top out at its reported performance level instead of scoring even higher?" - no anchor, presupposes unshared context, nothing for retrieval to bite on. Corrected: "ReasonFlux reportedly reached about 91% on math benchmarks - why didn't its template-based approach score higher?" (the figure is frame; the reason is the answer.)

Return structured data only."""


class Selection(BaseModel):
    claim_ids: list[str]


class Composed(BaseModel):
    action: Literal["write", "skip"]
    query: str | None = None
    reason: str | None = None


# ---- inputs ----------------------------------------------------------------

def load_eligible(claims_path: Path) -> list[dict]:
    """Videos with >=1 high-confidence claim and a publish date, each with its
    high-confidence claims and a claim_id->claim lookup."""
    out = []
    for ln in claims_path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        if "_meta" in rec:
            continue
        hc = [c for c in rec["claims"] if c["confidence"] == "high"]
        if hc and rec.get("published_at"):
            out.append({"video_id": rec["video_id"], "published_at": rec["published_at"],
                        "claims": hc, "by_id": {c["claim_id"]: c for c in hc}})
    return out


def stratify(eligible: list[dict], n_strata: int) -> list[list[dict]]:
    """Cut date-ordered videos into n equal-count strata (quantile boundaries)."""
    ordered = sorted(eligible, key=lambda v: v["published_at"])
    n = len(ordered)
    return [ordered[k * n // n_strata:(k + 1) * n // n_strata] for k in range(n_strata)]


def stratum_label(videos: list[dict]) -> str:
    """Compact YYYY-MM..YYYY-MM date range; full boundaries also go in _meta."""
    return f"{videos[0]['published_at'][:7]}..{videos[-1]['published_at'][:7]}"


# ---- LLM steps -------------------------------------------------------------

def _resolve_id(cid: str, video: dict) -> str | None:
    """Map a returned id to a real claim id. The model sometimes drops the
    `videoid#` prefix and returns a bare suffix (`c021`); accept that form too,
    since suffixes are unique within a video."""
    if cid in video["by_id"]:
        return cid
    full = f"{video['video_id']}#{cid.lstrip('#')}"
    return full if full in video["by_id"] else None


async def select_claims(video: dict) -> list[str]:
    """Return up to 2 valid, question-worthy claim ids for the video (order preserved)."""
    listing = "\n".join(f"[{c['claim_id']}] {c['text']}" for c in video["claims"])
    user = (f"Video claims (high-confidence only):\n{listing}\n\n"
            "Return the ids of the up to 2 most question-worthy claims.")
    out = await asyncio.wait_for(
        call_structured(SELECT_SYSTEM, user, Selection, model=MODEL,
                        max_tokens=SELECT_MAX_TOKENS, thinking={"type": "disabled"}),
        timeout=CALL_TIMEOUT,
    )
    seen, valid = set(), []
    for cid in out.claim_ids:
        rid = _resolve_id(cid, video)
        if rid and rid not in seen:
            seen.add(rid)
            valid.append(rid)
    return valid[:2]


async def compose(claim: dict, priors: list[str]) -> Composed:
    """Write one standalone question for the claim (firewall: claim + tags + prior
    questions only), or skip."""
    lines = [f"Claim: {claim['text']}",
             f"Topics: {', '.join(claim['topics'])}",
             f"Entities: {', '.join(claim['entities'])}"]
    if priors:
        lines.append("\nAlready written for other claims (do not resemble these):")
        lines += [f"- {q}" for q in priors]
    lines.append("\nWrite one natural standalone question this claim answers, or skip with a reason.")
    return await asyncio.wait_for(
        call_structured(COMPOSE_SYSTEM, "\n".join(lines), Composed, model=MODEL,
                        max_tokens=COMPOSE_MAX_TOKENS, thinking={"type": "adaptive"}),
        timeout=CALL_TIMEOUT,
    )


def _pick(video_id: str, ids: list[str], seed: int) -> tuple[str, str | None]:
    """Seeded 1-of-2 pick -> (primary, fallback|None), keyed by video so it is
    independent of async order."""
    if len(ids) == 1:
        return ids[0], None
    i = random.Random(f"{seed}:pick:{video_id}").randrange(2)
    return ids[i], ids[1 - i]


# ---- per-stratum driver ----------------------------------------------------

async def process_stratum(idx: int, videos: list[dict], target: int, seed: int) -> dict:
    """Walk the seeded-shuffled stratum queue until `target` candidates are composed.
    Videos at queue position < target are the initial sample; beyond are replacements
    drawn on a zero-keeper selection or a fully-skipped composition."""
    label = stratum_label(videos)
    queue = list(videos)
    random.Random(f"{seed}:s{idx}").shuffle(queue)

    priors: list[str] = []
    candidates: list[dict] = []
    selections: list[dict] = []
    n_skip = 0
    pos = 0
    while len(candidates) < target and pos < len(queue):
        video = queue[pos]
        role = "initial" if pos < target else "replacement"
        pos += 1
        try:
            selected = await select_claims(video)
        except Exception as e:  # noqa: BLE001 - one bad call must not kill the stratum
            selections.append({"video_id": video["video_id"], "role": role, "outcome": f"select_error:{type(e).__name__}"})
            continue
        if not selected:
            selections.append({"video_id": video["video_id"], "role": role, "selected": [], "outcome": "no_keepers"})
            continue
        primary, fallback = _pick(video["video_id"], selected, seed)
        order = [primary] + ([fallback] if fallback else [])
        composed = used = None
        skip_reasons = []
        for cid in order:
            try:
                res = await compose(video["by_id"][cid], priors)
            except Exception as e:  # noqa: BLE001
                skip_reasons.append({"claim_id": cid, "reason": f"compose_error:{type(e).__name__}"})
                continue
            if res.action == "write" and res.query and res.query.strip():
                composed, used = res.query.strip(), cid
                break
            skip_reasons.append({"claim_id": cid, "reason": res.reason or "skip"})
            n_skip += 1
        outcome = "composed" if composed else "all_skipped"
        selections.append({"video_id": video["video_id"], "role": role, "selected": selected,
                           "picked": order, "outcome": outcome, "skips": skip_reasons})
        if not composed:
            continue
        priors.append(composed)
        claim = video["by_id"][used]
        candidates.append({
            "tier": "factual", "slice": "claim_derived", "query": composed,
            "answer_video_ids": [video["video_id"]], "source_claim_ids": [used],
            "stratum": label, "gold_draft": [claim["text"]],
        })

    sampled = [v["video_id"] for v in queue[:target]]
    replacements = [v["video_id"] for v in queue[target:pos]]
    meta = {"index": idx, "label": label,
            "date_range": [videos[0]["published_at"], videos[-1]["published_at"]],
            "n_videos": len(videos), "sampled_video_ids": sampled,
            "replacement_video_ids": replacements, "selections": selections,
            "composer_skips": n_skip, "composed": len(candidates)}
    return {"candidates": candidates, "meta": meta}


# ---- io --------------------------------------------------------------------

def render_md(strata_meta: list[dict], by_video: dict, cand_by_video: dict) -> str:
    """Selection-quality reader: per composed candidate, the query, the chosen claim,
    and the video's full high-confidence claim list (what was passed over)."""
    out: list[str] = []
    for sm in strata_meta:
        out.append(f"# Stratum {sm['index']} ({sm['label']}) - {sm['composed']} composed\n")
        for sel in sm["selections"]:
            if sel.get("outcome") != "composed":
                out.append(f"- ({sel['outcome']}) {sel['video_id']}")
                continue
            vid = sel["video_id"]
            cand = cand_by_video[vid]
            chosen = cand["source_claim_ids"][0]
            chosen_chunks = ", ".join(by_video[vid]["by_id"][chosen]["chunk_ids"])
            out.append(f"## {cand['candidate_id']}  [{vid}]")
            out.append(f"Q: {cand['query']}")
            out.append(f"chosen: [{chosen}]  chunks: {chosen_chunks}")
            out.append("full high-confidence claims (chosen marked >>):")
            for c in by_video[vid]["claims"]:
                mark = ">>" if c["claim_id"] == chosen else "  "
                chunks = ", ".join(c["chunk_ids"])
                out.append(f"  {mark} [{c['claim_id']}] ({chunks}) {c['text']}")
            out.append("")
    return "\n".join(out)


async def amain(args: argparse.Namespace) -> None:
    eligible = load_eligible(args.claims)
    by_video = {v["video_id"]: v for v in eligible}
    strata = stratify(eligible, N_STRATA)
    print(f"eligible={len(eligible)} strata={N_STRATA} per_stratum={args.per_stratum} seed={args.seed}")

    results = await asyncio.gather(*(
        process_stratum(k, strata[k], args.per_stratum, args.seed) for k in range(N_STRATA)
    ))

    # number candidates deterministically by (stratum, within-stratum order)
    candidates, strata_meta = [], []
    for r in results:
        strata_meta.append(r["meta"])
        candidates.extend(r["candidates"])
    for i, c in enumerate(candidates, 1):
        c["candidate_id"] = f"fc-{i:04d}"
    cand_by_video = {c["answer_video_ids"][0]: c for c in candidates}

    total_skip = sum(m["composer_skips"] for m in strata_meta)
    meta = {"_meta": {
        "tier": "factual", "slice": "claim_derived", "model": MODEL, "seed": args.seed,
        "per_stratum": args.per_stratum, "n_strata": N_STRATA,
        "selection_thinking": "disabled", "composition_thinking": "adaptive",
        "counts": {"candidates": len(candidates), "composer_skips": total_skip},
        "strata": strata_meta,
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    per = {m["index"]: m["composed"] for m in strata_meta}
    print(f"composed {len(candidates)} candidates (per-stratum {per}, skips {total_skip}) -> {args.out}")

    if args.render:
        args.render.write_text(render_md(strata_meta, by_video, cand_by_video), encoding="utf-8")
        print(f"  rendered -> {args.render}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", type=Path, default=CLAIMS_DEFAULT)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260713)
    ap.add_argument("--per-stratum", type=int, default=10, help="target candidates per stratum")
    ap.add_argument("--render", type=Path, default=None, help="also write a selection-quality markdown reader")
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
