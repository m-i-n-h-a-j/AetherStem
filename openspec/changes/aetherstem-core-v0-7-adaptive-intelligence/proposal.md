# AetherStem Core v0.7: Adaptive Intelligence Layer

## Summary

Introduce the adaptive intelligence layer for AetherStem: artifact-aware reconstruction planning, confidence-gated processing, temporal stability scoring, perceptual analysis, hardware-aware quality scaling, deterministic graph descriptors, adaptive memory/scheduling plans, and reproducible benchmark corpus primitives.

## Motivation

v0.6 can run forensic reconstruction graphs, but graph selection is still mostly static and does not yet treat weak hardware, perceptual danger, temporal instability, or confidence as first-class inputs. v0.7 makes those signals explicit so future reconstruction stages can adapt without coupling DSP code to backend-specific execution details.

## Scope

This change adds deterministic primitives and contracts for:

- artifact intelligence and heatmaps
- region classification
- confidence gates
- temporal stability reports
- psychoacoustic/perceptual reports
- hardware tier profiling
- quality profile clamping
- backend selection contracts
- adaptive scheduling and memory planning
- runtime graph descriptors and fingerprints
- reproducible degradation benchmark cases

## Non-Goals

This initial slice does not ship large ML models, GPU kernels, Vulkan/DirectML execution, source-separation-based stem reconstruction, or long-form streaming renderers. It establishes the interfaces and deterministic baseline required to build those safely.
