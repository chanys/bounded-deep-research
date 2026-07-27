# without the .PHONY, if a file named `up` existed, then `make up` would say "up is up to date" and do nothing
.PHONY: up down logs reset api web smoke eval-runs eval-score corpus-dump corpus-restore

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

# ----- Phase 4 eval (offline) -----
# eval-runs drives Phase A: run the frozen agent over the 62 gold questions x 3,
# resumable, on the production dense pgvector path. Pass ARGS to restrict, e.g.
# `make eval-runs ARGS="--only lc-0011 --runs 1"`.
eval-runs:
	RETRIEVAL_BACKEND=pgvector PYTHONUNBUFFERED=1 uv run python -m eval.run_batch $(ARGS)

# eval-score drives Phase D: score the runs with the frozen judge + extractors. Pass ARGS to
# restrict, e.g. `make eval-score ARGS="--only lc-0011,fc-0001"` or `ARGS=--report-only`.
eval-score:
	RETRIEVAL_BACKEND=pgvector PYTHONUNBUFFERED=1 uv run python -m eval.score_runs $(ARGS)

# ----- corpus load (local -> RDS) -----
# These move the embedded corpus from the local Postgres into RDS, so we never
# re-ingest or re-embed. corpus-dump writes a compressed snapshot of the local DB;
# corpus-restore loads it into a target DATABASE_URL (e.g. RDS via the SSM tunnel).

# Local container that holds the corpus. We use ITS pg_dump/pg_restore (PG16) because
# the Mac's host tools are newer (PG18) and inject settings like transaction_timeout
# that the PG16 RDS target rejects. Using the container's matched tools avoids that.
LOCAL_PG_CONTAINER ?= bdr-postgres

# Target connection for the restore. Defaults point at the SSM tunnel (127.0.0.1:5455).
# Pass the password via PGPASSWORD in the environment, NOT a URL.
PGHOST     ?= 127.0.0.1
PGPORT     ?= 5455
PGUSER     ?= bdr
PGDATABASE ?= bdr

corpus-dump:
	# Dump with the CONTAINER's PG16 pg_dump, written to a host file via stdout redirect.
	@docker exec -e PGPASSWORD=bdr_dev $(LOCAL_PG_CONTAINER) pg_dump -Fc -U bdr -d bdr > corpus.dump
	@echo "wrote corpus.dump ($$(du -h corpus.dump | cut -f1))"

corpus-restore:
	# Convert the dump to SQL with the container's PG16 pg_restore, then load via the host
	# psql through the tunnel. Reads the password from PGPASSWORD in the environment.
	@docker exec -i $(LOCAL_PG_CONTAINER) pg_restore --no-owner --no-acl -f - < corpus.dump \
		| psql -h $(PGHOST) -p $(PGPORT) -U $(PGUSER) -d $(PGDATABASE)
	@echo "restored corpus into $(PGHOST):$(PGPORT)/$(PGDATABASE)"
