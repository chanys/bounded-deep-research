# SLICES.md - eval query slices for code4AI

Self-contained manifest of the query slices used to evaluate the AnswerTrail agent.
Each slice is reported on its own; results are never pooled across slices.

## claim_derived (the scored core)

The instrument slice. Questions are composed from atomic, dated, chunk-anchored claims
extracted per video (`claims_code4AI.jsonl`), never from the video summaries, so a
question cannot leak text that a retriever also indexes.
What the generator saw: claim text, tags, and prior questions only - never the transcript
and never the retriever output (a lexical firewall).
Generation history: factual (Task 4, temporally stratified sample), comparative (Task 5
claim-pair composition, then Task 5.5 semantic-leakage neutralization = composer v2, with a
meta-organizational stop-list applied on topic families), longitudinal (Task 6 dated-thread
composition with a deterministic wording-guard retry and an advisory-only leak sort).
Known couplings and bias direction: the groundable-claim filter is a mixed-instrument cache
(per-video and per-claim prompts; never report a pooled groundable rate without that footnote);
the longitudinal develop-test accepts topic-recurrence 'collections' alongside genuine arcs, so
the 505 pool is low-precision and was human-triaged to 38 keeps before grounding (D65/D66).
Permitted uses: this is the slice scored as the instrument.
Reporting rule: per-tier, never pooled across tiers or across slices.

## keypoint_derived (legacy, frozen)

The earlier slice, generated from the Stage 1 video summaries (`query_candidates_{tier}.jsonl`
-> grounded/scored -> `queryset_core`/`queryset_broad`).
Because the summaries are themselves indexable, this slice has a built-in leakage/circularity
coupling: a question written from a summary can echo text the retriever indexes.
Permitted uses: kept frozen as a circularity exhibit and provenance record; NEVER scored as the
instrument.
Reporting rule: reference only; not pooled with claim_derived.

## external (planned)

Placeholder for future externally-authored slices (e.g. reviewer- or user-supplied questions)
that would test generalization beyond creator-derived claims. None exist yet.

Grounded tiers present at last handoff: factual, comparative, longitudinal.
