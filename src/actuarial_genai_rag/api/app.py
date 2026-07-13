"""FastAPI application for the actuarial chatbot."""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from actuarial_genai_rag.api.schemas import ChatRequest, ChatResponse
from actuarial_genai_rag.generation.llm import generate_answer

logger = logging.getLogger(__name__)

app = FastAPI(title="Actuarial GenAI RAG", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        answer = generate_answer(question=request.question)
    except Exception as e:
        logger.exception("LLM call failed")
        raise HTTPException(
            status_code=503,
            detail=f"LLM indisponible. Vérifiez qu'Ollama est lancé avec le modèle chargé. ({e})",
        ) from e
    return ChatResponse(answer=answer, sources=[])
