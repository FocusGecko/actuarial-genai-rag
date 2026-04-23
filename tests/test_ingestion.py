import pytest

from actuarial_genai_rag.ingestion.chunker import chunk_text


def test_chunk_text_not_implemented():
    with pytest.raises(NotImplementedError):
        chunk_text("some text")
