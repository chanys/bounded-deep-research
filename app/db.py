import psycopg
from contextlib import contextmanager
from app.config import settings

def get_conn():
    return psycopg.connect(settings.database_url, row_factory=psycopg.rows.dict_row)

@contextmanager
def transaction():
    """Auto-commits on exit, rolls back on exception."""
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()