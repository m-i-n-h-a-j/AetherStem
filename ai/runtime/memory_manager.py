from __future__ import annotations


class MemoryManager:
    def estimate_audio_mb(self, channels: int, samples: int, bytes_per_sample: int = 4, multiplier: float = 6.0) -> float:
        return channels * samples * bytes_per_sample * multiplier / (1024 * 1024)

    def safe_batch_size(self, estimated_chunk_mb: float, available_mb: float | None, low_memory: bool = False) -> int:
        if low_memory or not available_mb or estimated_chunk_mb <= 0:
            return 1
        return max(1, int((available_mb * 0.65) // estimated_chunk_mb))

