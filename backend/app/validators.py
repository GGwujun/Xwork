from __future__ import annotations

from typing import Iterable

from .schemas import OpenSpec, Task, Workflow


class OpenSpecValidationError(ValueError):
    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        message = "OpenSpec validation failed: " + "; ".join(issues)
        super().__init__(message)


def validate_open_spec(spec: OpenSpec) -> None:
    issues: list[str] = []

    _validate_core(spec, issues)
    _validate_tasks(spec.tasks, issues)
    if spec.workflow:
        _validate_workflow(spec.workflow, issues)

    if issues:
        raise OpenSpecValidationError(issues)


def _validate_core(spec: OpenSpec, issues: list[str]) -> None:
    if not spec.project_name.strip():
        issues.append("project_name is required")
    if spec.spec_version != "0.2.0":
        issues.append("spec_version must be 0.2.0")
    if not spec.requirement.summary.strip():
        issues.append("requirement.summary is required")
    if not spec.requirement.description.strip():
        issues.append("requirement.description is required")


def _validate_tasks(tasks: Iterable[Task], issues: list[str]) -> None:
    ids = [task.id for task in tasks]
    if len(ids) != len(set(ids)):
        issues.append("task ids must be unique")
    known = set(ids)

    for task in tasks:
        for dep in task.dependencies:
            if dep not in known:
                issues.append(f"task dependency not found: {task.id} -> {dep}")

    if _has_cycle({task.id: task.dependencies for task in tasks}):
        issues.append("task dependency graph contains a cycle")


def _validate_workflow(workflow: Workflow, issues: list[str]) -> None:
    node_ids = [node.id for node in workflow.nodes]
    if len(node_ids) != len(set(node_ids)):
        issues.append("workflow node ids must be unique")

    known = set(node_ids)
    edges: dict[str, list[str]] = {node_id: [] for node_id in known}
    for edge in workflow.edges:
        if edge.source not in known or edge.target not in known:
            issues.append("workflow edge references unknown node")
            continue
        edges[edge.source].append(edge.target)

    if _has_cycle(edges):
        issues.append("workflow graph contains a cycle")


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    for node in graph:
        if visit(node):
            return True
    return False
