# Backend Setup

This backend uses `pyproject.toml` for dependency management.

## Quick start (Windows)

From `E:\\winning\\code\\vue3\\openwork\\backend`:

```bat
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install -e .
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Notes

- All Python dependencies are declared in `backend/pyproject.toml`.
- Use the same virtual environment for running the backend.
