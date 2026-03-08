from unittest.mock import patch, MagicMock
from app.gpt import init_ai_client

## --- Tests for init_ai_client ---


@patch("app.gpt.load_dotenv")  # Mock load_dotenv so it doesn't look for real files
@patch("app.gpt.os.getenv")  # Mock os.getenv to control the API key value
@patch("app.gpt.OpenAI")  # Mock the OpenAI class itself
def test_init_ai_client_success(mock_openai_class, mock_getenv, mock_load):
    """Test that the client initializes correctly when an API key is present."""

    # 1. Setup the mock return values
    mock_getenv.return_value = "sk-test-key-12345"
    mock_instance = MagicMock()
    mock_openai_class.return_value = mock_instance

    # 2. Call the function
    client = init_ai_client()

    # 3. Assertions
    # Verify load_dotenv was called
    mock_load.assert_called_once()

    # Verify os.getenv looked for the correct variable name
    mock_getenv.assert_called_with("OPENAI_API_KEY")

    # Verify OpenAI was instantiated with the key we provided
    mock_openai_class.assert_called_once_with(api_key="sk-test-key-12345")

    # Verify the function returned our mocked client
    assert client == mock_instance


@patch("app.gpt.os.getenv")
@patch("app.gpt.OpenAI")
def test_init_ai_client_missing_key(mock_openai_class, mock_getenv):
    """Test behavior when the environment variable is missing."""

    # Setup: os.getenv returns None
    mock_getenv.return_value = None

    # Run
    client = init_ai_client()

    # Verify: It still tries to initialize, but with None
    mock_openai_class.assert_called_once_with(api_key=None)
    assert client is not None
