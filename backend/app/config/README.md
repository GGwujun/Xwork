# Forge Config

Environment variables are loaded via `python-dotenv` and then validated by Pydantic.

## Database

- `DB_HOST` (default: localhost)
- `DB_PORT` (default: 5432)
- `DB_DATABASE` (default: forge)
- `DB_USER` (default: forge)
- `DB_PASSWORD` (default: empty)
- `DB_DRIVER` (default: postgresql)

## Redis

- `REDIS_HOST` (default: localhost)
- `REDIS_PORT` (default: 6379)
- `REDIS_PASSWORD` (optional)
- `REDIS_DB` (default: 0)
- `REDIS_MAX_CONNECTIONS` (default: 10)

## AI Models

- `AI_PROVIDER` (default: openai)
- `AI_MODEL_NAME` (default: gpt-4o-mini)
- `AI_API_KEY` (default: empty)
- `AI_TEMPERATURE` (default: 0.2)
- `AI_MODELS` (optional JSON list of models)

Example `AI_MODELS` value:

```json
[
  {"provider": "openai", "model_name": "gpt-4o-mini", "api_key": "...", "temperature": 0.2},
  {"provider": "anthropic", "model_name": "claude-3-5", "api_key": "...", "temperature": 0.3},
  {"provider": "deepseek", "model_name": "deepseek-reasoner", "api_key": "...", "temperature": 0.2}
]
```
