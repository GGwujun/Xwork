import tempfile
import unittest

from app.schemas import OpenSpec, Requirement
from app.spec_storage import SpecStorage


class SpecStorageTests(unittest.TestCase):
    def _spec(self) -> OpenSpec:
        return OpenSpec(
            project_name="StorageProject",
            requirement=Requirement(summary="Summary", description="Details"),
        )

    def test_save_and_load_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = SpecStorage(base_dir=tmp_dir)
            spec = self._spec()
            version = storage.save_spec(spec)
            self.assertTrue(version.version_id)

            loaded = storage.load_spec(spec.project_name, version.version_id)
            self.assertEqual(loaded.project_name, spec.project_name)
            self.assertEqual(loaded.requirement.summary, spec.requirement.summary)

    def test_list_versions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = SpecStorage(base_dir=tmp_dir)
            spec = self._spec()
            storage.save_spec(spec)
            storage.save_spec(spec)
            versions = storage.list_versions(spec.project_name)
            self.assertEqual(len(versions), 2)
            self.assertLessEqual(versions[0].created_at, versions[1].created_at)


if __name__ == "__main__":
    unittest.main()
