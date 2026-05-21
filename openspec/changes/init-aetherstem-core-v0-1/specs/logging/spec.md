## ADDED Requirements

### Requirement: Structured Logging
The system SHALL implement a structured logging utility in `utils/logger.py` that supports both console and file logging.

#### Scenario: Logger initialization
- **WHEN** the application starts
- **THEN** log messages are written to both the console and a file in the `logs/` directory with timestamps

### Requirement: Processing Stage Logging
The system SHALL log the entry and exit of major processing stages, including FFmpeg commands.

#### Scenario: FFmpeg command logging
- **WHEN** an FFmpeg command is executed
- **THEN** the exact command string and its return code are logged at the INFO level
