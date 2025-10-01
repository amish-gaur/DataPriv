import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db(max_retries: int = 20, delay_seconds: float = 1.5) -> None:
    """Initialize database and retry until Postgres is ready.

    This avoids startup race conditions when the API boots before the DB.
    """
    last_error: Exception | None = None
    for _ in range(max_retries):
        try:
            with engine.begin() as conn:
                conn.execute(text(
                    """
                    CREATE TABLE IF NOT EXISTS site_summary (
                      domain TEXT PRIMARY KEY,
                      source_url TEXT,
                      summary_json JSONB,
                      risk_score REAL,
                      updated_at TIMESTAMP DEFAULT NOW()
                    );
                    """
                ))
            return
        except Exception as e:  # pragma: no cover - defensive startup
            last_error = e
            time.sleep(delay_seconds)
    # If we exhausted retries, re-raise the last error for visibility
    if last_error:
        raise last_error
