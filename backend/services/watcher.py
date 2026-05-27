import json
import asyncio
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from connection_manager import manager
from services.init_scan import SUPPORTED_EXTENSIONS, IGNORED_DIRS, scan_repo


def _normalize(path) -> str:
    return os.fsdecode(path)


def _is_relevant(path: str) -> bool:
    p = Path(path)
    if IGNORED_DIRS.intersection(p.parts):
        return False
    return p.suffix in SUPPORTED_EXTENSIONS


class RepoEventHandler(FileSystemEventHandler):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

    def _broadcast(self):
        files = scan_repo()
        payload = json.dumps({
            "type": "init",
            "nodes": [
                {
                    "id": str(f),
                    "position": {"x": i * 100, "y": i * 25},
                    "data": {"label": f.name},
                }
                for i, f in enumerate(files)
            ],
            "edges": []
        })
        asyncio.run_coroutine_threadsafe(
            manager.broadcast(payload),
            self.loop
        )

    def on_created(self, event: FileSystemEvent):
        if not event.is_directory and _is_relevant(_normalize(event.src_path)):
            self._broadcast()


def start_watcher(repo_path: str, loop: asyncio.AbstractEventLoop) -> BaseObserver:
    handler = RepoEventHandler(loop)
    observer = Observer()
    observer.schedule(handler, repo_path, recursive=True)
    observer.start()
    return observer
