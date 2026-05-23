## Why

AetherStem v0.4 introduced the core inference runtime: canonical audio buffers, tensor contracts, execution contexts, backend isolation, ONNX Runtime integration, runtime adapter boundaries, chunk scheduling, streaming-compatible execution, and a Demucs-compatible separation adapter. That foundation is executable, but production inference requires stronger lifecycle, optimization, diagnostics, and contract systems before the runtime can scale to many models, hardware targets, and future realtime or plugin environments.

v0.5 extends the existing runtime into a production-grade desktop inference platform. It adds model registry manifests, deterministic model resolution, cache/download lifecycle management, precision and quantization infrastructure, hardware-aware preset selection, runtime telemetry, profiling, expanded tensor abstractions, formal architecture contracts, and production-safe diagnostics.

This change MUST extend the current architecture without weakening v0.4 boundaries:

- orchestration remains decoupled from model internals;
- adapters remain inference-only;
- backends remain isolated;
- chunk scheduling remains deterministic;
- model loading remains lazy;
- runtime execution remains reproducible and reportable.

## What Changes

- Add a manifest-driven model registry package under `ai/models/registry/`.
- Add model lifecycle management for local discovery, deterministic resolution, checksum validation, cache storage, and future remote registry compatibility.
- Add typed model manifests with semantic versioning, architecture metadata, backend compatibility, precision support, sample-rate/channel constraints, stems, model format, and checksums.
- Add precision policy and quantization infrastructure for fp32, fp16, int8-ready metadata, calibration hooks, and backend compatibility validation.
- Add hardware probing for CPU, CUDA, DirectML-ready hooks, memory limits, provider capability, and runtime preset selection.
- Optimize streaming runtime behavior with low-memory reconstruction, chunk prefetch boundaries, and bounded telemetry.
- Extend benchmarks and profiling with throughput, latency, memory, backend comparison, chunk efficiency, timeline tracing, and per-stage runtime metrics.
- Expand tensor contracts for batched tensors, stem tensors, model-specific input/output signatures, padding semantics, and backend-specific normalization.
- Add runtime telemetry and tracing with structured event capture and manifest integration.
- Formalize architecture contracts for adapters, backends, model manifests, tensor contracts, chunk plans, telemetry, and CLI diagnostics.
- Add production-safe diagnostics for missing models, incompatible backends, checksum failures, unavailable providers, OOM fallback, quantization mismatch, and unsupported precision.

## Capabilities

### New Capabilities

- `model-registry`: typed manifests, schema validation, semantic versioning, model discovery, deterministic resolution, compatibility checks, and local/future-remote registry support.
- `model-lifecycle`: cache directories, downloadable/cacheable model assets, checksum validation, lock files, cache integrity checks, and lazy model availability resolution.
- `precision-optimization`: precision policies, supported precision metadata, fp16 hooks, int8-ready quantization metadata, calibration hooks, and backend precision compatibility.
- `hardware-runtime-selection`: hardware probing, provider capability detection, memory-aware preset selection, and deterministic runtime profile resolution.
- `runtime-telemetry`: structured runtime events, trace spans, timing, memory snapshots, fallback records, and manifest integration.
- `runtime-profiling`: stage-level profiling, chunk-level profiling, backend comparison, timeline reports, and profiling-safe CLI flags.
- `expanded-tensor-contracts`: richer tensor signatures for audio, stems, batches, model inputs, model outputs, padding, layout, dtype, and backend normalization.
- `formal-runtime-contracts`: documented and testable contracts for adapters, backends, manifests, tensors, chunks, telemetry, diagnostics, and orchestration boundaries.

### Modified Capabilities

- `runtime-core`: extend execution context, chunk scheduling, memory management, streaming pipeline, and tensor contracts without breaking v0.4 APIs.
- `runtime-backends`: add capability descriptors, precision support, provider feature metadata, and profiling hooks.
- `real-separation`: resolve Demucs-compatible models through manifests and lifecycle manager rather than ad hoc paths.
- `cli`: add model registry, cache, diagnostics, profiling, and runtime preset commands/options.
- `benchmarking`: produce production runtime benchmark and profiling reports.
- `packaging`: keep base install lightweight while extending optional runtime dependency groups.

## Impact

v0.5 increases runtime surface area and must avoid making model execution opaque. Every optimization or fallback decision should be recorded. Every model used by the runtime should be resolved through a manifest and checked for backend, precision, input shape, sample-rate, channel, and checksum compatibility before execution.

The model registry should support local manifests first. Remote registries and automatic downloads should be designed as compatible extension points, but v0.5 does not need to depend on a hosted registry service.

The runtime should remain usable when no heavyweight dependencies are installed: analysis, manifest discovery, diagnostics, validation, and dry-run compatibility checks should work without requiring ONNX Runtime, CUDA, or PyTorch.

## Non-Goals

- No GUI.
- No distributed inference.
- No training or fine-tuning implementation.
- No realtime microphone capture.
- No DAW/plugin implementation.
- No hosted model registry service requirement.
- No requirement to ship pretrained model weights in source control.
- No orchestration rewrite.
