from __future__ import annotations

from .base import BaseConfig


class RedisConfig(BaseConfig):
    env_prefix = "REDIS_"

    host: str = "localhost"
    port: int = 6379
    password: str | None = None
    db: int = 0
    max_connections: int = 10

    def url(self) -> str:
        auth = ""
        if self.password:
            auth = f":{self.password}@"
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"
