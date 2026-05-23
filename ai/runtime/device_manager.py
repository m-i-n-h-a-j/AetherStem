from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceInfo:
    name: str
    available: bool
    memory_total_mb: float | None = None
    diagnostics: dict | None = None


class DeviceManager:
    def devices(self) -> list[DeviceInfo]:
        devices = [DeviceInfo(name="cpu", available=True, diagnostics={})]
        try:
            import torch

            if torch.cuda.is_available():
                props = torch.cuda.get_device_properties(0)
                devices.append(
                    DeviceInfo(
                        name="cuda",
                        available=True,
                        memory_total_mb=float(props.total_memory / (1024 * 1024)),
                        diagnostics={"device_name": props.name},
                    )
                )
        except Exception:
            pass
        devices.append(DeviceInfo(name="directml", available=False, diagnostics={"status": "reserved"}))
        return devices

    def resolve(self, requested: str = "auto", fallback_to_cpu: bool = True) -> DeviceInfo:
        available = {device.name: device for device in self.devices() if device.available}
        if requested != "auto" and requested in available:
            return available[requested]
        if requested != "auto" and requested not in available and not fallback_to_cpu:
            raise RuntimeError(f"Requested device is unavailable: {requested}")
        return available.get("cuda") or available["cpu"]

