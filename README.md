# actuarial-genai-rag

A Retrieval-Augmented Generation (RAG) system applied to the actuarial sector.
The system enables question-answering over actuarial documents (theses, standards, technical notes)
using semantic search combined with a large language model.

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com/).

```bash
make install
brew install ollama && ollama pull mistral-nemo

# Terminal 1 — backend
make serve

# Terminal 2 — frontend
make front
```

Open `http://localhost:8080` and start chatting.

## Development

```bash
make test         # Run tests
make lint         # Ruff linting
make format       # Ruff formatting
make typecheck    # MyPy type checking
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

- [x] Ingestion pipeline (Parquet → chunks → ChromaDB)
- [x] API backend (FastAPI + Ollama)
- [x] Frontend chat (Chainlit)
- [ ] RAG: connect vector store to LLM
- [ ] Streaming responses
- [ ] Source display in chat UI
