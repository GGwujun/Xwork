from __future__ import annotations

import asyncio
import logging
import time

from app.config.ai_models import AIModelConfig


class LlmClient:
    def __init__(self, provider: str | None = None, model_name: str | None = None):
        config = AIModelConfig.load()
        model = config.get_model(provider=provider, model_name=model_name)
        self.provider = model.provider
        self.model_name = model.model_name
        self.api_key = model.api_key
        self.temperature = model.temperature

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        provider = self.provider.strip().lower()
        start = time.perf_counter()
        try:
            if provider == "deepseek":
                result = await asyncio.to_thread(
                    self._generate_openai,
                    system_prompt,
                    user_prompt,
                    base_url="https://api.deepseek.com",
                )
            elif provider == "openai":
                result = await asyncio.to_thread(self._generate_openai, system_prompt, user_prompt)
            elif provider == "anthropic":
                result = await asyncio.to_thread(self._generate_anthropic, system_prompt, user_prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
            duration_ms = int((time.perf_counter() - start) * 1000)
            logging.getLogger(__name__).info(
                "LLM request completed",
                extra={"provider": self.provider, "model": self.model_name, "duration_ms": duration_ms},
            )
            return result
        except Exception as exc:
            logging.getLogger(__name__).error(
                "LLM request failed",
                extra={"provider": self.provider, "model": self.model_name},
                exc_info=exc,
            )
            raise

    def _generate_openai(self, system_prompt: str, user_prompt: str, base_url: str | None = None) -> str:
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:
            raise RuntimeError("openai package is required for OpenAI provider") from exc

        if base_url:
            client = OpenAI(api_key=self.api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""

    def _generate_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        try:
            import anthropic  # type: ignore
        except Exception as exc:
            raise RuntimeError("anthropic package is required for Anthropic provider") from exc

        client = anthropic.Anthropic(api_key=self.api_key)
        message = client.messages.create(
            model=self.model_name,
            temperature=self.temperature,
            system=system_prompt,
            max_tokens=2048,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if not message.content:
            return ""
        if isinstance(message.content, list):
            return "".join(getattr(block, "text", "") for block in message.content)
        return str(message.content)
