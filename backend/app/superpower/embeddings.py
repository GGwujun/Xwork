from __future__ import annotations

from dataclasses import dataclass

from app.config.ai_models import AIModelConfig


@dataclass
class EmbeddingResult:
    vector: list[float]
    model: str


class EmbeddingService:
    def __init__(self, provider: str | None = None, model_name: str | None = None):
        config = AIModelConfig.load()
        model = config.get_model(provider=provider, model_name=model_name)
        self.provider = model.provider
        self.model_name = model.model_name
        self.api_key = model.api_key

    def embed_text(self, text: str) -> EmbeddingResult:
        if self.provider == "openai":
            return self._embed_openai(text)
        raise ValueError(f"Unsupported embedding provider: {self.provider}")

    def _embed_openai(self, text: str) -> EmbeddingResult:
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:
            raise RuntimeError("openai package is required for embeddings") from exc

        client = OpenAI(api_key=self.api_key)
        response = client.embeddings.create(model=self.model_name, input=text)
        vector = response.data[0].embedding
        return EmbeddingResult(vector=vector, model=self.model_name)
