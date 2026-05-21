## ADDED Requirements

### Requirement: Python 3.11 Virtual Environment
The system SHALL be configured to use a Python 3.11 virtual environment named `.venv` for all development and execution tasks.

#### Scenario: Venv creation
- **WHEN** the user runs the initialization command
- **THEN** a `.venv` directory is created using `py -3.11 -m venv .venv`

#### Scenario: Python version verification
- **WHEN** the `.venv` is activated and `python --version` is run
- **THEN** the output MUST indicate a version of Python 3.11.x

### Requirement: Dependency Management
The project SHALL manage dependencies using a `pyproject.toml` file and support editable installs.

#### Scenario: Installing dependencies
- **WHEN** the user runs `pip install -e .` inside the `.venv`
- **THEN** all defined dependencies (numpy, scipy, soundfile, librosa, ffmpeg-python, pydub, rich, typer, pyyaml, tqdm) are installed successfully
