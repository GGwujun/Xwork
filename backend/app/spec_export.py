import json
from typing import Any, Dict

from .schemas import OpenSpec


def export_spec(spec: OpenSpec | Dict[str, Any], format: str) -> str:
    normalized = _normalize(spec)
    if format == "markdown":
        return _to_markdown(normalized)
    if format == "html":
        return _to_html(normalized)
    if format == "pdf":
        raise ValueError("pdf export is not implemented")
    raise ValueError("format must be 'markdown', 'html', or 'pdf'")


def _normalize(spec: OpenSpec | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(spec, OpenSpec):
        return spec.model_dump(mode="json", exclude_none=True)
    return dict(spec)


def _to_markdown(spec: Dict[str, Any]) -> str:
    requirement = spec.get("requirement", {})
    design = spec.get("design", {})
    tasks = spec.get("tasks", [])

    lines = [
        f"# OpenSpec: {spec.get('project_name', 'Untitled')}",
        "",
        "## Requirement",
        f"- Summary: {requirement.get('summary', '')}",
        f"- Description: {requirement.get('description', '')}",
    ]

    criteria = requirement.get("acceptance_criteria") or []
    if criteria:
        lines.append("- Acceptance Criteria:")
        for item in criteria:
            lines.append(f"  - {item}")

    if design:
        lines.extend([
            "",
            "## Design",
            f"- Architecture Overview: {design.get('architecture_overview', '')}",
        ])
        if design.get("api_endpoints"):
            lines.append("- API Endpoints:")
            for api in design.get("api_endpoints", []):
                lines.append(
                    f"  - {api.get('method', '').upper()} {api.get('path', '')}: {api.get('description', '')}"
                )
        if design.get("data_models"):
            lines.append("- Data Models:")
            for model in design.get("data_models", []):
                lines.append(f"  - {model.get('name', '')}")

    lines.extend(["", "## Tasks"])
    if tasks:
        for task in tasks:
            lines.append(f"- {task.get('id', '')}: {task.get('title', '')} ({task.get('status', '')})")
            description = task.get("description", "")
            if description:
                lines.append(f"  - {description}")
    else:
        lines.append("- No tasks defined")

    lines.extend(["", "## Raw OpenSpec JSON", "```json", json.dumps(spec, indent=2, ensure_ascii=True), "```"])
    return "\n".join(lines)


def _to_html(spec: Dict[str, Any]) -> str:
    markdown = _to_markdown(spec)
    escaped = (
        markdown.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return "\n".join(
        [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "  <meta charset=\"utf-8\" />",
            "  <title>OpenSpec Export</title>",
            "  <style>",
            "    body { font-family: Arial, sans-serif; margin: 32px; line-height: 1.6; }",
            "    pre { background: #f6f8fa; padding: 12px; overflow-x: auto; }",
            "    code { font-family: 'Courier New', monospace; }",
            "  </style>",
            "</head>",
            "<body>",
            "<pre>",
            escaped,
            "</pre>",
            "</body>",
            "</html>",
        ]
    )
