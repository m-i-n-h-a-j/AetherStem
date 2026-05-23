from ai.models._placeholder import StemPassthroughModel
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements


class DemucsPlaceholderModel(StemPassthroughModel):
    metadata = ModelMetadata(
        name="demucs-placeholder",
        version="0.3.0",
        family="demucs",
        description="Demucs-compatible placeholder adapter with lazy real-runtime boundary.",
        capabilities=ModelCapabilities(separate=True, stems=["vocals", "drums", "bass", "other", "instrumental"]),
        requirements=ModelRequirements(backends=["torch"], devices=["cpu", "cuda"], dependencies=["demucs"]),
    )

