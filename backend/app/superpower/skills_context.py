from __future__ import annotations

from .content_truncator import truncate_content
from .context_composer import compose_context
from .models import Skill
from .priority_sorter import sort_by_priority


def build_context(skills_with_scores: list[tuple[Skill, float]], max_tokens: int = 2000, model_name: str | None = None) -> str:
    ordered = sort_by_priority(skills_with_scores)
    skills = [item[0] for item in ordered]
    context = compose_context(skills)
    return truncate_content(context, max_tokens=max_tokens, model_name=model_name)
