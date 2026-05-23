from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np
import soundfile as sf

from ai.adapters.separation import SeparationOptions
from ai.compute.backend import BackendSelection, select_backend
from ai.inference.executor import InferenceExecutor
from ai.models.manager import ModelManager
from ai.models.demucs.runtime_adapter import DemucsRuntimeAdapter
from ai.models.registry.cache import ModelCache
from ai.models.registry.discovery import ManifestDiscovery
from ai.models.registry.resolver import ModelResolver
from ai.optimization.runtime_profiles import RuntimeProfileSelector
from ai.orchestration.decision_engine import DecisionEngine, ProcessingPlan
from ai.orchestration.routing import model_for_stage
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.context import ExecutionContext
from ai.runtime.executor import RuntimeExecutor
from ai.runtime.progress import ProgressReporter
from ai.telemetry.reports import write_json_report
from ai.validation.quality_comparator import QualityComparator
from dsp.visualizer import generate_spectrogram, generate_waveform


ProgressCallback = Callable[[str, str], None]


class AudioGraph:
    def __init__(
        self,
        model_manager: ModelManager | None = None,
        decision_engine: DecisionEngine | None = None,
        output_root: Path | str = "exports",
    ) -> None:
        self.model_manager = model_manager or ModelManager()
        self.decision_engine = decision_engine or DecisionEngine()
        self.output_root = Path(output_root)
        self.executor = InferenceExecutor()
        self.runtime_executor = RuntimeExecutor()
        self.comparator = QualityComparator()

    def execute(
        self,
        audio: np.ndarray,
        sample_rate: int,
        analysis,
        quality,
        workflow: str,
        input_path: Path,
        plan: ProcessingPlan | None = None,
        force: list[str] | None = None,
        config: dict[str, Any] | None = None,
        progress: ProgressCallback | None = None,
    ) -> dict[str, Any]:
        config = config or {}
        plan = plan or self.decision_engine.plan(analysis, quality, force=force)
        if workflow == "separate" and force == ["separate"]:
            plan.stages = [stage for stage in plan.stages if stage in {"separate", "validate", "export"}]
            plan.decisions = [
                decision.model_copy(update={"enabled": decision.stage in plan.stages})
                if decision.stage in {"denoise", "declip", "enhance"}
                else decision
                for decision in plan.decisions
            ]
        selection = select_backend(config.get("backend", "auto"), config.get("device", "auto"))
        run_dir = self._run_dir(input_path, workflow)
        run_dir.mkdir(parents=True, exist_ok=True)
        current = np.array(audio, copy=True)
        stage_results: dict[str, Any] = {}

        for stage in plan.stages:
            if progress:
                progress(stage, "running")
            if stage in {"denoise", "declip", "enhance"}:
                current, stage_results[stage] = self._run_model_stage(stage, current, sample_rate, selection, config)
            elif stage == "separate":
                stage_results[stage] = self._run_separation(current, sample_rate, selection, run_dir, config)
            elif stage == "validate":
                stage_results[stage] = self.comparator.compare(analysis, current)
                (run_dir / "validation_report.json").write_text(json.dumps(stage_results[stage], indent=2, default=str))
                (run_dir / "comparison_report.json").write_text(json.dumps(stage_results[stage], indent=2, default=str))
            elif stage == "export":
                accepted = bool(stage_results.get("validate", {}).get("accepted", True))
                stage_results[stage] = self._export_audio(current, sample_rate, run_dir, workflow, accepted)
            if progress:
                progress(stage, "complete")

        manifest = {
            "input": str(input_path),
            "workflow": workflow,
            "backend": selection.backend,
            "device": selection.device,
            "backend_diagnostics": selection.diagnostics,
            "plan": plan.model_dump(),
            "config": config,
            "stages": stage_results,
        }
        manifest_path = run_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
        return {"run_dir": str(run_dir), "audio": current, "sample_rate": sample_rate, "manifest": str(manifest_path), "stages": stage_results}

    def _run_model_stage(
        self,
        stage: str,
        audio: np.ndarray,
        sample_rate: int,
        selection: BackendSelection,
        config: dict[str, Any],
    ) -> tuple[np.ndarray, dict[str, Any]]:
        model_name = model_for_stage(stage, configured=config.get("models", {}))
        if model_name is None:
            return audio, {"skipped": True, "reason": "No compatible model registered."}
        model = self.model_manager.get(model_name, selection)
        result = self.executor.run(
            model,
            audio,
            sample_rate,
            {**config, "backend": selection.backend, "device": selection.device},
        )
        return result.audio if result.audio is not None else audio, result.model_dump(exclude={"audio", "stems"})

    def _run_separation(
        self,
        audio: np.ndarray,
        sample_rate: int,
        selection: BackendSelection,
        run_dir: Path,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        model_name = model_for_stage("separate", configured=config.get("models", {}))
        if model_name is None:
            return {"skipped": True, "reason": "No separation model registered."}
        if model_name == "demucs-runtime" or (model_name == "demucs-placeholder" and selection.backend == "onnx"):
            return self._run_runtime_separation(audio, sample_rate, selection, run_dir, config)
        model = self.model_manager.get(model_name, selection)
        result = self.executor.run(
            model,
            audio,
            sample_rate,
            {**config, "backend": selection.backend, "device": selection.device, "stems": ["vocals", "drums", "bass", "other"]},
        )
        stems_dir = run_dir / "stems"
        stems_dir.mkdir(parents=True, exist_ok=True)
        paths = {}
        for name, stem in result.stems.items():
            path = stems_dir / f"{name}.wav"
            sf.write(path, _sf_audio(stem.audio), sample_rate)
            paths[name] = str(path)
        return {"model": result.model.name, "warnings": result.warnings, "stems": paths}

    def _run_runtime_separation(
        self,
        audio: np.ndarray,
        sample_rate: int,
        selection: BackendSelection,
        run_dir: Path,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        adapter = DemucsRuntimeAdapter()
        context = ExecutionContext(
            backend=config.get("backend", selection.backend),
            device=config.get("device", selection.device),
            provider=config.get("provider", "auto"),
            precision=config.get("precision", "fp32"),
            low_memory=bool(config.get("low_memory", False)),
            fallback_to_cpu=bool(config.get("fallback_to_cpu", True)),
            diagnostics={"model_path": config.get("model_path") or config.get("demucs_model_path")},
            progress=ProgressReporter(),
        )
        profile = RuntimeProfileSelector().select(config.get("runtime_profile", "auto"))
        context.telemetry.emit("runtime_profile_selected", profile=profile.name, backend=profile.backend, device=profile.device, precision=profile.precision)
        resolved_model = self._resolve_runtime_model(config, sample_rate)
        if resolved_model:
            context.telemetry.emit(
                "model_resolved",
                model_id=resolved_model.manifest.id,
                version=resolved_model.manifest.version,
                backend=resolved_model.backend,
                precision=resolved_model.precision,
            )
            if (
                resolved_model.asset_path
                and not config.get("model_path")
                and resolved_model.diagnostics.get("cache", {}).get("available")
            ):
                context.diagnostics["model_path"] = str(resolved_model.asset_path)
        options = SeparationOptions(
            stems=["vocals", "drums", "bass", "other"],
            chunk_size=int(config.get("chunk_size", 44100 * 10)),
            overlap=float(config.get("overlap", config.get("overlap_ratio", 0.25))),
            model_path=config.get("model_path") or config.get("demucs_model_path"),
        )
        buffer = AudioBuffer(samples=audio, sample_rate=sample_rate, layout=_audio_layout(audio))
        self.runtime_executor.run(adapter.load(context))
        result = self.runtime_executor.run(adapter.separate(buffer, context, options))
        stems_dir = run_dir / "stems"
        stems_dir.mkdir(parents=True, exist_ok=True)
        paths = {}
        for name, stem in result.stems.items():
            path = stems_dir / f"{name}.wav"
            sf.write(path, _sf_audio(stem.audio.samples), stem.audio.sample_rate)
            paths[name] = str(path)
        telemetry_report = None
        profile_report = None
        if config.get("telemetry_enabled"):
            telemetry_report = str(write_json_report(run_dir / "telemetry.json", result.diagnostics.get("telemetry", context.telemetry.model_dump())))
        if config.get("profiling_enabled"):
            profile_report = str(write_json_report(run_dir / "profile.json", context.profiler.report()))
        return {
            "model": result.metadata.name,
            "runtime": "v0.4",
            "warnings": result.warnings,
            "diagnostics": {**result.diagnostics, "telemetry": context.telemetry.summary(), "profile": context.profiler.report()},
            "telemetry_report": telemetry_report,
            "profile_report": profile_report,
            "stems": paths,
        }

    def _resolve_runtime_model(self, config: dict[str, Any], sample_rate: int):
        try:
            roots = [Path(item) for item in config.get("manifest_dirs", ["ai/models/registry/manifests"])]
            manifests, errors = ManifestDiscovery(roots).discover()
            if errors:
                return None
            return ModelResolver(manifests, ModelCache(config.get("model_cache_dir", "cache/models"))).resolve(
                task="separate",
                backend=config.get("backend", "auto"),
                device=config.get("device", "auto"),
                precision=config.get("precision", "fp32"),
                sample_rate=None if config.get("allow_sample_rate_mismatch", True) else sample_rate,
                channels=2,
                stems=["vocals", "drums", "bass", "other"],
                require_asset=False,
            )
        except Exception:
            return None

    def _export_audio(self, audio: np.ndarray, sample_rate: int, run_dir: Path, workflow: str, accepted: bool) -> dict[str, str]:
        target_dir = run_dir if accepted else run_dir / "rejected"
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{workflow}.wav"
        sf.write(path, _sf_audio(audio), sample_rate)
        previews = {}
        try:
            previews["waveform"] = str(generate_waveform(audio, sample_rate, run_dir / "waveform.png"))
            previews["spectrogram"] = str(generate_spectrogram(audio, sample_rate, run_dir / "spectrogram.png"))
        except Exception as exc:
            previews["error"] = str(exc)
        return {"audio": str(path), "accepted": accepted, "previews": previews}

    def _run_dir(self, input_path: Path, workflow: str) -> Path:
        return self.output_root / f"{input_path.stem}_{workflow}"


def _sf_audio(audio: np.ndarray) -> np.ndarray:
    if audio.ndim == 2 and audio.shape[0] <= 8:
        return audio.T
    return audio


def _audio_layout(audio: np.ndarray) -> str:
    if audio.ndim == 1:
        return "mono"
    return "channels_first" if audio.shape[0] <= 8 else "channels_last"
