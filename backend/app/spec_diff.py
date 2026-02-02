import json
from dataclasses import dataclass
from difflib import unified_diff
from typing import Any, Dict, Iterable, List, Tuple

from .schemas import OpenSpec


@dataclass(frozen=True)
class DiffReport:
    diff: str
    added: List[str]
    removed: List[str]
    modified: List[str]


def diff_specs(left: OpenSpec | Dict[str, Any], right: OpenSpec | Dict[str, Any]) -> DiffReport:
    left_payload = _normalize(left)
    right_payload = _normalize(right)

    left_lines = json.dumps(left_payload, indent=2, sort_keys=True, ensure_ascii=True).splitlines()
    right_lines = json.dumps(right_payload, indent=2, sort_keys=True, ensure_ascii=True).splitlines()

    diff_text = "\n".join(
        unified_diff(left_lines, right_lines, fromfile="left", tofile="right", lineterm="")
    )

    added, removed, modified = _diff_paths(left_payload, right_payload)
    return DiffReport(diff=diff_text, added=sorted(added), removed=sorted(removed), modified=sorted(modified))


def merge_specs(
    base: OpenSpec | Dict[str, Any],
    incoming: OpenSpec | Dict[str, Any],
    *,
    strategy: str = "prefer_incoming",
) -> Dict[str, Any]:
    if strategy not in {"prefer_incoming", "prefer_base"}:
        raise ValueError("strategy must be 'prefer_incoming' or 'prefer_base'")
    return _merge_dicts(_normalize(base), _normalize(incoming), prefer_incoming=strategy == "prefer_incoming")


def _normalize(spec: OpenSpec | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(spec, OpenSpec):
        return spec.model_dump(mode="json", exclude_none=True)
    return dict(spec)


def _diff_paths(
    left: Dict[str, Any], right: Dict[str, Any], prefix: str = ""
) -> Tuple[List[str], List[str], List[str]]:
    added: List[str] = []
    removed: List[str] = []
    modified: List[str] = []

    left_keys = set(left.keys())
    right_keys = set(right.keys())

    for key in sorted(left_keys - right_keys):
        removed.append(_join_path(prefix, key))
    for key in sorted(right_keys - left_keys):
        added.append(_join_path(prefix, key))

    for key in sorted(left_keys & right_keys):
        left_val = left[key]
        right_val = right[key]
        path = _join_path(prefix, key)
        if isinstance(left_val, dict) and isinstance(right_val, dict):
            child_added, child_removed, child_modified = _diff_paths(left_val, right_val, path)
            added.extend(child_added)
            removed.extend(child_removed)
            modified.extend(child_modified)
        elif left_val != right_val:
            modified.append(path)

    return added, removed, modified


def _merge_dicts(base: Dict[str, Any], incoming: Dict[str, Any], prefer_incoming: bool) -> Dict[str, Any]:
    merged: Dict[str, Any] = dict(base)
    for key, value in incoming.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_dicts(merged[key], value, prefer_incoming)
        elif key in merged and isinstance(merged[key], list) and isinstance(value, list):
            merged[key] = value if prefer_incoming else merged[key]
        else:
            merged[key] = value if prefer_incoming or key not in merged else merged[key]
    return merged


def _join_path(prefix: str, key: str) -> str:
    return f"{prefix}.{key}" if prefix else key
