## 1. Runtime Package Foundation

- [ ] 1.1 Add `ai/runtime/` package and module skeletons.
- [ ] 1.2 Implement `AudioBuffer` with sample rate, channel count, dtype, layout, metadata, validation, and layout conversion helpers.
- [ ] 1.3 Implement tensor contracts for NumPy, Torch, and ONNX Runtime shape/dtype/layout movement.
- [ ] 1.4 Add `ExecutionContext` with backend, device, provider, precision, low-memory mode, fallback policy, diagnostics, progress, and cancellation.
- [ ] 1.5 Add progress reporter and cancellation token primitives.

## 2. Device and Memory Management

- [ ] 2.1 Implement `DeviceManager` for CPU, CUDA, DirectML-ready hooks, and future TensorRT/OpenVINO extension points.
- [ ] 2.2 Implement `MemoryManager` with runtime memory summaries and estimation utilities.
- [ ] 2.3 Add graceful fallback behavior for unavailable devices and unsupported providers.
- [ ] 2.4 Add structured diagnostics for selected device, provider, precision, and fallback decisions.

## 3. Backend Registry and ONNX Runtime

- [ ] 3.1 Add `ai/backends/` package with backend protocol and backend registry.
- [ ] 3.2 Implement ONNX Runtime backend with provider discovery.
- [ ] 3.3 Implement ONNX session lifecycle, session caching, model input/output inspection, and execution.
- [ ] 3.4 Support `CPUExecutionProvider` and `CUDAExecutionProvider`.
- [ ] 3.5 Add fp16 preference hooks without requiring fp16 conversion in v0.4.
- [ ] 3.6 Add optional PyTorch runtime backend as fallback interface.

## 4. Runtime Adapter Interfaces

- [ ] 4.1 Add `ai/adapters/` package.
- [ ] 4.2 Define strict async `SeparationAdapter`, `DenoiseAdapter`, and `EnhancementAdapter` contracts.
- [ ] 4.3 Define runtime result types for stems, denoised audio, enhanced audio, warnings, diagnostics, and timings.
- [ ] 4.4 Enforce adapter boundaries: no DSP analysis, export logic, file IO, or orchestration decisions.
- [ ] 4.5 Add runtime executor for calling async adapters from existing synchronous CLI/orchestration paths.

## 5. Chunk Scheduler

- [ ] 5.1 Implement deterministic `ChunkPlan` and `ChunkScheduler`.
- [ ] 5.2 Add configurable overlap, hop size, automatic padding, and duration-preserving trimming.
- [ ] 5.3 Add VRAM-aware chunk sizing and dynamic batch sizing.
- [ ] 5.4 Add sequential fallback for low-memory and OOM recovery.
- [ ] 5.5 Add deterministic overlap-add reconstruction utilities.

## 6. Streaming Pipeline

- [ ] 6.1 Implement generator-based chunk flow.
- [ ] 6.2 Add incremental reconstruction for low-memory mode.
- [ ] 6.3 Support progress and cancellation between chunks.
- [ ] 6.4 Keep streaming APIs realtime-ready without adding microphone capture or realtime playback.

## 7. Real Demucs-Compatible Separation

- [ ] 7.1 Implement Demucs-compatible runtime adapter with ONNX-first execution.
- [ ] 7.2 Add local ONNX model path support and registry-managed model reference hooks.
- [ ] 7.3 Add optional PyTorch fallback adapter boundary.
- [ ] 7.4 Implement stereo-safe input normalization and output reconstruction.
- [ ] 7.5 Implement chunk batching and overlap-add for separated stems.
- [ ] 7.6 Support `vocals.wav`, `drums.wav`, `bass.wav`, `other.wav`, and optional `instrumental` outputs through orchestration export.
- [ ] 7.7 Ensure orchestration graph can run real separation without model-specific branching.

## 8. CLI and Configuration

- [ ] 8.1 Extend AI CLI commands with `--device`, `--backend`, `--chunk-size`, `--overlap`, `--low-memory`, and `--benchmark-runtime`.
- [ ] 8.2 Add runtime diagnostics CLI command.
- [ ] 8.3 Extend YAML config with runtime backend, device, provider, chunking, low-memory, precision, and fallback policy.
- [ ] 8.4 Ensure CLI diagnostics use structured Rich output and stable non-zero failures.

## 9. Runtime Validation Tests

- [ ] 9.1 Add tests for `AudioBuffer` layout conversion and validation.
- [ ] 9.2 Add tests for tensor contract compatibility.
- [ ] 9.3 Add tests for deterministic chunk planning and overlap-add reconstruction.
- [ ] 9.4 Add tests for stereo reconstruction correctness and duration preservation.
- [ ] 9.5 Add tests for cancellation and progress callback behavior.
- [ ] 9.6 Add dependency-gated ONNX Runtime session tests.
- [ ] 9.7 Add integration test for Demucs-compatible separation when a test ONNX model is available.

## 10. Benchmarking

- [ ] 10.1 Extend benchmark runner with runtime throughput and latency metrics.
- [ ] 10.2 Add VRAM/memory usage reporting where available.
- [ ] 10.3 Add backend comparison report structure.
- [ ] 10.4 Add chunk scheduler efficiency metrics.
- [ ] 10.5 Add `--benchmark-runtime` report generation to CLI workflows.

## 11. Packaging

- [ ] 11.1 Move heavyweight inference dependencies out of base dependencies where possible.
- [ ] 11.2 Add optional dependency groups: `runtime-cpu`, `runtime-cuda`, and `runtime-dev`.
- [ ] 11.3 Keep test/development dependencies separate from runtime install groups.
- [ ] 11.4 Verify headless-safe execution remains intact.

## 12. Documentation

- [ ] 12.1 Create runtime lifecycle architecture documentation.
- [ ] 12.2 Document backend abstraction and provider selection.
- [ ] 12.3 Document model adapter integration rules.
- [ ] 12.4 Document chunk scheduler design and OOM fallback behavior.
- [ ] 12.5 Document streaming pipeline design and future realtime path.
