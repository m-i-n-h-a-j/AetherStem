## ADDED Requirements

### Requirement: DSP-Driven Decision Engine
The system SHALL inspect structured DSP analysis and produce deterministic processing decisions for denoising, declipping, bandwidth extension, source separation, validation, and export.

#### Scenario: Noise-driven denoise activation
- **WHEN** analysis reports a noise floor above the configured threshold
- **THEN** the decision engine enables denoising and records the observed value, threshold, and selected action

### Requirement: Avoid Unnecessary Enhancement
The decision engine SHALL skip enhancement stages when analysis does not justify them.

#### Scenario: Clean input
- **WHEN** analysis reports low noise, no clipping, and low lossy confidence
- **THEN** the generated plan skips denoise, declip, and bandwidth extension stages

### Requirement: Processing Graph Execution
The system SHALL execute audio processing through a modular graph with reusable nodes and typed outputs.

#### Scenario: Restore graph
- **WHEN** the user runs `aetherstem restore damaged.flac`
- **THEN** the graph runs analysis, selected enhancement stages, validation, and export in order

### Requirement: Conditional and Branchable Stages
Processing graphs SHALL support conditional execution and branchable stages for operations such as source separation and validation.

#### Scenario: Stem branch
- **WHEN** a graph includes separation
- **THEN** each generated stem can be validated and exported as a separate typed graph output

### Requirement: Preset Plans
The system SHALL load YAML presets and convert them into deterministic processing graph plans.

#### Scenario: Archival restore preset
- **WHEN** the user runs `aetherstem preset archival_restore input.flac`
- **THEN** the configured preset steps are loaded, validated, executed, and recorded in the export manifest
