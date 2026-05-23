from __future__ import annotations

from dataclasses import dataclass


class CancelledError(RuntimeError):
    pass


@dataclass
class CancellationToken:
    cancelled: bool = False

    def cancel(self) -> None:
        self.cancelled = True

    def throw_if_cancelled(self) -> None:
        if self.cancelled:
            raise CancelledError("Runtime execution was cancelled.")

