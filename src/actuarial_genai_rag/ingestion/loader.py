"""Document loaders for actuarial documents (PDF, DOCX, XLSX)."""

from pathlib import Path


def load_document(path: str | Path) -> str:
    """Load a document and return its raw text content."""
    raise NotImplementedError
