"""Vector store interface using ChromaDB."""

import chromadb
import numpy as np

from actuarial_genai_rag.ingestion.chunker import Chunk
from actuarial_genai_rag.ingestion.config import VectorStoreConfig


class ChromaStore:
    """ChromaDB vector store for document chunks."""

    def __init__(self, config: VectorStoreConfig):
        self.config = config
        self.client = chromadb.PersistentClient(path=config.persist_directory)

        if config.recreate:
            try:
                self.client.delete_collection(config.collection_name)
            except (ValueError, chromadb.errors.NotFoundError):
                pass

        self.collection = self.client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": config.distance},
        )

    def upsert_batch(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
        start_id: int = 0,
    ) -> None:
        """Upsert a batch of chunks with their embeddings."""
        ids = [f"chunk_{start_id + i}" for i in range(len(chunks))]
        documents = [c.text for c in chunks]
        metadatas = [{k: str(v) for k, v in c.metadata.items()} for c in chunks]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[dict]:
        """Search for similar chunks."""
        kwargs: dict = {
            "query_embeddings": [query_embedding.tolist()],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)

        return [
            {
                "text": doc,
                "metadata": meta,
                "distance": dist,
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    @property
    def count(self) -> int:
        """Return the number of items in the collection."""
        return self.collection.count()
