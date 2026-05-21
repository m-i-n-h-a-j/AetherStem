## ADDED Requirements

### Requirement: Deep Inspect Command
The CLI SHALL provide a `deep-inspect` command to display advanced technical audio analysis results.

#### Scenario: Running deep-inspect
- **WHEN** the user runs `aetherstem deep-inspect <path-to-audio-file>`
- **THEN** a report is displayed containing Peak level, RMS level, Crest factor, and a summary of spectral content.
