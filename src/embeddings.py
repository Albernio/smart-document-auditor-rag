from sentence_transformers import SentenceTransformer

from src.models import Chunk, Embedding

class EmbeddingModel:
    """Generate vector embeddings for the text"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def encode(self, text:str) -> list[float]:
        """Generate embedding for a single text."""

        embedding = self.model.encode(text)

        return embedding.tolist()

    def encode_chunks(self, chunks: list[Chunk]) -> list[Embedding]:
        """Generate embeddings for multiple chunks."""

        if not chunks:
            return []

        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(texts)

        return [
            Embedding(
                vector=vector.tolist(),
                dimension=len(vector),
            )
            for vector in embeddings
        ]