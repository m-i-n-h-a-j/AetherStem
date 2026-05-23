from ai.models.registry import default_registry


def test_registry_lists_metadata_without_loading_models():
    names = default_registry.names()

    assert "denoise-placeholder" in names
    assert "demucs-placeholder" in names


def test_registry_filters_by_capability():
    denoise_models = default_registry.find(denoise=True)

    assert [model.name for model in denoise_models] == ["denoise-placeholder"]


def test_registry_rejects_incompatible_backend():
    compatibility = default_registry.compatibility("mdx-placeholder", backend="torch", device="cpu")

    assert compatibility.compatible is False
    assert "onnx" in compatibility.reason

