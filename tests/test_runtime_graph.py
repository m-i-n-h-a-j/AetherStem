from pathlib import Path
from types import SimpleNamespace

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


def test_graph_separation_upgrades_legacy_demucs_placeholder_for_onnx(tmp_path):
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
            "backend": "onnx",
            "device": "cpu",
            "models": {"separate": "demucs-placeholder"},
            "chunk_size": 32,
            "overlap": 0.25,
        },
    )

    stage = result["stages"]["separate"]
    assert stage["model"] == "demucs-runtime"
    assert set(stage["stems"]) == {"vocals", "drums", "bass", "other"}


def test_separate_workflow_does_not_auto_run_torch_only_restoration_stages(tmp_path):
    samples = np.vstack([
        np.linspace(-0.5, 0.5, 96, dtype=np.float32),
        np.linspace(0.5, -0.5, 96, dtype=np.float32),
    ])
    input_path = tmp_path / "song.wav"
    input_path.write_bytes(b"placeholder")

    result = AudioGraph(output_root=tmp_path / "exports").execute(
        samples,
        sample_rate=48,
        analysis=SimpleNamespace(noise_floor_db=-10.0, clipping_count=5),
        quality=SimpleNamespace(is_transcoded=True, confidence=1.0),
        workflow="separate",
        input_path=input_path,
        force=["separate"],
        config={
            "backend": "onnx",
            "device": "cpu",
            "chunk_size": 32,
            "overlap": 0.25,
        },
    )

    assert set(result["stages"]) == {"separate", "validate", "export"}
