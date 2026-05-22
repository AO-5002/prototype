import os
from pathlib import Path

REPO_PATH = os.getenv("REPO_PATH")
SUPPORTED = {".py", ".ts", ".tsx", ".js", ".jsx"}


def scan_repo():
    root = Path(str(REPO_PATH))
    files = [
        f for f in root.rglob("*")
        if f.is_file()
        and f.suffix in {".ts", ".tsx"}
        and "node_modules" not in f.parts
        and ".git" not in f.parts
        and ".next" not in f.parts
    ]

    return files
