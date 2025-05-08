from psycopg_pool import ConnectionPool
from .config import VectorizeConfig
from typing import Optional


class PGConnection:
    def __init__(self, cfg: VectorizeConfig):
        # build a DSN string
        dsn = (
            f"host={cfg.host} "
            f"port={cfg.port} "
            f"dbname={cfg.dbname} "
            f"user={cfg.user} "
            f"password={cfg.password}"
        )
        self.pool = ConnectionPool(dsn)

    def execute(self, sql: str, params: Optional[tuple] = None, *, fetch: bool = False):
        with self.pool.connection() as conn:
            cur = conn.execute(sql, params or ())
            return cur.fetchall() if fetch else None
