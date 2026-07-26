---
name: gold-editing-longitudinal
description: Edit machine-drafted gold answers for AnswerTrail's longitudinal (how-did-X-evolve) eval questions. Use when reviewing, auditing, or finalizing a gold worksheet such as longitudinal_claim_vs_grounder.md. Claude does the editing and hands the human a short list of yes/no decisions.
---

# Gold editing for longitudinal questions

## The situation, in three sentences

AnswerTrail asks questions like "how did the creator's view of agentic AI
evolve from early 2025 to early 2026?". To grade an answer, we need an
answer key: a short list of things every correct answer must say, each
backed by real quotes from the videos. A model drafts this answer key,
the draft is always flawed in predictable ways, and this file describes
how to fix it.

## Who does what

**Claude edits. The human decides.**

Claude runs the checks below on every question and fixes what is clearly
wrong. When something cannot be settled from the page, Claude does not
guess. It writes the issue down as one specific question with a
recommended answer, like:

> lc-0130, milestone 5: the quotes show the creator describing a paper's
> claim and explicitly refusing to endorse it. My call: this milestone
> puts the paper's words in his mouth, so cut arc point 2. Override?

The human answers yes or no. Aim for zero to three of these flags per
question. Never ask the human to "review the edits" — that pushes the
work back onto them. Ask a decidable question instead.

## The vocabulary (four words)

