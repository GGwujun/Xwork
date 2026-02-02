from __future__ import annotations

import difflib
from pathlib import Path


class DiffGenerator:
    def generate_diff(self, file_path: str | Path, updated_content: str) -> str:
        path = Path(file_path)
        original = path.read_text(encoding="utf-8").splitlines(keepends=True)
        updated = updated_content.splitlines(keepends=True)
        diff = difflib.unified_diff(
            original,
            updated,
            fromfile=str(path),
            tofile=f"{path}.updated",
        )
        return "".join(diff)
