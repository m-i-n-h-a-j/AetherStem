# Streaming Pipeline

The v0.4 streaming path is generator-based low-memory inference, not realtime microphone capture.

`StreamPipeline` can:

- emit scheduled chunks from an `AudioBuffer`;
- process chunks incrementally;
- report progress after each chunk;
- honor cancellation between chunks;
- reconstruct output without keeping unnecessary intermediate state.

This API prepares the runtime for future realtime processing without adding realtime guarantees in v0.4.

