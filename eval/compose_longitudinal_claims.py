"""Task 6: longitudinal query candidates composed from dated claim threads (claim slice).

Longitudinal questions ask how a creator's position or results developed over time. A
thread is a set of dated high-confidence claims sharing one normalized topic, drawn from
several videos across a span. Thread building is deterministic and pre-LLM (reusing Task
5's tag normalizer and elevator alias verbatim); each surviving thread gets ONE LLM call
that runs a development test (rejecting mere repetition) and, if it passes, composes the
question plus its draft gold: trajectory-level must-say points and dated, chunk-anchored
milestone slots.

Anti-leakage is Option 3: the per-thread retry loop is DETERMINISTIC only (composer prompt
rules forbid disclosing the change's direction/outcome/waypoints; violation_scan gates a
max-2 retry for mechanical wording violations; persistent failures are flagged
neutralization_failed and kept, never dropped). A separate advisory LLM pass runs once over
accepted candidates to produce a reading order for the human gate - it never gates, never
auto-drops, and its output is a sort hint, not a verdict.

Seed/milestone bar: meta and self-reference claims may SEED and KEY threads (that is their
value) but are exactly what the groundable filter drops, so only groundable claims are
milestone-eligible; non-groundable claims may appear as [context-only] context but may not
be selected as milestones. Groundable classification reuses the shared cross-slice cache.

No DB, no grounding (Task 7).

Usage:
  uv run python -m eval.compose_longitudinal_claims --dry-run --render eval/artifacts/_thread_inventory.md
  uv run python -m eval.compose_longitudinal_claims --only-threads "topic:elevator/causal-reasoning-test" --render eval/artifacts/_lon_smoke.md --out eval/artifacts/_lon_smoke.jsonl
  uv run python -m eval.compose_longitudinal_claims                # full run
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from core.claude_llm import call_structured, enable_usage_capture, usage_totals
from core.provenance import PROVENANCE
from eval import groundable
from eval.compose_comparative_claims import is_stopped_topic, normalize, topic_family
from eval.text_guards import violation_scan

CLAIMS_DEFAULT = Path("eval/artifacts/claims_code4AI.jsonl")
OUT_DEFAULT = Path("eval/artifacts/query_candidates_longitudinal_claimslice.jsonl")
MODEL = "claude-sonnet-5"
COMPOSE_MAX_TOKENS = 4000   # adaptive thinking + question + must-say + milestone ids
ADVISORY_MAX_TOKENS = 1500
ADVISORY_BATCH = 40        # questions per advisory call; one giant call truncates and fails
CALL_TIMEOUT = 120
MAX_ATTEMPTS = 2            # deterministic-scan retries before neutralization_failed
MIN_MILESTONES = 2         # required count in gold (identity is substitutable)
VARIETY_WINDOW = 40        # rolling "do not resemble these" list passed to the composer


# ---- composition prompt (spec cc_06 draft, verbatim) -----------------------

SYSTEM = """\
You curate longitudinal evaluation questions about how an AI/ML YouTube creator's
positions and results developed over time. You are given a thread: dated claims on
one topic, in chronological order, drawn from multiple videos. Claims marked
[context-only] provide background and may NOT be selected as milestones.

First decide: does this thread show genuine DEVELOPMENT (a stance changing, results
evolving across attempts or versions, a position strengthening or reversing, an
assessment being revised as new evidence arrives)? REJECT threads that only show
the same point restated over time, or an entity merely mentioned repeatedly.
Rejecting is preferred over composing a strained question.

For accepted threads return:
1. question: ONE natural question about the development. Asking about "the creator's
   view/assessment/results over time" is appropriate here. Name the subject and state
   that it developed or evolved over time, but do NOT name the specific dimension or
   direction of the change when that dimension is itself what the thread reveals (for
   example, ask how a test "evolved," not how it changed "in scale and complexity" when
   that growth is the answer). NEVER reveal the direction, outcome, or any waypoint of
   the change. Prefer a single development axis; a genuinely two-axis arc may ask about
   both, but only if that is the honest shape of the thread. No invented dates; "since
   early 2025" style anchors are fine when the claims support them.
