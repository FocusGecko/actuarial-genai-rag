# actuarial-genai-rag

A Retrieval-Augmented Generation (RAG) system applied to the actuarial sector.
The system enables question-answering over actuarial documents (theses, standards, technical notes)
using semantic search combined with a large language model.

## Project structure

```
.
├── Data/                  # Raw actuarial documents (PDF, DOCX, XLSX)
├── notebooks/             # EDA and experimentation notebooks
│   ├── 01_eda_corpus.ipynb        # Corpus exploration
│   ├── 02_eda_chunks.ipynb        # Chunking analysis
│   └── 03_eda_embeddings.ipynb    # Embedding space visualisation
├── src/
│   ├── ingestion/         # Document loading & chunking
│   ├── retrieval/         # Embedding & vector store (ChromaDB)
│   ├── generation/        # LLM prompting (Anthropic Claude)
│   └── pipeline/          # End-to-end RAG orchestration
├── tests/
├── pyproject.toml         # uv-managed dependencies
└── .env.example
```

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
make install
cp .env.example .env   # then fill in your API keys
```

## Ingestion

Run the ingestion pipeline to chunk, embed, and store documents in ChromaDB:

```bash
make ingest
```

This uses `config/ingestion.yaml` for all parameters (chunk size, overlap, embedding model, etc.).
To use a custom config:

```bash
uv run python -m actuarial_genai_rag.pipeline.ingest config/my_config.yaml
```

## Roadmap

- [ ] EDA: corpus statistics (document count, language, length distribution)
- [ ] EDA: chunking strategy evaluation
- [ ] EDA: embedding space visualisation (UMAP)
- [ ] Ingestion pipeline (PDF → chunks → ChromaDB)
- [ ] Retrieval evaluation (recall@k)
- [ ] Generation with Claude + actuarial prompt
- [ ] End-to-end evaluation
