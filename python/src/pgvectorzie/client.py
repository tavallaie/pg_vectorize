# pgvectorize/client.py

from typing import Any, List, Optional
from .config import VectorizeConfig
from .connection import PGConnection
from .guc import VectorizeGuc


class PgVectorize:
    def __init__(self, cfg: VectorizeConfig):
        self.cfg = cfg
        self.conn = PGConnection(cfg)
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS vectorize CASCADE;")

    def _alter_system(self, key: str, value: Any):
        """Cluster-wide override + reload."""
        if isinstance(value, str):
            safe = value.replace("'", "''")
            literal = f"'{safe}'"
        else:
            literal = str(value)

        with self.conn.pool.connection() as conn:
            conn.autocommit = True
            conn.execute(f"ALTER SYSTEM SET {key} = {literal};")
            conn.execute("SELECT pg_reload_conf();")
            conn.autocommit = False

    def set_guc(self, guc: VectorizeGuc, value: Any):
        """
        Cluster-wide override + reload for any vectorize.* GUC.
        """
        self._alter_system(guc.value, value)

    def get_guc(self, guc: VectorizeGuc) -> Optional[str]:
        row = self.conn.execute(f"SHOW {guc.value};", fetch=True)
        return row[0][0] if row else None

    def init_table(
        self,
        job_name: str,
        relation: str,
        primary_key: str,
        columns: List[str],
        transformer: str,
        schedule: str = "realtime",
    ):
        sql = """
        SELECT vectorize.table(
          job_name    => %s,
          relation    => %s,
          primary_key => %s,
          columns     => %s::text[],
          transformer => %s,
          schedule    => %s
        );
        """
        self.conn.execute(
            sql, (job_name, relation, primary_key, columns, transformer, schedule)
        )

    def search(
        self,
        job_name: str,
        query: str,
        return_columns: List[str],
        num_results: int = 5,
    ):
        sql = """
        SELECT * FROM vectorize.search(
          job_name       => %s,
          query          => %s,
          return_columns => %s::text[],
          num_results    => %s
        );
        """
        rows = self.conn.execute(
            sql, (job_name, query, return_columns, num_results), fetch=True
        )
        return [r[0] for r in rows]

    def rag(
        self,
        job_name: str,
        query: str,
        chat_model: str = "openai/gpt-3.5-turbo",
    ) -> str:
        sql = """
        SELECT (vectorize.rag(
          job_name   => %s,
          query      => %s,
          chat_model => %s
        )).chat_response;
        """
        row = self.conn.execute(sql, (job_name, query, chat_model), fetch=True)
        return row[0][0] if row else ""

    def update_schedule(self, job_name: str, cron: str):
        sql = """
        SELECT vectorize.update_schedule(
          job_name => %s,
          schedule => %s
        );
        """
        self.conn.execute(sql, (job_name, cron))
