"""End-to-end ingestion pipeline: load → chunk → embed → store."""

from pathlib import Path

import numpy as np
from rich.console import Console
from tqdm import tqdm

from actuarial_genai_rag.ingestion.chunker import chunk_documents
from actuarial_genai_rag.ingestion.config import load_config
from actuarial_genai_rag.ingestion.loader import load_parquet
from actuarial_genai_rag.retrieval.embedder import Embedder
from actuarial_genai_rag.retrieval.vector_store import ChromaStore

console = Console()


def run_ingestion(config_path: str | Path = "config/ingestion.yaml") -> None:
    """Run the full ingestion pipeline."""
    console.print(f"[bold blue]Loading config from {config_path}[/]")
    config = load_config(config_path)

    # 1. Load documents
    console.print("[bold green]Step 1/4:[/] Loading documents...")
    documents = load_parquet(config.data)
    console.print(f"  Loaded {len(documents)} documents")

    # 2. Chunk documents
    console.print("[bold green]Step 2/4:[/] Chunking documents...")
    chunks = chunk_documents(documents, config.chunking)
    console.print(f"  Created {len(chunks)} chunks")

    # 3. Embed chunks
    console.print("[bold green]Step 3/4:[/] Embedding chunks...")
    embedder = Embedder(config.embedding)
    batch_size = config.embedding.batch_size
    all_texts = [c.text for c in chunks]

    embeddings_list = []
    for i in tqdm(range(0, len(all_texts), batch_size), desc="Embedding"):
        batch = all_texts[i : i + batch_size]
        batch_embeddings = embedder.embed_documents(batch)
        embeddings_list.append(batch_embeddings)

    embeddings = np.vstack(embeddings_list)
    console.print(f"  Embeddings shape: {embeddings.shape}")

    # 4. Store in ChromaDB
    console.print("[bold green]Step 4/4:[/] Storing in ChromaDB...")
    store = ChromaStore(config.vector_store)

    # Upsert in batches to avoid memory issues
    upsert_batch_size = 500
    for i in tqdm(range(0, len(chunks), upsert_batch_size), desc="Upserting"):
        batch_chunks = chunks[i : i + upsert_batch_size]
        batch_embeddings = embeddings[i : i + upsert_batch_size]
        store.upsert_batch(batch_chunks, batch_embeddings, start_id=i)

    console.print(
        f"[bold green]Done![/] {store.count} vectors stored in "
        f"collection '{config.vector_store.collection_name}'"
    )


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "config/ingestion.yaml"
    run_ingestion(path)
