from pathlib import Path

import numpy as np

from ai.orchestration.graph import AudioGraph


def test_graph_separation_uses_runtime_adapter_and_exports_stems(tmp_path):
    samples = np.vstack([
        np.linspace(-0.5, 0.5, 96, dtype=np.float32),
        np.linspace(0.5, -0.5, 96, dtype=np.float32),
    ])
    input_path = tmp_path / "song.wav"
    input_path.write_bytes(b"placeholder")

    result = AudioGraph(output_root=tmp_path / "exports").execute(
        samples,
        sample_rate=48,
        analysis=None,
        quality=None,
        workflow="separate",
        input_path=input_path,
        force=["separate"],
        config={
            "models": {"separate": "demucs-runtime"},
            "chunk_size": 32,
            "overlap": 0.25,
            "low_memory": True,
        },
    )

    stems = result["stages"]["separate"]["stems"]
    assert set(stems) == {"vocals", "drums", "bass", "other"}
    for path in stems.values():
        assert Path(path).exists()
    assert Path(result["manifest"]).exists()