2. trajectory_must_say: 2-4 short statements that any correct answer must convey,
   each directly supported by the shown claims. Do not extrapolate beyond them.
3. milestones: 3-6 claim ids from the thread whose dated statements best evidence
   the arc, spread across its time span. Only non-context-only claims are eligible.
   Prefer claims that name their subject; avoid claims with unresolved references
   ("the paper", "the study") unless the referent is unambiguous within this thread.
Return structured data only, echoing the thread key."""

COMPOSE_FP = hashlib.sha1(SYSTEM.encode()).hexdigest()[:8]   # provenance: a prompt edit is a new instrument


class ThreadComposition(BaseModel):
    thread_key: str                          # echoed for id validation
    develops: bool
    reason: str
    question: str | None = None
    trajectory_must_say: list[str] = []
    milestone_claim_ids: list[str] = []


# ---- advisory leak-risk sort (out of the loop; never gates) ----------------

ADVISORY_SYSTEM = """\
You are a reading-order aid for a human reviewing longitudinal evaluation questions for
leakage. For EACH question, judge how likely it discloses the direction, outcome, or a
waypoint of the development it asks about (a semantic leak that narrates the answer), or is
so neutral it no longer identifies the specific development (underdetermined). Return a risk
level (high, medium, or low) and a one-word hint (e.g. narrates, waypoint, neutral, ok).
This is advisory only: it orders the human's reading and decides nothing. Echo each
candidate_id."""

ADVISORY_FP = hashlib.sha1(ADVISORY_SYSTEM.encode()).hexdigest()[:8]


class AdvisoryItem(BaseModel):
    candidate_id: str
    risk: Literal["high", "medium", "low"]
    hint: str


class AdvisoryBatch(BaseModel):
    items: list[AdvisoryItem]


def _h(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()[:12]


# ---- inputs ----------------------------------------------------------------

def _parse_day(iso: str) -> dt.date:
    return dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()


def load_claims(path: Path) -> list[dict]:
    """High-confidence claims with normalized topic tags, dates, and chunk ids. All
    high-confidence claims are loaded (groundable or not); groundability gates only
    milestone-eligibility, decided later and lazily."""
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
                "claim_id": c["claim_id"], "video_id": rec["video_id"],
                "day": day, "date": day.isoformat(), "text": c["text"],
                "chunk_ids": c["chunk_ids"],
                "topics": {normalize(t) for t in c["topics"] if normalize(t)},
            })
    return out


# ---- thread building (deterministic, pre-LLM) ------------------------------

def build_threads(claims: list[dict], min_videos: int, min_span_days: int,
                  stop_fn=None) -> dict[str, list[int]]:
    """Normalized-topic thread_key -> claim indices, ordered oldest-first, kept only when
    the thread spans >= min_videos distinct videos and >= min_span_days. A claim can seed
    several threads (one per topic). Specific meta/self-reference topics are first-class
    thread keys; stop_fn is an optional predicate dropping generic non-trajectory topic
    labels (e.g. the comparative slice's meta-organizational stop-list)."""
    fam: dict[str, set[int]] = collections.defaultdict(set)
    for i, c in enumerate(claims):
        for norm in c["topics"]:
            if stop_fn and stop_fn(norm):
                continue
            fam[topic_family(norm)].add(i)
    threads: dict[str, list[int]] = {}
    for k, idxset in fam.items():
        idxs = sorted(idxset, key=lambda i: (claims[i]["day"], claims[i]["claim_id"]))
        vids = {claims[i]["video_id"] for i in idxs}
        if len(vids) < min_videos:
            continue
        span = (claims[idxs[-1]]["day"] - claims[idxs[0]]["day"]).days
        if span < min_span_days:
            continue
        threads[k] = idxs
    return threads


def sample_evenly(idxs: list[int], cap: int) -> list[int]:
    """Down-sample a day-sorted index list to cap, keeping the endpoints and spreading the
    rest evenly across position (a proxy for the time span)."""
    if len(idxs) <= cap:
        return idxs
    step = (len(idxs) - 1) / (cap - 1)
    picked = sorted({round(j * step) for j in range(cap)})
    return [idxs[p] for p in picked]


def thread_span_days(claims: list[dict], idxs: list[int]) -> int:
    return (claims[idxs[-1]]["day"] - claims[idxs[0]]["day"]).days


def thread_order(claims: list[dict], threads: dict[str, list[int]]) -> list[str]:
    """Deterministic processing order: richer/longer threads first (more likely to be real
    trajectories), then by key for total ordering."""
    def key(k: str):
        idxs = threads[k]
        vids = len({claims[i]["video_id"] for i in idxs})
        return (-vids, -thread_span_days(claims, idxs), k)
    return sorted(threads, key=key)


# ---- per-thread compose + deterministic checker ----------------------------

def _claim_line(c: dict, context_only: bool) -> str:
    tag = " [context-only]" if context_only else ""
    return f"[{c['claim_id']}]{tag} {c['date']} ({c['video_id']}): {c['text']}"


async def compose_thread(thread_key: str, claims: list[dict], idxs: list[int],
                         groundable_ids: set[str], priors: list[str],
                         retry_note: str | None) -> ThreadComposition:
    lines = [f"Thread key: {thread_key}", "", "Claims (chronological):"]
    lines += [_claim_line(claims[i], claims[i]["claim_id"] not in groundable_ids) for i in idxs]
    if priors:
        lines += ["", "Already written for other threads (do not resemble these):"]
        lines += [f"- {q}" for q in priors[-VARIETY_WINDOW:]]
    if retry_note:
        lines += ["", f"Your previous question was rejected by a deterministic wording scan: "
                      f"{retry_note}. Rewrite the question to remove that wording while keeping "
                      f"it answerable from this thread and disclosing no direction or outcome."]
    lines += ["", "Decide development and, if it develops, compose the question and gold."]
    comp = await asyncio.wait_for(
        call_structured(SYSTEM, "\n".join(lines), ThreadComposition, model=MODEL,
                        max_tokens=COMPOSE_MAX_TOKENS, thinking={"type": "adaptive"}),
        timeout=CALL_TIMEOUT,
    )
    if comp.thread_key != thread_key:
        raise ValueError(f"thread_key echo mismatch: sent {thread_key!r} got {comp.thread_key!r}")
    return comp


def build_milestones(comp: ThreadComposition, claims: list[dict], idxs: list[int],
                     groundable_ids: set[str]) -> tuple[list[dict], list[str]]:
    """Attach chunk_ids and dates from the inventory; drop any milestone id that is not an
    in-thread groundable claim. Returns (slots, invalid_ids)."""
    in_thread = {claims[i]["claim_id"]: claims[i] for i in idxs}
    slots, invalid = [], []
    for cid in comp.milestone_claim_ids:
        c = in_thread.get(cid)
        if c is None or cid not in groundable_ids or not c["chunk_ids"]:
            invalid.append(cid)
            continue
        slots.append({"slot_id": f"m{len(slots) + 1}", "date": c["date"], "claim_id": cid,
                      "statement": c["text"], "chunk_ids": c["chunk_ids"], "substitutable": True})
    return slots, invalid


# ---- advisory pass ---------------------------------------------------------

async def advisory_sort(accepted: list[dict], cache: dict, cache_path: Path | None) -> None:
    """Attach an advisory {risk, hint} to each accepted candidate for render sort order.

    Chunked (one call per ADVISORY_BATCH questions) and BEST-EFFORT: the advisory is a
    non-gating reading-order hint, so a failed or truncated batch must never block finalize
    or the artifact write - those candidates just default to an 'unrated' hint. Cached and
    prompt-fingerprinted; the cache persists per chunk so a resume continues where it left off.
    """
    def ckey(c: dict) -> str:
        return f"{ADVISORY_FP}:{c['candidate_id']}:{_h(c['query'])}"

    todo = [c for c in accepted if ckey(c) not in cache]
    for i in range(0, len(todo), ADVISORY_BATCH):
        chunk = todo[i:i + ADVISORY_BATCH]
        listing = "\n".join(f"[{c['candidate_id']}] {c['query']}" for c in chunk)
        try:
            out = await asyncio.wait_for(
                call_structured(ADVISORY_SYSTEM,
                                f"Questions:\n{listing}\n\nReturn a risk and one-word hint for "
                                f"EVERY candidate_id above, echoing each id.",
                                AdvisoryBatch, model=MODEL, max_tokens=ADVISORY_MAX_TOKENS,
                                thinking={"type": "disabled"}),
                timeout=CALL_TIMEOUT,
            )
            by_id = {c["candidate_id"]: c for c in chunk}
            for it in out.items:
                if it.candidate_id in by_id:
                    cache[ckey(by_id[it.candidate_id])] = {"risk": it.risk, "hint": it.hint}
        except Exception as e:  # noqa: BLE001 - advisory never gates; never block the artifact
            print(f"  advisory batch {i // ADVISORY_BATCH} failed ({type(e).__name__}); "
                  f"those candidates default to unrated", flush=True)
        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(cache, ensure_ascii=False))
    for c in accepted:
        c["advisory"] = cache.get(ckey(c), {"risk": "low", "hint": "unrated"})


