<!-- ============================================================
STATUS AND PROVENANCE (added on check-in, 2026-07-14)
============================================================ -->

> **Status: second external review (post-repair), pre-Task 7.**
> Conducted by an external model (ChatGPT) on the Task 5.5 v2 render — question
> wording **together with both gold claims per candidate**. Unlike the first
> external review (question text only), this one CAN speak to claim-level
> support, and several of its verdicts are reversals of the first review made
> on that basis (cc-0007, cc-0012, cc-0038).
>
> - Its verdicts and classification are **input to the Task 7 sitting, not a
>   default.** Its drop list is explicitly NOT executed at the repair stage:
>   per the approved v2.1 plan, repair fixes wording, Task 7 grounds and flags,
>   the human sitting drops.
> - Its process recommendations (independent post-repair audit, structured
>   comparison_axis field, closed final-status vocabulary, completeness
>   invariant, per-side leak granularity, tier-aware meta-reference guard)
>   were adopted into the v2.1 design, with two modifications: the
>   meta-reference guard is tier-conditional at the TIER level per committed
>   cc_06 (not thread-type level), and invalid_original_axis is advisory-only
>   (recorded and carried to Task 7, never a re-repair or re-pairing trigger).
> - It identified cc-0033 as absent from the v2 render (resolved: present in
>   the jsonl, unflagged; render-sample gap now prevented by the completeness
>   assertion).
>
> Verdicts carry into the Task 7 comparative review file as the secondary
> external-review field (external_review_verdict, external_review_reason,
> external_review_version = v2), keyed by candidate_id + source_claim_ids,
> never driving the clean-first sort.

<!-- ============================================================ -->

# AnswerTrail Phase 4: Second review of comparative candidates (post-Task 5.5 repair, with gold claims)

**Review date:** 2026-07-14
**Source reviewed:** Task 5.5 v2 render (`comparative_claimslice_v2_sample.md`) — recomposed and original questions with both gold claims per candidate.

## Overall verdict

This is a valuable diagnostic and partial repair, but I would not freeze the revised questions yet.

The most important result is not that 31 questions were recomposed. It is that 36 of 40 original comparative questions were flagged for semantic leakage. The leakage rate stayed similarly high across all four composition-order quartiles, with a descriptive correlation of only 0.029. That strongly suggests a prompt-level construction problem, not deterioration later in the run.

The repair pass successfully improved several questions. But it also introduced three new failure patterns:

- Stilted wording: many questions now begin with phrases such as "Regarding…," "In terms of…," or "When it comes to…"
- Meta-references: "In a previous video," "the second paper," "the unnamed paper," and "the creator's characterization."
- Two factual questions disguised as a comparison: the question asks what A does and what B does, without requiring an actual relationship or synthesis.

So the pass is best understood as proof that the strongest pairs can be neutralized, not proof that all 31 repaired questions are ready.

## What the repair did well

These revisions are substantially better than their originals:

| Candidate | Assessment |
|---|---|
| cc-0002 | Strong same-task comparison. The new question no longer reveals either model's strategy. |
| cc-0011 | Strong comparison between weight-changing specialization and DSPy-style context customization. |
| cc-0018 | Excellent neutral comparison of reasoning visibility in Claude and QwQ. |
| cc-0021 | Good physical-world-model architecture comparison. |
| cc-0026 | Technically meaningful comparison between two loss functions. |
| cc-0027 | Clean comparison between virtual loss and VQ-VAE training loss. |
| cc-0030 | Strong comparison of how KL regularization is used in two training settings. |
| cc-0034 | Good evaluation-method comparison: SoT baseline evaluation versus a deterministic judge. |
| cc-0035 | Good comparison between baseline evaluation and LLM-as-judge evaluation. |

These are the best candidates to carry forward.

## Important reversals after seeing the actual claims

The inclusion of claims A and B changes some of my earlier judgments.

### cc-0007: now drop

I previously considered the underlying R1-versus-RPT GRPO pair strong. But claim A does not explain how R1 uses GRPO. It only says that the R1 paper publicly documents GRPO.

The repair therefore changes the comparison into: public documentation surrounding R1, versus the creator's explanation of RPT's training loop. That is not a same-axis comparison. It should be dropped.

