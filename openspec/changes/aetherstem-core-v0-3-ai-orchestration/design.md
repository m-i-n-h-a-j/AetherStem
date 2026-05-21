## Context

AetherStem currently runs deterministic inspection and DSP analysis through `audio_io/`, `dsp/`, `pipeline/`, `models/`, and `cli/`. v0.3 adds AI-assisted processing while preserving the DSP-first architecture:

```text
Input Audio
  -> DSP Analysis
  -> Intelligent Decision Engine
  -> Model Orchestration
  -> Post-Process Validation
  -> Export
```

The implementation should favor interfaces, metadata, and graph execution over hard-coded end-to-end model pipelines. Model integrations are expected to mature incrementally: the first release should make the architecture executable with safe placeholder adapters where external models are unavailable, while real Demucs, MDX, denoising, and enhancement adapters can be enabled by installed dependencies and configured model identifiers.

## Goals / Non-Goals

**Goals:**

- Preserve deterministic DSP-first behavior and reproducible decisions.
- Add typed model abstractions with structured outputs and exception-safe inference.
- Support lazy model loading, version tracking, capability discovery, and backend compatibility checks.
- Provide compute backend abstractions for PyTorch, ONNX Runtime, and future TensorRT/DirectML implementations.
- Add chunked and overlap-aware execution for memory-safe processing.
- Build modular processing graphs with conditional stages and progress reporting.
- Validate enhanced audio against pre-process analysis and reject destructive results.
- Provide CLI workflows for restore, separate, denoise, enhance, presets, batch, and benchmark.

**Non-Goals:**

- Realtime constraints, streaming playback, and DAW integration.
- Remote inference, cloud storage, or distributed processing.
- Model training or fine-tuning.
- Bundling proprietary or large model weights in source control.

## Proposed Package Layout

```text
ai/
  orchestration/
    decision_engine.py
    routing.py
    validation.py
    presets.py
  inference/
    executor.py
    scheduler.py
    batching.py
    streaming.py
  models/
    base.py
    metadata.py
    registry.py
    manager.py
    loaders/
    demucs/
    mdx/
    denoise/
    enhancement/
    super_resolution/
  compute/
    backend.py
    torch_backend.py
    onnx_backend.py
    tensor_rt_backend.py
  validation/
    artifact_detector.py
    spectral_validator.py
    phase_validator.py
    quality_comparator.py
presets/
benchmarks/
exports/
```

The current project uses top-level packages rather than `aetherstem/`. v0.3 should initially add a top-level `ai/` package to avoid a broad namespace migration. A later packaging change can move all packages under `aetherstem/` if needed.

## Core Types

`ai/models/base.py` defines the stable contract:

```python
class AudioModel(Protocol):
    name: str
    version: str

    def load(self) -> None: ...

    def process(
        self,
        audio: np.ndarray,
        sample_rate: int,
        config: dict[str, Any] | None = None,
    ) -> ModelResult: ...
```

`ModelResult` should include processed audio or stems, sample rate, model metadata, backend/device, timing, warnings, and optional diagnostic metrics. The interface remains synchronous for v0.3 but should be async-ready by keeping execution isolated in scheduler/executor classes and avoiding CLI-bound side effects inside models.

`ai/models/metadata.py` should use Pydantic models for metadata:

- `ModelCapabilities`
- `ModelRequirements`
- `ModelMetadata`
- `ModelCompatibility`
- `ModelResult`
- `StemResult`

## Model Registry

The registry owns:

- Dynamic model registration.
- Installed model enumeration.
- Capability filtering.
- Lazy loading through factories.
- Version tracking.
- Backend compatibility checks.
- Device preference and fallback handling.
- Future plugin loading hooks.

The registry should not import heavyweight model packages at module import time. Adapters register lightweight metadata and a loader callable. Actual imports happen inside `load()` or model manager execution.

## Compute Backends

`ai/compute/backend.py` defines a unified interface for:

- Backend availability.
- Device discovery.
- Preferred device selection.
- Memory/VRAM summary when available.
- Input preparation and output normalization.
- Inference invocation.

