## 1. Dependencies & Packaging

- [ ] 1.1 Add AI dependencies to `pyproject.toml`: `torch`, `torchaudio`, `onnx`, `onnxruntime`, `huggingface_hub`, `einops`, `accelerate`, and `safetensors`
- [ ] 1.2 Confirm existing `pyyaml` and `tqdm` dependencies satisfy v0.3 requirements
- [ ] 1.3 Add the new `ai` package and update setuptools package discovery or package list
- [ ] 1.4 Add `presets/`, `benchmarks/`, and `exports/` directories with `.gitkeep` where appropriate

## 2. Model Abstraction & Metadata

- [ ] 2.1 Implement `ai/models/base.py` with `AudioModel` protocol and structured `ModelResult`
- [ ] 2.2 Implement `ai/models/metadata.py` with Pydantic metadata, capabilities, requirements, compatibility, and stem result models
- [ ] 2.3 Add exception-safe model execution helpers and typed warnings/errors
- [ ] 2.4 Ensure model interfaces are device-aware and async-ready without requiring async CLI commands in v0.3

## 3. Model Registry & Manager

- [ ] 3.1 Implement `ai/models/registry.py` with dynamic registration and capability discovery
- [ ] 3.2 Implement lazy loader registration without importing heavyweight model packages at startup
- [ ] 3.3 Implement version tracking and model availability validation
- [ ] 3.4 Implement backend compatibility checks and device preference resolution
- [ ] 3.5 Implement `ai/models/manager.py` for registry-backed model lifecycle management

## 4. Compute Backend Abstraction

- [ ] 4.1 Implement `ai/compute/backend.py` with unified backend/device interfaces
- [ ] 4.2 Implement `ai/compute/torch_backend.py` with CPU/CUDA detection and CPU fallback
- [ ] 4.3 Implement `ai/compute/onnx_backend.py` with ONNX Runtime provider detection
- [ ] 4.4 Add `ai/compute/tensor_rt_backend.py` as a future-ready placeholder with explicit unsupported diagnostics
- [ ] 4.5 Add backend selection configuration for preferred backend, device, and fallback policy

## 5. Inference Execution

- [ ] 5.1 Implement `ai/inference/executor.py` for unified model invocation and timing
- [ ] 5.2 Implement `ai/inference/scheduler.py` for device-aware scheduling and memory hints
- [ ] 5.3 Implement `ai/inference/batching.py` for chunked audio processing and overlap handling
- [ ] 5.4 Add `ai/inference/streaming.py` interfaces for future realtime support without enabling realtime playback

## 6. Model Family Adapters

- [ ] 6.1 Implement Demucs adapter package under `ai/models/demucs/`
- [ ] 6.2 Support configurable Demucs stem outputs: vocals, drums, bass, other, and instrumental
- [ ] 6.3 Implement MDX/UVR-compatible ONNX adapter under `ai/models/mdx/`
- [ ] 6.4 Implement reusable spectral masking utilities for MDX-style separation
- [ ] 6.5 Implement denoise abstractions for DeepFilterNet-style and RNNoise-style adapters
- [ ] 6.6 Implement enhancement and super-resolution placeholder adapters with validation-aware activation

## 7. Orchestration & Processing Graph

- [ ] 7.1 Implement `ai/orchestration/decision_engine.py` with deterministic rule-based decisions
- [ ] 7.2 Implement threshold-driven rules for lossy recovery, denoise, declip, and enhancement activation
- [ ] 7.3 Implement `ai/orchestration/routing.py` for mapping decisions to model capabilities
- [ ] 7.4 Implement modular graph nodes for analyze, separate, denoise, declip, enhance, validate, and export
- [ ] 7.5 Add branchable graph execution, conditional stage skipping, typed outputs, and progress reporting

## 8. Presets & Configuration

- [ ] 8.1 Extend YAML configuration for model selection, backend selection, chunk sizes, overlap, denoise strength, enhancement intensity, and validation thresholds
- [ ] 8.2 Implement `ai/orchestration/presets.py` for YAML preset loading and validation
- [ ] 8.3 Add presets: `archival_restore`, `vocal_cleanup`, `podcast_cleanup`, `lossy_recovery`, and `mastering_prep`
- [ ] 8.4 Ensure presets resolve to deterministic graph plans and record config in export manifests

## 9. Validation & Quality Comparison

- [ ] 9.1 Implement `ai/validation/artifact_detector.py`
- [ ] 9.2 Implement spectral, phase, and quality validators
- [ ] 9.3 Detect metallic ringing, pre-echo, transient smearing, hallucinated harmonics, phase corruption, and stereo instability
- [ ] 9.4 Implement `quality_comparator.py` with loudness delta, spectral restoration, noise reduction estimate, clipping reduction, stereo integrity, and dynamic range preservation
- [ ] 9.5 Reject destructive enhancement and write structured validation decisions

## 10. Export System

- [ ] 10.1 Implement export manifest generation with input fingerprint, config, model versions, backend, and timings
- [ ] 10.2 Export restored audio, separated stems, JSON analysis reports, comparison reports, and artifact reports
- [ ] 10.3 Generate waveform and spectrogram previews through existing visualization utilities
- [ ] 10.4 Keep rejected outputs separate from accepted final exports

## 11. Batch Processing

- [ ] 11.1 Implement recursive folder scanning with supported audio filters
- [ ] 11.2 Implement queue management and resumable job state
- [ ] 11.3 Add parallel processing controls with deterministic logging
- [ ] 11.4 Add batch failure isolation so one file does not abort the full queue

## 12. Benchmarking

- [ ] 12.1 Create benchmark runner under `benchmarks/`
- [ ] 12.2 Measure runtime, VRAM usage where available, processing latency, SDR, SNR, and artifact scores
- [ ] 12.3 Generate structured benchmark reports
- [ ] 12.4 Add benchmark CLI command integration

## 13. CLI Expansion

- [ ] 13.1 Add `restore`, `separate`, `denoise`, `enhance`, `preset`, `batch`, and `benchmark` commands
- [ ] 13.2 Use Rich progress bars and structured terminal diagnostics
- [ ] 13.3 Ensure failure-safe execution with useful exit codes and error messages
- [ ] 13.4 Verify output names for separation: `vocals.wav`, `drums.wav`, `bass.wav`, and `other.wav`

## 14. Tests

- [ ] 14.1 Add `tests/test_model_registry.py`
- [ ] 14.2 Add `tests/test_backend_abstraction.py`
- [ ] 14.3 Add `tests/test_orchestration.py`
- [ ] 14.4 Add `tests/test_validation_engine.py`
- [ ] 14.5 Add `tests/test_denoise_pipeline.py`
- [ ] 14.6 Add `tests/test_demucs_integration.py` with dependency-gated integration tests
- [ ] 14.7 Add tests for preset execution, export manifests, cache integrity, and batch processing

## 15. Documentation

- [ ] 15.1 Create `docs/AI_PIPELINE.md`
- [ ] 15.2 Create `docs/MODEL_INTEGRATION.md`
- [ ] 15.3 Create `docs/ORCHESTRATION.md`
- [ ] 15.4 Document backend abstraction, validation methodology, model lifecycle, and future realtime roadmap
