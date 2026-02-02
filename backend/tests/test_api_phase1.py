import unittest

from fastapi.testclient import TestClient

from main import app


class Phase1ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload.get("status"), "healthy")

    def test_generate_spec_endpoint(self) -> None:
        response = self.client.post(
            "/spec/generate",
            json={"summary": "Test", "description": "Generate a spec"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("project_name", payload)
        self.assertIn("requirement", payload)


if __name__ == "__main__":
    unittest.main()
