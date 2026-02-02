from __future__ import annotations

from .models import Skill


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def sort_by_priority(skills: list[tuple[Skill, float]]) -> list[tuple[Skill, float]]:
    return sorted(
        skills,
        key=lambda item: (_PRIORITY_ORDER.get(item[0].priority, 1), -item[1]),
    )
