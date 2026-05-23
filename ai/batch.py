from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".flac", ".mp3", ".m4a", ".opus", ".ogg", ".aiff", ".aif"}


def scan_audio_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS)


class BatchState:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = {"completed": [], "failed": {}}
        if path.exists():
            self.data.update(json.loads(path.read_text()))

    def completed(self, item: Path) -> bool:
        return str(item) in self.data["completed"]

    def mark_completed(self, item: Path) -> None:
        if str(item) not in self.data["completed"]:
            self.data["completed"].append(str(item))
        self.save()

    def mark_failed(self, item: Path, error: str) -> None:
        self.data["failed"][str(item)] = error
        self.save()

    def pending(self, items: Iterable[Path], force: bool = False) -> list[Path]:
        return [item for item in items if force or not self.completed(item)]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2))

