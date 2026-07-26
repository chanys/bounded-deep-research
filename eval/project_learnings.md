# Project learnings: AnswerTrail evaluation

Running log. Each entry is a claim, the incident that produced it, and
what it generalizes to. Updated at phase boundaries, not continuously -
the build log captures decisions as they happen; this file is the
distillation.

## The bar for getting in here

A learning belongs here only if it came from something that actually
went wrong or actually surprised us, and only if the incident is
recoverable - a question id, a number, a date. Generic advice does not
qualify. This is the same rule as the skill's known-pitfalls section,
applied one level up: no speculative entries.

---

## Measurement design

### 1. A metric can punish an answer for being right a different way

**What happened.** The first end-to-end run on lc-0011 produced an
answer I judged clearly good on reading it. Scored by chunk overlap
against the gold's milestone chunks, it recovered 1 of 7 and would have
scored about 14%. It had rebuilt the same trajectory from a different,
still-valid set of videos.

**The fix.** Score at the answer level: does the answer express the
things a correct answer must say, regardless of which evidence it used.
Groundedness is checked separately, per claim, against what the agent
actually retrieved.

**Generalizes to.** When multiple valid routes lead to the same
conclusion, the metric must grade the destination and verify the route
independently - not match the route against a canonical path. This is
the Pyramid/content-unit idea from summarization evaluation, arrived at
from the other direction.

### 2. The same failure recurs one level up, and is harder to see there

**What happened.** After moving to answer-level nuggets, the first gate
run scored a good lc-0024 answer at 0.4. The gold required two specific
mid-2025 stances; the agent proved the same turn with two different real
mid-2025 stances from other videos. Same disease as #1, but now inside
the nugget list rather than in the chunk matching.

**The fix.** Nuggets must be route-independent: start stance, turning
points, end stance, and the shift itself, each with a time window.
Anything that is one more sample inside an established stretch is
evidence, not a requirement. Test: could a correct answer, taking a
different route through the corpus, omit this and still tell the same
story?

**Generalizes to.** Fixing a metric at one level of abstraction does not
immunise the level above it. Re-run the same question against the new
design.

### 3. Do not build an instrument whose target has no ground truth

**What happened.** The plan briefly had two judges: an alignment judge
(is this nugget expressed?) and a quality judge scoring conciseness,
cohesion, narrative. The second was dropped before it was built.

**Why.** "Is nugget n2 expressed in this answer" has a fact of the
matter a human can also decide, so it can be calibrated. "Is this answer
cohesive, 1-5" anchors to somebody's taste and is known to suffer
verbosity and position bias. With one frozen system there is also no
comparison for it to drive.

**Generalizes to.** Prefer checkable proxies over rubric scores. Some
quality dimensions had ground truth and were kept: the shift nugget is
the narrative check, the date windows are the ordering check, the
unsupported-claim rate is the discipline check.

### 4. Calibration effort should follow error propagation, not effort

**What happened.** Three prompts run in this pipeline. Only one is
formally calibrated.

**The reasoning.** A judge error goes straight into a reported score,
one for one, roughly 180 times per run, unreviewed. An extractor error
passes through the judge and then through averaging before it reaches a
number, so it arrives shrunk. The gold-side extractor's output is read
by a human before it becomes gold, so review substitutes for
calibration entirely.

**Generalizes to.** Calibrate what is consumed without review. Inspect
what is reviewed. The one thing an inspection pass must look for beyond
individual errors is whether the errors have a *pattern* - random errors
wash out in an average, systematic ones do not.

### 5. A bundled requirement forces the judge to invent a middle category

**What happened.** The gate's judge emitted a "plausible" verdict worth
0.5, which nobody designed. It appeared on a nugget that required two
things at once ("the revolution stalled" AND "the SWE narrative did not
materialise"). The answer said the first only.

**The fix.** Split the nugget; keep verdicts binary. Every gold item
must be markable hit or miss with a plain yes or no, or the judge cannot
score it.

**Generalizes to.** When a grader starts inventing partial credit, look
at the rubric item, not the grader.

---

## Gold construction

### 6. Do not let the system under test write its own answer key

**What happened.** Comparing a single-pass gold draft against a ReAct
agent's answer on the same question: the agent had better coverage
(nine citations across five videos, and it filled a ten-month evidence
hole the draft had missed), but it silently dropped an entire arc point
while producing fluent, well-cited prose. The weaker gold caught the
stronger agent's blind spot.

**The rule that came out of it.** Evidence lists are open - a run may
contribute a supporting quote, subject to a human check. The nugget list
is closed - only a human ruling changes what the answer key requires.

**Generalizes to.** Two flawed processes with uncorrelated failures beat
either one promoted to oracle. This is also the reason not to regenerate
gold with the best available model: its blind spots would become the
definition of correct.

### 7. Wrong gold and incomplete gold are not the same risk

**What happened.** On lc-0014 the agent told a story that contradicted
the gold arc and was backed by real quotes. The gold said he hardened
into dismissing AGI; the agent said he dismissed the marketing while
retaining scientific AGI as a distant goal. Both threads were real; the
gold's arc was one-sided.

**Why the distinction matters.** Incomplete gold only deflates recall -
the eval errs conservative, which is acceptable and disclosable. Wrong
gold asserts a falsehood and punishes every correct answer that
disagrees. So: a run may expose gold that is wrong (repair it, with a
ruling); a run does not expand gold that is merely incomplete.

**Generalizes to.** Know the direction of your instrument's bias.
"Missing items can only deflate the score, never inflate it" is a
defensible sentence; "my gold is complete" is not.

### 8. Build the eval before the system is frozen, and derive requirements from the corpus only

**What happened.** Gold construction ran for weeks while the agent was
still changing. Late in that period the agent's read tool was removed as
redundant - a change to its action space and therefore to what evidence
it surfaces. Because no nugget had ever been derived from agent output,
nothing in the gold needed revisiting.

**Generalizes to.** Two separate points, and the second is the load
bearing one. Scheduling: the eval is the long pole and blocks nothing,
so it should start first and run in parallel. Independence: requirements
must derive from the corpus and the question, never from any system's
output - otherwise a moving system silently reshapes a fixed ruler.
Timing is a practical safeguard for a discipline you have to hold
anyway.

A bonus effect worth naming: reasoning hard about what evidence a good
answer needs is itself a design review of the system, conducted from
the outside. The read-tool redundancy became visible that way.

### 9. Guideline revision is convergence, not churn

**What happened.** The nugget definition was revised three times:
draft arcs to stance-level nuggets (after the first edit sweep found
voice errors and fused specifics), two weight classes to one (after the
distinction proved too granular for any decision it served), and
stance-level to turning-point (after the gate showed valid alternative
routes being punished). Each revision was forced by contact with real
output, versioned, and given a written motivation.

**Generalizes to.** This is annotation guideline development, and pilot
rounds are how the field has always done it. The revision history is
evidence of instrument development, not instability - provided each step
is tied to measured evidence rather than taste.

---

## Process and tooling

### 10. Push each decision to the most durable place that can hold it

**The hierarchy.** A chat instruction lasts one session. Prose in a
skill file lasts across sessions but must be re-read and re-applied
correctly each time. A check in a script executes identically forever.

**What happened.** The audit script flagged every shift nugget as a
"bundled" line, because shift nuggets legitimately summarise a whole
arc and are therefore long. The fix could have been an instruction to
ignore those warnings. Encoding it in the script instead removed nine
false positives - and three genuine bundles that had been hidden inside
the noise became visible immediately.

**Generalizes to.** Fix the instrument rather than teaching everyone to
squint through it. Reserve prose for judgments that have no mechanical
test - "is this a turning point or a waypoint" cannot be a string
match, so it stays in prose.

### 11. Every edge case invites an apparatus; most do not deserve one

**What happened.** The question "what if an agent's answer contradicts a
gold nugget" produced a design for an automatic contradiction detector -
an extra judge call on missed nuggets, a review log, a grounded-versus-
ungrounded split. It was cut before implementation. Reading the
lowest-scoring questions finds contradictions for free, and that reading
happens anyway.

**Generalizes to.** The failure mode of careful design discussion is
that each edge case gets a mechanism and the mechanisms become the
project. Before building, ask what the existing analysis already
surfaces.

### 12. Written procedure survives; conversation does not

**What happened.** The gold-editing procedure was captured as a skill -
a document plus an audit script - rather than as instructions per
session. When the procedure changed mid-sweep, the change had to be
applied by hand to work already done, because a skill describes a
procedure and not a to-do list. That gap between "rules changed" and
"work already done under the old rules" is a versioning problem the
format does not solve.

**Generalizes to.** Anything a future session needs must be in a file,
including the reasoning, or it gets re-litigated. And when the file
changes mid-flight, reconciliation of already-done work is a separate,
manual step.

---

## Which of these to use where

**Interview, primary exhibit:** #1 and #2 together, told as one story -
a metric disagreeing with human judgment twice, at two levels of
abstraction, each time diagnosed and fixed with a falsifiable rule and
a validating re-score. The full script is in
`gold_methodology_presentation_notes.md`.

**Interview, strong second:** #6 and #8 - why the system under test does
not write its own answer key, and why the eval was built before the
agent was frozen. These land well because most teams have done the
opposite and know it.

**Interview, answers to specific probes:**
- "How do you know your gold is complete?" -> #7
- "Why not calibrate everything?" -> #4
- "Isn't all this revision a sign of instability?" -> #9

**Blog material:** #10 and #12 are about skills and tooling rather than
evaluation, and belong with the Skills article rather than the eval
write-up.

**Not for interviews:** #11 is honest and useful but it is a story about
avoiding work, which needs the right audience to land well. Keep it for
the write-up's methodology section, where restraint reads as judgment.
