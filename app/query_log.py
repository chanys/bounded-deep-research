"""Persistent log of every /query request: who asked what, and what happened.

One row per request that got past the channel check, including the ones the spend
cap or the per-IP quota turned away, so the owner can see real usage (and who hits
the limits) via GET /admin/queries. Lives in Postgres next to daily_spend, so it
survives restarts and deploys; it does NOT survive a `terraform destroy` unless RDS
is dumped first.
"""
from core.db import transaction


def ensure_table() -> None:
    """Create the query_log table if it doesn't exist. Safe to call on every startup."""
    with transaction() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS query_log (
                id       BIGSERIAL PRIMARY KEY,
                ts       TIMESTAMPTZ NOT NULL DEFAULT now(),
                ip       TEXT NOT NULL,
                tier     TEXT NOT NULL,      -- 'anon' | 'coded' | 'owner'
                channel  TEXT NOT NULL,
                query    TEXT NOT NULL,
                outcome  TEXT NOT NULL,      -- 'answered' | 'cached' | 'error' | 'over_cap' | 'over_quota'
                run_id   TEXT,
                usd_cost NUMERIC
            )
            """
        )


def record(ip: str, tier: str, channel: str, query: str, outcome: str,
           run_id: str | None = None, usd_cost: float | None = None) -> None:
    """Append one request to the log."""
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO query_log (ip, tier, channel, query, outcome, run_id, usd_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (ip, tier, channel, query, outcome, run_id, usd_cost),
        )


def recent(limit: int) -> list[dict]:
    """The most recent `limit` requests, newest first."""
    with transaction() as conn:
        return conn.execute(
            """
            SELECT ts, ip, tier, channel, query, outcome, run_id, usd_cost
            FROM query_log ORDER BY id DESC LIMIT %s
            """,
            (limit,),
        ).fetchall()
