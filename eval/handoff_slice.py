"""Task 7 handoff: deterministic flags, per-tier review files, SLICES.md, prediction note.

Reads the grounded claim-slice artifacts (`query_grounded_{tier}_claimslice.jsonl`), computes
advisory flags (nothing is auto-dropped), pulls the gold chunk text from the DB so the truth
sits inline in the review file, and renders one human-readable review file per tier plus the
slice manifest and the two-prediction note. No LLM calls.

Every candidate is keyed by a composite identity (candidate_id + source_claim_ids + a hash of
the final query) so keep/drop decisions attach to content, not list position.

Usage:
  uv run python -m eval.handoff_slice --tiers longitudinal   # after the longitudinal smoke
  uv run python -m eval.handoff_slice                        # all present tiers + SLICES + note
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from eval import corpus_io as cio

OUT_DIR = Path("eval/artifacts")
CLAIMS = OUT_DIR / "claims_code4AI.jsonl"
TIERS = ["factual", "comparative", "longitudinal"]

ANAPHORA = re.compile(r"\bthe (paper|study|model|given)\b", re.I)  # "the creator" deliberately excluded
STRIDE = 30            # chunk window seconds; adjacency arithmetic
FLAG_LEAK = 0.3        # advisory: surface elevated lexical leak (below the grounder's 0.5 hard drop)


# ---- corpus lookups --------------------------------------------------------

def load_claim_index() -> tuple[dict, dict]:
    """claim_id -> {entities, text}; video_id -> {title, date}."""
    claims: dict[str, dict] = {}
    videos: dict[str, dict] = {}
    for ln in CLAIMS.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        if "_meta" in r:
            continue
        videos[r["video_id"]] = {"title": r["title"], "date": (r.get("published_at") or "")[:10]}
        for c in r["claims"]:
            claims[c["claim_id"]] = {"entities": c.get("entities", []), "text": c["text"]}
    return claims, videos


def _video_of(chunk_id: str) -> str:
    return chunk_id.rsplit(":", 1)[0]


def _start_s(chunk_id: str) -> int:
    return int(chunk_id.rsplit(":", 1)[1])


def _video_of_claim(claim_id: str) -> str:
    return claim_id.split("#", 1)[0]


def _norm(s: str) -> str:
    return re.sub(r"[\s-]", "", s.lower())


def chunk_text_map(chunk_ids: list[str], cache: dict) -> dict[str, str]:
    """chunk_id -> text, fetching each involved video's chunks once (DB)."""
    for vid in {_video_of(c) for c in chunk_ids}:
        if vid not in cache:
            cache[vid] = {c["chunk_id"]: c["text"] for c in cio.video_chunks(vid)}
    return {cid: cache[_video_of(cid)].get(cid, "") for cid in chunk_ids}


# ---- deterministic flags ---------------------------------------------------

def subject_in_gold(entities: list[str], gold_text: str) -> str:
    """full / partial / none: normalized entity substrings present in normalized gold text.

    Normalization is lowercase + strip hyphens and spaces (catches 'GPT-5' vs 'gpt 5').
    False negatives are acceptable; the flag errs toward showing things.
    """
    if not entities:
        return "none"
    g = _norm(gold_text)
    present = sum(1 for e in entities if _norm(e) and _norm(e) in g)
    if present == len(entities):
        return "full"
    return "partial" if present else "none"


def chunk_span(chunk_ids: list[str]) -> dict:
    """n + adjacency from chunk-id arithmetic (single-video consecutive = adjacent)."""
    n = len(chunk_ids)
    if n <= 1:
        return {"n": n, "shape": "single"}
    if len({_video_of(c) for c in chunk_ids}) > 1:
        return {"n": n, "shape": "multi-video"}
    starts = sorted(_start_s(c) for c in chunk_ids)
    adjacent = all(b - a == STRIDE for a, b in zip(starts, starts[1:]))
    return {"n": n, "shape": "adjacent" if adjacent else "non-adjacent"}


def anaphora_hits(*texts: str) -> list[str]:
    return sorted({m.group(0).lower() for t in texts for m in ANAPHORA.finditer(t or "")})


def identity_key(cand: dict) -> str:
    h = hashlib.sha1(cand["query"].encode("utf-8")).hexdigest()[:8]
    return f"{cand['candidate_id']} | {'+'.join(cand['source_claim_ids'])} | q:{h}"


