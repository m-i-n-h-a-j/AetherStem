from __future__ import annotations

from collections import deque
from typing import Any

from ai.telemetry.events import RuntimeEvent


class RuntimeTracer:
    def __init__(self, max_events: int = 2000) -> None:
        self.max_events = max_events
        self._events: deque[RuntimeEvent] = deque(maxlen=max_events)

    def emit(self, name: str, **payload: Any) -> None:
        self._events.append(RuntimeEvent(name=name, payload=payload))

    def events(self) -> list[RuntimeEvent]:
        return list(self._events)

    def summary(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for event in self._events:
            counts[event.name] = counts.get(event.name, 0) + 1
        return {"event_count": len(self._events), "counts": counts}

    def model_dump(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "events": [
                {"name": event.name, "timestamp": event.timestamp, "payload": event.payload}
                for event in self._events
            ],
        }

