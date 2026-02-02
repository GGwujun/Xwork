import unittest

from fastapi.testclient import TestClient

from main import app


class SkillsApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_list_skills(self) -> None:
        response = self.client.get("/skills")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_search_skills(self) -> None:
        response = self.client.post(
            "/skills/search",
            json={"query": "coding standards", "tags": [], "top_k": 3},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_context_build(self) -> None:
        response = self.client.post(
            "/context/build",
            json={"query": "coding standards", "top_k": 2, "max_tokens": 200},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("context", payload)
        self.assertIn("skills", payload)


if __name__ == "__main__":
    unittest.main()
