from pathlib import Path
from audio_io.audio_inspector import inspect_audio
from models.audio_metadata import AudioMetadata

class InspectStage:
    def execute(self, input_path: Path) -> AudioMetadata:
        metadata_dict = inspect_audio(input_path)
        # Add filesize if missing
        if "filesize_bytes" not in metadata_dict:
            metadata_dict["filesize_bytes"] = input_path.stat().st_size
        return AudioMetadata(**metadata_dict)
