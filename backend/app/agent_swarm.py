import json
import uuid
from typing import Any

from app.context_server import context_server
from app.llm.client import LlmClient
from app.prompts.templates import build_architect_prompt, build_developer_prompt, build_pm_prompt
from app.schemas import ApiEndpoint, DataModel, Design, OpenSpec, Requirement, Task

class AgentSwarm:
    def __init__(self):
        pass

    async def generate_spec(self, requirements: Requirement) -> OpenSpec:
        """
        Orchestrate the PM and Architect agents to generate an OpenSpec.
        """
        context, _skills = context_server.build_skills_context(
            query=requirements.summary or "coding standards",
            tags=[],
            top_k=5,
            max_tokens=1800,
        )

        client = LlmClient()

        pm_system, pm_user = build_pm_prompt(requirements, context)
        pm_response = await client.generate(pm_system, pm_user)
        pm_json = _parse_json(pm_response)

        arch_system, arch_user = build_architect_prompt(requirements, context)
        arch_response = await client.generate(arch_system, arch_user)
        arch_json = _parse_json(arch_response)

        dev_system, dev_user = build_developer_prompt(requirements, context)
        dev_response = await client.generate(dev_system, dev_user)
        dev_json = _parse_json(dev_response)

        project_name = f"Project-{uuid.uuid4().hex[:8]}"
        design = Design(
            architecture_overview=_normalize_architecture_overview(
                arch_json.get("architecture_overview", "")
            ),
            api_endpoints=[ApiEndpoint(**item) for item in arch_json.get("api_endpoints", [])],
            data_models=[DataModel(**item) for item in arch_json.get("data_models", [])],
        )

        tasks = [
            Task(
                id=str(uuid.uuid4()),
                title=task.get("title", "Untitled Task"),
                description=task.get("description", ""),
                status="pending",
            )
            for task in dev_json.get("tasks", [])
        ]

        requirements.summary = pm_json.get("summary", requirements.summary)
        requirements.description = pm_json.get("description", requirements.description)
        requirements.acceptance_criteria = pm_json.get("acceptance_criteria", requirements.acceptance_criteria)

        return OpenSpec(
            project_name=project_name,
            requirement=requirements,
            design=design,
            tasks=tasks,
        )


def _parse_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    if start == -1:
        raise ValueError("LLM response did not contain JSON")
    payload = text[start:]
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(payload)
    if not isinstance(data, dict):
        raise ValueError("LLM response JSON was not an object")
    return data


def _normalize_architecture_overview(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return str(value)

agent_swarm = AgentSwarm()
