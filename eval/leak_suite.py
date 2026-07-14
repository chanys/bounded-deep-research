"""Human-adjudicated regression suite for the comparative leak/audit instrument.

Ground truth from three review passes (two external, one internal). A TWO-SIDED calibration
set: positive cases (content that must be flagged) AND negative controls (clean questions that
must NOT be flagged). A suite with only positive cases measures recall, never precision - an
"always fire" classifier passes it - which is exactly how the corrected v2.1 instrument slipped
through before the negative controls existed. Any future instrument must reproduce BOTH sides.

This set is FROZEN as a calibration benchmark. Do not tune a prompt against it: a prompt hammered
into agreeing with these known items has memorized the suite, not learned the boundary.

Label kinds:
  leak_side     -> the leak classifier must return leaked_side != "none" (content disclosed).
  leak_none     -> negative control: the leak classifier must return leaked_side == "none" (clean).
  status        -> the audit must assign this primary final_status.
  status_any    -> the audit status (or advisory invalid_original_axis) must be one of these.
  must_not_pass -> the audit must NOT assign "pass".
"""

SUITE: dict[str, dict] = {
    "cc-0003": {"status": "gold_insufficient"},   # asks for GLM-5's approach; claim B has only a step count
    "cc-0007": {"must_not_pass": True},            # axis/gold - must not pass
    "cc-0013": {"status": "gold_insufficient"},
    "cc-0016": {"status": "subject_unnameable"},   # generic descriptor counts as unnamed
    "cc-0017": {"status": "subject_unnameable"},
    "cc-0011": {"leak_side": True},
    "cc-0024": {"leak_side": True},
    "cc-0029": {"leak_side": True},
    "cc-0031": {"leak_side": True},
    "cc-0035": {"leak_side": True},
    "cc-0040": {"leak_side": True},
    "cc-0022": {"status_any": ["two_factuals", "invalid_original_axis"]},   # invalid_original_axis is advisory
    "cc-0036": {"status": "unneutralizable"},
    "cc-0037": {"status": "unneutralizable"},
    # Negative controls (clean questions - name only subjects + a neutral/technical axis, disclose no
    # side's value or mechanism). The corrected instrument false-fired "both" on all three: precision failure.
    "cc-0026": {"leak_none": True, "label_source": "human_adjudicated"},   # "what loss does each optimize" - axis only
    "cc-0032": {"leak_none": True, "label_source": "human_adjudicated"},   # score-gap comparison, no values stated
    "cc-0033": {"leak_none": True, "label_source": "human_adjudicated"},   # score-gap comparison, no values stated
}


def check_case(label: dict, *, leaked_side: str, status: str, invalid_axis: bool) -> tuple[bool, str]:
    """(passed, detail) for one suite candidate given the instrument's pre-override outputs."""
    if "leak_side" in label:
        return leaked_side != "none", f"leaked_side={leaked_side} (want != none)"
    if "leak_none" in label:
        return leaked_side == "none", f"leaked_side={leaked_side} (want none)"
    if "must_not_pass" in label:
        return status != "pass", f"status={status} (want != pass)"
    if "status" in label:
        return status == label["status"], f"status={status} (want {label['status']})"
    if "status_any" in label:
        opts = label["status_any"]
        ok = status in opts or (invalid_axis and "invalid_original_axis" in opts)
        return ok, f"status={status} invalid_axis={invalid_axis} (want in {opts})"
    return True, ""