# ---- per-tier flag assembly ------------------------------------------------

def flags_factual(cand: dict, claims: dict, gold_text_by_chunk: dict) -> dict:
    gold_text = " ".join(gold_text_by_chunk.values())
    ent = claims.get(cand["source_claim_ids"][0], {}).get("entities", [])
    claim_text = cand["gold_draft"][0] if cand.get("gold_draft") else ""
    f = {
        "subject_in_gold": subject_in_gold(ent, gold_text),
        "chunk_span": chunk_span(cand["source_chunk_ids"]),
        "anaphora": anaphora_hits(cand["query"], claim_text),
        "leak": cand.get("leak", 0.0),
        "semantic_leak": None,  # factual carries none by decision
    }
    f["flagged"] = bool(f["subject_in_gold"] == "none" or f["anaphora"] or f["leak"] >= FLAG_LEAK)
    f["excluded"] = False
    return f


def flags_comparative(cand: dict, claims: dict, gold_text_by_chunk: dict) -> dict:
    sides = {}
    for side, cid in zip(("A", "B"), cand["source_claim_ids"]):
        vid = _video_of_claim(cid)
        side_gold = " ".join(t for c, t in gold_text_by_chunk.items() if _video_of(c) == vid)
        sides[side] = subject_in_gold(claims.get(cid, {}).get("entities", []), side_gold)
    status = cand.get("final_status")
    f = {
        "observed_shape": cand.get("observed_shape"),
        "subject_in_gold": sides,
        "chunk_span": chunk_span(cand["source_chunk_ids"]),
        "anaphora": anaphora_hits(cand["query"], *(cand.get("gold_draft") or [])),
        "leak": cand.get("leak", 0.0),
        "semantic_leak": {"final_status": status, "leaked_side_final": cand.get("leaked_side_final")},
        "one_side_unverified": cand.get("observed_shape") != "multi-video",
    }
    f["excluded"] = status != "pass"
    f["flagged"] = bool(
        not f["excluded"] and (
            f["one_side_unverified"] or "none" in sides.values()
            or f["anaphora"] or f["leak"] >= FLAG_LEAK
            or status in {"leak", "unneutralizable"}
        )
    )
    return f


def flags_longitudinal(cand: dict) -> dict:
    """Longitudinal uses milestone-support flags (from the grounded cross-check), not subject_in_gold."""
    grounded = set(cand["source_chunk_ids"])
    slots = cand["gold_draft"]["milestone_slots"]
    unsupported = [s["slot_id"] for s in slots if not (set(s["chunk_ids"]) & grounded)]
    cc = cand.get("composition_checks", {})
    sem = cc.get("status") != "pass" or bool(cc.get("scan_violations"))
    supported = len(slots) - len(unsupported)
    # anaphora over the QUERY only: the flag tests question self-containment, and "the paper"
    # is pervasive-but-benign in these paper-review milestone statements (scoring gold text there
    # would flag ~100% and defeat the graded sort). The composer already guards question wording.
    f = {
        "milestones_total": len(slots),
        "milestones_unsupported": unsupported,
        "support_frac": (supported / len(slots)) if slots else 0.0,
        "chunk_span": chunk_span(cand["source_chunk_ids"]),
        "anaphora": anaphora_hits(cand["query"]),
        "leak": cand.get("leak", 0.0),
        "semantic_leak": {"status": cc.get("status"), "scan_violations": cc.get("scan_violations", [])},
    }
    f["excluded"] = False
    # Graded: milestone-support does NOT flag the candidate; it demotes it in the sort
    # (low support sorts lower). Only real defects flag. (Q2 = graded support demoted in sort.)
    f["flagged"] = bool(sem or f["anaphora"] or f["leak"] >= FLAG_LEAK)
    return f


# ---- rendering -------------------------------------------------------------

def _gold_chunks_block(cand: dict, gold_text_by_chunk: dict) -> list[str]:
    out = ["**gold chunks (inline):**"]
    for cid in cand["source_chunk_ids"]:
        out.append(f"- `{cid}`  {gold_text_by_chunk.get(cid, '') or '(no text)'}")
    return out


