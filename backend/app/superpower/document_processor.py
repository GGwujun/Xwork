from __future__ import annotations

from pathlib import Path


def _chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    for paragraph in paragraphs:
        tentative = "\n\n".join(current + [paragraph])
        if len(tentative) <= max_chars:
            current.append(paragraph)
            continue
        if current:
            chunks.append("\n\n".join(current))
        if len(paragraph) > max_chars:
            for i in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[i : i + max_chars])
            current = []
        else:
            current = [paragraph]
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def process_markdown(path: str | Path) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    return _chunk_text(text)


def process_code(path: str | Path) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    return _chunk_text(text)
