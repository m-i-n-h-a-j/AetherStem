# AetherStem

AetherStem is a professional AI-assisted music source separation platform built for Windows. It provides deterministic DSP analysis, AI orchestration, a production-oriented inference runtime, and CLI guidance for both humans and external AI coding agents.

## Features

- **Windows-Native**: Optimized for Windows environments.
- **High-Fidelity Preprocessing**: Converts audio to 96kHz, 32-bit float WAV using FFmpeg.
- **Rich Metadata Inspection**: Detailed audio properties display via FFprobe and Rich tables.
- **Modular Architecture**: Clean separation of CLI, I/O, DSP, and AI components.
- **AI Orchestration**: DSP-driven restore, separate, denoise, enhance, preset, batch, and benchmark workflows.
- **v0.4 Runtime Core**: Canonical audio buffers, tensor contracts, execution contexts, cancellation, progress, chunk scheduling, and streaming-compatible chunk flow.
- **v0.5 Runtime Platform**: Manifest-based model discovery, cache/checksum lifecycle, runtime profiles, precision policy, telemetry, profiling, and expanded diagnostics.
- **Runtime Backends**: ONNX Runtime backend with CPU/CUDA provider selection and optional PyTorch runtime fallback hooks.
- **Demucs-Compatible Separation**: ONNX-first runtime adapter with chunk batching, overlap-add reconstruction, stereo-safe output, and automatic padding.
- **CLI Help and AI Guidance**: Contextual help, workflow guidance, troubleshooting, config introspection, and AI-readable command metadata.
- **v0.6 Reconstruction Engine**: Offline-quality forensic analysis, adaptive reconstruction graphs, harmonic regeneration, spectral repair, bandwidth extension, transient/stereo recovery, mastering, evaluation, and float-safe high-resolution rendering.
- **v0.7 Adaptive Intelligence Foundation**: Artifact intelligence, confidence gates, region classification, temporal/perceptual stability scoring, hardware-aware quality scaling, adaptive memory/scheduling plans, runtime graph fingerprints, and reproducible degradation benchmark primitives.
- **Structured Logging**: Diagnostic tracking for all major processing stages.

## Requirements

