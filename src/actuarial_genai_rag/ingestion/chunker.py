"""Text chunking strategies for RAG ingestion."""


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks."""
    raise NotImplementedError
