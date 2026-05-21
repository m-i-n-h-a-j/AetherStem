## ADDED Requirements

### Requirement: Unified Compute Backend Interface
The system SHALL define a backend-independent interface for model execution, availability checks, device discovery, and inference invocation.

#### Scenario: Backend selection
- **WHEN** the configuration requests automatic backend selection
- **THEN** the system selects a compatible available backend deterministically and records the selected backend in the run manifest

### Requirement: CPU Fallback
The system SHALL support CPU fallback when GPU acceleration is unavailable or incompatible.

#### Scenario: CUDA unavailable
- **WHEN** a PyTorch model is selected and CUDA is unavailable
- **THEN** the system falls back to CPU if the model supports CPU execution

### Requirement: ONNX Runtime Provider Detection
The ONNX backend SHALL detect available ONNX Runtime providers and select a compatible provider according to configuration.

#### Scenario: ONNX CPU provider only
- **WHEN** only the CPU provider is available
- **THEN** ONNX inference runs on CPU and records that provider in diagnostics

### Requirement: Future Accelerator Placeholders
The system SHALL include explicit placeholders for future TensorRT and DirectML-ready execution without requiring those runtimes in v0.3.

#### Scenario: TensorRT requested before support is implemented
- **WHEN** the user requests TensorRT execution
- **THEN** the system returns an actionable unsupported-backend error instead of silently using an incompatible backend

### Requirement: Memory-Safe Chunking
Inference execution SHALL support configurable chunk sizes and overlap to avoid loading entire long-form audio into model memory when unnecessary.

#### Scenario: Long input file
- **WHEN** an input exceeds the configured chunk duration
- **THEN** inference is executed in chunks with overlap handling and the output is reconstructed without changing the expected duration
