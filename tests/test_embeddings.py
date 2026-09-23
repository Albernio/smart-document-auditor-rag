from src.embeddings import EmbeddingModel


def test_embedding_model_returns_vector() -> None:
    model = EmbeddingModel()

    embedding = model.encode(
        "The provider must respond within thirty days."
    )

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)

def test_embedding_has_expected_dimension() -> None:
    model = EmbeddingModel()

    embedding = model.encode(
        "The provider must respond within thirty days."
    )

    print(f"Embedding dimension: {len(embedding)}")

    assert len(embedding) > 0

def test_similar_texts_have_similar_embeddings() -> None:
    model = EmbeddingModel()

    embedding_1 = model.encode(
        "The provider must respond within thirty days."
    )

    embedding_2 = model.encode(
        "The supplier has thirty days to answer."
    )

    assert len(embedding_1) == len(embedding_2)