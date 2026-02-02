from __future__ import annotations

from typing import Callable


def _fallback_counter(text: str) -> int:
    return max(1, len(text.split()))


def get_token_counter(model_name: str | None = None) -> Callable[[str], int]:
    try:
        import tiktoken  # type: ignore
    except Exception:
        return _fallback_counter
    encoding = tiktoken.encoding_for_model(model_name or "gpt-4")

    def counter(text: str) -> int:
        return len(encoding.encode(text))

    return counter
