## 1. Model Registry Package

- [ ] 1.1 Add `ai/models/registry/` package structure.
- [ ] 1.2 Implement strongly typed `ModelManifest`, `ModelAsset`, `TensorSignature`, `PrecisionSupport`, and `ResolvedModel` metadata types.
- [ ] 1.3 Add semantic version parsing and validation.
- [ ] 1.4 Add manifest schema validation and diagnostics.
- [ ] 1.5 Add local manifest discovery from configured directories.
- [ ] 1.6 Add deterministic manifest ordering and candidate rejection reporting.

## 2. Model Resolution and Compatibility

- [ ] 2.1 Implement resolver for task, architecture, backend, device, precision, sample rate, channels, stems, and model format.
- [ ] 2.2 Implement backend compatibility checks using runtime backend capabilities.
- [ ] 2.3 Implement precision compatibility checks.
- [ ] 2.4 Implement tensor signature compatibility checks.
- [ ] 2.5 Return structured `ResolvedModel` objects without loading model weights.

## 3. Model Lifecycle and Cache

- [ ] 3.1 Add model cache root configuration.
- [ ] 3.2 Implement cache path resolution and asset availability checks.
- [ ] 3.3 Implement SHA-256 checksum validation.
- [ ] 3.4 Add lock file handling for future downloads.
- [ ] 3.5 Add cache integrity diagnostics and repair recommendations.
- [ ] 3.6 Add future remote registry/download extension points without requiring hosted infrastructure.

## 4. Precision and Quantization Infrastructure

- [ ] 4.1 Add `ai/optimization/` package.
- [ ] 4.2 Implement precision policy for `fp32`, `fp16`, and `int8-ready` metadata.
- [ ] 4.3 Add quantization metadata structures.
- [ ] 4.4 Add calibration hook interfaces.
- [ ] 4.5 Validate requested precision against model manifest and backend capabilities.
- [ ] 4.6 Record precision fallback decisions in telemetry.

## 5. Hardware Capability Probing and Runtime Profiles

- [ ] 5.1 Extend device manager with richer CPU/CUDA/DirectML-ready capability data.
- [ ] 5.2 Add backend capability descriptors for providers, precision, memory, and execution features.
- [ ] 5.3 Implement runtime profiles: `cpu_safe`, `cuda_fast`, `cuda_low_memory`, `portable`, and `diagnostic`.
- [ ] 5.4 Implement deterministic runtime preset selection.
- [ ] 5.5 Record selected runtime profile in manifests and benchmark reports.

## 6. Streaming Runtime Optimization

- [ ] 6.1 Extend streaming pipeline with bounded telemetry.
- [ ] 6.2 Add chunk prefetch boundaries without increasing peak memory unexpectedly.
- [ ] 6.3 Add low-memory reconstruction diagnostics.
- [ ] 6.4 Add cancellation-safe cleanup for partial stream execution.

## 7. Runtime Telemetry and Tracing

- [ ] 7.1 Add `ai/telemetry/` package.
- [ ] 7.2 Implement structured runtime events and trace spans.
- [ ] 7.3 Add telemetry sinks for in-memory capture and JSON reports.
- [ ] 7.4 Integrate telemetry into execution context.
- [ ] 7.5 Emit events for model resolution, cache validation, backend/provider/precision selection, chunk planning, fallback, OOM, cancellation, and completion.

## 8. Profiling and Benchmarking

- [ ] 8.1 Add runtime profiler with stage and chunk timings.
- [ ] 8.2 Add optional memory snapshots where available.
- [ ] 8.3 Extend benchmark reports with runtime profile, model manifest, precision, cache status, and telemetry summary.
- [ ] 8.4 Add backend comparison benchmarks for compatible profiles.
- [ ] 8.5 Add CLI profiling and telemetry flags.

## 9. Expanded Tensor Contracts

- [ ] 9.1 Extend tensor contracts with input and output signatures.
- [ ] 9.2 Add stem tensor mapping.
- [ ] 9.3 Add model frame size and padding semantics.
- [ ] 9.4 Add dtype/layout conversion policies.
- [ ] 9.5 Add strict pre-execution tensor validation.
- [ ] 9.6 Add backend normalization rules.

## 10. CLI and Diagnostics

- [ ] 10.1 Add CLI command to list discovered model manifests.
- [ ] 10.2 Add CLI command to validate model cache.
- [ ] 10.3 Add CLI command to resolve a model for a task/backend/device/precision.
- [ ] 10.4 Extend runtime diagnostics with hardware profiles and model registry status.
- [ ] 10.5 Add production-safe error messages for missing models, corrupt cache, unsupported precision, incompatible providers, and checksum failures.

## 11. Runtime Contract Documentation

- [ ] 11.1 Document model manifest schema and lifecycle flow.
- [ ] 11.2 Document resolver determinism and compatibility rules.
- [ ] 11.3 Document precision/quantization policy.
- [ ] 11.4 Document runtime profile selection.
- [ ] 11.5 Document telemetry/profiling event model.
- [ ] 11.6 Document formal adapter/backend/tensor/chunk contracts.

## 12. Tests

- [ ] 12.1 Add manifest parsing and validation tests.
- [ ] 12.2 Add resolver determinism tests.
- [ ] 12.3 Add checksum validation and corrupt-cache tests.
- [ ] 12.4 Add precision compatibility tests.
- [ ] 12.5 Add hardware profile selection tests.
- [ ] 12.6 Add telemetry event capture tests.
- [ ] 12.7 Add profiling report tests.
- [ ] 12.8 Add expanded tensor contract tests.
- [ ] 12.9 Add CLI diagnostics tests for registry/cache/runtime profile commands.
