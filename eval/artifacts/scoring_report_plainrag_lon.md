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

- recall (incl shift, per design): macro 22.6% [range 22.6%-22.6%]  |  micro 23.4% (32/137)
    - stance-only recall (shift excluded): micro 23.5% (24/102)
    - macro = mean of per-run per-question ratios; micro = pooled ratio-of-totals
- groundedness: macro 99.2% [range 99.2%-99.2%] (mean of per-run ratios)  |  micro 99.4% (499/502 answer claims)
- shift-nugget pass rate: 22.9% (8/35)
- stance-miss breakdown: 8 timing (right stance, wrong/missing window), 70 stance (not conveyed) [un-calibrated reason-based diagnostic]
- retrieval ceiling:    27.5%  (28/102 gold nuggets had supporting evidence in the retrieved set) [pooled/ratio-of-totals]
- synthesis conversion: 75.0%  (of retrieved-evidence nuggets, fraction expressed in the answer) [pooled/ratio-of-totals]
- missed-nugget attribution: 7/78 synthesis (surfaced-but-unused), 71/78 retrieval (never-surfaced)
- inequality violations (answer HIT, chunks MISS): 3 - each is parametric leakage or a judge artifact, listed below

## Inequality violations (answer states it, retrieved chunks do not support it)

Each is either parametric leakage (agent stated gold content it did not retrieve) or a judge artifact (clean answer prose easier to confirm than garbled ASR). Read each.

- lc-0014 r0 n1 (stance): dir-3 said no support :: None of the chunks express skepticism that scaling alone would deliver AGI; they discuss marketing around AGI/superintelligence claims but not the scaling hypothesis specifically.
- lc-0111 r0 n1 (stance): dir-3 said no support :: The Jan 2025 chunk merely describes DeepSeek v3 as a mixture-of-experts model factually, without any language praising it as a genuine innovation.
- lc-0169 r0 n3 (stance): dir-3 said no support :: The 2026-02-22 chunk explicitly says fast weights are the hidden state/KV cache of the transformer (an inference-time, non-weight-matrix phenomenon), and separately describes modifying tensor weights via optimization for in-context learning as a distinct idea - it does not describe gradient descent physically modifying weight matrices as the creation of 'fast weights', contradicting the claim's specific framing.

## lc-0130 (SEGREGATED - no_change trap, excluded from recall average)

- r0: no_change MISS; stance 0/1

## 10 lowest-recall questions (for the human read)

- lc-0061: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 0 synthesis / 3 retrieval
- lc-0070: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 0 synthesis / 3 retrieval
- lc-0233: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 0 synthesis / 3 retrieval
- lc-0337: recall 0%; missed nuggets ['n1', 'n2', 'n3', 'n4']; attribution 0 synthesis / 4 retrieval
- lc-0388: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval
- lc-0418: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval
- lc-0452: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 2 retrieval
- lc-0476: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 0 synthesis / 3 retrieval
- lc-0478: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval
- lc-0481: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 2 retrieval