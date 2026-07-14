"""Task 5: comparative query candidates composed from claim pairs (claim slice).

Bottom-up comparative construction: two high-confidence claims from DIFFERENT videos
that name DIFFERENT subjects but share a comparison axis (a normalized TOPIC tag) are
composed into one question that needs both sides. The comparison exists in no chunk or
summary, so the query has no single parent to echo, and each side is already
chunk-anchored.

The axis is a topic (the thing you compare ON: a benchmark, task, or theme); the
compared subjects are the differing named entities in each claim (models, methods,
frameworks - e.g. LightRAG vs GraphRAG on the topic axis "knowledge graphs"). Entity
tags are NOT used as axes: an entity axis pairs on incidental shared tokens (model
sizes like "32b", hardware like "a100 gpu") that make meaningless comparisons.

Pairing is deterministic and pre-LLM: conservative tag normalization (preserve every
version/size token; a missed merge beats an over-merge), one narrowed alias folding the
creator's fragmented "elevator" causal-reasoning test into a single family, a
meta-organizational topic stop-list, and a non-subject entity filter (sizes, hardware,
orgs) so the compared subjects are real. Diversity caps (per family, per video) stop the
elevator family from dominating; they are enforced as a pre-call gate. Each surviving
pair gets one LLM call that checks comparability and, if it passes, composes the question
with a rolling "do not resemble these" variety list (consistent with the factual slice).

Scope bound (declared, in _meta and SLICES.md): cross-entity comparisons only.
Same-entity-over-time is Task 6; same-entity-different-benchmark can be a demo query.

No DB, no grounding (Task 7).

Usage:
  uv run python -m eval.compose_comparative_claims --only-families "topic:elevator/causal-reasoning-test" "topic:knowledge graphs" --render eval/artifacts/_cmp_smoke.md --out eval/artifacts/_cmp_smoke.jsonl
  uv run python -m eval.compose_comparative_claims                # full run
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import datetime as dt
import json
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from core.claude_llm import call_structured
from core.provenance import PROVENANCE

CLAIMS_DEFAULT = Path("eval/artifacts/claims_code4AI.jsonl")
OUT_DEFAULT = Path("eval/artifacts/query_candidates_comparative_claimslice.jsonl")
MODEL = "claude-sonnet-5"
MAX_TOKENS = 2500   # adaptive thinking + reason + a two-claim comparison question
CALL_TIMEOUT = 90
VARIETY_WINDOW = 40   # cap the rolling "don't resemble these" list passed to the model

ROLE_WORDS = {"system", "systems", "model", "models", "framework"}
# Meta/theme labels, not comparison axes: two claims sharing one are about different
# aspects, so they never make a clean comparison. Blocked before pairing.
STOP_TOPICS = {
    # meta-organizational
    "creator opinion", "creator assessment", "creator commentary", "methodology", "limitations",
    "paper authorship", "authorship", "paper publication", "publication date", "publication",
    "institutions",
    # generic evaluation/theme labels
    "benchmark results", "benchmark comparison", "benchmarks", "benchmark performance",
    "model comparison", "performance comparison", "comparison", "results", "experimental results",
    "experimental setup", "models tested", "model selection", "model performance",
    "model architecture", "research paper", "open source", "testing methodology",
    "training data", "reasoning",
}
STOP_TOPIC_PREFIXES = ("paper ", "publication ")
# Broad method/field families deliberately KEPT (not stopped): they can yield real
# method-vs-method comparisons (GRPO vs DPO under "reinforcement learning", two
# multi-agent frameworks, named deep-research systems), so the LLM comparability check
# is the backstop and a higher-than-band reject rate here is expected, not a failure.
KEPT_BROAD_METHODS = [
    "reinforcement learning", "multi agent", "fine tuning", "supervised fine tuning",
    "in context learning", "tool use", "deep research",
]
# Axis ordering is a coded judgment call, recorded like the stop-list:
ORDERING_RULE = ("families processed depth-first in descending distinct-subject count "
                 "(comparative promise), each capped at cap_per_key accepts and each video "
                 "at cap_per_video; deterministic total order (no RNG), seed is provenance only")
# entities that are not comparable subjects (used to filter the differing-subject set)
NONSUBJECT_ENTITIES = {
    "openai", "google", "github", "anthropic", "stanford university", "mit", "nvidia",
    "hugging face", "meta", "microsoft", "tsinghua university",
}
_SIZE_RE = re.compile(r"^\d+(\.\d+)?\s*[bmk]?$")   # "32b", "7b", "1.5b", "70m", "16k", "100"
_HARDWARE = ("gpu", "a100", "h100", "tpu", "cuda")


# ---- prompt (per-pair; task's rules, adapted to singular) -------------------

SYSTEM = """\
You curate comparative evaluation questions. You are given a pair of claims from two DIFFERENT videos by the same AI/ML creator, each with its video's publication date, and possibly a list of questions already written for other pairs.

