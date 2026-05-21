## Context

AetherStem is a new project targeting Windows 11 for AI-assisted music source separation. The current state is an empty project directory with OpenSpec and Gemini CLI initialized. The goal is to establish a robust foundation that avoids "Linux-only" assumptions and prioritizes modularity and future extensibility.

## Goals / Non-Goals

**Goals:**
- Establish a Python 3.11 virtual environment.
- Create a modular, production-oriented project structure.
- Implement a CLI with `version`, `inspect`, and `process` commands.
- Implement core utilities: logging and YAML configuration.
- Implement FFmpeg-based audio preprocessing to 96kHz/32-bit float WAV.
- Implement FFprobe-based audio metadata inspection.

**Non-Goals:**
- Implementation of AI models (Torch, CUDA, Demucs).
- Large model downloads or checkpoints.
- Linux-specific shell scripts or paths.

## Decisions

- **Environment Management**: Use `py -3.11 -m venv .venv` to ensure Windows-native Python 3.11 is used.
- **Dependency Management**: Use `pyproject.toml` with `setuptools` for modern metadata handling and editable install support (`pip install -e .`).
- **CLI Framework**: Use `Typer` for the CLI. It provides excellent type safety, automatic help generation, and integrates seamlessly with `Rich` for beautiful terminal output.
- **Audio Processing**: Call `ffmpeg` and `ffprobe` directly via `subprocess` instead of using high-level wrappers. This provides maximum control over arguments and better error handling for the specific 96kHz/32-bit float requirement.
- **Configuration**: Use `PyYAML` for `configs/default.yaml`. YAML is human-readable and supports the complex nested structures common in AI model configurations.
- **Modularity**: Distribute logic across specialized packages (`cli`, `pipeline`, `dsp`, `io`, `models`, `configs`, `utils`). This prevents the "giant script" anti-pattern and allows for independent testing and scaling of components.

## Risks / Trade-offs

- **[Risk] FFmpeg Availability** → **[Mitigation]** The system will verify FFmpeg availability at startup and provide clear instructions if missing from PATH.
- **[Risk] Path Handling** → **[Mitigation]** Use `pathlib` exclusively to ensure cross-platform compatibility and avoid hardcoded backslashes/forward slashes.
- **[Trade-off] Direct Subprocess vs Wrappers** → **[Rationale]** Direct subprocess calls are more verbose but avoid the limitations and extra dependencies of wrappers like `pydub` or `ffmpeg-python` for specialized conversion tasks.
- **[Risk] High Sample Rate (96kHz)** → **[Mitigation]** Ensure the conversion logic explicitly handles high bit depths and sample rates, and that the `io` module validates the output.
