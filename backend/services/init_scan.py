import os
from pathlib import Path

REPO_PATH = os.getenv("REPO_PATH")
SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
IGNORED_DIRS = {"node_modules", ".git", ".next", "__pycache__"}


def scan_repo() -> list[Path]:
    if not REPO_PATH:
        raise ValueError("REPO_PATH environment variable is not set")

    root = Path(REPO_PATH)
    return [
        f for f in root.rglob("*")
        if f.is_file()
        and f.suffix in SUPPORTED_EXTENSIONS
        and not IGNORED_DIRS.intersection(f.parts)
    ]