# ---- driver ----------------------------------------------------------------

_RISK_RANK = {"high": 0, "medium": 1, "low": 2}

_USAGE_FIELDS = ("calls", "input_tokens", "output_tokens",
                 "cache_read_input_tokens", "cache_creation_input_tokens")


def _resume_aware_usage(logged: list[dict]) -> dict:
    """Total token usage across the compose phase, summed over resume boundaries. Each
    record's cumulative `_usage` resets when the run was resumed (a lower calls count), so
    bank the last cumulative before each reset. This recovers the whole-run compose cost
    even when finalize runs in a separate (resumed) process."""
    total = dict.fromkeys(_USAGE_FIELDS, 0)
    prev = None
    for r in logged:
        u = r.get("_usage")
        if not u:
            continue
        if prev and u["calls"] < prev["calls"]:
            for k in _USAGE_FIELDS:
                total[k] += prev.get(k, 0)
        prev = u
    if prev:
        for k in _USAGE_FIELDS:
            total[k] += prev.get(k, 0)
    return total


async def amain(args: argparse.Namespace) -> None:
    claims = load_claims(args.claims)
    by_vid: dict[str, list[dict]] = collections.defaultdict(list)
    for c in claims:
        by_vid[c["video_id"]].append({"claim_id": c["claim_id"]})
    stop_fn = is_stopped_topic if args.use_comparative_stoplist else None
    threads = build_threads(claims, args.min_videos, args.min_span_days, stop_fn)
    if args.only_threads:
        threads = {k: v for k, v in threads.items() if k in set(args.only_threads)}
    order = thread_order(claims, threads)

    # Thread inventory line, always printed (free, deterministic).
    spans = [thread_span_days(claims, threads[k]) for k in order]
    sizes = [len({claims[i]["video_id"] for i in threads[k]}) for k in order]
    print(f"threads={len(threads)} (>= {args.min_videos} videos, >= {args.min_span_days}d span; "
          f"stoplist={'comparative' if stop_fn else 'none'}); "
          f"videos/thread min/median/max = "
          f"{min(sizes, default=0)}/{sorted(sizes)[len(sizes)//2] if sizes else 0}/{max(sizes, default=0)}; "
          f"span days min/median/max = "
          f"{min(spans, default=0)}/{sorted(spans)[len(spans)//2] if spans else 0}/{max(spans, default=0)}",
          flush=True)

    if args.dry_run:
        if args.render:
            args.render.write_text(render_inventory(claims, threads, order), encoding="utf-8")
            print(f"  inventory rendered -> {args.render}", flush=True)
        return

    # Crash-safe event log: one line per judged thread (candidate/reject/error), appended and
    # flushed as it completes, so a multi-hour sequential run is resumable and never lost.
    partial = args.out.with_suffix(".partial.jsonl")
    logged: list[dict] = []
    done: set[str] = set()
    if args.resume and partial.exists():
        for ln in partial.read_text().splitlines():
            ln = ln.strip()
            if ln:
                rec = json.loads(ln)
                logged.append(rec)
                done.add(rec["thread_key"])
        print(f"[resume] {len(done)} threads already done in {partial}", flush=True)
    remaining = [k for k in order if k not in done]

    # Lazy groundability on the claims of surviving threads only.
    cache = groundable.load_cache(args.filter_cache, by_vid)
    text_by_id = {c["claim_id"]: c["text"] for c in claims}
    thread_claim_ids = sorted({claims[i]["claim_id"] for k in order for i in threads[k]})
    n_to_classify = sum(1 for cid in thread_claim_ids if cid not in cache)
    n_compose = min(len(remaining), args.max_threads)
    # Rough pre-spend upper bound at Sonnet 5 intro pricing ($2/M in, $10/M out), assuming
    # ~2.5k input + ~1.5k output tokens/compose call. This is only an estimate; real per-call
    # token usage is captured below and the actual totals + cost are reported in _meta.
    enable_usage_capture()
    est_cost = n_compose * (2500 * 2 + 1500 * 10) / 1e6
    print(f"[cost estimate] rough upper bound: {n_compose} compose calls (x<= {MAX_ATTEMPTS} "
          f"attempts) + ~{(n_to_classify + args.filter_batch - 1) // args.filter_batch} groundable "
          f"calls + 1 advisory ~ ${est_cost:.2f} (intro pricing); actual usage reported in _meta",
          flush=True)

    sem = asyncio.Semaphore(args.filter_concurrency)
    fstats = await groundable.classify_uncached(thread_claim_ids, text_by_id, cache, sem=sem,
                                                batch_size=args.filter_batch,
                                                cache_path=args.filter_cache)
    groundable_ids = {cid for cid in thread_claim_ids if cache.get(cid)}
    dropped = [cid for cid in thread_claim_ids if not cache.get(cid)]
    dropped_sample = [{"claim_id": cid, "text": text_by_id[cid]} for cid in dropped[:5]]

    # Sequential per-thread compose (rolling variety is order-dependent, so no concurrency);
    # priors rebuilt from any resumed pass candidates so variety survives a resume.
    priors = [r["query"] for r in logged
              if r.get("_outcome") == "candidate" and r["composition_checks"]["status"] == "pass"]
    pf = partial.open("a" if args.resume else "w", encoding="utf-8")   # fresh unless resuming

    def log_event(rec: dict) -> None:
        rec["_usage"] = usage_totals()   # cumulative token snapshot -> live cost readable from disk
        pf.write(json.dumps(rec, ensure_ascii=False) + "\n")
        pf.flush()
        logged.append(rec)
        done.add(rec["thread_key"])

    n_new = 0
    for i, k in enumerate(order, 1):
        if len(done) >= args.max_threads:
            break
        if k in done:
            continue
        idxs = sample_evenly(threads[k], args.cap_claims)
        retry_note = None
        comp = None
        attempts = 0
        try:
            for attempts in range(1, MAX_ATTEMPTS + 1):
                comp = await compose_thread(k, claims, idxs, groundable_ids, priors, retry_note)
                if not comp.develops or not (comp.question or "").strip():
                    break
                viols = violation_scan(comp.question.strip(), "longitudinal")
                if not viols:
                    break
                retry_note = ", ".join(viols)
        except Exception as e:  # noqa: BLE001 - truncation/parse counted, never silent
            log_event({"thread_key": k, "_outcome": "error",
                       "error": f"{type(e).__name__}: {str(e)[:100]}"})
            print(f"[{i}/{len(order)}] {k} -> ERROR {type(e).__name__}", flush=True)
            continue

        if not comp.develops or not (comp.question or "").strip():
            log_event({"thread_key": k, "_outcome": "reject", "reason": comp.reason})
            print(f"[{i}/{len(order)}] {k} -> reject", flush=True)
            continue

        q = comp.question.strip()
        viols = violation_scan(q, "longitudinal")
        slots, invalid = build_milestones(comp, claims, idxs, groundable_ids)
        status = ("review_milestones" if len(slots) < MIN_MILESTONES
                  else "neutralization_failed" if viols else "pass")
        cand = {
            "_outcome": "candidate",
            "tier": "longitudinal", "slice": "claim_derived", "query": q,
            "answer_video_ids": sorted({claims[j]["video_id"] for j in idxs
                                        if claims[j]["claim_id"] in {s["claim_id"] for s in slots}}),
            "source_claim_ids": [s["claim_id"] for s in slots],
            "thread_key": k,
            "gold_draft": {"trajectory_must_say": comp.trajectory_must_say,
                           "milestone_slots": slots, "min_milestones": MIN_MILESTONES},
            "composition_checks": {"deterministic_scan": "fail" if viols else "pass",
                                   "scan_violations": viols, "attempts": attempts,
                                   "invalid_milestone_ids": invalid, "status": status},
        }
        log_event(cand)
        if status == "pass":
            priors.append(q)
        n_new += 1
        print(f"[{i}/{len(order)}] {k} -> {status}", flush=True)
    pf.close()

    # Finalize from the event log: assign ids, advisory-sort pass candidates, write the artifact.
    candidates = [{kk: vv for kk, vv in r.items() if kk not in ("_outcome", "_usage")}
                  for r in logged if r.get("_outcome") == "candidate"]
    for i, c in enumerate(sorted(candidates, key=lambda c: c["thread_key"]), 1):
        c["candidate_id"] = f"lc-{i:04d}"
    candidates.sort(key=lambda c: c["candidate_id"])

    pre_adv = usage_totals() or {}
    passed = [c for c in candidates if c["composition_checks"]["status"] == "pass"]
    if passed:
        adv_cache = json.loads(args.advisory_cache.read_text()) if args.advisory_cache.exists() else {}
        await advisory_sort(passed, adv_cache, args.advisory_cache)

    n_reject = sum(1 for r in logged if r.get("_outcome") == "reject")
    n_error = sum(1 for r in logged if r.get("_outcome") == "error")
    status_counts = collections.Counter(c["composition_checks"]["status"] for c in candidates)
    status_counts["rejected_no_development"] = n_reject
    reject_sample = [{"thread_key": r["thread_key"], "reason": r["reason"]}
                     for r in logged if r.get("_outcome") == "reject"][:25]
    error_sample = [{"thread_key": r["thread_key"], "error": r["error"]}
                    for r in logged if r.get("_outcome") == "error"][:10]
    # Whole-run usage = resume-aware compose (from the checkpoint records) + the advisory
    # delta (post-minus-pre around the advisory call). Using the advisory delta rather than
    # the live total avoids double-counting compose in the single-process case, and recovers
    # compose from the checkpoint in the finalize-only resume case.
    post_adv = usage_totals() or {}
    adv_delta = {k: post_adv.get(k, 0) - pre_adv.get(k, 0) for k in _USAGE_FIELDS}
    usage = {k: _resume_aware_usage(logged).get(k, 0) + adv_delta.get(k, 0) for k in _USAGE_FIELDS}

    meta = {"_meta": {
        "tier": "longitudinal", "slice": "claim_derived", "model": MODEL, "seed": args.seed,
        "anti_leakage": "option3: deterministic-only retry loop; advisory LLM sort out of loop, "
                        "never gates or reported",
        "compose_prompt_fp": COMPOSE_FP, "advisory_prompt_fp": ADVISORY_FP,
        "thread_params": {"min_videos": args.min_videos, "min_span_days": args.min_span_days,
                          "cap_claims": args.cap_claims,
                          "stoplist": "comparative" if stop_fn else "none",
                          "max_threads": args.max_threads, "threads_available": len(order)},
        "groundable_filter": {"thread_claims": len(thread_claim_ids),
                              "dropped_non_groundable": len(dropped),
                              "filter_calls": fstats["calls"], "filter_fallbacks": fstats["fallbacks"],
                              "dropped_sample": dropped_sample},
        "funnel": {"threads_formed": len(threads), "judged": len(candidates) + n_reject,
                   "rejected_no_development": n_reject, "errors": n_error,
                   "candidates": len(candidates)},
        "status_counts": dict(status_counts),
        "reject_sample": reject_sample,
        "error_sample": error_sample,
        "usage": usage,
        "usage_cost_usd": (round(usage["input_tokens"] * 2 / 1e6
                                 + usage["output_tokens"] * 10 / 1e6, 2) if usage else None),
        "usage_pricing_note": "Sonnet 5 intro $2/M input, $10/M output (through 2026-08-31); "
                              "adaptive-thinking tokens billed as output; cost is actual usage, "
                              "not the pre-spend estimate",
        "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
    }}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        f.write(json.dumps(meta["_meta"], ensure_ascii=False) + "\n")
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"candidates {len(candidates)} (judged {len(candidates) + n_reject}, rejected {n_reject}, "
          f"errors {n_error}; new this run {n_new}) -> {args.out}", flush=True)
    print(f"  status: {dict(status_counts)}", flush=True)
    if usage:
        print(f"  actual usage: {usage['calls']} calls, {usage['input_tokens']} in + "
              f"{usage['output_tokens']} out -> ${meta['_meta']['usage_cost_usd']} (intro pricing)",
              flush=True)

    if args.render:
        args.render.write_text(render_md(meta["_meta"], candidates), encoding="utf-8")
        print(f"  rendered -> {args.render}", flush=True)


