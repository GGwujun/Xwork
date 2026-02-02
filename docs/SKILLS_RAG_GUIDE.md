# Skills RAG Guide

This guide explains how Skills-based RAG works in the Enterprise Forge backend, how to write Skills, and how to use the APIs.

## Overview

The Skills-based RAG pipeline:

1. **Skills Loader** discovers `.opencode/skill/**/SKILL.md` and `.opencode/skills/**/SKILL.md`.
2. **Skills Retriever** scores skills using keyword, tag, and fuzzy matching.
3. **Skills Context Builder** composes and truncates the context.
4. **AgentSwarm** injects context into prompts for LLM generation.

## Directory Layout

```
.opencode/
  skill/
    coding-standards/
      SKILL.md
    framework-docs/
      SKILL.md
    best-practices/
      SKILL.md
    common-solutions/
      SKILL.md
```

## Skill File Format

Each skill is a markdown file with YAML frontmatter:

```
---
name: my-skill
description: Brief description
tags: [fastapi, api, testing]
priority: high
version: "1.0"
---

# Title
Content here...
```

### Frontmatter Fields

- `name` (required): Unique skill name.
- `description` (optional): Human-readable summary.
- `tags` (optional): Keyword tags to filter.
- `priority` (optional): `high`, `medium`, `low`.
- `version` (optional): Semantic string.

## APIs

### List Skills

`GET /skills`

Returns all loaded skills.

### Get a Skill

`GET /skills/{name}`

Returns a specific skill by name.

### Reload Skills

`POST /skills/reload`

Reloads skills from disk and returns a count.

### Search Skills

`POST /skills/search`

Body:

```json
{
  "query": "fastapi routing",
  "tags": ["fastapi"],
  "top_k": 5
}
```

Returns a list of skills with relevance scores.

### Build Context

`POST /context/build`

Body:

```json
{
  "query": "fastapi routing",
  "tags": ["fastapi"],
  "top_k": 5,
  "max_tokens": 1800,
  "model_name": "gpt-4o-mini"
}
```

Returns:

```json
{
  "context": "...",
  "skills": ["framework-docs", "coding-standards"]
}
```

## LLM Integration

`backend/app/agent_swarm.py` fetches context via `context_server.build_skills_context()` and injects it into prompt templates (`backend/app/prompts/templates.py`).

## Vector Search (Optional)

If `ENABLE_VECTOR_SEARCH=1`, the Context Server will initialize the hybrid retriever and index skill contents into ChromaDB. Vector search results are merged with Skills-based results.

## Troubleshooting

- **No skills loaded**: check `.opencode/skill` and `.opencode/skills` directories.
- **Search returns empty**: verify tags and query text.
- **Context too long**: lower `max_tokens`.
- **Embedding errors**: ensure `openai` and `chromadb` are installed and configured.

## Best Practices

- Keep skills focused and scoped.
- Use descriptive tags for better search.
- Avoid duplicate or overlapping content.
- Keep skill content up to date with internal standards.
