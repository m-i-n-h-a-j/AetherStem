# Model Registry

AetherStem v0.5 adds manifest-driven model lifecycle infrastructure under `ai/models/registry/`.

Manifests describe model identity, task, architecture, supported backends, supported precisions, sample rate, channels, stems, tensor signatures, model format, and checksum metadata. Discovery is local and deterministic by default.

Default manifest directory:

```text
ai/models/registry/manifests/
```

The resolver filters candidates by task, backend, precision, sample rate, channels, and stems. It returns metadata and cache paths without loading model weights or importing heavy runtime packages.

Cache checks are handled separately by `ModelCache` and `ModelLifecycleManager`, including missing asset and checksum diagnostics.

