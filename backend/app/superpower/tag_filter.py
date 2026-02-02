from __future__ import annotations

from .models import Skill


def filter_by_tags(skills: list[Skill], tags: list[str] | None, mode: str = "any") -> list[Skill]:
    if not tags:
        return skills
    normalized = {tag.lower() for tag in tags}
    result: list[Skill] = []
    for skill in skills:
        skill_tags = {tag.lower() for tag in skill.tags}
        if mode == "all":
            if normalized.issubset(skill_tags):
                result.append(skill)
        else:
            if normalized.intersection(skill_tags):
                result.append(skill)
    return result
