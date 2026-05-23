from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ProgressEvent:
    stage: str
    completed: int
    total: int
    message: str = ""


class ProgressReporter:
    def __init__(self, callback: Callable[[ProgressEvent], None] | None = None) -> None:
        self.callback = callback
        self.events: list[ProgressEvent] = []

    def report(self, stage: str, completed: int, total: int, message: str = "") -> None:
        event = ProgressEvent(stage=stage, completed=completed, total=total, message=message)
        self.events.append(event)
        if self.callback:
            self.callback(event)

