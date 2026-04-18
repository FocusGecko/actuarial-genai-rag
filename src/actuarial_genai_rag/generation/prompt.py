"""Prompt templates for the actuarial RAG system."""

RAG_SYSTEM_PROMPT = """You are an expert actuarial assistant. Answer the user's question
using only the provided context excerpts from actuarial documents.
If the answer cannot be found in the context, say so explicitly."""

RAG_USER_TEMPLATE = """Context:
{context}

Question: {question}"""
