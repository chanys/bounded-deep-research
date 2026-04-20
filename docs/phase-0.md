## Initialize uv and add dependencies

```
uv init --python 3.12
```
This creates `pyproject.toml`, `.python-version`, and a placeholder `main.py` and `README.md`. Delete the placeholder `main.py`

Add runtime deps:
```
uv add fastapi "uvicorn[standard]" opensearch-py anthropic langfuse "psycopg[binary]" sqlalchemy pydantic-settings tenacity tqdm pyyaml youtube-transcript-api
```

Add dev deps:
```
uv add --dev pytest pytest-asyncio httpx ruff
```

## Create the directory skeleton

```
mkdir -p app ingest eval web infra scripts data prompts
touch app/__init__.py ingest/__init__.py eval/__init__.py
touch docs/.gitkeep data/.gitkeep prompts/.gitkeep
```

## Create `.gitignore`

```
# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
*.egg-info/

# Node
node_modules/
.next/
.turbo/

# IDE
.idea/
.vscode/

# Env
.env
.env.local

# Data
/data/*
!/data/.gitkeep

# OS
.DS_Store
```

## Create `.env.example`

```
# LLM APIs
OPENAI_API_KEY=
# ANTHROPIC_API_KEY=      # needed Day 3 (agent ReAct loop)

# Langfuse Cloud (https://cloud.langfuse.com)
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASE_URL=https://us.cloud.langfuse.com

# Local infra (matches docker-compose)
POSTGRES_URL=postgresql://bdr:bdr_dev@localhost:5432/bdr
OPENSEARCH_URL=http://localhost:9200

# YOUTUBE_API_KEY=         # needed Phase 1 Day 2 (video metadata)
```

## Create FastAPI stub at `app/main.py`

```
from fastapi import FastAPI

app = FastAPI(title="bounded-deep-research")

@app.get("/health")
def health():
    return {"status": "ok"}
```

## Create `infra/docker-compose.yml`

```
services:
  # container that 'docker compose up' starts
  postgres:
    image: postgres:16
    container_name: bdr-postgres
    environment:                  # Postgres image reads below vars on first startup
      POSTGRES_USER: bdr          # superuser name
      POSTGRES_PASSWORD: bdr_dev  # superuser password
      POSTGRES_DB: bdr            # initial database
    ports:
      - "5432:5432"               # HOST:CONTAINER port mapping
    volumes:
      - postgres_data:/var/lib/postgresql/data         # a named volume persists data across restarts
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bdr -d bdr"]  # updates container's health status
      interval: 5s                                     # every 5 seconds. Why are we doing this health check?
      timeout: 5s                                      # so that when we do `make up` -> `docker compose up --wait`
      retries: 10                                      # which blocks the shell until every service reports healthy

  # container that 'docker compose up' starts
  opensearch:  # a search/analytics engine; indexes texts to enable query via BM25 / vector similarity
    image: opensearchproject/opensearch:2
    container_name: bdr-opensearch
    environment:
      - discovery.type=single-node          # tells OpenSearch not to try to form a cluster with siblings
      - DISABLE_SECURITY_PLUGIN=true        # turns off auth and TLS. Fine locally, never in production
      - DISABLE_INSTALL_DEMO_CONFIG=true    # skips demo certs/users installer (don't need since security is off)
      - OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g  # OpenSearch is a Java app; caps JVM heap at 1GB (min and max)
    ulimits:
      memlock: { soft: -1, hard: -1 }       # unlimited locked memory
      nofile:  { soft: 65536, hard: 65536 } # file descriptor limit
    ports:
      - "9200:9200"
    volumes:
      - opensearch_data:/usr/share/opensearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9200/_cluster/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 20

volumes:           # formally declares the named volumes
  postgres_data:
  opensearch_data:
```

## Create `scripts/smoke.sh` 

