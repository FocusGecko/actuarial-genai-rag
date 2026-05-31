from actuarial_genai_rag.ingestion.chunker import chunk_documents, chunk_text
from actuarial_genai_rag.ingestion.config import ChunkingConfig, load_config
from actuarial_genai_rag.ingestion.loader import Document


class TestChunker:
    def test_short_text_single_chunk(self):
        config = ChunkingConfig(chunk_size=100, chunk_overlap=0, min_chunk_size=5)
        result = chunk_text("This is a short text.", config)
        assert len(result) == 1
        assert result[0] == "This is a short text."

    def test_text_split_into_multiple_chunks(self):
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        config = ChunkingConfig(
            chunk_size=30, chunk_overlap=0, min_chunk_size=5, separators=[". ", " "]
        )
        result = chunk_text(text, config)
        assert len(result) > 1
        for chunk in result:
            assert len(chunk) <= 30 + config.chunk_overlap

    def test_overlap_applied(self):
        text = "AAAA. BBBB. CCCC. DDDD."
        config = ChunkingConfig(
            chunk_size=10, chunk_overlap=4, min_chunk_size=3, separators=[". ", " "]
        )
        result = chunk_text(text, config)
        assert len(result) >= 2

    def test_min_chunk_size_filters_small_chunks(self):
        text = "AB. CDE. FGHIJK."
        config = ChunkingConfig(chunk_size=10, chunk_overlap=0, min_chunk_size=5, separators=[". "])
        result = chunk_text(text, config)
        for chunk in result:
            assert len(chunk) >= 5

    def test_chunk_documents_preserves_metadata(self):
        docs = [
            Document(
                text="Some long enough text here.",
                metadata={"title": "Test", "year": 2024},
            )
        ]
        config = ChunkingConfig(chunk_size=100, chunk_overlap=0, min_chunk_size=5)
        chunks = chunk_documents(docs, config)
        assert len(chunks) == 1
        assert chunks[0].metadata["title"] == "Test"
        assert chunks[0].metadata["year"] == 2024
        assert chunks[0].metadata["chunk_index"] == 0


class TestConfig:
    def test_load_config(self, tmp_path):
        config_content = """
data:
  parquet_path: "data/test.parquet"
  text_field: "content"
  metadata_fields: ["title"]
  max_docs: 10

chunking:
  chunk_size: 256
  chunk_overlap: 32
  min_chunk_size: 20
  separators: ["\\n", " "]

embedding:
  model_name: "intfloat/multilingual-e5-small"
  batch_size: 16
  device: "cpu"
  prefix_passage: "passage: "
  prefix_query: "query: "

vector_store:
  collection_name: "test_collection"
  persist_directory: "data/test_chromadb"
  distance: "cosine"
  recreate: true
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        config = load_config(config_file)
        assert config.data.max_docs == 10
        assert config.chunking.chunk_size == 256
        assert config.embedding.model_name == "intfloat/multilingual-e5-small"
        assert config.vector_store.collection_name == "test_collection"


class TestLoader:
    def test_document_dataclass(self):
        doc = Document(text="hello", metadata={"title": "test"})
        assert doc.text == "hello"
        assert doc.metadata["title"] == "test"
