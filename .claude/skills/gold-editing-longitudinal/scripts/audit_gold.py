#!/usr/bin/env python3
"""Mechanical audit of a longitudinal gold worksheet.

Usage:
    uv run python audit_gold.py <worksheet.md>
    uv run python audit_gold.py <worksheet.md> --plot coverage.png

What this script does, in plain words
-------------------------------------
The worksheet contains one section per eval question. Each section has:
  - the question text,
  - an "advisory" line produced by the generation pipeline
    (risk / hint / leak numbers),
  - the trajectory lines (the drafted summary of how the creator's view
    changed),
  - dated milestones (evidence: one claim from one video on one day).

This script reads all of that and prints, for every question, the
warnings that can be detected *mechanically* — without understanding the
content. The judgment-heavy checks (voice, orphans, granularity) are
done by Claude following SKILL.md; this script just finds the problems a
regex and a calendar can find:

  1. COVERAGE HOLE   - a long stretch of the time span with no evidence
                       at all (e.g. 8 empty months in a 12-month story).
  2. ENDPOINT-ONLY   - all the evidence sits at the start and end of the
                       span; the middle of the story is asserted but
                       unproven.
  3. SINGLE-VIDEO END- the start (or end) of the story rests on quotes
                       from just one video, so one bad quote collapses
                       that whole end.
  4. NOT RE-FOUND    - the pipeline's grounder failed to independently
                       re-find a milestone's quote; a hint the quote is
                       hard to retrieve.
  5. WAYPOINT        - the question's own wording gives away the shape
                       of the answer ("...as he moved from X to Y...").
  6. LEAK            - pipeline-computed overlap between the gold and
                       the question; high values mean the answer key
                       gives credit for repeating the question.
  7. COPIED WORDING  - a trajectory line reuses a long run of words from
                       a transcript quote, i.e. it is a quotation
                       pretending to be a summary.
  8. MEGA-LINE       - a trajectory line so long it clearly bundles
                       several separate claims.
  9. OVERCLAIM WORDS - "repeatedly", "throughout", etc. in a trajectory
                       line: dated samples cannot prove continuity.

With --plot it also draws one row per question, one dot per milestone
date, so the holes of warning 1 and 2 are visible at a glance. Rows
with any warning are drawn in red.
"""
import re
import sys
from datetime import date

# Words in a trajectory line that claim continuous behavior. Milestones
# are dated samples; they prove what was said on particular days, not
# the space between. See SKILL.md, overclaim check.
OVERCLAIM_WORDS = ("repeatedly", "consistently", "throughout", "always",
                   "constantly", "continuously")

# A trajectory line longer than this many words almost always bundles
# several separate claims into one sentence (SKILL.md, granularity check).
MEGA_LINE_WORDS = 45

# If a trajectory line shares a run of at least this many consecutive
# words with a transcript quote, it is copying the quote's wording
# rather than summarizing the stance.
COPIED_RUN_WORDS = 7


def parse(path):
    """Read the worksheet into a list of question dictionaries.

    The worksheet format is markdown with '## lc-XXXX' headings. We split
    on those headings and pull out the pieces of each section with
    regular expressions. Nothing clever: the format is regular enough
    that regex is fine.
    """
    text = open(path, encoding="utf-8").read()

    # Split into (id, body, id, body, ...) pairs. [1:] drops whatever
    # precedes the first question heading.
    sections = re.split(r"^## (lc-\d+)\s*$", text, flags=re.M)[1:]

    questions = []
    for qid, body in zip(sections[0::2], sections[1::2]):
        q = {"id": qid}

        m = re.search(r"\*\*question:\*\* (.+)", body)
        q["question"] = m.group(1).strip() if m else ""

        # The advisory line looks like:  risk=low  hint=neutral  leak=0.1 ...
        # Turn it into a small dict.
        m = re.search(r"\*\*advisory:\*\* (.+)", body)
        q["advisory"] = dict(re.findall(r"(\w+)=([\w.\-]+)", m.group(1))) if m else {}

        # The trajectory block: consecutive '- ' bullet lines right after
        # the trajectory_must_say heading.
        arc = re.search(r"\*\*trajectory_must_say[^\n]*\n((?:- .+\n)+)", body)
        q["arc"] = [l[2:].strip() for l in arc.group(1).splitlines()] if arc else []

        # Milestones: '### m1  2025-02-22  claim `VIDEO#cNNN`' followed by
        # a '**statement:**' line.
        q["milestones"] = []
        for mm in re.finditer(
            r"### (m\d+)\s+(\d{4}-\d{2}-\d{2})\s+claim `([^`]+)`\n"
            r"\*\*statement:\*\* (.+)", body
        ):
            q["milestones"].append({
                "id": mm.group(1),
                "date": date.fromisoformat(mm.group(2)),
                "video": mm.group(3).split("#")[0],   # video id before '#'
                "statement": mm.group(4).strip(),
            })

        # How many quotes the grounder failed to independently re-find.
        q["not_refound"] = len(re.findall(r"\[not re-found\]", body))

        # All transcript quote texts in the section, for the
        # copied-wording check.
        q["chunks"] = [c.strip() for c in
                       re.findall(r"- `[^`]+` \[[^\]]+\]\s+(.+)", body)]

        questions.append(q)
    return questions


