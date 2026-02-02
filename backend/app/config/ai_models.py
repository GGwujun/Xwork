from __future__ import annotations

import json
import os

from pydantic import BaseModel, Field, field_validator

from .base import BaseConfig


class AIModelSettings(BaseModel):
    provider: str
    model_name: str
    api_key: str
    temperature: float = 0.2

    @field_validator("provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value


class AIModelConfig(BaseConfig):
    env_prefix = "AI_"

    provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    api_key: str = ""
    temperature: float = 0.2
    models: list[AIModelSettings] = Field(default_factory=list)

    @field_validator("provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @classmethod
    def load(cls, env_file: str | None = None, override: bool = False) -> "AIModelConfig":
        config = super().load(env_file=env_file, override=override)
        models_json = os.environ.get("AI_MODELS")
        if models_json:
            try:
                data = json.loads(models_json)
            except json.JSONDecodeError as exc:
                raise ValueError("AI_MODELS must be valid JSON") from exc
            if not isinstance(data, list):
                raise ValueError("AI_MODELS must be a JSON list")
            config.models = [AIModelSettings.model_validate(item) for item in data]

        if not config.models and config.api_key:
            config.models = [
                AIModelSettings(
                    provider=config.provider,
                    model_name=config.model_name,
                    api_key=config.api_key,
                    temperature=config.temperature,
                )
            ]
        return config

    def get_model(self, provider: str | None = None, model_name: str | None = None) -> AIModelSettings:
        if not self.models:
            raise ValueError("No AI models configured")
        if provider:
            provider = provider.strip().lower()
        for model in self.models:
            if provider and model.provider != provider:
                continue
            if model_name and model.model_name != model_name:
                continue
            return model
        raise ValueError("No matching AI model found")
