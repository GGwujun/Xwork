from __future__ import annotations

from .models import Skill


def compose_context(skills: list[Skill]) -> str:
    sections = []
    for skill in skills:
        header = f"## Skill: {skill.name}\nSource: {skill.file_path}"
        sections.append("\n".join([header, skill.content.strip()]))
    return "\n\n---\n\n".join(sections).strip()