- Python 3.11+
- FFmpeg (including FFprobe) available in system PATH.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AetherStem
   ```

2. **Create a virtual environment**:
   ```bash
   py -3.11 -m venv .venv
   ```

3. **Activate the environment**:
   ```bash
   .\.venv\Scripts\activate
   ```

4. **Install the package**:
   ```bash
   pip install -e .
   ```

Optional runtime installs:

```bash
pip install -e ".[runtime-cpu]"
pip install -e ".[runtime-cuda]"
pip install -e ".[runtime-dev]"
```

The base install remains focused on analysis and orchestration. Install a runtime extra when you want ONNX/PyTorch model execution.

## Usage

AetherStem provides a command-line interface with several commands:

### Check Version
```bash
aetherstem version
```

### Inspect Audio File
```bash
aetherstem inspect <path-to-audio-file>
```

### Process Audio File (Conversion)
```bash
aetherstem process <path-to-audio-file>
```
Enforces conversion of the input file into a 96kHz, 32-bit float WAV file.

### Analyze Audio File
```bash
aetherstem analyze <path-to-audio-file>
```
Runs the full pipeline: inspects metadata, preprocesses, calculates loudness (EBU R128 metrics, True Peak, LRA), performs spectral analysis, stereo/phase analysis, counts clipping, estimates noise floor/dynamic range, generates visualizations (spectrogram, waveform, vectorscope, phase correlation graph), and saves a JSON report under `reports/`.

### Quick Lossy Detector
```bash
aetherstem detect-lossy <path-to-audio-file>
```
Checks if the file was likely upsampled or transcoded from a lossy source (e.g. 128kbps, 192kbps, 320kbps MP3/AAC) based on high-frequency cutoff heuristics.

### Generate Visualizations
```bash
aetherstem spectrogram <path-to-audio-file>
aetherstem waveform <path-to-audio-file>
aetherstem phase <path-to-audio-file>
```
Specifically generates the requested plots (Spectrogram, Waveform, Vectorscope/Phase Correlation Graph) and outputs them to the `output/` directory.

### AI Runtime Workflows
```bash
aetherstem restore <path-to-audio-file>
aetherstem separate <path-to-audio-file>
aetherstem denoise <path-to-audio-file>
aetherstem enhance <path-to-audio-file>
aetherstem preset archival_restore <path-to-audio-file>
aetherstem batch <folder>
aetherstem benchmark <path-to-audio-file>
```

Runtime flags are available on AI commands:

```bash
aetherstem separate song.flac --backend onnx --device cpu --chunk-size 441000 --overlap 0.25 --low-memory --benchmark-runtime
```

The Demucs-compatible runtime adapter prefers an ONNX model path when configured. Set `ai.model_path` in `configs/default.yaml` or pass it through workflow config/presets. Without a configured model file, the runtime uses a deterministic chunked projection fallback so the graph, scheduler, reconstruction, export, and diagnostics remain executable without bundled weights.

### Runtime Diagnostics
```bash
aetherstem runtime-diagnostics
```

Prints available runtime backends, backend capabilities, ONNX providers, Torch CUDA status, device summaries, selected runtime profile, and model registry status.

### Contextual Help and AI Guidance
```bash
aetherstem help
aetherstem help separate
aetherstem help runtime
aetherstem guide separate
aetherstem troubleshoot
aetherstem config-info ai
aetherstem model-registry
aetherstem ai-metadata
```

`ai-metadata` emits deterministic JSON for external AI agents and tool runners. It includes commands, examples, workflows, diagnostics guidance, and project conventions without terminal markup.

### Ultra-Quality Reconstruction
```bash
aetherstem forensic song.mp3
aetherstem reconstruct song.mp3 --profile extreme --target-rate 192000 --multi-pass --bandwidth-extension
aetherstem remaster mix.flac --mastering-profile studio
aetherstem archival tape.wav --target-rate 192000
aetherstem upscale song.flac --target-rate 192000
```

AetherStem does not claim true lossless recovery from lossy sources. Reconstruction workflows produce plausibly reconstructed high-resolution masters with confidence, uncertainty, stage diagnostics, and evaluation reports.

### Model Registry and Runtime Profiles

v0.5 discovers local model manifests from `ai/models/registry/manifests/` by default and reports cache state without loading model weights. Configure runtime model assets in YAML manifests or through `ai.model_path`.

Default runtime config lives in `configs/default.yaml`:

- `ai.manifest_dirs`
- `ai.model_cache_dir`
- `ai.runtime_profile`
- `ai.telemetry_enabled`
- `ai.profiling_enabled`
- `ai.precision`
- `ai.model_path`

## Running Tests

To run the unit and integration tests:
```bash
pytest
```

## Validation Framework

AetherStem also includes a v1.0 validation framework for higher-confidence regression checks across static structure, unit tests, DSP correctness, golden-reference comparison, and report generation.

Install the validation extras when you want the full static toolchain available:

```bash
pip install -e ".[validation]"
```

Run the quick validation pipeline:

```bash
python -m validation.run_full_validation --quick
```

To make ruff, mypy, and pyright findings blocking during local cleanup, add strict static validation:

```bash
python -m validation.run_full_validation --quick --strict-static
```

The runner writes:

- `reports/validation/validation_report.json`
- `reports/validation/validation_report.html`

Current required checks cover config validation, import graph validation, pytest, deterministic synthetic DSP roundtrips, and synthetic golden-reference comparisons. Ruff, mypy, and pyright run as advisory checks in quick mode until the legacy static-analysis baseline is cleaned up. Enterprise tiers such as hardware scalability, long-duration stability, fuzzing, perceptual regression, backend equivalence, and streaming validation are scaffolded as explicit validation tiers and tracked in `openspec/changes/aetherstem-validation-framework-v1-0/`.

## Project Structure

- `cli/`: Typer CLI and command runner logic.
- `audio_io/`: Audio file loading, safe conversion, and metadata inspection.
- `dsp/`: Core digital signal processing (loudness, spectral analysis, stereo, phase, clipping, noise floor, visualizer).
- `pipeline/`: Orchestrates the step-based analysis workflow.
- `models/`: Strongly typed Pydantic models (AudioMetadata, AudioAnalysis, etc.) and future AI model abstractions.
- `ai/runtime/`: v0.4 runtime contracts for audio buffers, tensor movement, devices, memory, chunks, streaming, progress, and cancellation.
- `ai/backends/`: Runtime backend registry and ONNX/PyTorch backend adapters.
- `ai/adapters/`: Strict inference-only adapter interfaces.
- `ai/models/demucs/`: Demucs-compatible runtime separation adapter and reconstruction utilities.
- `ai/models/registry/`: v0.5 model manifests, discovery, resolver, compatibility, cache, and lifecycle management.
- `ai/optimization/`: Precision policy, quantization metadata, calibration hooks, and runtime profile selection.
- `ai/telemetry/`: Runtime events, tracing, profiling, and JSON report helpers.
- `cli/help/`: Contextual help, AI metadata, workflow guidance, troubleshooting, and rendering.
- `ai/reconstruction/`: v0.6 forensic analysis, adaptive reconstruction graph, restoration stages, evaluation, rendering, and diagnostics.
- `ai/reconstruction/intelligence/`: v0.7 artifact detections, heatmaps, confidence gating, and region classification.
- `ai/reconstruction/temporal/`: v0.7 temporal stability scoring.
- `ai/reconstruction/perceptual/`: v0.7 psychoacoustic and perceptual scoring.
- `ai/runtime/quality/`, `ai/runtime/profiling/`, `ai/runtime/scheduling/`, `ai/runtime/memory/`, `ai/runtime/graph/`, `ai/runtime/backends/`: v0.7 hardware-aware quality scaling, planning, graph descriptors, and backend selection contracts.
- `ai/benchmarking/`: Controlled degradation benchmark corpus primitives.
- `configs/`: YAML configurations for processing.
- `cache/`: Caching layer for analysis results.
- `reports/`: Target output folder for JSON reports.
- `output/`: Folder for generated PNG plots.
- `logs/`: Application log files.
- `tests/`: Pytest test suite.
- `validation/`: Validation framework runner, metrics, synthetic fixture generation, golden-reference comparison, and report contracts.
- `golden_references/`, `fuzzing/`, `performance/`, `fixtures/`, `synthetic_audio/`, `degradation_profiles/`: Validation lab directories for reference corpora, generated fixtures, fuzz cases, performance data, and controlled degradation profiles.
- `docs/`: Technical and design documentation.

## License

[MIT License](LICENSE)
