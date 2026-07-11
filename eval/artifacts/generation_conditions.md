# Stage 2 query generation: conditions of record

Human-readable record of the exact conditions the query set was generated and selected under, for the methods section and a reviewer.
The prompts live as inline constants in the eval scripts, tied to this run by the git-SHA provenance fingerprint stamped on every artifact.
Channel: code4AI only.
This reflects the revised pipeline (v2), after the first generation was found to produce supply-side questions and was redesigned around a demand-side practitioner persona.
This file is the short summary; the step-by-step runbook, the full scoring prompt, and the methods narrative live in `../bounded-deep-research-notes/eval/phase4_stage2_build_log.md` (Sections 6b and 8b), which is the single source of truth.

## Models and settings

| Step | Script | Model | Thinking | max_tokens | Concurrency |
|---|---|---|---|---|---|
| Generation | `eval/generate_queries.py` | claude-sonnet-5 | adaptive | 3000 | 3 |
| Grounding | `eval/ground_queries.py` | claude-sonnet-5 | disabled | 1000 | 4 |
| Filter + core scoring | `eval/screen_queries.py` | claude-sonnet-5 | adaptive | 8000 | 4 |
| Core/broad selection | `eval/select_queries.py` | none (deterministic code) | - | - | - |

Low concurrency and a 90-150s per-call timeout were used because the account's rate limit throttles sustained adaptive-thinking traffic; the timeout bounds any call caught in rate-limit backoff so a batch never appears hung.

## Generation persona and prompts

Queries are written from the demand side: the model simulates a curious AI practitioner who knows the channel's general area but has not seen any specific video, and asks a standalone question to find out whether it is answered.
The shared prompt forbids referencing the source ("this video", "the creator", "both papers"), forbids incidental trivia and metadata (exact dates, institutions, one-off numbers), forbids bare web-search factoids, and allows naming a model or method only if a practitioner would recognize it.
Each tier prompt carries two before/after examples rewriting an insider-phrased question into a natural standalone one.
Comparative is framed as approach-space ("what are the different approaches to X and how do they compare?"), never paper-versus-paper; longitudinal is framed as topic trajectory ("how have approaches to X evolved?"), never "the creator's view".

## Sampling (stratified on topic_cluster x tier)

One generation cell is one small API call. A factual cell is one source video (summary + key_points), a comparative cell is two videos from the same cluster, a longitudinal cell is a time-ordered slice of up to six videos from one cluster (summaries only).
Factual and comparative cells (50 each) are allocated across clusters proportional to video_count with a floor of 1; source videos are chosen by content richness. Longitudinal uses one slice per cluster spanning at least eight active months (15 clusters qualified).

## Grounding and answerability

Each query is located against its source video(s) DB chunk list by the LLM (never the pgvector retriever), producing source_chunk_ids; a query no chunk supports is dropped as unanswerable. These chunks are the verified-answerable seed for Stage 3, not a completeness claim.

## Filter + core scoring (one batched pass)

Batches of ~15 grounded candidates are judged in one pass. Each candidate is presented with its query, code signals (tier, observed_shape, chunk and video counts, leak), and a bounded sample of up to four grounded chunk texts. The model returns keep-or-drop against a persona floor and, for keepers, a core-worthiness score of 1 to 5 on four properties: exemplary naturalness, trustworthy/unambiguous gold, substance/non-triviality, and tier-fit. Parse omissions default to keep at a neutral score.

## Selection (deterministic)

Per tier, kept candidates are ranked by core-worthiness score; the top 20 are chosen for core under a per-cluster cap of 3 (topic spread) and a minimum score of 3 (quality floor). Of the remainder, those scoring at least 4 become broad and those below 4 are dropped (a deliberate quality-over-coverage choice for the broad layer). The human then reviews the pre-filled per-tier CSV and may override any verdict.
Targets: core 20 per tier (60 total); broad the score->=4 remainder.

## Post-filters

Leakage (content-trigram overlap between query and grounded chunks, reject at >= 0.5) and near-duplicate removal (token-Jaccard >= 0.8) run during grounding.

## Yields (this run, v2)

| Tier | Generated | Grounded (kept) | Unanswerable | Screen kept | Screen dropped | Core / broad (score>=4) |
|---|---|---|---|---|---|---|
| factual | 200 | 200 | 0 | 194 | 6 | 20 / 135 |
| comparative | 178 | 176 | 2 | 169 | 7 | 20 / 88 |
| longitudinal | 84 | 83 | 1 | 82 | 1 | 20 / 33 |
| total | 462 | 459 | 3 | 445 | 14 | 60 / 256 |

The broad floor of 4 dropped 129 candidates that scored 2 or 3 (kept in the review CSVs with a blank verdict for audit); core was already entirely score>=4, so it is unchanged.
Generation lost 4 cells to the per-call timeout under rate-limit backoff (absorbed by over-generation).
Leakage and near-duplicate drops were zero. The low screen-drop rate (14 of 459) reflects that the persona prompt fixed the quality problem at the source, leaving the filter to catch only stragglers (obscure-name questions, elevator-puzzle transcript trivia, and a few whose evidence did not support the claim).
Grounding produced far fewer unanswerable drops than v1 (3 vs 33) because the more general demand-side questions are more readily answered from the corpus.
Cost of this re-run was roughly $10 (grounding dominant); cumulative Stage 2 spend across v1 and v2 is roughly $20.
