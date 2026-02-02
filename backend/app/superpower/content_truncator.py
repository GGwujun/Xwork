from __future__ import annotations

from .token_counter import get_token_counter


def truncate_content(text: str, max_tokens: int, model_name: str | None = None) -> str:
    counter = get_token_counter(model_name)
    if counter(text) <= max_tokens:
        return text
    lines = text.splitlines()
    truncated: list[str] = []
    for line in lines:
        truncated.append(line)
        if counter("\n".join(truncated)) >= max_tokens:
            break
    return "\n".join(truncated).strip()
