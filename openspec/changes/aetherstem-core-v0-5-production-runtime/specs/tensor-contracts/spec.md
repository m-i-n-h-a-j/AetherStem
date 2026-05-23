## MODIFIED Requirements

### Requirement: Expanded Tensor Signatures
Tensor contracts SHALL define model input and output signatures, batch dimensions, stem tensor mapping, frame-size constraints, padding semantics, dtype policy, and layout policy.

#### Scenario: Validating model input
- **WHEN** a model is selected for execution
- **THEN** the runtime validates the prepared tensor against the manifest input signature before inference starts

### Requirement: Stem Tensor Mapping
Separation models SHALL declare how output tensors map to named stems.

#### Scenario: Demucs output mapping
- **WHEN** a Demucs-compatible model returns a multi-stem tensor
- **THEN** tensor contracts map outputs deterministically to vocals, drums, bass, and other

### Requirement: Backend Normalization Rules
Tensor contracts SHALL define backend-specific normalization rules without embedding those rules in orchestration.

#### Scenario: ONNX input normalization
- **WHEN** ONNX Runtime receives an audio tensor
- **THEN** tensor conversion follows the backend normalization contract rather than adapter-local shape guessing
