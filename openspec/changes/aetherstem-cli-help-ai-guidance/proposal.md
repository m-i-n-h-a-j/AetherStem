## Why

AetherStem has grown from deterministic DSP analysis into a runtime-oriented AI audio platform. The CLI now exposes analysis, restoration, separation, presets, batch processing, benchmarking, runtime diagnostics, and model runtime settings. As the command surface expands, users and external AI coding agents need discoverable, structured guidance without hunting through docs or source code.

This change adds a production-grade help, onboarding, diagnostics, and AI-guidance layer for the CLI. It serves both human users and external agents such as Codex, Claude, Cursor, Antigravity, and OpenHands by providing contextual help, examples, workflows, config introspection, runtime troubleshooting, and machine-readable command metadata.

## What Changes

- Add `cli/help/` package with command registry, examples, workflows, diagnostics, metadata export, search, and rendering helpers.
- Add contextual help commands:
  - `aetherstem help`
  - `aetherstem help separate`
  - `aetherstem help runtime`
  - `aetherstem help benchmark`
- Add interactive command discovery and guided workflow recommendations.
- Add AI-readable command metadata export for external coding agents and tool runners.
- Add config/schema introspection commands.
- Add runtime troubleshooting guidance that reuses existing runtime diagnostics and model/runtime metadata.
- Add example generation for common workflows and backend/device combinations.
- Add structured developer documentation generation support.

## Capabilities

### New Capabilities

- `cli-help`: contextual help registry, command-specific examples, workflow recommendations, runtime-aware help, and formatted rendering.
- `cli-agent-metadata`: machine-readable command metadata and integration hints for external AI agents.
- `cli-guidance`: guided workflow suggestions for analysis, separation, restore, denoise, enhance, batch, benchmark, runtime diagnostics, and model setup.
- `cli-troubleshooting`: runtime troubleshooting assistant for missing dependencies, unavailable providers, missing models, cache failures, unsupported precision, and common configuration issues.
- `cli-config-introspection`: config/schema inspection for runtime, AI, paths, audio, and pipeline settings.
- `cli-doc-generation`: structured developer documentation generation from registered command metadata.

## Impact

The CLI should become self-documenting while preserving the current modular architecture. Help/guidance code must not run DSP analysis, load models, initialize heavyweight backends unnecessarily, or alter runtime behavior. It may read configuration and lightweight diagnostics, and it may call existing diagnostics functions that are safe without optional runtime dependencies.

## Non-Goals

- No GUI.
- No network-dependent AI assistant.
- No LLM inference inside AetherStem.
- No replacement for Typer's built-in `--help`.
- No changes to runtime adapter responsibilities.
