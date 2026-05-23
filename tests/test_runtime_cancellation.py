import pytest

from ai.runtime.cancellation import CancelledError, CancellationToken


def test_cancellation_token_raises_structured_error():
    token = CancellationToken()
    token.cancel()

    with pytest.raises(CancelledError):
        token.throw_if_cancelled()

