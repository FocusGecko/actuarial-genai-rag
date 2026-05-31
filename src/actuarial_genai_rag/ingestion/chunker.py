"""Text chunking strategies for RAG ingestion."""

from dataclasses import dataclass, field

from actuarial_genai_rag.ingestion.config import ChunkingConfig
from actuarial_genai_rag.ingestion.loader import Document


@dataclass
class Chunk:
    """A text chunk with inherited metadata from its parent document."""

    text: str
    metadata: dict[str, str | int | float] = field(default_factory=dict)


def _recursive_split(text: str, separators: list[str], chunk_size: int) -> list[str]:
    """Recursively split text using a hierarchy of separators."""
    if len(text) <= chunk_size:
        return [text]

    # Try each separator in order
    for i, sep in enumerate(separators):
        if sep in text:
            parts = text.split(sep)
            result = []
            current = ""
            for part in parts:
                candidate = current + sep + part if current else part
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        result.append(current)
                    # If the part itself is too large, recurse with next separator
                    if len(part) > chunk_size and i + 1 < len(separators):
                        result.extend(_recursive_split(part, separators[i + 1 :], chunk_size))
                    else:
                        current = part
            if current:
                result.append(current)
            return result

    # Fallback: hard split by chunk_size
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def chunk_text(text: str, config: ChunkingConfig) -> list[str]:
    """Split text into overlapping chunks using recursive character splitting."""
    raw_chunks = _recursive_split(text, config.separators, config.chunk_size)

    # Apply overlap between consecutive chunks
    chunks_with_overlap = []
    for i, chunk in enumerate(raw_chunks):
        if i > 0 and config.chunk_overlap > 0:
            # Prepend the tail of the previous chunk as overlap
            prev_tail = raw_chunks[i - 1][-config.chunk_overlap :]
            chunk = prev_tail + chunk

        if len(chunk) >= config.min_chunk_size:
            chunks_with_overlap.append(chunk)

    return chunks_with_overlap


def chunk_documents(documents: list[Document], config: ChunkingConfig) -> list[Chunk]:
    """Chunk a list of documents, preserving metadata on each chunk."""
    all_chunks = []
    for doc in documents:
        text_chunks = chunk_text(doc.text, config)
        for i, text in enumerate(text_chunks):
            chunk_metadata = {**doc.metadata, "chunk_index": i}
            all_chunks.append(Chunk(text=text, metadata=chunk_metadata))
    return all_chunks
