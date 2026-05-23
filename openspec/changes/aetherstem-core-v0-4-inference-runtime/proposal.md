## Why

AetherStem v0.3 established AI orchestration, model metadata, backend selection, validation, exports, presets, batch workflows, and placeholder adapters. The system can now plan and execute restoration graphs, but it still lacks a canonical inference runtime for real model execution. Audio buffers, tensor movement, chunk scheduling, device selection, cancellation, streaming flow, and backend sessions need stable contracts before replacing placeholders with production model integrations.

v0.4 introduces the inference runtime layer. It keeps orchestration decoupled from model internals while making adapters executable, async-ready, chunk-safe, backend-aware, and stream-compatible. The first real integration targets Demucs-compatible source separation through an ONNX-first backend, with optional PyTorch fallback.

## What Changes

- Add `ai/runtime/` with canonical audio buffers, tensor contracts, device/memory management, chunk scheduling, streaming pipeline, progress reporting, and cancellation primitives.
- Refactor model adapters behind strict runtime interfaces: `SeparationAdapter`, `DenoiseAdapter`, and `EnhancementAdapter`.
- Add async execution contracts with progress callbacks, cancellation support, chunked inference, and stream-safe processing.
- Add an ONNX Runtime backend with session management, provider selection, CPU/CUDA provider support, fp16 hooks, and backend registry integration.
- Integrate the first executable Demucs-compatible separation backend with ONNX-preferred execution and optional PyTorch fallback.
- Add adaptive chunk scheduling, overlap-add reconstruction, stereo-safe reconstruction, automatic padding, dynamic batching, memory estimation, and graceful OOM fallback behavior.
- Add generator-based streaming inference for long audio and future realtime processing.
- Extend CLI workflows with runtime flags and diagnostics: `--device`, `--backend`, `--chunk-size`, `--overlap`, `--low-memory`, `--benchmark-runtime`, and a runtime diagnostics command.
- Add validation tests and benchmarks for tensor compatibility, chunk integrity, stereo reconstruction, deterministic overlap-add, throughput, latency, VRAM usage, backend comparison, and scheduler efficiency.
- Move heavyweight inference dependencies into optional dependency groups while keeping base install lightweight.
- Add runtime architecture and model integration documentation.

## Capabilities

### New Capabilities

- `runtime-core`: canonical audio buffer, tensor contracts, execution context, device manager, memory manager, chunk scheduler, stream pipeline, progress, and cancellation.
- `runtime-backends`: backend registry and ONNX Runtime backend with session/provider management.
- `runtime-adapters`: strict inference-only adapter contracts for separation, denoise, and enhancement models.
- `real-separation`: Demucs-compatible real separation runtime with ONNX-first execution, PyTorch fallback hooks, chunk batching, overlap-add, padding, and stereo-safe reconstruction.
- `streaming-runtime`: generator-based low-memory chunk flow and incremental reconstruction.
- `runtime-validation`: tests for tensor movement, chunk integrity, overlap-add determinism, stereo correctness, and cancellation behavior.
- `runtime-benchmarking`: runtime throughput, latency, memory, backend comparison, and scheduler-efficiency reports.

### Modified Capabilities

- `orchestration`: graph execution SHALL invoke model adapters through runtime contracts without knowing model internals.
- `cli`: AI commands SHALL accept runtime execution flags and expose runtime diagnostics.
- `config`: runtime configuration SHALL include backend, device, chunk size, overlap, low-memory mode, fp16 preference, and fallback policy.
- `packaging`: heavyweight runtime dependencies SHALL move to optional dependency groups.

## Impact

This change replaces v0.3 placeholders with executable runtime foundations while preserving the orchestration boundary. It introduces new complexity around device behavior, provider availability, memory limits, and model format variability. The design must make unsupported providers, missing model files, OOM conditions, and fallback decisions explicit and reportable instead of crashing or silently changing behavior.

The first real model integration should be narrow and production-shaped: Demucs-compatible separation only. Denoise and enhancement adapters move to strict runtime interfaces but may remain non-executable until model-specific integrations are added in later releases.

## Non-Goals

- No GUI.
- No distributed inference.
- No training or fine-tuning pipelines.
- No realtime microphone capture.
- No DAW plugin.
- No requirement to bundle pretrained model weights in source control.
- No orchestration rewrite.
