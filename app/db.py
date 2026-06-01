import psycopg
from contextlib import contextmanager
from pgvector.psycopg import register_vector
from app.config import settings

"""
1. psycopg.connect(settings.database_url, ...): opens connection to Postgres using the URL from settings
2. row_factory=psycopg.rows.dict_row : sets how query results are shaped.
     - dict_row: query results are returned as dict, e.g. {"id": ..., "title": ...} instead of default ("...", "...") tuple.
3. register_vector(conn): allow conversion between Python list[float] and Postgres vector(3072).
                          without this, you will get raw bytes back from 'SELECT embedding' instead of Python list.
"""
def get_conn():
    conn = psycopg.connect(settings.database_url, row_factory=psycopg.rows.dict_row)
    register_vector(conn)
    return conn

"""
@contextmanager lets me write a `with` block that: runs setup code, gives the block something to use, does cleanup after

Without the @contextmanager, every place using the database would need the following plumbing code:
```
conn = get_conn()
try:
    result = conn.execute("SELECT 1").fetchall()
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

But now with @contextmanager, I can just write:
with transaction() as conn:
    result = conn.execute("SELECT 1").fetchall()
"""
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
