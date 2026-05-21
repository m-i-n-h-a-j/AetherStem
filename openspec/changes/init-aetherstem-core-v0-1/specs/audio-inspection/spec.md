## ADDED Requirements

### Requirement: FFprobe Metadata Extraction
The system SHALL use FFprobe to extract audio metadata including codec, sample rate, bit depth, channels, and duration.

#### Scenario: Metadata extraction
- **WHEN** the `inspect` command is called on an MP3 file
- **THEN** FFprobe is executed and the resulting JSON metadata is parsed into a structured object

### Requirement: Rich Metadata Display
The CLI SHALL display the extracted metadata in a formatted Rich table.

#### Scenario: Table display
- **WHEN** metadata is successfully extracted
- **THEN** a table with headers "Codec", "Sample Rate", "Bit Depth", "Channels", and "Duration" is printed to the console
