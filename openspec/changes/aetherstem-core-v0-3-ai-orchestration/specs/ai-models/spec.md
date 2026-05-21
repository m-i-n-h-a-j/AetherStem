## ADDED Requirements

### Requirement: Audio Model Protocol
The system SHALL define a typed `AudioModel` protocol for AI audio processors with `name`, `version`, `load()`, and `process(audio, sample_rate, config)` members.

#### Scenario: Processing through a registered model
- **WHEN** a model receives a NumPy audio buffer and sample rate
- **THEN** it returns a structured model result containing processed audio or stems, metadata, timing, backend, device, warnings, and diagnostics

### Requirement: Structured Model Metadata
The system SHALL represent model capabilities, requirements, versions, compatibility, and result objects with strict typed models.

#### Scenario: Discovering denoise models
- **WHEN** the registry is queried for models with `denoise=True`
- **THEN** only models advertising denoise capability are returned

### Requirement: Lazy Model Loading
The system SHALL avoid loading model weights or importing heavyweight model packages until a model is selected for execution.

#### Scenario: Listing models
- **WHEN** the user lists or validates available models
- **THEN** metadata is available without loading large weights into memory

### Requirement: Backend Compatibility Checks
The model registry SHALL verify that a selected model is compatible with the requested backend and device before inference starts.

#### Scenario: ONNX-only model on torch backend
- **WHEN** an ONNX-only model is selected with a PyTorch-only backend
- **THEN** execution is rejected with a structured compatibility error before processing audio

### Requirement: Model Family Adapters
The system SHALL provide adapter packages for Demucs, MDX/UVR-compatible separation, denoising, enhancement, and super-resolution model families.

#### Scenario: Demucs stem separation
- **WHEN** `aetherstem separate input.flac` uses a Demucs-compatible model
- **THEN** the model adapter produces configurable stem outputs for vocals, drums, bass, and other
