from __future__ import annotations

from pathlib import Path

from .models import SkillMetadata


def _parse_frontmatter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- ") and current_list_key:
            items = data.get(current_list_key)
            if isinstance(items, list):
                items.append(line[2:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            data[key] = []
            current_list_key = key
            continue
        current_list_key = None
        if value.startswith("[") and value.endswith("]"):
            items = [
                item.strip().strip("\"'")
                for item in value[1:-1].split(",")
                if item.strip()
            ]
            data[key] = items
        else:
            data[key] = value.strip("\"'")
    return data


def parse_markdown_with_frontmatter(file_path: str | Path) -> tuple[SkillMetadata, str]:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end_index = None
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                end_index = index
                break
        if end_index is not None:
            frontmatter = _parse_frontmatter(lines[1:end_index])
            metadata = SkillMetadata.model_validate(frontmatter)
            content = "\n".join(lines[end_index + 1 :]).strip()
            return metadata, content
    return SkillMetadata(), text.strip()
