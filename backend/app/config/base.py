from __future__ import annotations

import os
from typing import ClassVar, Type, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

ConfigT = TypeVar("ConfigT", bound="BaseConfig")


class BaseConfig(BaseModel):
    """Base configuration loader using .env + environment variables."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)
    env_prefix: ClassVar[str] = ""

    @classmethod
    def _env_key(cls, field_name: str) -> str:
        return f"{cls.env_prefix}{field_name}".upper()

    @classmethod
    def load(cls: Type[ConfigT], env_file: str | None = None, override: bool = False) -> ConfigT:
        load_dotenv(dotenv_path=env_file, override=override)
        values: dict[str, str] = {}
        for field_name in cls.model_fields:
            key = cls._env_key(field_name)
            if key in os.environ:
                values[field_name] = os.environ[key]
        return cls.model_validate(values)
