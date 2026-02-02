import tempfile
import unittest
from pathlib import Path

from app.superpower.skills_loader import SkillsLoader
from app.superpower.skills_retriever import SkillsRetriever


class SkillsRetrieverTests(unittest.TestCase):
    def test_retriever_matches_query(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir) / "skills" / "beta"
            base.mkdir(parents=True, exist_ok=True)
            (base / "SKILL.md").write_text(
                """
---
name: beta-skill
description: Handles FastAPI endpoints
tags: [fastapi, api]
priority: medium
---

FastAPI routing guidance.
""".strip(),
                encoding="utf-8",
            )

            loader = SkillsLoader()
            loader.reload([Path(temp_dir) / "skills"])
            retriever = SkillsRetriever(loader)
            results = retriever.retrieve("fastapi endpoints", top_k=3)
            self.assertTrue(results)
            self.assertEqual(results[0][0].name, "beta-skill")


if __name__ == "__main__":
    unittest.main()
