## ADDED Requirements

### Requirement: Raw Buffer Loading
The audio I/O module SHALL support loading audio files directly into floating-point NumPy arrays for DSP processing.

#### Scenario: Loading to NumPy
- **WHEN** a WAV file is loaded via the `load_raw` utility
- **THEN** a NumPy array of shape (channels, samples) with 32-bit float values is returned.
