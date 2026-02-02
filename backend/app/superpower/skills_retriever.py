from __future__ import annotations

from .fuzzy_matcher import fuzzy_score
from .keyword_matcher import keyword_score, _tokenize
from .models import Skill
from .relevance_scorer import relevance_score
from .skills_cache import LruCache
from .skills_loader import SkillsLoader
from .tag_filter import filter_by_tags


class SkillsRetriever:
    def __init__(self, loader: SkillsLoader, max_cache: int = 256):
        self.loader = loader
        self._query_cache = LruCache[list[tuple[Skill, float]]](max_cache)

    def retrieve(self, query: str, tags: list[str] | None = None, top_k: int = 5) -> list[tuple[Skill, float]]:
        cache_key = f"{query}|{','.join(tags or [])}|{top_k}"
        cached = self._query_cache.get(cache_key)
        if cached is not None:
            return cached

        skills = self.loader.list_skills()
        skills = filter_by_tags(skills, tags)

        corpus_tokens = [_tokenize(skill.content) for skill in skills]
        results: list[tuple[Skill, float]] = []
        for skill in skills:
            keyword = keyword_score(query, skill, corpus_tokens)
            tag_score = 1.0 if tags and any(tag.lower() in [t.lower() for t in skill.tags] for tag in tags) else 0.0
            fuzzy = fuzzy_score(query, skill)
            score = relevance_score(skill, keyword, tag_score, fuzzy)
            results.append((skill, score))

        results.sort(key=lambda item: item[1], reverse=True)
        top = results[:top_k]
        self._query_cache.set(cache_key, top)
        return top
