## ADDED Requirements

### Requirement: Typer-based CLI
The system SHALL provide a command-line interface implemented using the Typer library.

#### Scenario: Running the CLI
- **WHEN** the user runs `aetherstem --help`
- **THEN** a help message listing available commands (`version`, `inspect`, `process`) is displayed

### Requirement: Version Command
The CLI SHALL provide a `version` command to display the current application version.

#### Scenario: Displaying version
- **WHEN** the user runs `aetherstem version`
- **THEN** the output MUST be "AetherStem v0.1"

### Requirement: Inspect Command
The CLI SHALL provide an `inspect` command to display audio file metadata.

#### Scenario: Inspecting an audio file
- **WHEN** the user runs `aetherstem inspect <path-to-audio-file>`
- **THEN** a Rich table is displayed containing codec, sample rate, bit depth, channels, and duration
