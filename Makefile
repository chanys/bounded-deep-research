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
