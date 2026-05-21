## ADDED Requirements

### Requirement: FFmpeg Audio Conversion
The system SHALL use FFmpeg to convert input audio files to 32-bit float WAV files at a 96kHz sample rate.

#### Scenario: Successful audio conversion
- **WHEN** the user provides a stereo FLAC file to the `process` command
- **THEN** FFmpeg is called to generate a 96kHz, 32-bit float stereo WAV file in the `temp/` directory

### Requirement: Input Validation
The audio I/O module SHALL validate that the input file is stereo and in a supported format (WAV, FLAC, MP3, M4A).

#### Scenario: Unsupported file format
- **WHEN** an unsupported file type (e.g., .txt) is provided
- **THEN** the system SHALL log an error and exit gracefully
