"""Configuration model for the ingestion pipeline."""

from pathlib import Path

import yaml
from pydantic import BaseModel


class DataConfig(BaseModel):
    parquet_path: str
    text_field: str
    metadata_fields: list[str]
    max_docs: int | None = None


class ChunkingConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 64
    min_chunk_size: int = 50
    separators: list[str] = ["\n\n", "\n", ". ", " "]


class EmbeddingConfig(BaseModel):
    model_name: str = "intfloat/multilingual-e5-base"
    batch_size: int = 32
    device: str = "mps"
    prefix_passage: str = "passage: "
    prefix_query: str = "query: "


class VectorStoreConfig(BaseModel):
    collection_name: str = "actuarial_abstracts"
    persist_directory: str = "data/chromadb"
    distance: str = "cosine"
    recreate: bool = True


class IngestionConfig(BaseModel):
    data: DataConfig
    chunking: ChunkingConfig
    embedding: EmbeddingConfig
    vector_store: VectorStoreConfig


def load_config(config_path: str | Path) -> IngestionConfig:
    """Load ingestion configuration from a YAML file."""
    config_path = Path(config_path)
    with open(config_path) as f:
        raw = yaml.safe_load(f)
    return IngestionConfig(**raw)
