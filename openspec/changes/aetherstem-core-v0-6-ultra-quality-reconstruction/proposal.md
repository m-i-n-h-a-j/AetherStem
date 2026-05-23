## Why

AetherStem now has deterministic DSP analysis, AI orchestration, a v0.4 runtime, v0.5 model lifecycle infrastructure, telemetry, profiling, and CLI guidance. The next step is an offline-quality-first reconstruction subsystem that treats damaged, lossy, clipped, smeared, or bandwidth-limited audio as restoration material.

v0.6 transforms AetherStem into an experimental high-end AI-assisted audio reconstruction, restoration, and remastering platform. It prioritizes maximum perceptual quality, forensic transparency, archival rendering, and modular reconstruction pipelines over realtime constraints, low resource usage, or fast processing.

The system MUST NOT market results as “true lossless recovery” for lossy sources. It performs reconstruction, restoration, regeneration, remastering, spectral repair, and perceptual optimization to produce plausibly reconstructed high-resolution masters.

## What Changes

- Add `ai/reconstruction/` as a major top-level subsystem.
- Add deterministic forensic source analysis and artifact profiling.
- Add restoration feasibility and confidence scoring.
- Add adaptive reconstruction graph generation.
- Add modular stages for denoise, declip, dereverb-ready hooks, dynamic recovery, stereo reconstruction, harmonic regeneration, spectral repair, bandwidth extension, transient recovery, AI stem cleanup, psychoacoustic optimization, and AI mastering.
- Add multi-pass reconstruction pipelines and profile presets.
- Add ultra-quality rendering for 32-bit float, high-sample-rate offline output.
- Add quality evaluation and visual diagnostics hooks.
- Add CLI commands: `reconstruct`, `remaster`, `archival`, `forensic`, and `upscale`.
- Integrate telemetry/profiling and existing runtime boundaries.

## Capabilities

### New Capabilities

- `reconstruction-core`: reusable reconstruction subsystem, profiles, stage contracts, graph execution, pipeline presets, and deterministic reports.
- `forensic-analysis`: source profile, artifact profile, spectral fingerprint, feasibility, confidence, codec/transcode heuristics, transient smear, stereo collapse, ringing, phase corruption, and temporal consistency.
- `adaptive-reconstruction-graph`: deterministic graph generation from forensic profiles and requested reconstruction profile.
- `harmonic-regeneration`: phase-aware overtone synthesis, harmonic filling, smoothing, continuity repair, and tonal balance preservation.
- `bandwidth-extension`: high-frequency synthesis and bandwidth extension hooks with stereo/phase safety.
- `transient-recovery`: attack reconstruction, codec smear correction, microdynamic recovery, and overshoot prevention.
- `stereo-reconstruction`: stereo width recovery, phase restoration, ambience-ready hooks, mid/side repair, and mono compatibility constraints.
- `spectral-repair`: spectral interpolation, notch repair, ringing suppression, hole filling, temporal smoothing, and continuity repair.
- `psychoacoustic-optimization`: masking-aware enhancement, perceived detail optimization, fatigue reduction, and adaptive brightness balancing.
- `ai-mastering`: mastering profiles, tonal balancing, loudness-aware mastering, dynamic reconstruction, stereo optimization, adaptive limiting, harmonic saturation, and intelligent EQ hooks.
- `ultra-quality-rendering`: float-safe rendering, high-quality resampling, anti-alias filtering hooks, dithering metadata, and 96/192kHz offline exports.
- `reconstruction-evaluation`: reconstruction score, artifact reduction score, spectral recovery score, stereo integrity score, transient score, and mastering consistency score.

### Modified Capabilities

- `cli`: add reconstruction-oriented commands and options.
- `runtime-telemetry`: capture reconstruction confidence, stage timings, artifact reduction metrics, clipping prevention, and scheduler performance.
- `batch-export`: allow reconstruction workflows to reuse export/report conventions.
- `cli-help`: include reconstruction commands, examples, and philosophical guidance.

## Impact

v0.6 deliberately accepts long render times, high VRAM usage, multiple passes, and experimental processing. Determinism, transparent uncertainty, and reportable decisions remain mandatory. The first implementation may use deterministic DSP-first reconstruction stages and runtime hooks where model weights are unavailable, but the architecture must be ready for future bandwidth extension, restoration, mastering, declipping, harmonic synthesis, and transient reconstruction models.

## Non-Goals

- No realtime audio engine.
- No VST/DAW plugin.
- No cloud inference.
- No distributed rendering.
- No microphone streaming.
- No claim of mathematically original studio master recovery from lossy sources.
