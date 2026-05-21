# AetherStem

AetherStem is a professional AI-assisted music source separation platform built for Windows. It provides high-fidelity audio preprocessing and modular architecture for future AI model integration.

## Features

- **Windows-Native**: Optimized for Windows environments.
- **High-Fidelity Preprocessing**: Converts audio to 96kHz, 32-bit float WAV using FFmpeg.
- **Rich Metadata Inspection**: Detailed audio properties display via FFprobe and Rich tables.
- **Modular Architecture**: Clean separation of CLI, I/O, DSP, and AI components.
- **Structured Logging**: Diagnostic tracking for all major processing stages.

## Requirements

- Python 3.11+
- FFmpeg (including FFprobe) available in system PATH.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AetherStem
   ```

2. **Create a virtual environment**:
   ```bash
   py -3.11 -m venv .venv
   ```

3. **Activate the environment**:
   ```bash
   .\.venv\Scripts\activate
   ```

4. **Install the package**:
   ```bash
   pip install -e .
   ```

## Usage

AetherStem provides a command-line interface with several commands:

### Check Version
```bash
aetherstem version
```

### Inspect Audio File
```bash
aetherstem inspect <path-to-audio-file>
```

### Process Audio File (Conversion)
```bash
aetherstem process <path-to-audio-file>
```
Converted files are stored in the `temp/` directory by default.

## Project Structure

- `cli/`: Command-line interface logic.
- `io/`: Audio input/output and conversion utilities.
- `utils/`: Common utilities (logging, config loading).
- `configs/`: YAML configuration files.
- `pipeline/`: Future AI processing pipeline.
- `dsp/`: Digital Signal Processing components.
- `models/`: AI model definitions and checkpoints.
- `logs/`: Application log files.
- `temp/`: Temporary processing artifacts.
- `output/`: Final processed output.

## License

[MIT License](LICENSE)
