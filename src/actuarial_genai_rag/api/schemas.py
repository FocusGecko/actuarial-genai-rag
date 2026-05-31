"""Request/response models for the chat API."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    title: str
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []
