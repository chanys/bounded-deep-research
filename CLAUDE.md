# CLAUDE.md

## What this is

AnswerTrail is a bounded-corpus deep-research agent: a roll-your-own ReAct loop (search, read, reason, answer) over a fixed library of single-creator YouTube transcripts.
Retrieval is dense-only over Postgres/pgvector; the model is stateless and drives its own exploration until it decides to answer.
It is live in production on AWS at `answertrail.yeesengchan.com`.

Phases 0 through 5 have shipped (local skeleton, ingestion, agent loop, frontend, AWS deployment).
Phase 4, the evaluation instrument (gold set, calibrated LLM judges, eval runner), is the next phase and is **not built yet**; see "Not yet built" below before assuming any eval code, gold set, or `hypotheses.md` exists.

I drive planning; you handle execution.

## Planning docs live in a separate repo

The plans, build logs, and operational notes are not in this repo.
They live in the sibling repo `../bounded-deep-research-notes` (its own git, gitignored from this one, so it assumes that checkout is present next to this one).

Start with its `README.md`, which indexes every file. The ones you will reach for most:

- `master-plan-v4.4.md` is the current plan (research framing, phases, experimental design; includes the v4.5 delta).
- `day-log.md` is the day-by-day build history through Phase 5; the clearest record of why things are the way they are.
- `operations-cheatsheet.md` is the AWS deploy/debug runbook (ECS, RDS tunnel, secrets, teardown/rebuild).
- `tech-debt.md` is the deferred-work ledger.

## Conventions

Concise. Prose over bullets unless 3+ parallel items genuinely need separating.
Explain decisions briefly as you code; I want to understand, not just have it done.
Don't run install/setup commands unsolicited, and don't ask permission for obvious things (web search, reading files, smoke tests); just do them.
As Phase 4 is built, document each eval stage at methods grade in its notes build log (`../bounded-deep-research-notes/eval/phase4_*_build_log.md`): the exact inputs, prompts, hyperparameters, the rationale a reviewer would probe, and honest human-versus-AI attribution of decisions.
Do this when a stage produces artifacts, not at write-up time; reconstructing it later is miserable and several items are paper methods.
(Global style rules, uv/pnpm, and git conventions live in `~/.claude/CLAUDE.md` and are not repeated here.)

## Commands

Infra (Postgres + OpenSearch via docker): `make up`, `make down`, `make reset` (drops volumes), `make logs`.
Run these before anything that touches the DB.

Backend: `make api` (uvicorn on :8000, reload).
Frontend: `make web` (Next dev on :3000).

Verify the stack: `make smoke` checks Postgres, OpenSearch, and `/health` are all serving.
There is no Python test suite yet (pytest is a dev dep, `eval/` is a stub), so `make smoke` plus `scripts/full_agent_smoke.py` are how you confirm a change works end to end.

Lint: `uv run ruff check` (Python), `cd web && pnpm lint` (frontend).
Web build check: `cd web && pnpm build`.

Corpus move (local -> RDS, never re-ingest): `make corpus-dump` then `PGPASSWORD=... make corpus-restore`.
It deliberately uses the container's PG16 tools, not the host's PG18; see the Makefile comments and `operations-cheatsheet.md`.

Ingest pipeline (offline, per channel, in order): `list_channel_videos` -> `fetch_transcripts` -> `clean_transcripts` (ASR fix via gpt-5.4-mini; skip with `register_channel --manual-clean` for human captions) -> `chunk_transcripts` (fixed 30s windows) -> `embed_chunks` -> `index_chunks` (OpenSearch, local eval only).
Each runs as `uv run python -m ingest.<name>`.
Postgres is the source of truth; OpenSearch and embeddings are derived.

## Architecture

Backend is FastAPI (`app/`), frontend is Next.js (`web/`), corpus lives in Postgres+pgvector.

**Request path.**
All HTTP endpoints live in `app/main.py` (one file, docstringed).
`POST /query` runs the agent and streams progress to the browser as SSE, bridging two async tasks over an `asyncio.Queue`: the agent produces events, a generator drains them to the response.
Before any paid work, three gates run: channel-exists, per-tier daily spend cap (`app/limits.py`), and per-IP daily quota.
Tiers (anon / coded / owner) come from the access code and draw on separate budget buckets, so a live demo can't be blocked by public traffic.

**Agent loop** (`app/agent.py`).
`run_agent` owns the conversation; the model is stateless (`store=False`).
Each exploration turn the model calls `search_transcripts` / `read_video_segment` in parallel, or `mark_ready` to signal done.
Exploration runs at reasoning effort `none`; the final answer is a dedicated forced `submit_answer` turn at `synthesis_reasoning_effort` (low), and only that turn streams its text to the UI.
If the step budget runs out first, a final turn forces synthesis.
The same event stream feeds both the SSE sink and an `EvidenceCollector` that folds it into a `RunEvidenceState` for the Run Audit panel (`GET /runs/{id}/evidence`); `RunEvidenceState` and `EvidenceCollector` live in `app/evidence.py`.