def _videos_line(cand: dict, videos: dict) -> str:
    parts = [f"{v} ({videos.get(v, {}).get('date', '?')})" for v in cand["answer_video_ids"]]
    return "source videos: " + "; ".join(parts)


def ext_review_key(cand: dict) -> str:
    """External-review verdicts attach to content (pairs/claims), not the query hash."""
    return f"{cand['candidate_id']}|{'+'.join(cand['source_claim_ids'])}"


def render_candidate(tier: str, cand: dict, f: dict, gold_text_by_chunk: dict,
                     videos: dict, review: dict) -> list[str]:
    out = [f"\n### {identity_key(cand)}"]
    q, oq = cand["query"], cand.get("original_query")
    out.append(f"**Q:** {q}")
    if oq and oq != q:
        out.append(f"_original:_ {oq}")
    out.append(_videos_line(cand, videos))
    ext = review.get(ext_review_key(cand))
    if ext:  # secondary field, must not drive the sort; shown only where a review exists
        out.append(f"external_review: {ext.get('verdict')} - {ext.get('reason', '')}")
    # flags line
    if tier == "factual":
        out.append(f"flags: subject_in_gold={f['subject_in_gold']}  "
                   f"chunk_span={f['chunk_span']['n']}/{f['chunk_span']['shape']}  "
                   f"anaphora={f['anaphora'] or '-'}  leak={f['leak']}")
        out.append(f"**gold (draft answer):** {cand['gold_draft'][0]}")
    elif tier == "comparative":
        out.append(f"flags: observed_shape={f['observed_shape']}  "
                   f"subject_in_gold(A/B)={f['subject_in_gold']['A']}/{f['subject_in_gold']['B']}  "
                   f"chunk_span={f['chunk_span']['n']}/{f['chunk_span']['shape']}  "
                   f"anaphora={f['anaphora'] or '-'}  leak={f['leak']}  "
                   f"final_status={f['semantic_leak']['final_status']}  "
                   f"leaked_side={f['semantic_leak']['leaked_side_final']}")
        out.append(f"pair_key: {cand.get('pair_key')}")
        gd = cand.get("gold_draft") or ["", ""]
        out.append(f"**gold A:** {gd[0]}")
        out.append(f"**gold B:** {gd[1] if len(gd) > 1 else ''}")
    else:  # longitudinal
        unsup = f["milestones_unsupported"]
        out.append(f"flags: milestone_support={f['milestones_total'] - len(unsup)}/{f['milestones_total']}"
                   f"{' UNSUPPORTED=' + ','.join(unsup) if unsup else ''}  "
                   f"chunk_span={f['chunk_span']['n']}/{f['chunk_span']['shape']}  "
                   f"anaphora={f['anaphora'] or '-'}  leak={f['leak']}  "
                   f"comp_status={f['semantic_leak']['status']}")
        out.append(f"thread_key: {cand.get('thread_key')}")
        out.append("**trajectory_must_say:**")
        out += [f"- {p}" for p in cand["gold_draft"]["trajectory_must_say"]]
        out.append("**milestones:**")
        for s in cand["gold_draft"]["milestone_slots"]:
            mark = "  [NO INDEP. GROUND SUPPORT]" if s["slot_id"] in unsup else ""
            out.append(f"- {s['date']}  `{s['claim_id']}`  chunk_ids={s['chunk_ids']}{mark}")
            out.append(f"    {s['statement']}")
    out += _gold_chunks_block(cand, gold_text_by_chunk)
    return out


def read_grounded(tier: str) -> tuple[dict, list[dict]]:
    path = OUT_DIR / f"query_grounded_{tier}_claimslice.jsonl"
    meta, recs = {}, []
    for ln in path.read_text().splitlines():
        if not ln.strip():
            continue
        o = json.loads(ln)
        if "_meta" in o:
            meta = o["_meta"]
        else:
            recs.append(o)
    return meta, recs


NOTES = {
    "longitudinal": ["Note: lc-0014 and lc-0024 are an overlapping family (AGI-as-goal vs "
                     "reasoning-authenticity); keep-both-or-pick-one is a sitting decision."],
}