Make it executable `chmod +x`
```
#!/usr/bin/env bash
set -u

# A bash script that tests all three things are actually serving requests

GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'  # special ANSI codes to set terminal colors
ok()   { echo -e "${GREEN}✅ $1${NC}"; }            # sets foreground to green, then back to default
fail() { echo -e "${RED}❌ $1${NC}"; FAILED=1; }    # sets foreground to red, then back to default
FAILED=0

# 1. Postgres
# Checks whether Postgres is ready
if command -v pg_isready >/dev/null && pg_isready -h localhost -p 5432 -U bdr >/dev/null 2>&1; then
  ok "Postgres ready"
elif docker exec bdr-postgres pg_isready -U bdr >/dev/null 2>&1; then
  ok "Postgres ready (via docker exec)"
else
  fail "Postgres not ready"
fi

# 2. OpenSearch
# `curl`: a command line tool that makes HTTP requests and prints the response
# GETs `/_cluster/health` , extracting the `status` field
STATUS=$(curl -sf http://localhost:9200/_cluster/health 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [[ "$STATUS" == "green" || "$STATUS" == "yellow" ]]; then
  ok "OpenSearch cluster $STATUS"
else
  fail "OpenSearch not healthy (status=${STATUS:-unreachable})"
fi

# 3. FastAPI
# GETs `/health`
RESP=$(curl -sf http://localhost:8000/health 2>/dev/null)
if [[ "$RESP" == '{"status":"ok"}' ]]; then
  ok "FastAPI /health ok"
else
  fail "FastAPI /health: ${RESP:-unreachable}"
fi

# FAILED == 0 , means all green, 1 means at least one failed
exit $FAILED
```

## Create `Makefile`

```
# without the .PHONY, if a file named `up` existed, then `make up` would say "up is up to date" and do nothing
.PHONY: up down logs reset api web smoke

up:
	# starts Postgres + OpenSearch in the background, waits for healthy
	# -d = detached (runs in the background)
	# --wait = block until every service with a healthcare reports healthy
	# without `--wait`, `make up` returns as soon as the containers are started, but Postgres takes 5-10s, OpenSearch takes 20-40s
	docker compose -f infra/docker-compose.yml up -d --wait

down:
	# stops the containers
	docker compose -f infra/docker-compose.yml down

logs:
	# tails logs from all containers. Ctrl-C to exit; containers keep running
	docker compose -f infra/docker-compose.yml logs -f

reset:
	# stops and deletes volumes. Nuclear option.
	docker compose -f infra/docker-compose.yml down -v

api:
	# import app.main, find the object named `app`, and serve it
	# `--reload` watches files and restarts the server on change
	uv run uvicorn app.main:app --reload --port 8000

web:
	# runs the Next.js dev server
	cd web && pnpm dev

smoke:
	# runs the smoke bash script
	bash scripts/smoke.sh
```

## Create `CLAUDE.md` and `README.md`

```
# CLAUDE.md

See `docs/master-plan-v4.2.md` for the project plan.

Conventions: TBD — fill in after Phase 1.
```

`README.md`:
```
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
```

## Next.js scaffold

Next.js is a framework for building websites and web apps in React. React by itself is just a library for describing UI in JavaScript — it doesn't tell you how to handle routing between pages, fetch data on the server, bundle your code for production, or serve the result over HTTP. Next.js wraps React with all of that: file-based routing (a file at `app/about/page.tsx` automatically becomes the `/about` URL), a dev server with hot reload, server-side rendering, API routes, image optimization, and a production build command. For your project, it's the thing running on port 3000 that will show the query input, stream the agent's response, and render citation cards. You picked it because it's the industry default for React apps in 2026 — tons of documentation, Vercel maintains it, and it's what `create-next-app` gives you in 30 seconds.

Download the latest Next.js scaffolder, run it, and create the project in `./web/`.
When it finishes, `web/` is a complete runnable Next.js app.
```
pnpm create next-app@latest web
```

Accept the default when prompted.


## shadcn

shadcn is a way of getting pre-built, good-looking UI components (buttons, dialogs, dropdowns, form inputs, etc.) into your project. The twist that makes it different from traditional component libraries: instead of installing it as a dependency you import from, shadcn's CLI copies the component's source code directly into your repo — so `components/ui/button.tsx` is a file you own and can edit freely. You get Tailwind-styled, accessibility-correct components without the lock-in of a library you can't customize. When you ran `shadcn add button`, you added one file; when you need a dialog later, you'll run `shadcn add dialog` and get another file. For a backend-focused person on a tight frontend budget, this is ideal — you get professional-looking UI without becoming a CSS expert.

```
cd web

# temporarily downloads shadcn's CLI and runs its `init` command
pnpm dlx shadcn@latest init
# accept defaults, neutral base color, CSS variables yes ; pick Radix ; pick Nova

# copies the Button component source to `web/components/ui/button.tsx`
pnpm dlx shadcn@latest add button
cd ..
```

## Verify services

Run the following in 3 different shells:
```
# Shell 1
make up          # wait for "Container bdr-postgres Healthy" + opensearch healthy

# Shell 2
make api         # should see "Uvicorn running on http://127.0.0.1:8000"

# Shell 3
make web         # Next.js on http://localhost:3000
```

Then in a different shell, run:
```
make smoke
```

Then browse to the following to confirm:
```
http://localhost:8000/health
http://localhost:3000
```

