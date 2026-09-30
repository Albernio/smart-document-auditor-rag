from unittest.mock import Mock

from src.llm.ollama_client import OllamaClient
    
def test_ollama_client_returns_generated_text() -> None:
    ollama_client = Mock()

    ollama_client.chat.return_value = {
        "message": {
            "content": "The provider has thirty days to respond."
        }
    }

    client = OllamaClient(
        model_name="qwen3:8b",
        client=ollama_client,
    )

    result = client.generate(
        "How many days does the provider have to respond?"
    )

    assert result == "The provider has thirty days to respond."


def test_ollama_client_sends_prompt_to_ollama() -> None:
    ollama_client = Mock()

    ollama_client.chat.return_value = {
        "message": {
            "content": "The provider has thirty days to respond."
        }
    }

    client = OllamaClient(
        model_name="qwen3:8b",
        client=ollama_client,
    )

    prompt = "How many days does the provider have to respond?"

    client.generate(prompt)

    ollama_client.chat.assert_called_once_with(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )