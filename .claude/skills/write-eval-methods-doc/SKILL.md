---
name: write-eval-methods-doc
description: Write or condense an evaluation methodology document from the eval artifacts and code. Two modes - a detailed methods reference, or a concise README section derived from it. Use when turning eval build logs, gold sets, prompts, and run results into a reader-facing write-up in the project house style.
---

# Writing evaluation methodology documents

## When to use this

Use this when the task is to explain, for a reader, how some part of the evaluation works or what it found: how the gold was built, how scoring works, what an experiment showed.
There are two modes, and a document is usually one or the other:

- **Detailed reference** - the full methods record, written like a paper with an inline appendix. Keeps pseudocode, worked examples, and the verbatim prompts (pushed to an appendix).
- **Concise README section** - a condensed version of a detailed reference, for a repo README or a blog. Omits pseudocode and the appendix, trims tables, and inlines short prompt snippets with links to source.

Both modes share everything in "Grounding," "Voice and flow," and "Presenting evidence" below; they differ only in "The two modes."

## Who does what

Claude drafts from the artifacts and code; the human reviews and rules on what to include.
Draft to a file, then surface it section by section for review before treating it as done - do not dump the whole thing and ask "is this good."
Gate any expensive downstream step (a big table, a full appendix, a second document) on a cheap human look at a sample first, so a style or inclusion problem is caught while it is still a quick fix.

## Grounding (non-negotiable)

Every number, example, prompt, and file path comes from the real artifacts or code, never from memory or invention.
In practice:

- Pull statistics by computing them from the actual run files or gold files, not by recalling them.
- Pull prompt text and symbol line numbers by grepping the code, and link to them.
- Pull worked examples (claim ids, nugget text, judge reasons) verbatim from the artifacts.
- If a fact cannot be traced to an artifact, do not state it. Verify before writing, not after.

## Voice and flow

This is the rule most often gotten wrong, so it is first.
Write in an academic-paper register - precise, measured, every number stated as measured - **but the document must read as connected prose, not a list of facts.**
A first draft almost always comes out as disconnected sections and disconnected sentences; that draft is not done.

- After the first draft, do a dedicated **transitions pass**: every section must open by handing off from the previous one, and within a section each paragraph should follow from the last. If two paragraphs could be swapped without the reader noticing, the connective tissue is missing.
- Lead with an abstract or executive summary that names the few key objects and then the pipeline chain among them (for example: nuggets are extracted from claims, which are extracted from chunks), so that nothing - no term, no concept - appears later without having been set up.
- Define vocabulary before it is used.
- Preface a hard or negative result with why it is hard before stating it did poorly, so the number reads as expected difficulty rather than a bare verdict.
- Global writing rules from `~/.claude/CLAUDE.md` apply and are not repeated here: no em dashes (use a plain dash or restructure), each full sentence on its own physical line in long files, no emojis.

## Presenting evidence

- Introduce every table and every prompt snippet before showing it: say what it is, and for a prompt what it ingests and what it returns. Never drop a code block or table cold.
- Show short prompt **snippets**, not full prompts, and link each to its source (symbol name plus line anchor, e.g. `SYSTEM` in `eval/judge.py#L51`). If the source file was removed from the default branch, pin the link to a commit SHA instead, and say so.
- Use real worked examples from the artifacts; never synthetic, and never an unrepresentative one (do not illustrate a "content-ful claim" with a setup claim, etc.).
- Prefer an intuitive name over jargon when both exist (retrieval ceiling, not attribution).
- Avoid loaded words (say "rarely asserts a claim its evidence does not support," not "does not hallucinate").

## The two modes

**Detailed reference.** Written as a paper with an inline appendix.
Each major procedure gets a readable, function-style pseudocode block, always paired with an in-words explanation or numbered steps.
Every table is introduced in prose and followed by its takeaway.
The verbatim prompts go in an "Appendix A" at the bottom, referenced from the body.

**Concise README section.** A condensation of a detailed reference.
Omit the pseudocode, the appendix, and any large table; trim a kept table to only the rows that are actually discussed.
Transform the detailed doc's subsections into numbered steps or short bullets.
Inline a short prompt snippet where the detailed doc pointed to its appendix, with the source link.
Keep the abstract, the vocabulary, the worked examples, and the connective prose.

## Consistency across the pair

When both a detailed and a concise version of the same material exist, they must agree on counts, names, and framing.
Reconcile them explicitly: a count that reads 35 in one and 36 in the other, or a metric named two ways, is a defect.
Decide the reader-facing number once (usually the simplest true one) and use it in both.

## Known pitfalls (from real edits)

Add to this list only when a new defect actually occurs; do not pad it.

1. **Count mismatch across the document.** If the text says "three directions," the results table must have three rows and any later list must name three, or the reader hits an unannounced fourth thing (this bit us with `shift` and with `attribution`). Keep "N things" equal everywhere it appears.
2. **Dangling reference after trimming.** Cutting a setup sentence can orphan a later one ("those 3 videos" with no antecedent). After any cut, reread the surrounding sentences.
3. **Broken list indentation.** A continuation paragraph or nested bullet under a numbered item needs the same indent as the item's text (three spaces under "1. "), or it renders outside the item. Two-vs-three-space drift silently breaks it.
4. **Misattributing a model's verdicts as ground truth.** "The judge determined 36 hits" is not "the correct distribution is 36 hits." Say whose labels a number is.
5. **Jargon over an intuitive name.** If a metric has a plain-language name, use it.
6. **The list-not-prose regression.** The document slides back into a bare list whenever a section is edited; re-run the transitions pass after edits, not just on the first draft.

## The procedure

1. Read the source material (the detailed doc, the build log, the gold and run artifacts).
2. Gather the evidence: compute the stats, grep the prompts and line anchors, pull the example ids and text.
3. Draft to a file (not inline in chat).
4. Run the transitions pass.
5. Surface the draft section by section; apply the human's rulings on inclusion and wording.
6. If a sibling document exists, reconcile counts and names against it.

## Done when

- every number, example, and prompt is traceable to an artifact or to code;
- the document reads as connected prose, with each section handing off to the next, not as a list;
- an abstract sets up every term and the pipeline chain before the body uses them;
- tables and snippets are each introduced, and snippets link to source;
- counts and names are consistent within the document and with any sibling document;
- the human has reviewed and ruled.
