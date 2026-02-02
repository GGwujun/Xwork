from __future__ import annotations

from .models import Skill


def relevance_score(
    skill: Skill,
    keyword: float,
    tag: float,
    fuzzy: float,
    weights: dict[str, float] | None = None,
) -> float:
    w = weights or {"keyword": 0.6, "tag": 0.2, "fuzzy": 0.2}
    priority_boost = {"high": 0.1, "medium": 0.0, "low": -0.05}.get(skill.priority, 0.0)
    return keyword * w["keyword"] + tag * w["tag"] + fuzzy * w["fuzzy"] + priority_boost
