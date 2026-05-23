# AetherStem AI Pipeline

AetherStem v0.3 keeps DSP analysis as the source of truth. The AI layer runs after analysis, builds a deterministic processing plan, executes only requested or justified stages, validates the result, and writes a manifest under `exports/`.

The initial model adapters are placeholders unless real runtimes and model weights are configured. They preserve the execution contract without bundling large model files.

Pipeline:

```text
audio input -> DSP analysis -> decision engine -> graph execution -> validation -> export
```

CLI workflows:

- `aetherstem restore input.flac`
- `aetherstem separate input.flac`
- `aetherstem denoise input.wav`
- `aetherstem enhance input.mp3`
- `aetherstem preset archival_restore input.flac`
- `aetherstem batch ./folder`
- `aetherstem benchmark input.flac`

Each run writes a manifest containing input path, workflow, backend/device selection, plan decisions, configuration, and stage outputs.

