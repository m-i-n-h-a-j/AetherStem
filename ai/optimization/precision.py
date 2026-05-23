from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrecisionResolution:
    requested: str
    selected: str
    fallback: bool = False
    reason: str = ""


class PrecisionPolicy:
    def resolve(
        self,
        requested: str,
        model_precisions: list[str] | tuple[str, ...],
        backend_precisions: list[str] | tuple[str, ...],
        allow_fallback: bool = True,
    ) -> PrecisionResolution:
        if requested in model_precisions and requested in backend_precisions:
            return PrecisionResolution(requested=requested, selected=requested)
        if not allow_fallback:
            raise RuntimeError(f"Unsupported precision: {requested}")
        for candidate in ("fp32", "fp16", "int8"):
            if candidate in model_precisions and candidate in backend_precisions:
                return PrecisionResolution(
                    requested=requested,
                    selected=candidate,
                    fallback=True,
                    reason=f"{requested} unsupported; selected {candidate}",
                )
        raise RuntimeError("No compatible precision is available.")