First decide comparability. A valid comparison contrasts two DIFFERENT named subjects (models, systems, methods, or papers). REJECT if: both claims are about the SAME subject - they attribute their content to the same model/system/method/concept even across two videos (e.g. both describe the design of the same test, or both describe RAG in general); either claim's subject is a general concept ("RAG", "the benchmark itself", "reinforcement learning") rather than a specific named entity; either claim merely states that a subject exists, was tested, or was mentioned without giving a comparable property, behavior, result, or design detail (a bare "X was tested" grounds nothing to compare); the claims address different aspects and a comparison would be apples-to-oranges; they restate the same fact; they differ only in granularity; the two claims are actually about the SAME entity in different spelling or a variant suffix ("o1" vs "o1-mini", "Opus 4.5" vs "Opus 4.6" are DIFFERENT and comparable; but "GPT OSS 120B" vs "GPT-OSS-120B" is the same entity - reject); either claim contains an unresolved reference ("the paper", "the study", "the model") whose referent cannot be named from the claim itself; or no practitioner would plausibly ask this comparison. Rejecting is the PREFERRED outcome: if the pair does not support a clean comparison between two distinct named subjects, REJECT rather than force a strained question. Otherwise ACCEPT and write ONE natural comparison question requiring BOTH claims to answer. Design-vs-design and method-vs-method comparisons between two named entities are fully in scope; the claims need not be about performance numbers.

Question rules for accepted pairs:
- Answerable from the two claims together; unanswerable from either alone.
- Never reveal the outcome of the comparison (no winner, no margin) in the question.
- Name both subjects and the comparison axis, but disclose NEITHER side's mechanism, finding, result, or design content. Do not paraphrase the claims into the question ("how does A's <what A does> compare to B's <what B does>") - that lets the answer be recovered without retrieval. Name what is compared, not what each side did.
- Standalone practitioner phrasing; no "these videos" / "the creator" / "both tests". Public entity names are fine; creator-specific constructs get a natural description.
- If the comparison only makes sense with time context (results a year apart), it is fine to phrase it neutrally ("in their respective evaluations") - do not invent dates.
- Vary opening and structure; avoid resembling the previously written questions, if any are provided.
Return: accept/reject, a short reason, and the question if accepted."""


class Judgement(BaseModel):
    verdict: Literal["accept", "reject"]
    reason: str
    question: str | None = None


# ---- groundable-claim pre-filter (same bar as the factual slice's selector) ----

FILTER_SYSTEM = """\
You identify which of one video's claims are groundable comparison material. Return the ids of claims that state a substantive, comparable property: a concrete result, finding, number, comparison, method or mechanism detail, design choice, behavior, or creator judgment with real content. EXCLUDE content-free setup or meta claims (e.g. "the creator tests two models side by side", "a closer look will follow"), moment-by-moment demo narration, and claims too thin or generic to compare against another claim. Return ONLY claim ids."""


