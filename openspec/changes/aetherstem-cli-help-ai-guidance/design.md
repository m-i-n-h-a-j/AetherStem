## Context

The current CLI is implemented with Typer in `cli/main.py`. Runtime diagnostics already exist, and v0.4/v0.5 runtime work adds backend, model registry, telemetry, profiling, and configuration surfaces. The help system should sit above those modules and describe them; it should not become part of orchestration or runtime execution.

## Proposed Package Layout

```text
cli/
  help/
    __init__.py
    registry.py
    formatter.py
    examples.py
    workflows.py
    diagnostics.py
    metadata.py
    search.py
    rendering/
      __init__.py
      rich_renderer.py
```

## Command Registry

The help registry stores command metadata:

- command name;
- category;
- summary;
- detailed description;
- usage;
- options;
- examples;
- related commands;
- machine-readable notes;
- troubleshooting references.

Metadata should be plain Python data so it can be rendered for humans or exported as JSON for AI agents.

## Human Help Rendering

Human output should use Rich tables/panels when available through the existing CLI dependency set. It should support:

- command list overview;
- single command details;
- topic aliases such as `runtime`, `models`, `config`, `benchmark`;
- examples;
- recommended next commands.

## AI Metadata Export

AI metadata should be deterministic JSON with:

- CLI command list;
- stable command names;
- argument and option summaries;
- examples;
- workflow recipes;
- diagnostics guidance;
- file/directory conventions;
- runtime/model setup notes.

External agents should be able to consume the JSON without scraping terminal formatting.

## Guided Workflows

Workflow guidance maps user intent to commands:

- inspect/analyze file;
- separate stems;
- restore damaged audio;
- denoise speech/music;
- enhance lossy audio;
- process a folder;
- benchmark runtime;
- diagnose runtime/model setup.

Guidance should include examples and caveats, but should not execute workflows automatically.

## Diagnostics Guidance

Troubleshooting should combine static guidance with lightweight runtime status:

- missing ONNX Runtime;
- missing Torch;
- unavailable CUDA;
- no configured model path;
- missing model cache;
- unsupported precision;
- corrupt cache/checksum;
- output directory/report location confusion.

## Config Introspection

The CLI should expose config sections and current values in both human and JSON forms. This helps users and agents see which backend, device, chunk, model, path, and validation settings are active.

## Risks / Trade-offs

- **Help drift**: centralize command metadata to reduce duplication.
- **Over-eager diagnostics**: avoid importing heavyweight runtime dependencies beyond safe availability checks.
- **Agent compatibility**: keep JSON stable and explicit.
- **CLI conflict**: add a `help` command while preserving Typer's native `--help`.