def render_tier(tier: str, claims: dict, videos: dict, review: dict) -> dict:
    meta, recs = read_grounded(tier)
    cache: dict = {}
    rows = []
    for cand in recs:
        gtb = chunk_text_map(cand["source_chunk_ids"], cache)
        if tier == "factual":
            f = flags_factual(cand, claims, gtb)
        elif tier == "comparative":
            f = flags_comparative(cand, claims, gtb)
        else:
            f = flags_longitudinal(cand)
        rows.append((cand, f, gtb))

    clean = [r for r in rows if not r[1]["flagged"] and not r[1]["excluded"]]
    flagged = [r for r in rows if r[1]["flagged"] and not r[1]["excluded"]]
    excluded = [r for r in rows if r[1]["excluded"]]

    def sort_key(r):
        # longitudinal: high grounding-support first, low support demoted within the group
        if tier == "longitudinal":
            return (-r[1].get("support_frac", 0.0), r[0]["candidate_id"])
        return (0.0, r[0]["candidate_id"])
    for grp in (clean, flagged, excluded):
        grp.sort(key=sort_key)

    out = [f"# Task 7 review - {tier} (claim slice)", ""]
    out.append(f"grounded {meta.get('kept')}/{meta.get('input')} candidates; "
               f"dropped {meta.get('dropped')}; grounding_errors={meta.get('grounding_errors')}"
               + (f"; grounding_variant={meta['grounding_variant']}" if meta.get("grounding_variant") else ""))
    out.append(f"clean {len(clean)} | flagged {len(flagged)} | excluded {len(excluded)}")
    if tier == "longitudinal" and rows:
        fr = [r[1]["support_frac"] for r in rows]
        full = sum(1 for x in fr if x == 1.0)
        out.append(f"milestone-support (grounded, longitudinal_v1): mean {sum(fr)/len(fr):.0%}, "
                   f"fully-supported {full}/{len(rows)}; list sorted high-support first (low = demoted, not flagged)")
    out += NOTES.get(tier, [])

    fam = {}
    if tier == "comparative":
        for cand, f, _ in rows:
            if f.get("one_side_unverified"):
                fam[cand.get("pair_key")] = fam.get(cand.get("pair_key"), 0) + 1
        out.append("")
        out.append("one-side-unverified (observed_shape != multi-video) by pair-family: "
                   + (", ".join(f"{k}={v}" for k, v in sorted(fam.items())) if fam else "none"))

    out.append("\n---\n## CLEAN")
    for cand, f, gtb in clean:
        out += render_candidate(tier, cand, f, gtb, videos, review)
    out.append("\n---\n## FLAGGED (advisory - read the flags; nothing auto-dropped)")
    for cand, f, gtb in flagged:
        out += render_candidate(tier, cand, f, gtb, videos, review)
    if excluded:
        out.append("\n---\n## EXCLUDED (failure status carried through for reference)")
        for cand, f, gtb in excluded:
            out += render_candidate(tier, cand, f, gtb, videos, review)

    path = OUT_DIR / f"{tier}_claimslice_handoff.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {"tier": tier, "clean": len(clean), "flagged": len(flagged), "excluded": len(excluded),
            "meta": meta, "family_unverified": fam}


# ---- SLICES.md + prediction note -------------------------------------------

