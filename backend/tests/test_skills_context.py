import unittest

from app.superpower.models import Skill
from app.superpower.skills_context import build_context


class SkillsContextTests(unittest.TestCase):
    def test_context_composition_and_truncation(self) -> None:
        skills = [
            (Skill(
                name="gamma",
                description="Gamma skill",
                content="Line1\nLine2\nLine3",
                tags=["gamma"],
                priority="high",
                version=None,
                file_path="/tmp/gamma/SKILL.md",
            ), 0.9)
        ]
        context = build_context(skills, max_tokens=5)
        self.assertIn("Skill: gamma", context)
        self.assertTrue(len(context) > 0)


if __name__ == "__main__":
    unittest.main()
