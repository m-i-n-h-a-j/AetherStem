from __future__ import annotations

import numpy as np


def ensure_stereo_channels_first(samples: np.ndarray) -> np.ndarray:
    array = np.asarray(samples, dtype=np.float32)
    if array.ndim == 1:
        return np.vstack([array, array])
    if array.shape[0] == 1:
        return np.vstack([array[0], array[0]])
    if array.shape[0] >= 2:
        return array[:2]
    if array.shape[-1] >= 2:
        return array.T[:2]
    raise ValueError("Unable to normalize audio to stereo channels-first layout.")


def deterministic_stem_projection(chunk: np.ndarray, stems: list[str]) -> dict[str, np.ndarray]:
    stereo = ensure_stereo_channels_first(chunk)
    mid = ((stereo[0] + stereo[1]) * 0.5).reshape(1, -1)
    side = ((stereo[0] - stereo[1]) * 0.5).reshape(1, -1)
    mono_mid = np.vstack([mid[0], mid[0]])
    stereo_side = np.vstack([side[0], -side[0]])
    outputs: dict[str, np.ndarray] = {}
    for stem in stems:
        if stem == "vocals":
            outputs[stem] = mono_mid.astype(np.float32)
        elif stem == "drums":
            outputs[stem] = (stereo - mono_mid).astype(np.float32) * 0.35
        elif stem == "bass":
            outputs[stem] = (mono_mid * 0.25).astype(np.float32)
        elif stem == "instrumental":
            outputs[stem] = (stereo - mono_mid).astype(np.float32)
        else:
            outputs[stem] = stereo_side.astype(np.float32)
    return outputs

