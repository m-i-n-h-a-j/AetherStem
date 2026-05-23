# CLI Help and AI Guidance

AetherStem includes a self-documenting CLI guidance layer in `cli/help/`.

Human-facing commands:

```bash
aetherstem help
aetherstem help separate
aetherstem help runtime
aetherstem guide separate
aetherstem troubleshoot
aetherstem config-info ai
aetherstem model-registry
```

AI-agent metadata:

```bash
aetherstem ai-metadata
```

The metadata output is deterministic JSON with commands, options, examples, workflow recipes, diagnostics guidance, and project conventions. It is intended for Codex, Claude, Cursor, Antigravity, OpenHands, and similar external coding agents.

Guidance commands do not execute audio processing, load model weights, or create runtime sessions.

