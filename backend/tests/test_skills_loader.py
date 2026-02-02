import tempfile
import unittest
from pathlib import Path

from app.superpower.skills_loader import SkillsLoader


class SkillsLoaderTests(unittest.TestCase):
    def test_loader_parses_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir) / "skills" / "alpha"
            base.mkdir(parents=True, exist_ok=True)
            skill_path = base / "SKILL.md"
            skill_path.write_text(
                """
---
name: alpha-skill
description: Alpha description
tags: [alpha, test]
priority: high
version: "1.2"
---

Hello world
""".strip(),
                encoding="utf-8",
            )

            loader = SkillsLoader()
            skills = loader.reload([Path(temp_dir) / "skills"])
            self.assertEqual(len(skills), 1)
            self.assertEqual(skills[0].name, "alpha-skill")
            self.assertEqual(skills[0].description, "Alpha description")
            self.assertIn("alpha", skills[0].tags)
            self.assertEqual(skills[0].priority, "high")
            self.assertEqual(skills[0].version, "1.2")


if __name__ == "__main__":
    unittest.main()
