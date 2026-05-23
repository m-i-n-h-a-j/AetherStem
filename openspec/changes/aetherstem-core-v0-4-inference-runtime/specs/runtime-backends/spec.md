## ADDED Requirements

### Requirement: Backend Registry
The system SHALL provide a runtime backend registry for discovering, selecting, and invoking executable inference backends.

#### Scenario: Listing runtime backends
- **WHEN** runtime diagnostics are requested
- **THEN** the registry reports available backends, devices, providers, and optional dependency status

### Requirement: ONNX Runtime Backend
The system SHALL implement an ONNX Runtime backend with session management, provider discovery, provider selection, and structured diagnostics.

#### Scenario: CPU provider execution
- **WHEN** an ONNX model runs on a system with only `CPUExecutionProvider`
- **THEN** inference executes on CPU and records the provider in runtime diagnostics

### Requirement: CUDA Provider Selection
The ONNX backend SHALL support `CUDAExecutionProvider` when available and requested.

#### Scenario: CUDA requested
- **WHEN** CUDA is requested and `CUDAExecutionProvider` is available
- **THEN** the ONNX backend selects CUDA deterministically

### Requirement: Unsupported Provider Handling
The runtime SHALL return structured errors for unavailable or unsupported providers unless fallback policy permits an alternate provider.

#### Scenario: CUDA requested without fallback
- **WHEN** CUDA is requested, unavailable, and fallback is disabled
- **THEN** runtime initialization fails before inference starts with an unsupported-provider error

### Requirement: Precision Hooks
The ONNX backend SHALL expose fp16 preference hooks without requiring model conversion in v0.4.

#### Scenario: fp16 requested for fp32 model
- **WHEN** fp16 is requested but the model/session does not support it
- **THEN** the backend records a precision warning and runs according to fallback policy
