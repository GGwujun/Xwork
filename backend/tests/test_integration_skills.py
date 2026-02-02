import unittest

from fastapi.testclient import TestClient

from main import app


class SkillsIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_search_then_build_context(self) -> None:
        search = self.client.post(
            "/skills/search",
            json={"query": "framework", "tags": [], "top_k": 2},
        )
        self.assertEqual(search.status_code, 200)
        results = search.json()
        self.assertIsInstance(results, list)

        context = self.client.post(
            "/context/build",
            json={"query": "framework", "top_k": 2, "max_tokens": 300},
        )
        self.assertEqual(context.status_code, 200)
        payload = context.json()
        self.assertIsInstance(payload.get("context"), str)
        self.assertIsInstance(payload.get("skills"), list)


if __name__ == "__main__":
    unittest.main()
