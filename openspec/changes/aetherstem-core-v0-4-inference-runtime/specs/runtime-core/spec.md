## ADDED Requirements

### Requirement: Canonical Audio Buffer
The system SHALL define a canonical `AudioBuffer` abstraction for runtime inference with sample rate, channel count, dtype, layout, samples, and metadata.

#### Scenario: Validating adapter input
- **WHEN** an adapter receives audio for inference
- **THEN** it receives an `AudioBuffer` with validated sample rate, channel count, dtype, and layout instead of an untyped NumPy array

### Requirement: Tensor Contracts
The runtime SHALL standardize tensor movement between NumPy, Torch, and ONNX Runtime using explicit shape, dtype, layout, and batch-dimension contracts.

#### Scenario: ONNX tensor preparation
- **WHEN** a stereo audio buffer is prepared for ONNX Runtime
- **THEN** the tensor contract produces the configured channels-first or batched layout without adapter-specific shape guessing

### Requirement: Execution Context
The runtime SHALL pass backend, device, provider, precision, low-memory mode, fallback policy, diagnostics, progress, and cancellation through an execution context.

#### Scenario: CUDA unavailable with fallback enabled
- **WHEN** CUDA is requested but unavailable and CPU fallback is enabled
- **THEN** the context records the fallback decision and continues on CPU

### Requirement: Progress and Cancellation
Runtime execution SHALL support progress callbacks and cancellation tokens across chunked and streaming inference.

#### Scenario: Cancel between chunks
- **WHEN** cancellation is requested during a long separation job
- **THEN** the runtime stops before the next chunk and returns a structured cancellation error

### Requirement: Streaming-Compatible Runtime
The runtime SHALL expose generator-based chunk processing and incremental reconstruction for long audio without requiring full output materialization during intermediate stages.

#### Scenario: Low-memory long file
- **WHEN** low-memory mode is enabled for a long file
- **THEN** chunks are processed incrementally with bounded memory and duration-preserving reconstruction
