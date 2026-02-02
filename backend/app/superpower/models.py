from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


PriorityLevel = Literal["high", "medium", "low"]


class SkillMetadata(BaseModel):
    name: str = ""
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    priority: PriorityLevel = "medium"
    version: str | None = None


class Skill(BaseModel):
    name: str
    description: str
    content: str
    tags: list[str] = Field(default_factory=list)
    priority: PriorityLevel = "medium"
    version: str | None = None
    file_path: str
