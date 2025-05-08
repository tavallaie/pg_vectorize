import os
from dataclasses import dataclass, field


@dataclass
class VectorizeConfig:
    host: str = field(default_factory=lambda: os.getenv("PG_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("PG_PORT", "5432")))
    dbname: str = field(default_factory=lambda: os.getenv("PG_DATABASE", "postgres"))
    user: str = field(default_factory=lambda: os.getenv("PG_USERNAME", "postgres"))
    password: str = field(default_factory=lambda: os.getenv("PG_PASSWORD", "postgres"))