class Groundable(BaseModel):
    claim_ids: list[str]


async def filter_video(video_id: str, vclaims: list[dict], sem: asyncio.Semaphore) -> set[str] | None:
    """Return the groundable claim ids for one video, or None on API failure (caller
    falls back to keeping all of that video's claims; the checker is the backstop)."""
    valid = {c["claim_id"] for c in vclaims}
    listing = "\n".join(f"[{c['claim_id']}] {c['text']}" for c in vclaims)
    user = f"Video claims (high-confidence):\n{listing}\n\nReturn the ids of all groundable claims."
    async with sem:
        try:
            out = await asyncio.wait_for(
                call_structured(FILTER_SYSTEM, user, Groundable, model=MODEL,
                                max_tokens=1200, thinking={"type": "disabled"}),
                timeout=CALL_TIMEOUT,
            )
        except Exception as e:  # noqa: BLE001
            print(f"  filter ERROR {video_id}: {type(e).__name__}")
            return None
    keep = set()
    for cid in out.claim_ids:      # accept bare-suffix ids too (same fix as the factual slice)
        if cid in valid:
            keep.add(cid)
        elif (full := f"{video_id}#{cid.lstrip('#')}") in valid:
            keep.add(full)
    return keep


LEGACY_VIDEO_CACHE = Path("eval/artifacts/groundable_claims_code4AI.json")


def load_groundable_cache(path: Path, by_vid: dict[str, list[dict]]) -> dict[str, bool]:
    """Claim-level groundability cache {claim_id: bool}, so classifications accumulate
    across slices (Task 6 reuses them). Pre-warmed once from the legacy video-level cache
    so already-paid classifications become an asset, not sunk cost."""
    if path.exists():
        return json.loads(path.read_text())
    cache: dict[str, bool] = {}
    if LEGACY_VIDEO_CACHE.exists():
        vc = json.loads(LEGACY_VIDEO_CACHE.read_text())
        for vid, gids in vc.items():
            g = set(gids)
            for c in by_vid.get(vid, []):
                cache[c["claim_id"]] = c["claim_id"] in g
    return cache


# ---- normalization ---------------------------------------------------------

def normalize(tag: str) -> str:
    t = tag.lower()
    t = re.sub(r"\([^)]*\)", " ", t)      # drop parenthetical asides
    t = re.sub(r"-+", " ", t)             # hyphens -> space ("gpt-oss 120b" == "gpt oss 120b")
    t = re.sub(r"\s+", " ", t).strip()
    toks = t.split()
    while toks and toks[-1] in ROLE_WORDS:   # strip trailing role words, preserve version/size tokens
        toks.pop()
    return " ".join(toks)


def topic_family(norm: str) -> str:
    """One narrowed semantic alias: fold the elevator/causal-reasoning test into a
    single family. Trigger on 'elevator', or 'causal reason' only with test/puzzle/
    benchmark; bare 'causal reasoning' keeps its own family."""
    if "elevator" in norm or ("causal reason" in norm
                              and any(w in norm for w in ("test", "puzzle", "benchmark"))):
        return "topic:elevator/causal-reasoning-test"
    return f"topic:{norm}"


def is_stopped_topic(norm: str) -> bool:
    return norm in STOP_TOPICS or norm.startswith(STOP_TOPIC_PREFIXES)


def substantive(entities: set[str]) -> set[str]:
    """Keep only entities that are real comparison subjects (drop bare sizes, hardware,
    orgs), so a pair compares actual models/methods rather than incidental shared tokens."""
    out = set()
    for e in entities:
        if _SIZE_RE.match(e) or e in NONSUBJECT_ENTITIES or any(h in e for h in _HARDWARE):
            continue
        out.add(e)
    return out


# ---- inputs ----------------------------------------------------------------

def _parse_day(iso: str) -> dt.date:
    return dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()


