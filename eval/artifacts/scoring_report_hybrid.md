# Phase 4 scoring report

Score-time provenance:
```
{
  "judge_model": "claude-sonnet-5",
  "judge_prompt_sha": "a7d71e4a",
  "judge_calibration": {
    "kappa": 0.879,
    "raw_agreement": 0.939,
    "n_pairs": 66,
    "seed": 20260726
  },
  "answer_claim_extractor_sha": "c7cbc275",
  "factual_nugget_extractor_sha": "910a6696",
  "entailment_audit_sha": "ddfc49a9",
  "miss_classifier_sha": "249c27fc",
  "factual_gold": "factual-gold-v1.0",
  "longitudinal_gold": "gold-v0.2.2"
}
```

## longitudinal (35 questions x 1 runs)

- recall (incl shift, per design): macro 31.1% [range 31.1%-31.1%]  |  micro 31.4% (43/137)
    - stance-only recall (shift excluded): micro 28.4% (29/102)
    - macro = mean of per-run per-question ratios; micro = pooled ratio-of-totals
- groundedness: macro 99.1% [range 99.1%-99.1%] (mean of per-run ratios)  |  micro 99.0% (506/511 answer claims)
- shift-nugget pass rate: 40.0% (14/35)
- stance-miss breakdown: 2 timing (right stance, wrong/missing window), 71 stance (not conveyed) [un-calibrated reason-based diagnostic]
- retrieval ceiling:    40.2%  (41/102 gold nuggets had supporting evidence in the retrieved set) [pooled/ratio-of-totals]
- synthesis conversion: 58.5%  (of retrieved-evidence nuggets, fraction expressed in the answer) [pooled/ratio-of-totals]
- missed-nugget attribution: 17/73 synthesis (surfaced-but-unused), 56/73 retrieval (never-surfaced)
- inequality violations (answer HIT, chunks MISS): 5 - each is parametric leakage or a judge artifact, listed below

## Inequality violations (answer states it, retrieved chunks do not support it)

Each is either parametric leakage (agent stated gold content it did not retrieve) or a judge artifact (clean answer prose easier to confirm than garbled ASR). Read each.

- lc-0087 r0 n3 (stance): dir-3 said no support :: The chunks discuss various continual-learning/catastrophic-forgetting solutions but never frame a stance about 'memory optimization alone being insufficient' or explicitly state a refined view that more than memory optimization is needed for true continuous learning.
- lc-0111 r0 n1 (stance): dir-3 said no support :: The January 2025 chunks merely describe DeepSeek's MoE architecture (e.g., 'strong mixture of expert language model') without praising it as a genuine innovation; the explicit praise for MoE cost reduction appears only in a May 2025 chunk, outside the claimed window.
- lc-0123 r0 n2 (stance): dir-3 said no support :: While the July 2025 chunks (evwdJef_9U0) show DPO criticized as overfitting to superficial patterns, other May-July 2025 chunks (VTFzdYrlpko, lQrADbBxpQg) actually praise DPO's theoretical elegance ('works so beautifully', 'shared unifying principle') rather than framing it as a flawed SFT special case, and no chunk in the window shows near-zero empirical gains or a 'DPO is dead' framing, so the compound claim is not fully supported.
- lc-0349 r0 n1 (stance): dir-3 said no support :: No chunk is dated Jan 2025 (the earliest are Feb 2025 or later), so the specific time window in the claim isn't matched by any chunk's publish date, making the claim unsupported per the strict dating rule.
- lc-0413 r0 n1 (stance): dir-3 said no support :: None of the chunks mention Grok 3 or Claude Sonnet 3.7 catching and fixing their own mistakes; the retrieved text discusses self-correction generically in other models/papers without supporting these specific examples.

## lc-0130 (SEGREGATED - no_change trap, excluded from recall average)

- r0: no_change MISS; stance 0/1

## 10 lowest-recall questions (for the human read)

- lc-0127: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 2 retrieval
- lc-0177: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 0 synthesis / 3 retrieval
- lc-0251: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 2 retrieval
- lc-0337: recall 0%; missed nuggets ['n1', 'n2', 'n3', 'n4']; attribution 1 synthesis / 3 retrieval
- lc-0418: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval
- lc-0476: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 2 retrieval
- lc-0478: recall 0%; missed nuggets ['n1', 'n2']; attribution 1 synthesis / 1 retrieval
- lc-0481: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval
- lc-0497: recall 0%; missed nuggets ['n1', 'n2', 'n3', 'n4']; attribution 1 synthesis / 3 retrieval
- lc-0504: recall 0%; missed nuggets ['n1', 'n2']; attribution 1 synthesis / 1 retrieval