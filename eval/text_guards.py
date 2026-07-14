"""Deterministic wording guards shared across composition tasks (Tasks 5 and 6).

Permanent standing guards. `completeness_assert` and `stilted_opener` are identical
across tiers; `meta_reference` is tier-conditional at the TIER level per committed cc_06
(comparative bans creator AND video/corpus references; longitudinal allows creator
references - stance arcs need them - but still bans video/corpus-navigation).
"""
from __future__ import annotations

import re

# Question-initial topic-marker preambles ("In terms of X, how...") - stilted throat-clearing.
STILTED_OPENERS = ("in terms of", "when it comes to", "regarding", "with respect to",
                   "as for", "on the topic of", "in the context of", "as far as")
_STILTED = re.compile(r"^\W*(?:" + "|".join(re.escape(o) for o in STILTED_OPENERS) + r")\b[^,?]*,", re.I)

_CORPUS_NAV = re.compile(r"\b(?:previous video|earlier video|the second paper|this video|these videos|the other video)\b", re.I)
_VIDEO = re.compile(r"\bvideos?\b", re.I)
_UNNAMED = re.compile(r"\bunnamed\b", re.I)
_CREATOR = re.compile(r"\bcreator'?s?\b", re.I)
_TEMPORAL_NAV = re.compile(r"\b(?:previously|earlier)\b", re.I)


def stilted_opener(q: str) -> bool:
    """True if the question opens with a topic-marker preamble followed by a comma.
    Mid-sentence occurrences do not fire (question-initial only)."""
    return bool(_STILTED.match(q))


def meta_reference(q: str, tier: str) -> list[str]:
    """Banned reference kinds present in the question, by tier."""
    hits: list[str] = []
    if _CORPUS_NAV.search(q):
        hits.append("corpus_nav")
    if _VIDEO.search(q):
        hits.append("video_ref")
    if _UNNAMED.search(q):
        hits.append("unnamed_ref")
    if tier == "comparative":              # longitudinal allows creator + bare temporal
        if _CREATOR.search(q):
            hits.append("creator_ref")
        if _TEMPORAL_NAV.search(q):
            hits.append("temporal_nav")
    return hits


def violation_scan(q: str, tier: str) -> list[str]:
    """All deterministic wording violations for a tier (meta references + stilted opener)."""
    v = meta_reference(q, tier)
    if stilted_opener(q):
        v.append("stilted_opener")
    return v


def completeness_assert(input_ids: list[str], output_ids: list[str]) -> None:
    """Hard pipeline invariant: output ids equal input ids exactly - no missing, no extra,
    no duplicates, one row per input candidate. Raise before any render/write proceeds."""
    dup = sorted({x for x in output_ids if output_ids.count(x) > 1})
    missing = sorted(set(input_ids) - set(output_ids))
    extra = sorted(set(output_ids) - set(input_ids))
    if dup or missing or extra or len(input_ids) != len(output_ids):
        raise AssertionError(f"completeness violation: missing={missing} extra={extra} "
                             f"duplicates={dup} n_in={len(input_ids)} n_out={len(output_ids)}")
