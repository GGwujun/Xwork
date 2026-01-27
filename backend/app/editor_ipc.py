"""
Editor IPC - Integration with Visual Studio Code.

This module provides:
1. Open file in VS Code at a specific line
2. Apply diffs to files
3. Show notification in VS Code (via extension, future)
"""

import subprocess
import os
from typing import Optional, List
from pydantic import BaseModel

class FileEdit(BaseModel):
    """Represents a file edit operation."""
    path: str
    start_line: int
    end_line: int
    old_content: str
    new_content: str

class EditorIPC:
    """
    Interface for communicating with VS Code.
    Uses the `code` CLI command.
    """

    def __init__(self):
        self.code_path = self._find_code_executable()

    def _find_code_executable(self) -> str:
        """Find the VS Code CLI path."""
        # On Windows, usually in PATH after installation
        if os.name == 'nt':
            return "code"
        # On macOS/Linux
        return "code"

    def is_available(self) -> bool:
        """Check if VS Code CLI is available."""
        try:
            result = subprocess.run(
                [self.code_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def open_file(self, file_path: str, line: Optional[int] = None, column: Optional[int] = None) -> bool:
        """Open a file in VS Code, optionally at a specific line."""
        try:
            args = [self.code_path, "--goto"]
            
            if line:
                location = f"{file_path}:{line}"
                if column:
                    location += f":{column}"
                args.append(location)
            else:
                args.append(file_path)
            
            subprocess.Popen(args, shell=False)
            return True
        except Exception as e:
            print(f"Failed to open file in VS Code: {e}")
            return False

    def open_folder(self, folder_path: str) -> bool:
        """Open a folder in VS Code."""
        try:
            subprocess.Popen([self.code_path, folder_path], shell=False)
            return True
        except Exception as e:
            print(f"Failed to open folder in VS Code: {e}")
            return False

    def open_diff(self, file1: str, file2: str) -> bool:
        """Open a diff view between two files."""
        try:
            subprocess.Popen([self.code_path, "--diff", file1, file2], shell=False)
            return True
        except Exception as e:
            print(f"Failed to open diff in VS Code: {e}")
            return False

    def apply_file_edits(self, edits: List[FileEdit]) -> dict:
        """
        Apply a list of file edits.
        Returns a summary of applied edits.
        """
        applied = []
        failed = []
        
        for edit in edits:
            try:
                # Read the file
                with open(edit.path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Apply the edit (replace lines start_line to end_line with new_content)
                new_lines = (
                    lines[:edit.start_line - 1] +
                    [edit.new_content + '\n'] +
                    lines[edit.end_line:]
                )
                
                # Write back
                with open(edit.path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                
                applied.append(edit.path)
            except Exception as e:
                failed.append({"path": edit.path, "error": str(e)})
        
        return {
            "applied": applied,
            "failed": failed,
            "success": len(failed) == 0,
        }

# Global instance
editor_ipc = EditorIPC()

# --- API Helpers ---

async def open_in_vscode(file_path: str, line: Optional[int] = None) -> dict:
    """Open a file in VS Code."""
    success = editor_ipc.open_file(file_path, line)
    return {"opened": success, "path": file_path}

async def apply_edits(edits: List[dict]) -> dict:
    """Apply file edits from AI-generated changes."""
    file_edits = [FileEdit(**e) for e in edits]
    return editor_ipc.apply_file_edits(file_edits)
