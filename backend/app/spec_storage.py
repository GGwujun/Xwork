import json
import logging
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .schemas import OpenSpec, Metadata

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _default_base_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", "data", "specs"))


@dataclass(frozen=True)
class SpecVersion:
    version_id: str
    file_path: str
    created_at: str


class SpecStorage:
    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir or _default_base_dir()

    def save_spec(self, spec: OpenSpec, project_name: Optional[str] = None) -> SpecVersion:
        normalized = self._normalize_spec(spec)
        name = project_name or normalized.project_name
        project_dir = self._project_dir(name)
        _ensure_dir(project_dir)

        version_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
        file_path = os.path.join(project_dir, f"{version_id}.json")

        payload = normalized.model_dump(mode="json", exclude_none=True)
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=True)

        created_at = normalized.metadata.created_at if normalized.metadata else _utc_now()
        logger.info(
            "Spec saved",
            extra={"project": name, "version_id": version_id, "file_path": file_path},
        )
        return SpecVersion(version_id=version_id, file_path=file_path, created_at=created_at)

    def load_spec(self, project_name: str, version_id: Optional[str] = None) -> OpenSpec:
        versions = self.list_versions(project_name)
        if not versions:
            logger.warning(
                "Spec not found",
                extra={"project": project_name, "version_id": version_id},
            )
            raise FileNotFoundError(f"No specs stored for project '{project_name}'")

        if version_id is None:
            selected = versions[-1]
        else:
            matches = [version for version in versions if version.version_id == version_id]
            if not matches:
                logger.warning(
                    "Spec not found",
                    extra={"project": project_name, "version_id": version_id},
                )
                raise FileNotFoundError(
                    f"Spec version '{version_id}' not found for project '{project_name}'"
                )
            selected = matches[0]

        with open(selected.file_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        logger.info(
            "Spec loaded",
            extra={"project": project_name, "version_id": selected.version_id, "file_path": selected.file_path},
        )
        return OpenSpec.model_validate(payload)

    def list_projects(self) -> List[str]:
        if not os.path.isdir(self.base_dir):
            return []
        return sorted(
            name
            for name in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, name))
        )

    def list_versions(self, project_name: str) -> List[SpecVersion]:
        project_dir = self._project_dir(project_name)
        if not os.path.isdir(project_dir):
            return []
        versions: List[SpecVersion] = []
        for filename in sorted(os.listdir(project_dir)):
            if not filename.endswith(".json"):
                continue
            version_id = filename[:-5]
            file_path = os.path.join(project_dir, filename)
            created_at = _extract_created_at(file_path)
            versions.append(
                SpecVersion(version_id=version_id, file_path=file_path, created_at=created_at)
            )
        versions.sort(key=lambda entry: entry.created_at)
        return versions

    def _normalize_spec(self, spec: OpenSpec) -> OpenSpec:
        created_at = spec.metadata.created_at if spec.metadata else _utc_now()
        updated_at = _utc_now()
        metadata = Metadata(
            created_at=created_at,
            updated_at=updated_at,
            tfs_work_item_id=spec.metadata.tfs_work_item_id if spec.metadata else None,
        )
        return spec.model_copy(update={"metadata": metadata})

    def _project_dir(self, project_name: str) -> str:
        safe_name = project_name.replace(os.sep, "_")
        return os.path.join(self.base_dir, safe_name)


def _extract_created_at(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        metadata = payload.get("metadata") or {}
        created_at = metadata.get("created_at")
        if created_at:
            return created_at
    except (OSError, json.JSONDecodeError, AttributeError, TypeError):
        pass
    stat = os.stat(file_path)
    return datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()


spec_storage = SpecStorage()
