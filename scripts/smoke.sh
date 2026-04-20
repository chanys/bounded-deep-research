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
