from ai.models._placeholder import PassthroughModel
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements


class DenoisePlaceholderModel(PassthroughModel):
    metadata = ModelMetadata(
        name="denoise-placeholder",
        version="0.3.0",
        family="denoise",
        description="DeepFilterNet/RNNoise-style denoise placeholder adapter.",
        capabilities=ModelCapabilities(denoise=True),
        requirements=ModelRequirements(backends=["torch"], devices=["cpu", "cuda"]),
    )