# ---- renders ---------------------------------------------------------------

def render_inventory(claims: list[dict], threads: dict[str, list[int]], order: list[str]) -> str:
    out = [f"# Longitudinal thread inventory: {len(threads)} threads\n",
           "thread_key | #videos | span_days | #claims (oldest -> newest first/last date)"]
    for k in order:
        idxs = threads[k]
        vids = len({claims[i]["video_id"] for i in idxs})
        out.append(f"\n### {k}  [videos={vids}, span={thread_span_days(claims, idxs)}d, "
                   f"claims={len(idxs)}]  {claims[idxs[0]]['date']} -> {claims[idxs[-1]]['date']}")
        for i in idxs[:8]:
            out.append(f"  {claims[i]['date']} [{claims[i]['claim_id']}] {claims[i]['text'][:140]}")
        if len(idxs) > 8:
            out.append(f"  ... (+{len(idxs) - 8} more)")
    return "\n".join(out)


def render_md(meta: dict, candidates: list[dict]) -> str:
    gf = meta["groundable_filter"]
    out = [f"# Longitudinal claim-slice: {len(candidates)} candidates\n",
           f"funnel: {meta['funnel']}", f"status: {meta['status_counts']}",
           f"groundable filter: {gf['dropped_non_groundable']}/{gf['thread_claims']} thread claims "
           f"dropped as content-free ({gf['filter_calls']} calls, {gf['filter_fallbacks']} fallbacks)",
           f"advisory sort hint is a reading order for leak review, NOT a verdict "
           f"(prompt fp {meta['advisory_prompt_fp']})\n",
           "## 5 sample claims DROPPED as non-groundable (spot-check the filter isn't eating real material)"]
    for d in gf["dropped_sample"]:
        out.append(f"  [{d['claim_id']}] {d['text']}")

    flagged = [c for c in candidates if c["composition_checks"]["status"] != "pass"]
    passed = [c for c in candidates if c["composition_checks"]["status"] == "pass"]
    passed.sort(key=lambda c: (_RISK_RANK.get(c.get("advisory", {}).get("risk", "low"), 2),
                               c["candidate_id"]))

    if flagged:
        out.append("\n## FLAGGED - kept for human review, read these first")
        for c in flagged:
            out.append(_render_candidate(c))
    out.append("\n## accepted candidates (sorted by advisory leak-risk, highest first)")
    for c in passed:
        out.append(_render_candidate(c))

    out.append("\n## rejected threads (no development)")
    for r in meta["reject_sample"]:
        out.append(f"  ({r['thread_key']}) {r['reason']}")
    if meta.get("error_sample"):
        out.append("\n## errors (truncation/parse - counted, not silent)")
        for e in meta["error_sample"]:
            out.append(f"  {e['thread_key']}: {e['error']}")
    return "\n".join(out)


