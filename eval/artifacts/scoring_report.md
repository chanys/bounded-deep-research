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

## longitudinal (35 questions x 3 runs)

- recall (incl shift, per design): macro 32.2% [range 30.9%-33.2%]  |  micro 32.8% (135/411)
    - stance-only recall (shift excluded): micro 31.7% (97/306)
    - macro = mean of per-run per-question ratios; micro = pooled ratio-of-totals
- groundedness: macro 97.9% [range 97.3%-98.7%] (mean of per-run ratios)
- shift-nugget pass rate: 36.2% (38/105)
- stance-miss breakdown: 11 timing (right stance, wrong/missing window), 198 stance (not conveyed) [un-calibrated reason-based diagnostic]
- retrieval ceiling:    43.5%  (133/306 gold nuggets had supporting evidence in the retrieved set) [pooled/ratio-of-totals]
- synthesis conversion: 63.9%  (of retrieved-evidence nuggets, fraction expressed in the answer) [pooled/ratio-of-totals]
- missed-nugget attribution: 48/209 synthesis (surfaced-but-unused), 161/209 retrieval (never-surfaced)
- inequality violations (answer HIT, chunks MISS): 12 - each is parametric leakage or a judge artifact, listed below

## factual (25 questions x 3 runs)

- recall (incl shift, per design): macro 86.9% [range 85.3%-88.0%]  |  micro 84.9% (135/159)
    - stance-only recall (shift excluded): micro 84.9% (135/159)
    - macro = mean of per-run per-question ratios; micro = pooled ratio-of-totals
- groundedness: macro 96.0% [range 93.9%-97.1%] (mean of per-run ratios)
- retrieval ceiling:    86.8%  (138/159 gold nuggets had supporting evidence in the retrieved set) [pooled/ratio-of-totals]
- synthesis conversion: 97.1%  (of retrieved-evidence nuggets, fraction expressed in the answer) [pooled/ratio-of-totals]
- missed-nugget attribution: 4/24 synthesis (surfaced-but-unused), 20/24 retrieval (never-surfaced)
- inequality violations (answer HIT, chunks MISS): 1 - each is parametric leakage or a judge artifact, listed below

## Inequality violations (answer states it, retrieved chunks do not support it)

Each is either parametric leakage (agent stated gold content it did not retrieve) or a judge artifact (clean answer prose easier to confirm than garbled ASR). Read each.

- fc-0033 r1 fc-0033_n2 (fact): dir-3 said no support :: The chunks state that prioritizing the 12B model *prevents* it from being corrupted by dumber configurations, which is the opposite of the claim that the 12B became 'more stupid'.
- lc-0011 r1 n1 (stance): dir-3 said no support :: The only early-2025 chunk (Z9IpO3TTskU, 2025-02-15) merely recites paper content about agentic AI trends and even ends noting models 'still trail human cognition,' showing no clear expression of personal optimism, and other chunks are largely skeptical about agentic AI's real-world capability, so the claim is not supported.
- lc-0011 r2 n1 (stance): dir-3 said no support :: The only early-2025 chunk (Z9IpO3TTskU) merely recites paper/survey content about agent trends without the creator expressing personal optimism, and even ends noting models 'still trail human cognition' and needing oversight, so it does not support a clear optimistic stance.
- lc-0027 r1 n1 (stance): dir-3 said no support :: The mid-2025 chunks (July's caution about security risks, September's harsh critique calling AI scientists 'expert producers of methodologically flawed science') show he was already offering independent critique rather than merely relaying optimistic claims uncritically.
- lc-0061 r0 n3 (stance): dir-3 said no support :: None of the January 2026 chunks (7d4bEfj7wmc, O9HxArmWChs, Z1dOSop6KbM) state that chain-of-thought is an 'illusion' or 'paint over cracks'; the closest is a vague remark about companies not being fully transparent in CoT syncing, which does not convey a firm conclusion that CoT is not real reasoning.
- lc-0111 r1 n1 (stance): dir-3 said no support :: The January 2025 chunks describe DeepSeek's model as a mixture-of-experts model with enthusiasm about its performance, but never single out the MoE architecture itself as a 'genuine innovation'.
- lc-0251 r0 n1 (stance): dir-3 said no support :: None of the Jan-Mar 2025 chunks mention a 'lazy regime' preceding grokking (they speak of a 'soft mix' mechanism instead), so the specific technical framing in the claim is not supported by the text.
- lc-0337 r1 n4 (stance): dir-3 said no support :: While the April 2026 chunk supports the coin-flip finding (50% of runs below baseline), no chunk states or implies a finding about prompt optimization failing to recoup its compute costs, so the compound claim is only partially supported.
- lc-0349 r1 n3 (stance): dir-3 said no support :: The Jan 2026 chunks discuss RAG failing on knowledge conflicts and suggest fine-tuning over RAG for belief updates, but they never frame RAG or in-context learning as merely a 'temporary fix to the knowledge-cutoff problem' versus a lasting solution, so the specific claim is not substantiated.
- lc-0349 r2 n1 (stance): dir-3 said no support :: The only chunk published in Jan 2025 (DoI4nWQuywI) merely references a GraphRAG research survey and does not convey RAG as 'the obvious default answer' for updating an LLM's knowledge; other chunks discussing RAG-as-default (e.g., N7dDq54_akY) are from September 2025, outside the claimed Jan 2025 window.
- lc-0349 r2 n2 (stance): dir-3 said no support :: None of the Sep 2025 (or surrounding 2025) chunks describe classic RAG as one-shot, stateless, or non-adaptive; while some chunks mention hallucination or safety issues with RAG, the specific structural weaknesses claimed are not supported by the transcripts.
- lc-0413 r1 n1 (stance): dir-3 said no support :: While the March 2025 chunk discusses self-correction/backtracking as an emergent reasoning capability, none of the chunks mention Grok 3 or Claude Sonnet 3.7 specifically catching and fixing their own mistakes, so the specific examples in the compound claim are unsupported.
- lc-0413 r2 n1 (stance): dir-3 said no support :: The chunks discuss self-correction/backtracking generally across many videos but never mention Grok 3 or Claude Sonnet 3.7 specifically, so the specific claim is unsupported.

## lc-0130 (SEGREGATED - no_change trap, excluded from recall average)

- r2: no_change MISS; stance 0/1
- r1: no_change MISS; stance 0/1
- r0: no_change MISS; stance 0/1

## 10 lowest-recall questions (for the human read)

- lc-0127: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 4 synthesis / 5 retrieval
- lc-0087: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 8 retrieval
- fc-0004: recall 0%; missed nuggets ['fc-0004_n1', 'fc-0004_n2', 'fc-0004_n3']; attribution 0 synthesis / 9 retrieval
- lc-0481: recall 0%; missed nuggets ['n1', 'n2']; attribution 2 synthesis / 4 retrieval
- fc-0042: recall 0%; missed nuggets ['fc-0042_n1', 'fc-0042_n2']; attribution 3 synthesis / 3 retrieval
- lc-0418: recall 0%; missed nuggets ['n1', 'n2']; attribution 0 synthesis / 6 retrieval
- lc-0233: recall 0%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 8 retrieval
- lc-0497: recall 7%; missed nuggets ['n1', 'n2', 'n3', 'n4']; attribution 6 synthesis / 6 retrieval
- lc-0251: recall 8%; missed nuggets ['n1', 'n2', 'n3']; attribution 2 synthesis / 6 retrieval
- lc-0070: recall 8%; missed nuggets ['n1', 'n2', 'n3']; attribution 1 synthesis / 7 retrieval