import unittest

from app.spec_diff import diff_specs, merge_specs


class SpecDiffTests(unittest.TestCase):
    def test_diff_report_detects_changes(self) -> None:
        left = {"project_name": "A", "requirement": {"summary": "S", "description": "D"}}
        right = {
            "project_name": "A",
            "requirement": {"summary": "S", "description": "Updated"},
            "tasks": [{"id": "t1"}],
        }
        report = diff_specs(left, right)
        self.assertIn("requirement.description", report.modified)
        self.assertIn("tasks", report.added)
        self.assertTrue(report.diff)

    def test_merge_prefers_incoming(self) -> None:
        base = {"project_name": "A", "requirement": {"summary": "S", "description": "D"}}
        incoming = {"requirement": {"description": "New"}, "tasks": [{"id": "t1"}]}
        merged = merge_specs(base, incoming, strategy="prefer_incoming")
        self.assertEqual(merged["requirement"]["description"], "New")
        self.assertEqual(len(merged["tasks"]), 1)


if __name__ == "__main__":
    unittest.main()
