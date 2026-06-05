"""Persistent daily spend circuit-breaker.

A public demo must never run up an unbounded OpenAI bill. We keep a running total of
per-run cost for the current (UTC) day in a Postgres table, so it survives restarts and
deploys (unlike an in-memory counter), and refuse new queries once the day's total
reaches a cap. This is the absolute ceiling that makes the URL safe to share.
"""
from datetime import datetime, timezone, date

from app.db import transaction


def ensure_tables() -> None:
    """Create the tables we need if they don't exist. Safe to call on every startup."""
    with transaction() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_spend (
                day    DATE NOT NULL,
                bucket TEXT NOT NULL,          -- 'public' or 'owner' (separate budgets)
                usd    NUMERIC NOT NULL DEFAULT 0,
                PRIMARY KEY (day, bucket)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ip_usage (
                day   DATE NOT NULL,
                ip    TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (day, ip)
            )
            """
        )


def _today() -> date:
    # UTC, so the daily window is stable no matter where the server runs.
    return datetime.now(timezone.utc).date()


def today_spend(bucket: str) -> float:
    """Total USD spent so far today in one budget bucket ('public' or 'owner')."""
    with transaction() as conn:
        row = conn.execute(
            "SELECT usd FROM daily_spend WHERE day = %s AND bucket = %s",
            (_today(), bucket),
        ).fetchone()
    return float(row["usd"]) if row else 0.0


def add_spend(bucket: str, usd: float) -> None:
    """Add one run's cost to today's running total for its budget bucket."""
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO daily_spend (day, bucket, usd) VALUES (%s, %s, %s)
            ON CONFLICT (day, bucket) DO UPDATE SET usd = daily_spend.usd + EXCLUDED.usd
            """,
            (_today(), bucket, usd),
        )


def over_cap(bucket: str, cap: float) -> bool:
    """True if today's spend in `bucket` has already reached `cap`."""
    return today_spend(bucket) >= cap


def check_and_count(ip: str, limit: int) -> bool:
    """Atomically: if this IP is under `limit` for today, count this request and return
    True (allowed); otherwise return False (over quota) and count nothing.

    The single SQL statement does it race-free: a brand-new (day, ip) inserts count=1;
    an existing row increments ONLY while still under the limit (the WHERE on the
    conflict update). When at/over the limit the update is skipped, so RETURNING yields
    no row and we return False.
    """
    with transaction() as conn:
        row = conn.execute(
            """
            INSERT INTO ip_usage (day, ip, count) VALUES (%s, %s, 1)
            ON CONFLICT (day, ip) DO UPDATE
                SET count = ip_usage.count + 1
                WHERE ip_usage.count < %s
            RETURNING count
            """,
            (_today(), ip, limit),
        ).fetchone()
    return row is not None
