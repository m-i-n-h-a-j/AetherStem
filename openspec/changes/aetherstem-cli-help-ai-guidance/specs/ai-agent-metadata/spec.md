## ADDED Requirements

### Requirement: AI-Readable Metadata Export
The CLI SHALL export deterministic machine-readable command metadata for external AI agents.

#### Scenario: Agent metadata request
- **WHEN** an external tool requests CLI metadata
- **THEN** the output includes commands, arguments, options, examples, workflows, diagnostics, and project conventions as JSON

### Requirement: Stable Metadata Shape
The AI metadata JSON SHALL use stable keys and deterministic ordering.

#### Scenario: Comparing metadata output
- **WHEN** metadata is exported twice with the same code/config
- **THEN** command ordering and top-level keys remain stable

### Requirement: No Terminal Formatting in JSON
Machine-readable exports SHALL NOT include Rich markup or terminal control sequences.

#### Scenario: Parsing metadata
- **WHEN** an AI agent parses the metadata JSON
- **THEN** it can consume plain strings, lists, and objects without stripping terminal formatting
