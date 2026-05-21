## ADDED Requirements

### Requirement: YAML Configuration Loader
The system SHALL implement a YAML-based configuration loader that validates the input against a predefined schema.

#### Scenario: Loading default config
- **WHEN** the application starts without a user-provided config file
- **THEN** the settings from `configs/default.yaml` are loaded into a typed configuration object

### Requirement: Configuration Validation
The configuration loader SHALL ensure that critical parameters (sample rate, chunk size, overlap ratio) are present and within valid ranges.

#### Scenario: Missing configuration parameter
- **WHEN** a configuration file with a missing `sample_rate` is loaded
- **THEN** the system SHALL raise a validation error and stop execution
