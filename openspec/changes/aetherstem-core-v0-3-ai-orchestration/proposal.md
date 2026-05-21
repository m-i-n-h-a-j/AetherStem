## Why

AetherStem v0.2 established deterministic DSP analysis, but the project still stops at diagnostics. The next step is to let those diagnostics drive audio restoration and enhancement decisions automatically. v0.3 introduces an AI-assisted processing layer that keeps DSP analysis as the source of truth while adding model orchestration, backend abstraction, post-process validation, and reproducible exports.

The intent is not to build one monolithic "AI pipeline". The system should remain modular: analysis produces typed evidence, a deterministic decision engine builds a processing graph, model adapters execute only the required enhancement stages, validation compares pre/post quality, and export writes audio plus structured reports.

## What Changes

- Add an `ai/` package with model abstractions, registry, compute backends, inference scheduling, orchestration, and validation modules.
- Add typed model metadata and capability discovery for separation, denoising, declipping, bandwidth extension, super-resolution, and mastering-oriented models.
- Add backend-independent execution interfaces for PyTorch, ONNX Runtime, and future TensorRT/DirectML-compatible execution.
- Add rule-based orchestration that consumes existing DSP analysis results and builds deterministic processing graphs.
- Add AI processing commands: `restore`, `separate`, `denoise`, `enhance`, `preset`, `batch`, and `benchmark`.
- Add YAML presets for archival restoration, vocal cleanup, podcast cleanup, lossy recovery, and mastering prep.
- Add post-process validation, artifact detection, before/after comparison reports, structured exports, batch processing, and benchmarks.
- Add documentation for the AI pipeline, model integration lifecycle, orchestration methodology, and future realtime roadmap.

## Capabilities

### New Capabilities

- `ai-models`: model protocol, typed result objects, registry, metadata, lazy loading, model managers, and model-family adapters.
- `compute-backends`: backend/device abstraction for PyTorch, ONNX Runtime, and future accelerator backends with CPU fallback.
- `orchestration`: deterministic decision engine, routing, presets, processing graph execution, and progress reporting.
- `ai-validation`: post-process spectral, phase, artifact, and quality comparison validation.
- `batch-export`: resumable batch queues, structured export directories, JSON reports, stems, restored audio, and previews.
- `benchmarking`: repeatable runtime, memory, latency, SDR/SNR, and artifact-score reports.

### Modified Capabilities

- `cli`: expand from analysis commands into restoration, separation, denoising, enhancement, presets, batch, and benchmark workflows.
- `config`: extend YAML configuration for model selection, backend selection, chunking, overlap, validation thresholds, denoise strength, and enhancement intensity.
- `audio-analysis`: expose analysis summaries in a stable shape that orchestration can consume without depending on CLI formatting.

## Impact

This change introduces heavyweight optional AI dependencies and a larger runtime surface. Model execution must be lazy, backend-aware, memory-safe, and failure-safe. The current flat package layout may either be preserved with a top-level `ai/` package or migrated later into a single `aetherstem/` namespace; v0.3 should avoid a disruptive package migration unless required.

New dependencies include `torch`, `torchaudio`, `onnx`, `onnxruntime`, `huggingface_hub`, `pyyaml`, `einops`, `accelerate`, `tqdm`, and `safetensors`. Existing `pydantic>=2.0`, `rich`, `typer`, `numpy`, `scipy`, `soundfile`, and `librosa` remain central.

## Non-Goals

- No GUI.
- No realtime playback.
- No cloud deployment.
- No DAW plugin.
- No distributed cluster execution.
- No requirement to ship pretrained model weights in the repository.
- No destructive enhancement without validation and reportable rejection criteria.
