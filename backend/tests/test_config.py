import json
import os
import tempfile
import unittest

from app.config.base import BaseConfig
from app.config.database import DatabaseConfig
from app.config.redis import RedisConfig
from app.config.ai_models import AIModelConfig


class DummyConfig(BaseConfig):
    env_prefix = "DUMMY_"

    name: str
    count: int = 0


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env_backup = os.environ.copy()

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env_backup)

    def test_base_config_loads_from_env_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("DUMMY_NAME=from_file\nDUMMY_COUNT=42\n")
            temp_path = temp_file.name

        try:
            config = DummyConfig.load(env_file=temp_path, override=True)
        finally:
            os.remove(temp_path)

        self.assertEqual(config.name, "from_file")
        self.assertEqual(config.count, 42)

    def test_database_config_dsn(self) -> None:
        os.environ.update(
            {
                "DB_HOST": "db.local",
                "DB_PORT": "5433",
                "DB_DATABASE": "forge_db",
                "DB_USER": "forge_user",
                "DB_PASSWORD": "secret",
            }
        )
        config = DatabaseConfig.load()
        self.assertEqual(
            config.dsn(),
            "postgresql://forge_user:secret@db.local:5433/forge_db",
        )

    def test_redis_config_url(self) -> None:
        os.environ.update(
            {
                "REDIS_HOST": "redis.local",
                "REDIS_PORT": "6380",
                "REDIS_PASSWORD": "pass",
                "REDIS_DB": "2",
            }
        )
        config = RedisConfig.load()
        self.assertEqual(config.url(), "redis://:pass@redis.local:6380/2")

    def test_ai_model_config_from_json(self) -> None:
        models = [
            {
                "provider": "openai",
                "model_name": "gpt-4o-mini",
                "api_key": "key-a",
                "temperature": 0.1,
            },
            {
                "provider": "anthropic",
                "model_name": "claude-3-5",
                "api_key": "key-b",
                "temperature": 0.3,
            },
        ]
        os.environ["AI_MODELS"] = json.dumps(models)
        config = AIModelConfig.load()
        self.assertEqual(len(config.models), 2)
        self.assertEqual(config.get_model(provider="anthropic").model_name, "claude-3-5")


if __name__ == "__main__":
    unittest.main()
