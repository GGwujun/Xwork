"""Configuration package for Forge Engine."""

from pydantic import BaseModel

from .ai_models import AIModelConfig, AIModelSettings
from .base import BaseConfig
from .database import DatabaseConfig
from .redis import RedisConfig


class AppConfig(BaseModel):
    database: DatabaseConfig
    redis: RedisConfig
    ai: AIModelConfig

    @classmethod
    def load(cls, env_file: str | None = None) -> "AppConfig":
        return cls(
            database=DatabaseConfig.load(env_file=env_file),
            redis=RedisConfig.load(env_file=env_file),
            ai=AIModelConfig.load(env_file=env_file),
        )


def load_configs(env_file: str | None = None) -> AppConfig:
    return AppConfig.load(env_file=env_file)


__all__ = [
    "AIModelConfig",
    "AIModelSettings",
    "AppConfig",
    "BaseConfig",
    "DatabaseConfig",
    "RedisConfig",
    "load_configs",
]
