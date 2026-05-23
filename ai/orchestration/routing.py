from __future__ import annotations

from ai.models.registry import ModelRegistry, default_registry


DEFAULT_MODELS = {
    "separate": "demucs-runtime",
    "denoise": "denoise-placeholder",
    "declip": "denoise-placeholder",
    "enhance": "enhancement-placeholder",
}


def model_for_stage(stage: str, registry: ModelRegistry | None = None, configured: dict | None = None) -> str | None:
    configured = configured or {}
    if stage in configured:
        return configured[stage]
    registry = registry or default_registry
    fallback = DEFAULT_MODELS.get(stage)
    return fallback if fallback in registry.names() else None