**Tools** (`app/tools.py`).
Citations are IDs only (`video_id, start_ts, end_ts`); the agent never writes chunk text, and `submit_answer` validates every citation exists in the index before the answer is accepted.
`submit_answer` being a tool (not prose) is what gives structured citations, a clean stop signal, and forced termination.

**Retrieval** (`app/retrieval.py`) has two backends selected by `settings.retrieval_backend`, by consumer not environment.
`pgvector` is dense-only kNN over the Postgres HNSW index and serves ALL production traffic (mode is forced to dense regardless of what the caller asks), so laptop and AWS run identical retrieval code.
`opensearch` (bm25 / dense / hybrid-RRF) is built lazily and used ONLY by offline eval/ablation scripts.
Embeddings are `text-embedding-3-large` at Matryoshka-reduced 1536 dims; the query embedder and the corpus embed job MUST share that dimension.

**Channels** (`app/channels.py`) is the single source of truth for each corpus.
The research recipe is never forked per channel; a channel's `output_directive` is appended to the system prompt to steer output language (e.g. Traditional Chinese for TransGlobalTV) while retrieval and the recipe stay shared.

**Config** (`app/config.py`).
All settings via pydantic-settings from env/`.env`.
In prod the DB password arrives separately and `DATABASE_URL` is assembled from parts (never splice a secret into a URL).
Langfuse keys are also mirrored into `os.environ` because its SDK reads env directly.

**Web note.**
`web/AGENTS.md`: this Next.js version has breaking changes vs training data.
Read the relevant guide under `web/node_modules/next/dist/docs/` before writing frontend code.

## Gotchas

- Embeddings are 1536-dim Matryoshka truncations of `text-embedding-3-large` (native 3072), chosen so a `vector(1536)` column fits under pgvector's 2000-dim HNSW index cap. Do not "upgrade" the dimension.
- Retrieval is forced to dense pgvector in production regardless of the requested mode. OpenSearch (bm25/hybrid) is local-only for the offline ablation and is never deployed.
- The daily spend circuit-breaker lives in a Postgres table keyed by `(day, bucket)` with separate public and owner budgets. It must stay in Postgres so it survives task restarts and deploys; do not replace it with in-process state.
- SSE streams need a `: keepalive` comment line every 15s, or the synthesis-turn pause trips the ALB's 150s idle timeout and drops the connection.
- The agent runs on OpenAI (`gpt-5.4`). Eval judges, when Phase 4 builds them, are intended to run on the Claude family on purpose (cross-family, to avoid self-preference bias). Changing either forces recalibration.
- The corpus is multi-channel (code4AI, TransGlobalTV, and more on disk), but the agent answers over a single channel per query.
- Video metadata `tags` are channel boilerplate, near-identical across videos and carry no signal; use titles and descriptions.
- Known accepted issue: the share-link passcode travels in the URL (`?k=`), so it lands in browser history and server logs. It is scrubbed from the address bar client-side after capture and the spend breaker bounds the blast radius. Documented in the writeup; do not "fix" without discussion.

## Treat as code

`prompts/research_recipe.md` is versioned (currently 0.6.0).
Bump `version` on behavioral changes: minor for tweaks, major for a restructure.
When Phase 4 lands, gold-set files and judge prompts get the same discipline: versioned artifacts, never edited in place without a commit.

Rule of thumb for eval artifacts: methodology and small reviewed outputs (the gold set, prompts, induced criteria, `hypotheses.md`, small human-readable outputs like the corpus inventory) go in git; bulk generated data (per-video summaries, run outputs, large intermediates) goes to S3 or a durable backup, not core git, provenance-stamped either way.

## Do not touch

- Live AWS: don't run `terraform apply`/`destroy` or otherwise mutate deployed resources. Applying and other account actions are the user's trigger to pull. Editing the infra code under `infra/terraform/` in-repo is fine when asked.
- The registered plan and (once it exists) the pre-registered hypotheses in the notes repo: amend by adding dated entries, don't rewrite committed text.

## Not yet built (Phase 4)

The evaluation instrument does not exist yet.
There is no gold set, no calibrated judge, no calibration harness, no `hypotheses.md`, no stats code, and no `make` target for any of them.
What exists is scaffolding only: `RunEvidenceState` and the `/system` page's eval placeholder.
The design lives in `../bounded-deep-research-notes/eval/phase4_evaluation_proposal_v2.md` (the why) and `eval/phase4_execution_plan_v5.md` (the what, in what order, and who does it).
Do not reference these artifacts as if they are present.
