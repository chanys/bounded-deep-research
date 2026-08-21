"""Two-sided guard regression for text_guards (Task 6 spec item).

The longitudinal tier must ALLOW creator-stance phrasing - trajectory questions are
inherently about the creator's evolving position - while still BANNING video/corpus
navigation. These tests pin both directions so a future edit to meta_reference cannot
silently make the longitudinal tier permissive to navigation refs, nor punitive to the
creator phrasing that tier needs. The comparative contrasts confirm the tier gate itself.
"""
from eval.text_guards import meta_reference, violation_scan


def test_longitudinal_allows_creator_stance():
    q = "How has the creator's assessment of inference-time compute changed over time?"
    assert violation_scan(q, "longitudinal") == []


def test_longitudinal_bans_video_navigation():
    q = "In the previous video, how did the results on the elevator test evolve?"
    hits = violation_scan(q, "longitudinal")
    assert "corpus_nav" in hits
    assert "video_ref" in hits


def test_comparative_bans_creator_reference():
    # the SAME creator phrasing is banned for comparative (tier gate active)
    q = "How does the creator's GRPO setup compare to their DPO setup?"
    assert "creator_ref" in violation_scan(q, "comparative")


def test_bare_temporal_allowed_longitudinal_banned_comparative():
    q = "How has the model's benchmark performance developed since it was previously measured?"
    assert "temporal_nav" not in meta_reference(q, "longitudinal")
    assert "temporal_nav" in meta_reference(q, "comparative")
