from __future__ import annotations

from pathlib import Path
import logging

from .markdown_parser import parse_markdown_with_frontmatter
from .models import Skill
from .skills_cache import LruCache
from .skills_scanner import scan_skill_files

logger = logging.getLogger(__name__)


class SkillsLoader:
    def __init__(self, max_cache: int = 256):
        self._skill_cache = LruCache[Skill](max_cache)
        self._skills_by_name: dict[str, Skill] = {}
        self._skills_by_tag: dict[str, list[Skill]] = {}

    def reload(self, base_dirs: list[Path] | None = None) -> list[Skill]:
        self._skills_by_name.clear()
        self._skills_by_tag.clear()
        self._skill_cache.clear()
        skills = []
        for path in scan_skill_files(base_dirs):
            skill = self._load_skill(path)
            if not skill:
                continue
            self._skills_by_name[skill.name] = skill
            for tag in skill.tags:
                self._skills_by_tag.setdefault(tag, []).append(skill)
            skills.append(skill)
        logger.info("Skills reloaded", extra={"skill_count": len(skills)})
        return skills

    def list_skills(self) -> list[Skill]:
        return list(self._skills_by_name.values())

    def get_skill(self, name: str) -> Skill | None:
        cached = self._skill_cache.get(name)
        if cached:
            return cached
        skill = self._skills_by_name.get(name)
        if skill:
            self._skill_cache.set(name, skill)
        return skill

    def skills_by_tag(self, tag: str) -> list[Skill]:
        return self._skills_by_tag.get(tag, [])

    def _load_skill(self, path: Path) -> Skill | None:
        metadata, content = parse_markdown_with_frontmatter(path)
        name = metadata.name or path.parent.name
        return Skill(
            name=name,
            description=metadata.description,
            content=content,
            tags=metadata.tags,
            priority=metadata.priority,
            version=metadata.version,
            file_path=str(path),
        )
