"""Vector store interface (ChromaDB backend)."""


def build_index(chunks: list[str], embeddings: list[list[float]]) -> None:
    """Persist chunks and their embeddings to the vector store."""
    raise NotImplementedError


def search(query_embedding: list[float], top_k: int = 5) -> list[str]:
    """Return the top-k most similar chunks for a query embedding."""
    raise NotImplementedError
