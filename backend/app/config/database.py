from __future__ import annotations

from pydantic import Field

from .base import BaseConfig


class DatabaseConfig(BaseConfig):
    env_prefix = "DB_"

    host: str = "localhost"
    port: int = 5432
    database: str = "forge"
    user: str = "forge"
    password: str = ""
    driver: str = Field(default="postgresql", description="Database driver name")

    def dsn(self) -> str:
        credentials = self.user
        if self.password:
            credentials = f"{self.user}:{self.password}"
        return f"{self.driver}://{credentials}@{self.host}:{self.port}/{self.database}"
