from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import IntEnum
from os import cpu_count
from typing import Any

from ai.runtime.device_manager import DeviceInfo, DeviceManager


class HardwareTier(IntEnum):
    LEGACY = 0
    ENTRY_MODERN = 1
    MIDRANGE = 2
    ENTHUSIAST = 3


@dataclass(frozen=True)
class HardwareCapability:
    tier: HardwareTier
    cpu_threads: int
    preferred_device: str
    available_memory_mb: float | None
    recommended_concurrency: int
    diagnostics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tier"] = int(self.tier)
        payload["tier_name"] = self.tier.name.lower()
        return payload


class HardwareProfiler:
    def __init__(self, device_manager: DeviceManager | None = None) -> None:
        self.device_manager = device_manager or DeviceManager()

    def profile(self) -> HardwareCapability:
        devices = self.device_manager.devices()
        cpu_threads = cpu_count() or 1
        preferred = _preferred_device(devices)
        tier = _tier(cpu_threads, preferred)
        memory = preferred.memory_total_mb
        concurrency = max(1, min(cpu_threads // 2, int(tier) + 1))
        return HardwareCapability(tier, cpu_threads, preferred.name, memory, concurrency, {"devices": [device.__dict__ for device in devices]})


def _preferred_device(devices: list[DeviceInfo]) -> DeviceInfo:
    available = [device for device in devices if device.available]
    return next((device for device in available if device.name == "cuda"), available[0])


def _tier(cpu_threads: int, device: DeviceInfo) -> HardwareTier:
    if device.name == "cuda" and (device.memory_total_mb or 0) >= 12000:
        return HardwareTier.ENTHUSIAST
    if device.name == "cuda" and (device.memory_total_mb or 0) >= 4096:
        return HardwareTier.MIDRANGE
    if cpu_threads >= 8:
        return HardwareTier.ENTRY_MODERN
    return HardwareTier.LEGACY
