import tempfile
import unittest

from fastapi.testclient import TestClient

from main import app
from app.schemas import OpenSpec
from app.spec_storage import SpecStorage
from app.validators import validate_open_spec


class Phase1IntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_generate_validate_store_roundtrip(self) -> None:
        response = self.client.post(
            "/spec/generate",
            json={"summary": "Roundtrip", "description": "Spec storage"},
        )
        self.assertEqual(response.status_code, 200)
        spec = OpenSpec.model_validate(response.json())
        validate_open_spec(spec)

        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = SpecStorage(base_dir=tmp_dir)
            version = storage.save_spec(spec)
            loaded = storage.load_spec(spec.project_name, version.version_id)
            self.assertEqual(loaded.project_name, spec.project_name)
            self.assertEqual(loaded.requirement.summary, spec.requirement.summary)


if __name__ == "__main__":
    unittest.main()