def load_claims(path: Path) -> list[dict]:
    """High-confidence claims with normalized topic axes and substantive subject sets."""
    out = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        if "_meta" in rec or not rec.get("published_at"):
            continue
        day = _parse_day(rec["published_at"])
        for c in rec["claims"]:
            if c["confidence"] != "high":
                continue
            out.append({
                "claim_id": c["claim_id"], "video_id": rec["video_id"], "day": day,
                "text": c["text"],
                "topics": {normalize(t) for t in c["topics"] if normalize(t)},
                "subjects": substantive({normalize(e) for e in c["entities"] if normalize(e)}),
            })
    return out


# ---- pair generation -------------------------------------------------------

def build_families(claims: list[dict]) -> tuple[dict[str, list[int]], dict[str, int]]:
    """topic family_key -> claim indices (>=2 distinct videos, not stopped), and the
    stop-listed topic -> video-count map for the over-block eyeball."""
    fam: dict[str, list[int]] = collections.defaultdict(list)
    fam_vids: dict[str, set] = collections.defaultdict(set)
    stopped_vids: dict[str, set] = collections.defaultdict(set)
    for i, c in enumerate(claims):
        for norm in c["topics"]:
            if is_stopped_topic(norm):
                stopped_vids[f"topic:{norm}"].add(c["video_id"])
                continue
            k = topic_family(norm)
            fam[k].append(i)
            fam_vids[k].add(c["video_id"])
    kept = {k: idxs for k, idxs in fam.items() if len(fam_vids[k]) >= 2}
    stopped = {k: len(vs) for k, vs in sorted(stopped_vids.items(), key=lambda kv: -len(kv[1]))}
    return kept, stopped


def family_richness(claims: list[dict], idxs: list[int]) -> int:
    """Distinct subjects in a family - a proxy for comparative promise."""
    s: set[str] = set()
    for i in idxs:
        s |= claims[i]["subjects"]
    return len(s)


def generate_pairs(claims: list[dict], families: dict[str, list[int]],
                   per_family_gen: int, nongroundable: set[str]) -> list[dict]:
    """Cross-video, different-subject, both-anchored claim pairs. Each unique pair is
    owned by the richest family that emits it. Within a family, dedupe by distinguishing-
    subject signature; date gap is RECORDED as a covariate but is not a selection weight
    (weighting it pulled stale setup-description claims). Deterministic (no RNG)."""
    seen: set[tuple[str, str]] = set()
    pairs: list[dict] = []
    order = sorted(families, key=lambda k: (-family_richness(claims, families[k]), k))
    for k in order:
        idxs = families[k]
        cand = []
        for a in range(len(idxs)):
            ca = claims[idxs[a]]
            if not ca["subjects"] or ca["claim_id"] in nongroundable:
                continue
            for b in range(a + 1, len(idxs)):
                cb = claims[idxs[b]]
                if (cb["video_id"] == ca["video_id"] or not cb["subjects"]
                        or cb["claim_id"] in nongroundable):
                    continue
                if not (ca["subjects"] ^ cb["subjects"]):   # identical subjects = same thing
                    continue
                key = tuple(sorted((ca["claim_id"], cb["claim_id"])))
                if key in seen:
                    continue
                gap = abs((ca["day"] - cb["day"]).days)
                sig = frozenset(ca["subjects"] ^ cb["subjects"])
                cand.append((gap, sig, key, idxs[a], idxs[b]))
        cand.sort(key=lambda t: t[2])   # deterministic by claim-id; date gap not weighted
        taken_sigs: set = set()
        n = 0
        for gap, sig, key, ia, ib in cand:
            if sig in taken_sigs:
                continue
            taken_sigs.add(sig)
            seen.add(key)
            pairs.append({"pair_key": k, "a": ia, "b": ib, "date_gap_days": gap,
                          "richness": family_richness(claims, idxs)})
            n += 1
            if n >= per_family_gen:
                break
    return pairs


