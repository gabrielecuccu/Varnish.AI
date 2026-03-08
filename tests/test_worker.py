import pytest
from unittest.mock import MagicMock
from openai import APIConnectionError
from app.worker import Worker

## --- Mocks for the Stream ---


class MockEvent:
    def __init__(self, delta):
        self.type = "response.output_text.delta"
        self.delta = delta


@pytest.fixture
def mock_client():
    """Creates a mock OpenAI client that supports the stream context manager."""
    client = MagicMock()
    # Mocking the context manager: client.responses.stream(...) as stream
    stream_mock = MagicMock()
    client.responses.stream.return_value.__enter__.return_value = stream_mock
    return client, stream_mock


## --- Tests ---


def test_worker_emits_partial_and_finished(qtbot, mock_client):
    client, stream_mock = mock_client

    # 1. Setup the stream to yield a few "chunks" of text
    stream_mock.__iter__.return_value = [
        MockEvent("Hello "),
        MockEvent("Varnish"),
        MockEvent("!"),
    ]

    worker = Worker(client, "You are a polisher", "Fix this text")

    # 2. Use qtbot to listen for signals
    captured_deltas = []
    worker.partial.connect(lambda d: captured_deltas.append(d))

    with qtbot.waitSignal(worker.finished, timeout=1000):
        worker.run()

    # 3. Assertions
    assert captured_deltas == ["Hello ", "Varnish", "!"]
    client.responses.stream.assert_called_once()


def test_worker_handles_connection_error(qtbot, mock_client):
    client, _ = mock_client

    # 1. Setup the stream to raise a Connection Error immediately
    client.responses.stream.side_effect = APIConnectionError(request=MagicMock())

    worker = Worker(client, "Prompt", "Message")

    # 2. Catch the error signal
    # Signal format: error.emit(title, message, is_critical)
    with qtbot.waitSignal(worker.error, timeout=1000) as blocker:
        worker.run()

    # 3. Verify signal arguments
    title, msg, critical = blocker.args
    assert title == "Error"
    assert "Connection error" in msg
    assert critical is False


def test_worker_handles_unexpected_exception(qtbot, mock_client):
    client, _ = mock_client

    # 1. Simulate a generic crash
    client.responses.stream.side_effect = Exception("Boom!")

    worker = Worker(client, "Prompt", "Message")

    with qtbot.waitSignal(worker.error, timeout=1000) as blocker:
        worker.run()

    assert "Unexpected error: Boom!" in blocker.args[1]
