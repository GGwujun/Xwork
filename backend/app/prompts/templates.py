from __future__ import annotations

from app.schemas import Requirement


def build_pm_prompt(requirement: Requirement, context: str) -> tuple[str, str]:
    system = "You are a product manager. Produce concise user stories and acceptance criteria in JSON."
    user = (
        "Use the context below to follow company standards.\n\n"
        f"Context:\n{context}\n\n"
        "Return JSON with keys: summary, description, acceptance_criteria (list of strings).\n\n"
        f"Requirement summary: {requirement.summary}\n"
        f"Requirement description: {requirement.description}\n"
    )
    return system, user


def build_architect_prompt(requirement: Requirement, context: str) -> tuple[str, str]:
    system = "You are a software architect. Produce architecture and API design in JSON."
    user = (
        "Use the context below to follow company standards.\n\n"
        f"Context:\n{context}\n\n"
        "Return JSON with keys: architecture_overview (string), api_endpoints (list), data_models (list).\n\n"
        f"Requirement summary: {requirement.summary}\n"
        f"Requirement description: {requirement.description}\n"
    )
    return system, user


def build_developer_prompt(requirement: Requirement, context: str) -> tuple[str, str]:
    system = "You are a senior developer. Propose an implementation task list in JSON."
    user = (
        "Use the context below to follow company standards.\n\n"
        f"Context:\n{context}\n\n"
        "Return JSON with key: tasks (list of objects with title, description).\n\n"
        f"Requirement summary: {requirement.summary}\n"
        f"Requirement description: {requirement.description}\n"
    )
    return system, user
