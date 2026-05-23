## 1. Help Package

- [ ] 1.1 Add `cli/help/` package structure.
- [ ] 1.2 Implement command metadata dataclasses.
- [ ] 1.3 Implement command registry with all existing user-facing commands.
- [ ] 1.4 Implement topic aliases for runtime, models, config, benchmark, restore, and separate.

## 2. Human Rendering

- [ ] 2.1 Add Rich-based formatter for command overview.
- [ ] 2.2 Add command-specific contextual help rendering.
- [ ] 2.3 Add example rendering.
- [ ] 2.4 Add related command and next-step recommendations.

## 3. AI Metadata Export

- [ ] 3.1 Implement JSON metadata export.
- [ ] 3.2 Include commands, options, examples, workflows, diagnostics, and project conventions.
- [ ] 3.3 Keep output deterministic and stable for external agents.

## 4. Guided Workflows

- [ ] 4.1 Implement workflow recommendation registry.
- [ ] 4.2 Add workflow help for analysis, separation, restoration, denoise, enhance, batch, benchmark, runtime diagnostics, and model setup.
- [ ] 4.3 Add example generation for common backend/device configurations.

## 5. Diagnostics Assistant

- [ ] 5.1 Add runtime troubleshooting guidance.
- [ ] 5.2 Integrate lightweight runtime/backend diagnostics.
- [ ] 5.3 Add model/cache/config troubleshooting messages.
- [ ] 5.4 Support human and JSON output.

## 6. Config Introspection

- [ ] 6.1 Add config section inspection.
- [ ] 6.2 Add JSON config export.
- [ ] 6.3 Add schema-like summaries for audio, pipeline, AI, runtime, and paths.

## 7. CLI Integration

- [ ] 7.1 Add `aetherstem help [topic]`.
- [ ] 7.2 Add AI metadata export command.
- [ ] 7.3 Add workflow guidance command.
- [ ] 7.4 Add troubleshooting command.
- [ ] 7.5 Add config introspection command.

## 8. Tests and Docs

- [ ] 8.1 Add tests for registry metadata.
- [ ] 8.2 Add tests for JSON metadata export.
- [ ] 8.3 Add tests for help search/topic resolution.
- [ ] 8.4 Update README usage.
- [ ] 8.5 Add developer docs for AI-agent integration.