- A **question** is the eval question itself ("how did his view of X
  evolve?").
- The **trajectory** (the `trajectory_must_say` lines) is a short
  written summary of how the creator's view actually changed. This is
  the heart of the answer key.
- A **milestone** is one dated piece of evidence: a claim from one video
  on one day, with the transcript quotes underneath it.
- A **nugget** is one gradeable item in the final answer key: a stance
  plus the time window when he held it. Every nugget is required — if a
  correct answer does not need to say it, it does not belong in the
  list.

## Where nuggets come from

One rule covers both question tiers:

> **Nuggets come from the text that defines a correct answer, minus
> whatever the question already gives away.**

For a factual question, one claim IS the answer, so nuggets are the facts
in the claim that are not already in the question.

For a longitudinal question, no single claim is the answer. The answer
is a pattern across many claims, and the trajectory lines are the
written form of that pattern. So nuggets come from the trajectory lines,
after subtracting what the question hands out for free: the topic, the
overall time span, and the bare fact that something changed.

What survives the subtraction, and therefore earns credit:

- **stance + window**: what he thought, and during which stretch. The
  question names the endpoints of the whole span, but not where the
  turns happen inside it — so the internal timing is still earnable.
- **triggers**: what caused each turn, when the videos show it.
- **specifics**: memorable details like "he put the ceiling at 30%"
  usually do NOT become nuggets. They stay in the milestones as
  evidence. A specific is promoted to a nugget only if no correct
  answer could omit it.

**Milestones are never turned into nuggets directly.** A milestone is
one sample of a stance on one day, not the stance itself. If we made
nuggets from milestones, a stance the creator repeated in four videos
would become four duplicate nuggets, and a milestone that misquotes him
would walk straight into the answer key. Both of these actually happened
in the lc-0130 draft. Milestones have one job: to prove the trajectory
lines. Trajectory lines have one job: to be the rubric.

One caution that follows from this: the trajectory is a summary written
by a model, one step further from the transcripts than a claim is. It
can be wrong in ways no single quote reveals — the wrong voice, or a
smooth story drawn through thin evidence. That is exactly why this
editing procedure exists.

## The procedure

### Step 1 — run the audit script

```
python3 scripts/audit_gold.py <worksheet.md> --plot coverage.png
```

Run it, do not read it. It prints one line per question with mechanical
warnings (explained inside the script), and the plot shows each
question's evidence as dots on a timeline, so gaps are visible at a
glance. Edit the questions with the most warnings first.

### Step 2 — edit each question

Work from the page. Every milestone carries its transcript quotes, and
those quotes are the evidence — the full transcripts are not needed.
For each question, run these checks in order:

**a. Voice check — always first, because it can invalidate everything
else.** For each milestone ask: is this the creator's own opinion, or is
he describing what a paper says? The quotes usually tell you. Phrases
like "the authors say", "they argue", or "I would not stress this part"
mean it is the paper talking, not him. A milestone that presents a
paper's claim as his opinion is wrong for a question about *his* view.
Fix it or cut it. If his own position is genuinely unclear, flag it.

**b. Orphan check.** Every milestone must support some trajectory line.
A milestone that is true but supports nothing is an orphan — cut it.

**c. Granularity check, in both directions.**
A trajectory line can be too narrow: it quotes one specific argument he
made ("agents can't resolve LLM incoherence") when the real point is the
stance behind it ("he turned skeptical"). The stance is the nugget;
the specific wording stays in the milestone where it already lives.
A line can also be too broad: one long sentence bundling four separate
findings. Split it, because each piece must be markable as hit or miss
on its own. Rule of thumb: if you cannot answer "did the answer say
this?" with a plain yes or no, the line needs splitting.

**d. Coverage check.** Every nugget needs at least one milestone
whose quotes support it. The script finds gaps in *time*; this check
finds gaps in *evidence*. If a nugget has none, the missing milestone is
a reason to SEARCH, never a reason to cut on its own. Search the whole
chunk store — the entire database, not just the videos already in the
worksheet (the draft already picked its videos; the proof is often in
one it never sampled). Topic words plus a date filter. If evidence
exists, add it as a new milestone. Only if the corpus truly does not
contain it, cut the nugget — we cannot grade what we cannot cite.

**e. Overclaim check.** Words like "repeatedly", "consistently",
"throughout" claim more than dated samples can prove. Milestones show
what he said on particular days, not the space between. Prefer "held X
during [window]".

**f. Shift nugget.** Every question gets one nugget saying: the answer
must describe the change itself, not just each period separately.
Two exceptions:
- If the question is waypoint-flagged (its own wording gives the arc
  shape away, e.g. "...as he moved from reporting to critiquing..."),
  the shift is free and this nugget earns nothing. Prefer rewording the
  question to neutral form; if the waypoint phrasing is the only way to
  identify the topic, skip the shift nugget and note why.
- If editing collapses the arc to a single stance — his view did not
  actually change over the period — use the mirror instead: a
  **no-change nugget** ("the answer states his view stayed consistent
  across the period, rather than inventing an evolution"). This matters
  because the question's wording presupposes change, so weak answers
  will fabricate one; the no-change nugget is what catches that.

**g. Milestone tags.** Give every surviving milestone a `supports: n2`
style tag naming the nugget it proves. This makes the coverage check
mechanical next time.

### Step 3 — hand over the flags

Collect all unresolved calls into one list for the whole worksheet, each
written as a single decidable question with a recommendation. Wait for
the rulings, apply them, and the gold is final. Tag it with a version
(`gold-v1.0`).

### Step 4 — keep the gold alive (after the eval starts running)

When an agent run cites a quote that genuinely supports a nugget, add
that quote to the nugget's evidence list — evidence lists are open.
When a run asserts a stance the gold does not contain, that is a flag
for the human: either the gold missed a real point (add it, bump the
version) or the agent made it up (count it against the run). Claude
recommends; the human rules. The nugget list itself never changes
without a human decision — if the system being graded could edit its own
answer key, the eval would stop meaning anything.

## How this gold gets scored (so the editor knows what it is for)

Each question's nuggets form one flat list. An automatic judge reads an
agent's answer and marks each nugget hit or miss. Recall = hits divided
by total. Four content nuggets plus one shift nugget, all expressed:
5/5 = 100%.

- Content nuggets are checked as facts: "does the answer say he was
  optimistic in early 2025?"
- The shift nugget is checked as a connection: "does the answer say his
  view *changed*, rather than describing each period separately?" Its
  mirror, the no-change nugget (used when the arc collapsed to one
  stance), is checked the same way: "does the answer say his view
  stayed consistent, rather than inventing an evolution?"
- Waypoint questions have no shift nugget, so their denominator is
  smaller. That is fine; recall is per-question.
- The shift nugget's hit/miss is also logged as its own boolean per
  run. Reason: answers that hit all content nuggets but miss the shift
  are a pure synthesis failure (the facts were found, the connection
  was not written), which points at the answering prompt rather than at
  retrieval.

This is why every nugget must be markable with a plain yes or no — the
judge cannot score a line that cannot be answered that way. That
requirement drives the granularity check above.

## The gold is done when

- every nugget states a stance, has a date window, and has at least
  one supporting quote on the page;
- there is exactly one shift nugget, or a note explaining why not;
- every milestone carries a `supports:` tag and no orphans remain;
- no trajectory line copies chunk wording, bundles several claims, or
  overclaims its coverage;
- every voice question is either resolved or flagged — never guessed;
- the flag list has been delivered and ruled on.

## Known pitfalls

Real defects found in real worksheets. Do not pad this list with
hypothetical entries; add one only when a new defect actually occurs,
with the question id where it happened.

1. **The paper's voice in the creator's mouth** (lc-0130 m5). He
   described a paper's emergent-intelligence claim and explicitly
   declined to endorse it; the draft recorded it as his view and built a
   whole arc point on it. The disproving quote was in the same record.
   This is why the voice check runs first.
2. **Orphan milestone** (lc-0011 m5). A true statement about
   architecture that supported no arc point, padding the milestone count
   without adding evidence.
3. **Stance fused with wording** (lc-0011). An arc line hard-coded one
   specific argument, so an answer expressing the same stance through a
   different argument he also made would have been scored a miss.
4. **Mega-line** (lc-0130). One arc line bundling four separate
   findings — impossible to mark hit or miss cleanly.
5. **Missing shift nugget** (all early drafts). Nothing required the
   answer to describe the change, so two disconnected period summaries
   could score full marks.
6. **Evidence hole mid-span** (20 of 37 questions, 2026-07 worksheet).
   Milestones cluster at the endpoints; the middle of the story is
   asserted but unproven. The audit script now catches this.
7. **A global milestone minimum hides per-nugget gaps** (lc-0011). The
   worksheet required two milestones per question and passed, while half
   the arc had zero evidence. The count that matters is per nugget.
8. **Overclaiming words** (lc-0130 and two others). "Repeatedly ...
   through January 2026" on four dated samples. The script now flags
   these words; the fix is milder wording or more evidence.
9. **"No milestone" read as "cut"** (lc-0011, second sweep). A true
   nugget (mid-2025 tempering) was dropped because it had no milestone —
   but the evidence existed in the chunk store, in a video the draft
   never sampled (bPbkT7MtwGE). The rule is: a missing milestone means
   search the store; only a missing corpus means cut. The coverage
   check above now says this explicitly.
10. **Trusting an advisory tag over the wording on the page**
   (lc-0260). The pipeline tagged the question hint=waypoint, but the
   actual wording was neutral — topic and span only, no arc shape. The
   agent correctly overruled the tag by reading the question. Advisory
   tags are hints to check, never rulings; the text decides.

## Files in this skill

- `SKILL.md` — this file.
- `scripts/audit_gold.py` — the mechanical checks and the timeline
  plot. Run it; reading it is never necessary (it is commented for
  humans who want to anyway).
