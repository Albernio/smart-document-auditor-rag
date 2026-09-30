from src.llm.ollama_client import OllamaClient


def test_ollama_generates_real_response() -> None:
    client = OllamaClient(
        model_name="qwen3:8b",
    )

    result = client.generate(
        "Answer with exactly one sentence: "
        "How many days are in a week?"
    )

    assert isinstance(result, str)
    assert result.strip()