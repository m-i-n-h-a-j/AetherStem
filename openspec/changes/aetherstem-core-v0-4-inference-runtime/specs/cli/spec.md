## MODIFIED Requirements

### Requirement: Runtime Flags
AI CLI commands SHALL accept runtime execution flags for backend, device, chunk size, overlap, low-memory mode, and runtime benchmarking.

#### Scenario: Selecting CPU ONNX runtime
- **WHEN** the user runs `aetherstem separate input.flac --backend onnx --device cpu`
- **THEN** separation uses the ONNX CPU runtime if compatible and records the runtime selection in the manifest

### Requirement: Runtime Diagnostics Command
The CLI SHALL provide a runtime diagnostics command that reports backend availability, providers, devices, memory summaries, and optional dependency status.

#### Scenario: Inspecting runtime environment
- **WHEN** the user runs runtime diagnostics
- **THEN** the CLI prints available ONNX providers, Torch CUDA status, selected defaults, and fallback capability

### Requirement: Runtime Benchmark Flag
AI CLI commands SHALL optionally write runtime benchmark metrics when `--benchmark-runtime` is enabled.

#### Scenario: Benchmarking separation
- **WHEN** the user runs separation with runtime benchmarking enabled
- **THEN** the manifest or benchmark report includes throughput, latency, memory, backend, provider, and chunk scheduler metrics