def _render_candidate(c: dict) -> str:
    cc = c["composition_checks"]
    adv = c.get("advisory")
    hint = f"  [advisory: {adv['risk']}/{adv['hint']}]" if adv else ""
    lines = [f"\n### {c['candidate_id']}  [{c['thread_key']}]  status={cc['status']}"
             f"  attempts={cc['attempts']}{hint}",
             f"Q: {c['query']}"]
    if cc["scan_violations"]:
        lines.append(f"  ! deterministic scan: {cc['scan_violations']}")
    if cc["invalid_milestone_ids"]:
        lines.append(f"  ! dropped invalid/context-only milestone ids: {cc['invalid_milestone_ids']}")
    lines.append("  trajectory_must_say:")
    lines += [f"    - {p}" for p in c["gold_draft"]["trajectory_must_say"]]
    lines.append(f"  milestones (need >= {c['gold_draft']['min_milestones']}, substitutable):")
    for s in c["gold_draft"]["milestone_slots"]:
        lines.append(f"    {s['slot_id']} {s['date']} [{s['claim_id']}] {s['statement'][:120]}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", type=Path, default=CLAIMS_DEFAULT)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260714)   # provenance only; deterministic order
    ap.add_argument("--min-videos", type=int, default=3)
    ap.add_argument("--min-span-days", type=int, default=90)
    ap.add_argument("--cap-claims", type=int, default=25)
    ap.add_argument("--max-threads", type=int, default=100000)   # effectively uncapped; full coverage
    ap.add_argument("--use-comparative-stoplist", action="store_true",
                    help="drop generic meta-organizational topics via the comparative slice's stop-list")
    ap.add_argument("--only-threads", nargs="*", help="restrict to these thread keys (smoke)")
    ap.add_argument("--resume", action="store_true", help="skip threads already in the .partial.jsonl log")
    ap.add_argument("--dry-run", action="store_true", help="build threads and render inventory, no LLM")
    ap.add_argument("--filter-cache", type=Path,
                    default=Path("eval/artifacts/groundable_claims.json"))
    ap.add_argument("--filter-batch", type=int, default=50)
    ap.add_argument("--filter-concurrency", type=int, default=8)
    ap.add_argument("--advisory-cache", type=Path,
                    default=Path("eval/artifacts/longitudinal_advisory_cache.json"))
    ap.add_argument("--render", type=Path, default=None)
    args = ap.parse_args()
    asyncio.run(amain(args))


if __name__ == "__main__":
    main()
