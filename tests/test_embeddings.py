from src.embeddings import EmbeddingModel
from src.models import Chunk


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

def test_encode_chunks_returns_one_embedding_per_chunk() -> None:
    model = EmbeddingModel()

    chunks = [
        Chunk(
            text= "The provider must respond within thirty days.",
            index = 0,
            document_hash="abc123"
        ),
        Chunk(
            text= "The supplier must protect personal data.",
            index = 1,
            document_hash="abc123"
        )
    ]

    embeddings = model.encode_chunks(chunks)

    assert len(embeddings) == len(chunks)

    for embedding in embeddings:
        assert embedding.dimension == 384
        assert len(embedding.vector) == 384

def test_encode_empty_chunks_returns_empty_list() -> None:
    model = EmbeddingModel()

    embeddings = model.encode_chunks([])

    assert embeddings == []

def test_create_vector_records_preserves_chunk_order() -> None:
    model = EmbeddingModel()

    chunks = [
        Chunk(
            text="The provider must respond within thirty days.",
            index=0,
            document_hash="abc123",
        ),
        Chunk(
            text="The supplier must protect personal data.",
            index=1,
            document_hash="abc123",
        ),
    ]

    records = model.create_vector_records(chunks)

    assert len(records) == len(chunks)

    for record, chunk in zip(records, chunks):
        assert record.chunk == chunk
        assert record.embedding.dimension == 384