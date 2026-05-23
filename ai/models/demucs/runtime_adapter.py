from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ai.adapters.base import RuntimeStem
from ai.adapters.separation import SeparationOptions, SeparationResult
from ai.backends.onnx_runtime import OnnxRuntimeBackend
from ai.models.demucs.onnx_session import DemucsOnnxSession
from ai.models.demucs.reconstruction import deterministic_stem_projection, ensure_stereo_channels_first
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.chunk_scheduler import ChunkScheduler, overlap_add
from ai.runtime.context import ExecutionContext


class DemucsRuntimeAdapter:
    metadata = ModelMetadata(
        name="demucs-runtime",
        version="0.4.0",
        family="demucs",
        description="Demucs-compatible runtime separation adapter with ONNX-first execution.",
        capabilities=ModelCapabilities(separate=True, stems=["vocals", "drums", "bass", "other", "instrumental"]),
        requirements=ModelRequirements(backends=["onnx", "torch"], devices=["cpu", "cuda"], dependencies=["onnxruntime"]),
    )

    def __init__(self, scheduler: ChunkScheduler | None = None) -> None:
        self.scheduler = scheduler or ChunkScheduler()
        self._onnx: DemucsOnnxSession | None = None

    async def load(self, context: ExecutionContext) -> None:
        model_path = context.diagnostics.get("model_path")
        if model_path:
            path = Path(str(model_path))
            if not path.exists():
                raise FileNotFoundError(f"Configured Demucs ONNX model not found: {path}")
            self._onnx = DemucsOnnxSession(path, OnnxRuntimeBackend())

    async def separate(
        self,
        audio: AudioBuffer,
        context: ExecutionContext,
        options: SeparationOptions,
    ) -> SeparationResult:
        started = time.perf_counter()
        context.cancellation.throw_if_cancelled()
        model_path = options.model_path or context.diagnostics.get("model_path")
        if model_path and self._onnx is None:
            self._onnx = DemucsOnnxSession(Path(str(model_path)), OnnxRuntimeBackend())
        source = AudioBuffer(
            samples=ensure_stereo_channels_first(audio.as_channels_first().samples),
            sample_rate=audio.sample_rate,
            layout="channels_first",
            metadata=dict(audio.metadata),
        )
        plan = self.scheduler.plan(
            source,
            chunk_size=options.chunk_size,
            overlap_ratio=options.overlap,
            low_memory=context.low_memory,
        )
        per_stem_chunks: dict[str, list] = {stem: [] for stem in options.stems}
        prepared_context = context
        for index, chunk in enumerate(plan.chunks, start=1):
            context.cancellation.throw_if_cancelled()
            if self._onnx is not None:
                stem_outputs, prepared_context = self._run_onnx_chunk(chunk.samples, context, options.stems)
            else:
                stem_outputs = deterministic_stem_projection(chunk.samples, options.stems)
                prepared_context.diagnostics["fallback"] = "No ONNX model configured; used deterministic runtime projection."
            for stem, values in stem_outputs.items():
                per_stem_chunks.setdefault(stem, []).append((chunk, values))
            context.progress.report("separate", index, len(plan.chunks), "processed chunk")
        stems = {}
        for stem, chunks in per_stem_chunks.items():
            reconstructed = overlap_add(chunks, plan.total_samples)
            stems[stem] = RuntimeStem(
                name=stem,
                audio=AudioBuffer(samples=reconstructed, sample_rate=audio.sample_rate, layout="channels_first"),
            )
        return SeparationResult(
            metadata=self.metadata,
            stems=stems,
            warnings=[] if self._onnx else ["No ONNX model configured; deterministic runtime projection was used."],
            diagnostics={
                **prepared_context.diagnostics,
                "chunk_size": plan.chunk_size,
                "overlap": plan.overlap,
                "hop_size": plan.hop_size,
                "batch_size": plan.batch_size,
                "chunks": len(plan.chunks),
                "estimated_memory_mb": plan.estimated_memory_mb,
            },
            duration_ms=(time.perf_counter() - started) * 1000,
        )

    def _run_onnx_chunk(
        self,
        chunk: np.ndarray,
        context: ExecutionContext,
        stems: list[str],
    ) -> tuple[dict[str, np.ndarray], ExecutionContext]:
        assert self._onnx is not None
        raw, prepared_context = self._onnx.run(chunk, context)
        if isinstance(raw, list):
            arrays = [np.asarray(item).squeeze(0) for item in raw]
            return {stem: arrays[index] for index, stem in enumerate(stems) if index < len(arrays)}, prepared_context
        output = np.asarray(raw)
        if output.ndim == 4:
            output = output[0]
        if output.ndim == 3:
            return {stem: output[index] for index, stem in enumerate(stems) if index < output.shape[0]}, prepared_context
        if output.ndim == 2:
            return {stems[0]: output}, prepared_context
        raise RuntimeError(f"Unsupported Demucs ONNX output shape: {output.shape}")

