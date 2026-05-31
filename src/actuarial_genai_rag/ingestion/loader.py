"""Document loader: reads parquet and produces Document objects."""

from dataclasses import dataclass, field

import pandas as pd

from actuarial_genai_rag.ingestion.config import DataConfig


@dataclass
class Document:
    """A loaded document with its text content and metadata."""

    text: str
    metadata: dict[str, str | int | float] = field(default_factory=dict)


def load_parquet(config: DataConfig) -> list[Document]:
    """Load documents from a parquet file.

    Returns a list of Document objects with text and metadata fields.
    """
    df = pd.read_parquet(config.parquet_path)

    if config.text_field not in df.columns:
        raise ValueError(
            f"Text field '{config.text_field}' not found in parquet. "
            f"Available columns: {list(df.columns)}"
        )

    df = df.dropna(subset=[config.text_field])

    if config.max_docs is not None:
        df = df.head(config.max_docs)

    documents = []
    for _, row in df.iterrows():
        metadata = {}
        for field_name in config.metadata_fields:
            if field_name in df.columns and pd.notna(row[field_name]):
                metadata[field_name] = row[field_name]

        documents.append(
            Document(
                text=str(row[config.text_field]),
                metadata=metadata,
            )
        )

    return documents
