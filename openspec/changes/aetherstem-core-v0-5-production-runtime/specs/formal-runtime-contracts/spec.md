## ADDED Requirements

### Requirement: Adapter Contract Preservation
Runtime adapters SHALL remain inference-only and SHALL NOT perform DSP analysis, export logic, input file IO, report writing, or orchestration decisions.

#### Scenario: Adapter review
- **WHEN** a new runtime adapter is added
- **THEN** tests or review checks verify that orchestration and export responsibilities remain outside the adapter

### Requirement: Backend Isolation
Backends SHALL expose capabilities and execution methods without leaking provider-specific logic into orchestration.

#### Scenario: Adding OpenVINO later
- **WHEN** a future OpenVINO backend is added
- **THEN** orchestration continues to route through backend and adapter contracts without OpenVINO-specific branches

### Requirement: Deterministic Runtime Reports
Runtime execution SHALL record resolution, compatibility, fallback, precision, backend, provider, and chunk scheduling decisions.

#### Scenario: Reproducing a run
- **WHEN** a run manifest is inspected
- **THEN** it contains enough runtime decision data to explain model selection and execution behavior

### Requirement: Backward-Compatible Runtime Extension
v0.5 SHALL extend v0.4 runtime APIs without breaking existing v0.4 orchestration workflows.

#### Scenario: Existing separate command
- **WHEN** `aetherstem separate` runs with existing v0.4-style configuration
- **THEN** it still executes through the runtime boundary while optionally using v0.5 registry metadata when available
