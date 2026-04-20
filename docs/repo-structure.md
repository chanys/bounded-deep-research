# Directory structure

This is the *eventual* layout through Week 8. Most files are stubs or absent on Day 1 and come in during the phase noted beside them. Items marked "(Phase N)" are created later; everything unmarked exists by end of Day 1.

```
~/projects/bounded-deep-research/
├── .claude/                    # Claude Code settings (auto-created)
├── .git/
├── .gitignore
├── .env                        # gitignored
├── .env.example
├── .python-version             # created by `uv init`
├── CLAUDE.md                   # stub for now — points at master plan
├── README.md                   # one-page setup + Phase 0 exit criteria
├── Makefile                    # up / down / logs / reset / api / web / smoke
├── pyproject.toml              # uv-managed
├── uv.lock                     # uv-managed, committed
│
├── app/                        # FastAPI backend
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, routes (Day 1: GET /health stub)
│   ├── agent.py                # ReAct loop (Day 3)
│   ├── tools.py                # search_transcripts, read_video_segment, submit_answer (Day 3)
│   ├── retrieval.py            # OpenSearch client wrapper (Phase 1)
│   ├── llm.py                  # Anthropic client + Langfuse wrap (Day 3)
│   ├── config.py               # pydantic-settings, reads .env (Day 3)
│   └── schemas.py              # Pydantic models — Query, Citation, etc. (Day 3)
│
├── ingest/                     # Ingestion scripts (standalone CLI)
│   ├── __init__.py
│   ├── seed_videos.py          # hardcoded 10 video IDs (Day 2)
│   ├── fetch_transcripts.py    # YouTube → JSONL (Day 2, expanded Phase 1)
│   ├── chunk.py                # JSONL → 30s-window chunks (Day 2)
│   ├── cleanup.py              # Haiku cleanup pass (Phase 1)
│   ├── embed.py                # OpenAI text-embedding-3-large (Phase 1)
│   └── index.py                # → OpenSearch (Day 2, hardened Phase 1)
│
├── eval/                       # Eval harness (Phase 4)
│   ├── __init__.py
│   ├── runner.py               # `uv run eval ...` entry
│   ├── metrics.py              # P/R/F1/MRR, citation format + pointer checks
│   ├── judge.py                # LLM judge + TPR/TNR calibration + bootstrap CIs
│   └── gold/                   # gold set JSONs (committed to git)
│       ├── transglobal.json    # 25 queries, wife-labeled
│       ├── discover_ai.json    # 12–15 queries, self-labeled
│       └── adversarial.json    # 5–8 adversarial retrieval probe queries
│
├── prompts/                    # Versioned prompt artifacts (v4.2)
│   ├── .gitkeep
│   └── research_recipe.md      # Phase 2 / Week 3 — numbered procedural prompt;
│                               # treated as code, swapped only at ablation boundaries
│
├── web/                        # Next.js 15 app (scaffolded Day 1 via `pnpm create next-app`)
│   ├── app/                    # App Router — default page.tsx until Day 4
│   ├── components/
│   ├── components.json         # shadcn config
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   └── ...                     # standard Next.js files
│
├── infra/                      # Local + (later) cloud infra
│   ├── docker-compose.yml      # Phase 0: Postgres + OpenSearch (Langfuse is cloud)
│   ├── init.sql                # Postgres schema init (Phase 1)
│   └── terraform/              # Phase 5 — empty for now
│       └── .gitkeep
│
├── configs/                    # YAML eval + ablation configs (Phase 4)
│   ├── baseline.yaml
│   ├── A1-bm25.yaml
│   ├── A1-dense.yaml
│   ├── A1-hybrid.yaml
│   └── .gitkeep
│
├── scripts/                    # Dev utilities
│   ├── smoke.sh                # infra + API health check (Day 1)
│   └── .gitkeep
│
├── tests/                      # pytest (Day 3 onward)
│   ├── __init__.py
│   ├── test_tools.py           # unit tests for agent tools
│   ├── test_retrieval.py       # retrieval sanity tests
│   └── test_smoke.py           # E2E /query test (Day 5)
│
├── docs/                       # Plans, retros, findings
│   ├── master-plan-v4.2.md     # the master plan (v4.2, current)
│   ├── repo-structure.md       # this file
│   ├── hypotheses.md           # Phase 4 pre-registration (H1, H2)
│   ├── phase-0-retro.md        # Day 5
│   ├── project-b-baseline-findings.md   # Phase 6 / Week 7 synthesis
│   └── .gitkeep
│
└── data/                       # gitignored — local only
    ├── transcripts/            # {video_id}.jsonl (Day 2)
    ├── chunks/                 # {video_id}.jsonl (Day 2)
    ├── manifests/              # corpus manifests with SHA-256 hashes (Phase 1)
    └── .gitkeep
```