# ---- per-pair judge + compose ----------------------------------------------

async def judge(pair: dict, claims: list[dict], priors: list[str]) -> Judgement:
    ca, cb = claims[pair["a"]], claims[pair["b"]]
    lines = [f"key={pair['pair_key']}",
             f"A ({ca['video_id']}, published {ca['day']}): {ca['text']}",
             f"B ({cb['video_id']}, published {cb['day']}): {cb['text']}"]
    if priors:
        lines.append("\nAlready written for other pairs (do not resemble these):")
        lines += [f"- {q}" for q in priors[-VARIETY_WINDOW:]]
    lines.append("\nDecide comparability and, if comparable, write the question.")
    return await asyncio.wait_for(
        call_structured(SYSTEM, "\n".join(lines), Judgement, model=MODEL,
                        max_tokens=MAX_TOKENS, thinking={"type": "adaptive"}),
        timeout=CALL_TIMEOUT,
    )


# ---- driver ----------------------------------------------------------------

async def amain(args: argparse.Namespace) -> None:
    claims = load_claims(args.claims)
    by_vid: dict[str, list[dict]] = collections.defaultdict(list)
    for c in claims:
        by_vid[c["video_id"]].append(c)
    families, stopped = build_families(claims)
    if args.only_families:
        families = {k: v for k, v in families.items() if k in set(args.only_families)}
        print(f"restricted to {len(families)} families: {list(families)}")
    videos_needed = {claims[i]["video_id"] for k in families for i in families[k]}

    cache = load_groundable_cache(args.filter_cache, by_vid)   # {claim_id: bool}, pre-warmed
    # Pre-run cost estimate BEFORE any spend - the last outage happened because a heavy pass
    # was not visible as heavy until it ran. Rough upper bound at ~$0.01/call.
    uncached_vids = {v for v in videos_needed if any(c["claim_id"] not in cache for c in by_vid[v])}
    print(f"[cost estimate] rough upper bound <= {len(uncached_vids)} filter calls "
          f"+ <= {args.max_judged} judge calls ~ ${(len(uncached_vids) + args.max_judged) * 0.01:.2f}",
          flush=True)   # flush so the pre-spend estimate is visible even under block-buffered stdout

    # Lazy classification: pair generation is local and free, so generate first, then classify
    # ONLY the videos whose claims appear in generated pairs; drop non-groundable and regenerate
    # until the pair set is stable. Cache is claim-level and persists across slices.
    sem = asyncio.Semaphore(args.filter_concurrency)
    n_filter_calls = n_filter_fallback = 0
    while True:
        nong = {cid for cid, ok in cache.items() if not ok}
        pairs = generate_pairs(claims, families, args.per_family_gen, nong)
        involved = {claims[p[s]]["claim_id"] for p in pairs for s in ("a", "b")}
        todo = sorted({cid.rsplit("#", 1)[0] for cid in involved if cid not in cache})
        if not todo:
            break
        results = await asyncio.gather(*(filter_video(v, by_vid[v], sem) for v in todo))
        n_filter_calls += len(todo)
        for v, keep in zip(todo, results):
            if keep is None:
                for c in by_vid[v]:
                    cache[c["claim_id"]] = True   # fallback: keep all; the checker backstops
                n_filter_fallback += 1
            else:
                for c in by_vid[v]:
                    cache[c["claim_id"]] = c["claim_id"] in keep
        args.filter_cache.parent.mkdir(parents=True, exist_ok=True)
        args.filter_cache.write_text(json.dumps(cache, ensure_ascii=False))

    pairs.sort(key=lambda p: (-p["richness"], p["pair_key"], -p["date_gap_days"],
                              claims[p["a"]]["claim_id"], claims[p["b"]]["claim_id"]))
    scoped = [c for c in claims if c["video_id"] in videos_needed and c["claim_id"] in cache]
    n_dropped = sum(1 for c in scoped if not cache[c["claim_id"]])
    dropped_sample = [{"claim_id": c["claim_id"], "text": c["text"]}
                      for c in scoped if not cache[c["claim_id"]]][:5]
    print(f"claims={len(claims)} families={len(families)} videos={len(videos_needed)} "
          f"filter_calls={n_filter_calls} classified={len(scoped)} dropped={n_dropped} "
          f"generated_pairs={len(pairs)}")

    fam_ct: collections.Counter = collections.Counter()
    vid_ct: collections.Counter = collections.Counter()
    claim_ct: collections.Counter = collections.Counter()
    ns_judged: collections.Counter = collections.Counter()
    ns_reject: collections.Counter = collections.Counter()
    accepted: list[dict] = []
    priors: list[str] = []
    reject_sample: list[dict] = []
    error_sample: list[dict] = []
    n_judged = n_skip_cap = n_error = 0

    for p in pairs:
        if len(accepted) >= args.target or n_judged >= args.max_judged:
            break
        ca, cb = claims[p["a"]], claims[p["b"]]
        if (fam_ct[p["pair_key"]] >= args.cap_per_key
                or vid_ct[ca["video_id"]] >= args.cap_per_video
                or vid_ct[cb["video_id"]] >= args.cap_per_video
                or claim_ct[ca["claim_id"]] >= args.cap_per_claim
                or claim_ct[cb["claim_id"]] >= args.cap_per_claim):
            n_skip_cap += 1
            continue
        try:
            j = await judge(p, claims, priors)
        except Exception as e:  # noqa: BLE001 - truncation/parse failures are counted, never silent
            n_error += 1
            if len(error_sample) < 10:
                error_sample.append({"a": ca["claim_id"], "b": cb["claim_id"],
                                     "error": f"{type(e).__name__}: {str(e)[:100]}"})
            print(f"  judge ERROR {ca['claim_id']} vs {cb['claim_id']}: {type(e).__name__}")
            continue
        n_judged += 1
        ns_judged["topic"] += 1
        if j.verdict == "accept" and j.question and j.question.strip():
            q = j.question.strip()
            accepted.append({
                "tier": "comparative", "slice": "claim_derived", "query": q,
                "answer_video_ids": [ca["video_id"], cb["video_id"]],
                "source_claim_ids": [ca["claim_id"], cb["claim_id"]],
                "pair_key": p["pair_key"], "gold_draft": [ca["text"], cb["text"]],
                "date_gap_days": p["date_gap_days"],
            })
            priors.append(q)
            fam_ct[p["pair_key"]] += 1
            vid_ct[ca["video_id"]] += 1
            vid_ct[cb["video_id"]] += 1
            claim_ct[ca["claim_id"]] += 1
            claim_ct[cb["claim_id"]] += 1
        else:
            ns_reject["topic"] += 1
            if len(reject_sample) < 25:
                reject_sample.append({"pair_key": p["pair_key"], "reason": j.reason,
                                      "a": ca["claim_id"], "b": cb["claim_id"]})

    for i, c in enumerate(accepted, 1):
        c["candidate_id"] = f"cc-{i:04d}"

    reject_rate = round(ns_reject["topic"] / ns_judged["topic"], 2) if ns_judged["topic"] else None
    meta = {"_meta": {
        "tier": "comparative", "slice": "claim_derived", "model": MODEL, "seed": args.seed,
        "scope_bound": "cross-entity comparisons only (topic axis, differing subjects); "
                       "same-entity-over-time is Task 6",
        # axis-selection decisions persist in the record (carried to SLICES.md at Task 7),
        # not just the render print
        "axis_selection": {
            "ordering_rule": ORDERING_RULE,
            "stopped_topics": sorted(STOP_TOPICS),
            "stopped_topic_prefixes": list(STOP_TOPIC_PREFIXES),
            "kept_broad_methods": KEPT_BROAD_METHODS,
        },
        "caps": {"per_key": args.cap_per_key, "per_video": args.cap_per_video,
                 "per_claim": args.cap_per_claim, "target": args.target},
        "groundable_filter": {"videos": len(videos_needed), "classified": len(scoped),
                              "dropped_non_groundable": n_dropped, "filter_calls": n_filter_calls,
                              "filter_fallbacks": n_filter_fallback, "dropped_sample": dropped_sample},
        "funnel": {"topic_families": len(families), "generated_pairs": len(pairs),
                   "judged": n_judged, "skipped_by_cap": n_skip_cap,
                   "errors": n_error, "accepted": len(accepted)},
        "reject_rate": reject_rate,
        "reject_sample": reject_sample,
        "error_sample": error_sample,
        "stop_list_video_counts": stopped,
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for c in accepted:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"accepted {len(accepted)} (judged {n_judged}, cap-skipped {n_skip_cap}, "
          f"errors {n_error}) -> {args.out}")
    print(f"  per-family accepts: {dict(fam_ct)}")
    print(f"  reject rate: {reject_rate}")

    if args.render:
        args.render.write_text(render_md(meta["_meta"], accepted, claims), encoding="utf-8")
        print(f"  rendered -> {args.render}")


def render_md(meta: dict, accepted: list[dict], claims: list[dict]) -> str:
    by_id = {c["claim_id"]: c for c in claims}
    gf = meta["groundable_filter"]
    out = [f"# Comparative claim-slice: {len(accepted)} candidates\n",
           f"funnel: {meta['funnel']}", f"reject rate: {meta['reject_rate']}",
           f"groundable filter: {gf['dropped_non_groundable']}/{gf['classified']} claims dropped "
           f"as content-free ({gf['filter_calls']} calls, {gf['filter_fallbacks']} fallbacks)\n",
           "## 5 sample claims DROPPED as non-groundable (spot-check the filter isn't eating real material)"]
    for d in gf["dropped_sample"]:
        out.append(f"  [{d['claim_id']}] {d['text']}")
    out.append("\n## stop-list (topic -> #videos blocked; eyeball for over-blocking)")
    for tag, n in list(meta["stop_list_video_counts"].items())[:25]:
        out.append(f"  {n:3d}  {tag}")
    out.append("\n## accepted candidates")
    for c in accepted:
        a, b = by_id[c["source_claim_ids"][0]], by_id[c["source_claim_ids"][1]]
        out.append(f"\n### {c['candidate_id']}  [{c['pair_key']}]  gap={c['date_gap_days']}d")
        out.append(f"Q: {c['query']}")
        out.append(f"  A [{a['claim_id']}] {a['text']}")
        out.append(f"  B [{b['claim_id']}] {b['text']}")
    out.append("\n## reject sample")
    for r in meta["reject_sample"]:
        out.append(f"  ({r['pair_key']}) {r['a']} vs {r['b']}: {r['reason']}")
    if meta.get("error_sample"):
        out.append("\n## errors (truncation/parse - counted, not silent)")
        for e in meta["error_sample"]:
            out.append(f"  {e['a']} vs {e['b']}: {e['error']}")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", type=Path, default=CLAIMS_DEFAULT)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260713)
    ap.add_argument("--per-family-gen", type=int, default=4)
    ap.add_argument("--cap-per-key", type=int, default=3)
    ap.add_argument("--cap-per-video", type=int, default=6)
    ap.add_argument("--cap-per-claim", type=int, default=2)
    ap.add_argument("--target", type=int, default=40)
    ap.add_argument("--max-judged", type=int, default=250)
    ap.add_argument("--filter-cache", type=Path,
                    default=Path("eval/artifacts/groundable_claims.json"))  # claim-level, cross-slice
    ap.add_argument("--filter-concurrency", type=int, default=8)
    ap.add_argument("--only-families", nargs="*", help="restrict to these family keys (smoke)")
    ap.add_argument("--render", type=Path, default=None)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
