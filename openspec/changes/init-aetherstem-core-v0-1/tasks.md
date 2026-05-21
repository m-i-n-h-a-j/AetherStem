## 1. Environment & Project Structure

- [x] 1.1 Create Python 3.11 virtual environment: `py -3.11 -m venv .venv`
- [x] 1.2 Create directory structure: `cli/`, `pipeline/`, `dsp/`, `io/`, `models/`, `configs/`, `utils/`, `tests/`, `temp/`, `output/`, `logs/`, `docs/`
- [x] 1.3 Create `.gitignore` for Python/AI/Audio projects
- [x] 1.4 Create `pyproject.toml` with metadata and initial dependencies
- [x] 1.5 Perform initial editable install: `pip install -e .`

## 2. Core Utilities

- [x] 2.1 Implement structured logging in `utils/logger.py`
- [x] 2.2 Create `configs/default.yaml` with initial settings (sample rate, chunk size, etc.)
- [x] 2.3 Implement YAML configuration loader in `utils/config_loader.py` (or similar)

## 3. Audio I/O & Preprocessing

- [x] 3.1 Implement FFmpeg-based audio conversion in `io/audio_converter.py`
- [x] 3.2 Implement FFprobe-based metadata extraction in `io/audio_inspector.py`
- [x] 3.3 Add input validation for stereo and supported formats (WAV, FLAC, MP3, M4A)

## 4. CLI Implementation

- [x] 4.1 Create `cli/main.py` using Typer
- [x] 4.2 Implement `version` command
- [x] 4.3 Implement `inspect` command using `audio_inspector` and Rich tables
- [x] 4.4 Implement `process` command scaffolding using `audio_converter`

## 5. Documentation & Validation

- [x] 5.1 Generate `README.md` with project overview and setup instructions
- [x] 5.2 Verify CLI `version` and `inspect` commands
- [x] 5.3 Verify audio conversion to 96kHz/32-bit float WAV
- [x] 5.4 Document remaining TODOs and next steps for AI model integration