Initial backends:

- `TorchBackend`: CPU/CUDA, with DirectML readiness through device abstraction rather than direct dependency.
- `OnnxBackend`: ONNX Runtime providers and CPU fallback.
- `TensorRTBackend`: placeholder capability detector and clear unsupported errors until implemented.

Backend selection should be deterministic given configuration and environment. Automatic selection may choose GPU only when available and compatible, otherwise CPU fallback is required.

## Model Families

### Demucs

Demucs integration supports vocal, instrumental, drums, bass, and other stems. Processing must be chunked with overlap and configurable stem output. The first implementation may wrap an installed Demucs package if present and fail gracefully with actionable diagnostics when absent.

### MDX / UVR-Compatible

MDX-style adapters should support ONNX execution, spectral masking utilities, configurable aggressiveness, and reusable separation helpers. The adapter should be compatible with local ONNX model files and future registry-managed downloads.

### Denoising

Denoising is represented through adapter abstractions for DeepFilterNet-style and RNNoise-style processing. The orchestration layer selects denoise strength based on analysis, while models handle broadband noise, hiss, hum, and environmental cleanup.

### Bandwidth Extension

Bandwidth extension and super-resolution are introduced as interfaces and placeholders with validation-aware activation. Future adapters may target AudioSR, HiFi-GAN variants, or other neural reconstruction models.

## Decision Engine

The initial engine is deterministic and rule-based. It consumes structured DSP analysis and produces a processing plan:

- Enable bandwidth extension when lossy/transcode confidence crosses configured thresholds.
- Enable denoising when noise floor exceeds configured thresholds.
- Enable declipping when clipping is detected.
- Avoid enhancement when analysis does not justify it.
- Record every decision with threshold, observed value, and chosen action.

The design should keep a path open for ML-driven policy selection later, but v0.3 decisions must be reproducible.

## Processing Graph

`AudioGraph` should execute reusable nodes:

- `Analyze`
- `Separate`
- `Denoise`
- `Declip`
- `Enhance`
- `Validate`
- `Export`

Graph execution requirements:

- Conditional execution.
- Branchable stages.
- Typed outputs.
- Progress callbacks.
- Structured logs.
- Failure-safe node boundaries.
- Reportable skipped stages.

## Validation

Post-process validation reruns or reuses analysis against processed audio and compares pre/post metrics. Validation should detect:

- Phase correlation regressions.
- New clipping.
- HF hallucination.
- Metallic ringing.
- Pre-echo.
- Transient smearing.
- Stereo instability.
- Dynamic range collapse.

Validation returns structured acceptance/rejection decisions. Rejected destructive enhancement should not overwrite accepted exports; the report should include rejected stage details.

## Export

Exports are written under `exports/` by default:

- Restored audio.
- Separated stems.
- JSON analysis reports.
- JSON comparison reports.
- Artifact analysis reports.
- Waveform and spectrogram previews.
- Run manifest with model versions, backend, config, thresholds, and input fingerprint.

## CLI

New commands:

- `aetherstem restore input.flac`
- `aetherstem separate input.flac`
- `aetherstem denoise input.flac`
- `aetherstem enhance input.flac`
- `aetherstem preset archival_restore input.flac`
- `aetherstem batch ./music/`
- `aetherstem benchmark input.flac`

CLI behavior should use Rich progress, structured logs, detailed diagnostics, non-zero exit codes on failure, and stable export paths.

## Risks / Trade-offs

- **Heavy dependencies** -> keep model imports lazy and document optional installation constraints.
- **Model availability variability** -> registry reports missing dependencies and unavailable weights without crashing unrelated commands.
- **GPU memory pressure** -> chunking, overlap, scheduler memory estimates, and CPU fallback.
- **Quality regressions** -> validation rejects destructive output and exports comparison reports.
- **Package layout drift** -> add top-level `ai/` now, defer full `aetherstem/` namespace migration.
- **External model APIs change** -> wrap integrations behind local adapters and metadata contracts.
