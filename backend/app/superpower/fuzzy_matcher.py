from __future__ import annotations

from .models import Skill


def _ratio(a: str, b: str) -> float:
    try:
        from rapidfuzz import fuzz  # type: ignore
    except Exception:
        from difflib import SequenceMatcher

        return SequenceMatcher(None, a, b).ratio()
    return fuzz.ratio(a, b) / 100


def fuzzy_score(query: str, skill: Skill) -> float:
    if not query:
        return 0.0
    name_score = _ratio(query.lower(), skill.name.lower())
    file_score = _ratio(query.lower(), skill.file_path.lower())
    return max(name_score, file_score)
