from __future__ import annotations

from pathlib import Path
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def _project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".opencode").exists():
            return parent
    return current.parents[3]


def default_skill_dirs() -> list[Path]:
    root = _project_root()
    return [root / ".opencode" / "skill", root / ".opencode" / "skills"]


def scan_skill_files(base_dirs: list[Path] | None = None) -> list[Path]:
    dirs = base_dirs or default_skill_dirs()
    results: list[Path] = []
    for base in dirs:
        if not base.exists():
            continue
        results.extend(base.rglob("SKILL.md"))
    if results:
        logger.info(
            "Skill files scanned",
            extra={"skill_count": len(results)},
        )
    return results


class SkillWatcher:
    def __init__(self, base_dirs: list[Path] | None, on_change: Callable[[str], None]):
        self._dirs = base_dirs or default_skill_dirs()
        self._on_change = on_change
        self._observer = None

    def start(self) -> None:
        from watchdog.events import FileSystemEventHandler  # type: ignore
        from watchdog.observers import Observer  # type: ignore

        class Handler(FileSystemEventHandler):
            def __init__(self, callback: Callable[[str], None]):
                self._callback = callback

            def on_modified(self, event):
                src_path = str(event.src_path)
                if not event.is_directory and src_path.endswith("SKILL.md"):
                    self._callback(src_path)

            def on_created(self, event):
                src_path = str(event.src_path)
                if not event.is_directory and src_path.endswith("SKILL.md"):
                    self._callback(src_path)

            def on_deleted(self, event):
                src_path = str(event.src_path)
                if not event.is_directory and src_path.endswith("SKILL.md"):
                    self._callback(src_path)

        observer = Observer()
        for directory in self._dirs:
            if directory.exists():
                observer.schedule(Handler(self._on_change), str(directory), recursive=True)
        observer.start()
        self._observer = observer

    def stop(self) -> None:
        if not self._observer:
            return
        self._observer.stop()
        self._observer.join()
        self._observer = None
