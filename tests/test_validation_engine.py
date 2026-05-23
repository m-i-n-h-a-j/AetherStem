import numpy as np

from ai.validation.quality_comparator import QualityComparator


def test_quality_comparator_rejects_new_clipping():
    audio = np.array([0.0, 1.0, -1.0], dtype=np.float32)
    report = QualityComparator().compare(None, audio)

    assert report["accepted"] is False
    assert report["reasons"]

