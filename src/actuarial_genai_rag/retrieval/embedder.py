"""Embedding model wrapper using sentence-transformers."""

import numpy as np
from sentence_transformers import SentenceTransformer

from actuarial_genai_rag.ingestion.config import EmbeddingConfig


class Embedder:
    """Wraps a sentence-transformers model for encoding text."""

    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.model = SentenceTransformer(config.model_name, device=config.device)

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        """Embed document/passage texts (adds passage prefix for E5 models)."""
        prefixed = [self.config.prefix_passage + t for t in texts]
        return self.model.encode(
            prefixed,
            batch_size=self.config.batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
        )

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query (adds query prefix for E5 models)."""
        prefixed = self.config.prefix_query + query
        return self.model.encode(
            [prefixed],
            normalize_embeddings=True,
        )[0]
