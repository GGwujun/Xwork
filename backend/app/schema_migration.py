from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict


def migrate_v0_1_to_v0_2(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Upgrade an OpenSpec dict from v0.1.0 to v0.2.0."""

    migrated: Dict[str, Any] = deepcopy(spec)
    migrated["spec_version"] = "0.2.0"

    migrated.setdefault("design", {})
    migrated["design"].setdefault("architecture_overview", "")
    migrated["design"].setdefault("api_endpoints", [])
    migrated["design"].setdefault("data_models", [])
    migrated["design"].setdefault("tech_stack", {})
    migrated["design"].setdefault("dependencies", [])

    migrated.setdefault("workflow", {"nodes": [], "edges": []})
    migrated.setdefault("collaboration", {"owner": "", "collaborators": [], "shared": True})

    now = datetime.now(timezone.utc).isoformat()
    metadata = migrated.get("metadata") or {}
    metadata.setdefault("created_at", now)
    metadata.setdefault("updated_at", now)
    metadata.setdefault("tfs_work_item_id", None)
    migrated["metadata"] = metadata

    tasks = migrated.get("tasks", [])
    for task in tasks:
        if "assigned_agent" not in task:
            task["assigned_agent"] = None
        if "dependencies" not in task:
            task["dependencies"] = []
        if "file_changes" not in task:
            task["file_changes"] = []

    return migrated
