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

## factual (25 questions x 1 runs)

- recall (incl shift, per design): macro 82.0% [range 82.0%-82.0%]  |  micro 79.2% (42/53)
    - stance-only recall (shift excluded): micro 79.2% (42/53)
    - macro = mean of per-run per-question ratios; micro = pooled ratio-of-totals
- groundedness: macro 96.0% [range 96.0%-96.0%] (mean of per-run ratios)  |  micro 98.5% (128/130 answer claims)
- retrieval ceiling:    81.1%  (43/53 gold nuggets had supporting evidence in the retrieved set) [pooled/ratio-of-totals]
- synthesis conversion: 97.7%  (of retrieved-evidence nuggets, fraction expressed in the answer) [pooled/ratio-of-totals]
- missed-nugget attribution: 1/11 synthesis (surfaced-but-unused), 10/11 retrieval (never-surfaced)
- inequality violations (answer HIT, chunks MISS): 0 - each is parametric leakage or a judge artifact, listed below

## Inequality violations (answer states it, retrieved chunks do not support it)

Each is either parametric leakage (agent stated gold content it did not retrieve) or a judge artifact (clean answer prose easier to confirm than garbled ASR). Read each.

- (none)

## 10 lowest-recall questions (for the human read)

- fc-0001: recall 0%; missed nuggets ['fc-0001_n1', 'fc-0001_n2', 'fc-0001_n3']; attribution 0 synthesis / 3 retrieval
- fc-0004: recall 0%; missed nuggets ['fc-0004_n1', 'fc-0004_n2', 'fc-0004_n3']; attribution 0 synthesis / 3 retrieval
- fc-0009: recall 0%; missed nuggets ['fc-0009_n1', 'fc-0009_n2']; attribution 0 synthesis / 2 retrieval
- fc-0042: recall 0%; missed nuggets ['fc-0042_n1', 'fc-0042_n2']; attribution 1 synthesis / 1 retrieval
- fc-0017: recall 50%; missed nuggets ['fc-0017_n2']; attribution 0 synthesis / 1 retrieval
- fc-0002: recall 100%; missed nuggets -; attribution 0 synthesis / 0 retrieval
- fc-0005: recall 100%; missed nuggets -; attribution 0 synthesis / 0 retrieval
- fc-0006: recall 100%; missed nuggets -; attribution 0 synthesis / 0 retrieval
- fc-0007: recall 100%; missed nuggets -; attribution 0 synthesis / 0 retrieval
- fc-0010: recall 100%; missed nuggets -; attribution 0 synthesis / 0 retrieval