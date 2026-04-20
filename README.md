# bounded-deep-research

A bounded-corpus deep research agent over YouTube video corpora. See `docs/master-plan-v4.2.md`.

## Prereqs
Docker, pnpm, uv, Python 3.12.

## Setup
1. `cp .env.example .env` and fill in keys (OpenAI + Langfuse required for Day 1; Anthropic by Day 3; YouTube by Phase 1 Day 2).
2. In three shells:
   - `make up`   — starts Postgres + OpenSearch
   - `make api`  — FastAPI on :8000
   - `make web`  — Next.js on :3000
3. `make smoke` — verifies all three are healthy.

## Phase 0 exit criteria (end of Week 1)
Streaming query → answer with ≥3 citations, end-to-end, on both channels (TransGlobal, Discover AI).