def write_slices_md(present: list[str]) -> None:
    lines = [
        "# SLICES.md - eval query slices for code4AI",
        "",
        "Self-contained manifest of the query slices used to evaluate the AnswerTrail agent.",
        "Each slice is reported on its own; results are never pooled across slices.",
        "",
        "## claim_derived (the scored core)",
        "",
        "The instrument slice. Questions are composed from atomic, dated, chunk-anchored claims",
        "extracted per video (`claims_code4AI.jsonl`), never from the video summaries, so a",
        "question cannot leak text that a retriever also indexes.",
        "What the generator saw: claim text, tags, and prior questions only - never the transcript",
        "and never the retriever output (a lexical firewall).",
        "Generation history: factual (Task 4, temporally stratified sample), comparative (Task 5",
        "claim-pair composition, then Task 5.5 semantic-leakage neutralization = composer v2, with a",
        "meta-organizational stop-list applied on topic families), longitudinal (Task 6 dated-thread",
        "composition with a deterministic wording-guard retry and an advisory-only leak sort).",
        "Known couplings and bias direction: the groundable-claim filter is a mixed-instrument cache",
        "(per-video and per-claim prompts; never report a pooled groundable rate without that footnote);",
        "the longitudinal develop-test accepts topic-recurrence 'collections' alongside genuine arcs, so",
        "the 505 pool is low-precision and was human-triaged to 38 keeps before grounding (D65/D66).",
        "Permitted uses: this is the slice scored as the instrument.",
        "Reporting rule: per-tier, never pooled across tiers or across slices.",
        "",
        "## keypoint_derived (legacy, frozen)",
        "",
        "The earlier slice, generated from the Stage 1 video summaries (`query_candidates_{tier}.jsonl`",
        "-> grounded/scored -> `queryset_core`/`queryset_broad`).",
        "Because the summaries are themselves indexable, this slice has a built-in leakage/circularity",
        "coupling: a question written from a summary can echo text the retriever indexes.",
        "Permitted uses: kept frozen as a circularity exhibit and provenance record; NEVER scored as the",
        "instrument.",
        "Reporting rule: reference only; not pooled with claim_derived.",
        "",
        "## external (planned)",
        "",
        "Placeholder for future externally-authored slices (e.g. reviewer- or user-supplied questions)",
        "that would test generalization beyond creator-derived claims. None exist yet.",
        "",
        f"Grounded tiers present at last handoff: {', '.join(present) if present else 'none'}.",
    ]
    (OUT_DIR / "SLICES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _legacy_leak_rate(tier: str) -> float | None:
    path = OUT_DIR / f"query_grounded_{tier}.jsonl"
    if not path.exists():
        return None
    for ln in path.read_text().splitlines():
        o = json.loads(ln)
        if "_meta" in o:
            m = o["_meta"]
            inp = m.get("input") or 0
            return (m.get("dropped", {}).get("leakage", 0) / inp) if inp else None
    return None


def write_prediction_note(summaries: list[dict]) -> None:
    lines = ["# Grounding prediction note (Task 7)", "",
             "Two pre-registered predictions (cc_07 item 5). A failure is a stop-and-investigate signal.",
             ""]
    for s in summaries:
        tier, m = s["tier"], s["meta"]
        inp = m.get("input") or 0
        drop = m.get("dropped", {})
        leak_rate = (drop.get("leakage", 0) / inp) if inp else 0.0
        unans_rate = (drop.get("unanswerable", 0) / inp) if inp else 0.0
        legacy = _legacy_leak_rate(tier)
        lines.append(f"## {tier}")
        lines.append(f"input {inp}; leakage-drop {drop.get('leakage', 0)} ({leak_rate:.1%}); "
                     f"unanswerable-drop {drop.get('unanswerable', 0)} ({unans_rate:.1%}); "
                     f"errors {m.get('grounding_errors', 0)}")
        if legacy is not None:
            verdict = "OK (lower)" if leak_rate <= legacy else "INVESTIGATE (not lower - firewall may have leaked)"
            lines.append(f"(a) leakage vs legacy {legacy:.1%}: {verdict}")
        else:
            lines.append("(a) leakage vs legacy: no legacy grounded file to compare")
        b = "OK (low)" if unans_rate <= 0.20 else "INVESTIGATE (high - possible extractor hallucination)"
        lines.append(f"(b) unanswerable attrition: {b}")
        lines.append("")
    (OUT_DIR / "grounding_prediction_note.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- driver ----------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", nargs="*", choices=TIERS)
    ap.add_argument("--review-file", default=None,
                    help="optional external review JSON keyed by candidate_id+source_claim_ids")
    args = ap.parse_args()

    review: dict = {}
    if args.review_file:
        review = json.loads(Path(args.review_file).read_text())
    claims, videos = load_claim_index()

    wanted = args.tiers or TIERS
    present = [t for t in wanted if (OUT_DIR / f"query_grounded_{t}_claimslice.jsonl").exists()]
    summaries = []
    for tier in present:
        s = render_tier(tier, claims, videos, review)
        summaries.append(s)
        print(f"{tier}: clean {s['clean']} | flagged {s['flagged']} | excluded {s['excluded']} "
              f"-> {tier}_claimslice_handoff.md", flush=True)

    write_slices_md(present)
    if summaries:
        write_prediction_note(summaries)
    print(f"wrote SLICES.md; grounded tiers present: {present}", flush=True)


if __name__ == "__main__":
    main()
