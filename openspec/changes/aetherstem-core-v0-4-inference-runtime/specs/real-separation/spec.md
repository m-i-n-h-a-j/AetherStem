## ADDED Requirements

### Requirement: Demucs-Compatible ONNX Separation
The system SHALL provide a Demucs-compatible separation adapter that prefers ONNX Runtime execution.

#### Scenario: ONNX separation
- **WHEN** a configured Demucs-compatible ONNX model is available
- **THEN** `aetherstem separate input.flac` executes real separation through the runtime adapter and exports stems through the orchestration export layer

### Requirement: PyTorch Fallback Hook
The Demucs-compatible adapter SHALL support an optional PyTorch fallback path when configured and available.

#### Scenario: ONNX unavailable with fallback enabled
- **WHEN** ONNX Runtime is unavailable and PyTorch fallback is enabled
- **THEN** the adapter attempts PyTorch execution and records the fallback in diagnostics

### Requirement: Stereo-Safe Reconstruction
Separation SHALL preserve stereo channel structure and output duration after chunking, padding, and overlap-add reconstruction.

#### Scenario: Stereo input reconstruction
- **WHEN** stereo audio is processed in overlapping chunks
- **THEN** each stem preserves stereo layout and matches the input duration after padding is trimmed

### Requirement: Stem Outputs
The separation adapter SHALL support vocals, drums, bass, other, and optional instrumental outputs.

#### Scenario: Default stem export
- **WHEN** separation completes with default options
- **THEN** `vocals.wav`, `drums.wav`, `bass.wav`, and `other.wav` are available to the export layer

### Requirement: Orchestration Decoupling
Real model execution SHALL not require model-specific branching in the orchestration graph.

#### Scenario: Swapping separation backend
- **WHEN** a separation model is changed from placeholder to Demucs-compatible ONNX
- **THEN** orchestration continues to route by capability and adapter contract only
