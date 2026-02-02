import unittest

from app.spec_export import export_spec


class SpecExportTests(unittest.TestCase):
    def test_markdown_export_contains_sections(self) -> None:
        spec = {
            "project_name": "ExportProject",
            "requirement": {"summary": "Summary", "description": "Details"},
            "tasks": [{"id": "t1", "title": "Task", "description": "Desc", "status": "pending"}],
        }
        markdown = export_spec(spec, "markdown")
        self.assertIn("# OpenSpec: ExportProject", markdown)
        self.assertIn("## Requirement", markdown)
        self.assertIn("## Tasks", markdown)

    def test_html_export_contains_title(self) -> None:
        spec = {
            "project_name": "ExportProject",
            "requirement": {"summary": "Summary", "description": "Details"},
        }
        html = export_spec(spec, "html")
        self.assertIn("OpenSpec Export", html)
        self.assertIn("ExportProject", html)


if __name__ == "__main__":
    unittest.main()
