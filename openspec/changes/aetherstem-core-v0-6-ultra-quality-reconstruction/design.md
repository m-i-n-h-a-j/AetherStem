## Context

AetherStem v0.4/v0.5 provide runtime contracts, backends, model manifests, telemetry, profiling, model lifecycle diagnostics, and CLI guidance. v0.6 adds an offline reconstruction subsystem above those runtime foundations.

Target pipeline:

```text
Input Audio
  -> Forensic Analysis
  -> Artifact Profiling
  -> Restoration Feasibility Analysis
  -> Adaptive Reconstruction Graph
  -> Multi-Pass Refinement
  -> High-Resolution Rendering
  -> JSON/visual diagnostics
```

## Package Layout

```text
ai/reconstruction/
  analysis/
  profiling/
  orchestration/
  pipelines/
  restoration/
  spectral/
  harmonic/
  transients/
  stereo/
  bandwidth/
  mastering/
  psychoacoustics/
  rendering/
  evaluation/
  diagnostics/
  presets/
```

## Philosophy

AetherStem does not perform true lossless recovery from lossy sources. Reports and CLI text should use language such as reconstruction, restoration, regeneration, remastering, spectral repair, and perceptual optimization.

The intended output is a plausibly reconstructed high-resolution master, with confidence and uncertainty exposed transparently.

## Forensic Analysis

Forensic analysis remains deterministic and produces:

- `SourceProfile`
- `ArtifactProfile`
- `SpectralFingerprint`
- `RestorationFeasibility`
- `RestorationConfidence`

The first implementation can use deterministic DSP heuristics from existing analysis and additional NumPy/SciPy spectral metrics. Future AI classifiers can be added behind the same types.

## Reconstruction Graph

Graph generation maps forensic profiles to stages. Examples:

- clipping detected -> declip stage;
- lossy severity high -> bandwidth extension and spectral repair;
- stereo collapse -> stereo reconstruction;
- transient smear -> transient recovery;
- noisy source -> denoise;
- archival/extreme profiles -> harmonic regeneration, psychoacoustic optimization, mastering, multi-pass refinement.

Graph generation must be reproducible for identical inputs/configuration.

## Stage Contracts

Stages are reusable, deterministic, telemetry-aware units:

```python
class RestorationStage(Protocol):
    name: str
    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult: ...
```

Stages may use runtime adapters later, but must not own CLI/export behavior.

## Rendering

Rendering is float-safe throughout. Primary outputs:

- 32-bit float WAV;
- 32-bit float FLAC where supported;
- 192kHz archival renders;
- 96kHz mastering renders.

Internal clipping should be avoided with headroom normalization and float processing.

## Evaluation and Diagnostics

Evaluation compares source and reconstructed audio for:

- artifact reduction;
- spectral recovery;
- stereo integrity;
- transient quality;
- mastering consistency;
- clipping prevention.

Diagnostics include JSON reports and optional visual artifacts such as before/after spectrograms and waveform comparisons.

## CLI

New commands:

- `aetherstem forensic input.mp3`
- `aetherstem reconstruct input.mp3`
- `aetherstem remaster input.flac`
- `aetherstem archival input.wav`
- `aetherstem upscale input.flac`

These commands should reuse runtime/config/help/telemetry conventions.
