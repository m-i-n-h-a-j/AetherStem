from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import TypeVar

T = TypeVar("T")


class RuntimeExecutor:
    def run(self, awaitable: Awaitable[T]) -> T:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(awaitable)
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(awaitable)
        finally:
            loop.close()

