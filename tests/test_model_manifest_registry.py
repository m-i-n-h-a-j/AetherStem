from pathlib import Path

from ai.models.registry.discovery import ManifestDiscovery
from ai.models.registry.resolver import ModelResolver
from ai.models.registry.validation import manifest_from_dict, validate_semver


def test_manifest_validation_and_semver():
    manifest = manifest_from_dict(
        {
            "id": "test-model",
            "version": "1.2.3",
            "architecture": "demucs-compatible",
            "task": "separate",
            "supported_backends": ["onnx"],
            "supported_precisions": ["fp32"],
            "sample_rate": 44100,
            "channels": 2,
            "stems": ["vocals", "other"],
            "model_format": "onnx",
        }
    )

    assert validate_semver(manifest.version)
    assert manifest.id == "test-model"


def test_manifest_discovery_and_resolution_are_deterministic(tmp_path):
    manifest_path = tmp_path / "model.yaml"
    manifest_path.write_text(
        """
id: test-demucs
version: 1.0.0
architecture: demucs-compatible
task: separate
supported_backends: [onnx]
supported_precisions: [fp32]
sample_rate: 44100
channels: 2
stems: [vocals, drums, bass, other]
sha256: ""
model_format: onnx
"""
    )

    manifests, errors = ManifestDiscovery([tmp_path]).discover()
    resolved = ModelResolver(manifests).resolve(task="separate", backend="onnx", precision="fp32", channels=2)

    assert errors == []
    assert [manifest.id for manifest in manifests] == ["test-demucs"]
    assert resolved.manifest.id == "test-demucs"

