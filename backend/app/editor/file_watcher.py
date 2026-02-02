from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class FileChange:
    path: str
    event_type: str


class FileWatcher:
    def __init__(self, root: str | Path, on_change: Callable[[FileChange], None]):
        self.root = Path(root)
        self.on_change = on_change
        self._observer = None

    def start(self) -> None:
        from watchdog.events import FileSystemEventHandler  # type: ignore
        from watchdog.observers import Observer  # type: ignore

        class Handler(FileSystemEventHandler):
            def __init__(self, callback: Callable[[FileChange], None]):
                self._callback = callback

            def on_modified(self, event):
                if event.is_directory:
                    return
                self._callback(FileChange(path=event.src_path, event_type="modified"))

            def on_created(self, event):
                if event.is_directory:
                    return
                self._callback(FileChange(path=event.src_path, event_type="created"))

            def on_deleted(self, event):
                if event.is_directory:
                    return
                self._callback(FileChange(path=event.src_path, event_type="deleted"))

        observer = Observer()
        observer.schedule(Handler(self.on_change), str(self.root), recursive=True)
        observer.start()
        self._observer = observer

    def stop(self) -> None:
        if not self._observer:
            return
        self._observer.stop()
        self._observer.join()
        self._observer = None