### cc-0012: weaker than it first appeared

The question asks about MiroFlow's "design," but claim A only establishes that it is an open-source deep-research framework, version three, developed for more than a year. It does not describe MiroFlow's architecture or workflow. Claim B describes a direct o3-full run with a time and source count.

The item can support a framework-versus-direct-run contrast, but not a detailed design comparison. I would mark it borderline rather than strong.

### cc-0038: drop

The original symbolic-versus-latent reasoning comparison sounded promising. But the selected claims are merely references to what two earlier videos covered. The repaired question makes this explicit and becomes: what did one earlier video cover, and what did another earlier video claim? That is meta-retrieval, not a meaningful comparative research question.

## Clear gold or axis failures

### cc-0003
The revised question asks about GLM-5's approach and step count. Claim B only says that GLM-5 produced an 11-step candidate at one point. It does not describe the approach. This repeats the factual-run problem where the question requests more than the chosen gold contains. Drop it, especially because cc-0002 is the stronger elevator comparison.

### cc-0016 and cc-0017
Both revised questions literally say "the unnamed paper." That should be an automatic rejection, not a valid repaired output. The system should never neutralize an unresolved subject by openly calling it unnamed.

### cc-0019
Still compares different axes: Claude, whether users can see its reasoning; o1/o3, the structural form of reasoning traces. Visibility policy and reasoning topology are not directly comparable.

### cc-0020
Xiaomi's physical-world model and Dream to Chat's dialogue world model share the phrase "world model," but operate in fundamentally different domains. This looks tag-driven rather than practitioner-driven.

### cc-0025
The revision asks two separate factual questions about two very different benchmarks. It does not form a meaningful comparative synthesis.

### cc-0040
The question asks how a broad creator opinion about Anthropic pricing "relates to" a specific Claude cost premium. The claims do not explicitly state that relationship. The answer would require interpretation beyond the two gold claims.

## My current classification

**Strong survivors:** cc-0002, cc-0011, cc-0018, cc-0021, cc-0026, cc-0027, cc-0030, cc-0034, cc-0035

**Potentially salvageable** (useful underlying pairs; need another targeted rewrite, entity cleanup, or stronger anchoring): cc-0001, cc-0004, cc-0005, cc-0008, cc-0009, cc-0010, cc-0012, cc-0024, cc-0031, cc-0040

**Drop:** cc-0003, cc-0006, cc-0007, cc-0013, cc-0014, cc-0015, cc-0016, cc-0017, cc-0019, cc-0020, cc-0022, cc-0023, cc-0025, cc-0028, cc-0029, cc-0032, cc-0036, cc-0037, cc-0038, cc-0039

## Unresolved error

cc-0033 is absent from the render. The summary reports one error, and this is the only missing candidate ID. It should be recovered and rendered before the repair pass is considered complete. An API error cannot silently become a dropped candidate.

## What the repair prompt still needs

The repair prompt should enforce a simpler rule: a comparative question may contain the two entity names and a neutral common axis, but no side-specific result, mechanism, value, or conclusion.

It should also reject rather than repair when: either subject is unnamed; the comparison axis cannot be stated naturally without describing both answers; the claims address different conceptual levels; the result would be two independent factual questions joined by "compared to"; the question requires phrases such as "the unnamed paper," "the second paper," or "in a previous video."

A useful additional output field: `{"comparison_axis": "...", "neutral_question": "...", "both_sides_required": true}` — then validate that the question mentions only the subjects and comparison_axis, not the actual side-specific properties.

## Missing post-repair evidence

The render reports the pre-repair leakage results, but it does not report a second leakage pass over the NEW questions. Before declaring Task 5.5 successful: post-repair leakage rate; post-repair comparability check; naturalness or meta-reference check; count of repaired questions that remain fully supported by both original claims; recovery of cc-0033.

## Bottom line

The leakage detector worked very well and exposed a genuine systemic defect. The repairer successfully rescued roughly nine clearly strong questions, with perhaps another ten salvageable. But "recomposed" should not be treated as synonymous with "repaired."

The next step should be a targeted second repair only for the strongest salvageable pairs, not another automatic attempt to preserve every candidate. The pool already has enough strong material that ambiguous, meta, or strained pairs can be dropped honestly.