def longest_common_run(a, b):
    """Longest run of consecutive words appearing in both strings.

    Used for the copied-wording check: a shared run of 7+ words means
    the trajectory line lifted the quote's phrasing.
    """
    aw, bw = a.lower().split(), b.lower().split()
    best = 0
    for i in range(len(aw)):
        for j in range(len(bw)):
            k = 0
            while i + k < len(aw) and j + k < len(bw) and aw[i + k] == bw[j + k]:
                k += 1
            best = max(best, k)
    return best


def audit(q):
    """Run the mechanical checks on one question; return (milestones, flags)."""
    flags = []
    ms = sorted(q["milestones"], key=lambda m: m["date"])
    dates = [m["date"] for m in ms]

    if len(dates) >= 2:
        span = (dates[-1] - dates[0]).days
        gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]

        # Warning 1: one gap covering more than half the span (and at
        # least ~4 months) means a stretch of the story has no evidence.
        biggest = max(gaps)
        if span > 0 and biggest > 0.5 * span and biggest > 120:
            i = gaps.index(biggest)
            flags.append(f"coverage hole: {biggest} days empty between "
                         f"{dates[i]} and {dates[i+1]}")

        # Warning 2: for spans over ~8 months, is there any milestone
        # that is NOT within 60 days of either endpoint? If not, all the
        # evidence sits at the edges.
        mid = [d for d in dates
               if (d - dates[0]).days > 60 and (dates[-1] - d).days > 60]
        if span > 240 and not mid:
            flags.append("endpoint-only evidence: no milestone in the "
                         "middle of the span")

        # Warning 3: do all milestones near the start (or end) come from
        # a single video? Then that whole end of the story hangs on one
        # source.
        for end, name in ((dates[0], "start"), (dates[-1], "end")):
            vids = {m["video"] for m in ms
                    if abs((m["date"] - end).days) <= 30}
            if len(vids) == 1 and span > 240:
                flags.append(f"single-video {name}: the {name} of the arc "
                             f"rests on one video ({vids.pop()})")

    # Warning 4: quotes the grounder could not independently re-find.
    if q["not_refound"]:
        flags.append(f"{q['not_refound']} chunk(s) [not re-found] "
                     f"by the grounder")

    # Warnings 5 and 6 come straight from the pipeline's advisory line.
    adv = q["advisory"]
    if adv.get("hint") == "waypoint":
        flags.append("question hints the arc shape (waypoint): "
                     "answers get the trajectory for free")
    if float(adv.get("leak", 0)) >= 0.1:
        flags.append(f"leak={adv['leak']}: arc or question may copy "
                     f"chunk wording")

    # Warnings 7-9: per trajectory line.
    for a in q["arc"]:
        hits = [w for w in OVERCLAIM_WORDS if w in a.lower()]
        if hits:
            flags.append(f"arc line overclaims ('{hits[0]}'): milestones "
                         f"prove sampled dates, not the space between: "
                         f"\"{a[:60]}...\"")
        if len(a.split()) > MEGA_LINE_WORDS:
            flags.append(f"arc line bundles several claims "
                         f"({len(a.split())} words): \"{a[:60]}...\"")
        for c in q["chunks"]:
            if longest_common_run(a, c) >= COPIED_RUN_WORDS:
                flags.append(f"arc line copies chunk wording: "
                             f"\"{a[:60]}...\"")
                break
    return ms, flags


def main():
    path = sys.argv[1]
    plot_path = None
    if "--plot" in sys.argv:
        plot_path = sys.argv[sys.argv.index("--plot") + 1]

    rows = []
    for q in parse(path):
        ms, flags = audit(q)
        rows.append((q, ms, flags))

        dates = [m["date"] for m in ms]
        span = f"{dates[0]} .. {dates[-1]}" if dates else "no dated milestones"
        print(f"{q['id']}  arc={len(q['arc'])}  milestones={len(ms)}  "
              f"{span}  flags={len(flags)}")
        for f in flags:
            print(f"    ! {f}")

    flagged = sum(1 for _, _, f in rows if f)
    total = sum(len(f) for _, _, f in rows)
    print(f"\n{len(rows)} questions, {flagged} with at least one flag, "
          f"{total} flags total")

    if plot_path:
        # One horizontal row per question, one dot per milestone date.
        # Red rows have at least one warning. The visual point: most
        # drafts show two clusters of dots with a gap in the middle —
        # the endpoint-sampling signature.
        import matplotlib
        matplotlib.use("Agg")            # no display needed; write a file
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(11, 0.32 * len(rows) + 1.5))
        for y, (q, ms, flags) in enumerate(rows):
            dates = [m["date"] for m in ms]
            color = "#c0392b" if flags else "#2c7fb8"
            if dates:
                ax.plot(dates, [y] * len(dates), "o-", ms=4, lw=0.8,
                        color=color)
            ax.text(date(2024, 12, 1), y, q["id"], ha="right",
                    va="center", fontsize=7)
        ax.set_yticks([])
        ax.invert_yaxis()                # first question at the top
        ax.set_title("Milestone coverage per question "
                     "(red = has at least one audit flag)")
        fig.tight_layout()
        fig.savefig(plot_path, dpi=150)
        print(f"plot written to {plot_path}")


if __name__ == "__main__":
    main()
