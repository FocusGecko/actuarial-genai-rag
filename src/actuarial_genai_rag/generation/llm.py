"""LLM client using OpenAI-compatible API (Ollama local)."""

from pathlib import Path

import yaml
from openai import OpenAI
from pydantic import BaseModel

from actuarial_genai_rag.generation.prompt import (
    NAIVE_SYSTEM_PROMPT,
    RAG_SYSTEM_PROMPT,
    RAG_USER_TEMPLATE,
)

CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "generation.yaml"


class LLMConfig(BaseModel):
    model: str = "mistral-nemo"
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "ollama"


def load_llm_config(config_path: Path = CONFIG_PATH) -> LLMConfig:
    """Load LLM configuration from a YAML file."""
    with open(config_path) as f:
        raw = yaml.safe_load(f)
    return LLMConfig(**raw.get("llm", {}))


def _get_client(config: LLMConfig) -> OpenAI:
    """Return an OpenAI client from config."""
    return OpenAI(base_url=config.base_url, api_key=config.api_key)


def generate_answer(question: str, context: list[str] | None = None) -> str:
    """Generate an answer, optionally grounded in retrieved context chunks."""
    config = load_llm_config()
    client = _get_client(config)

    if context:
        system_prompt = RAG_SYSTEM_PROMPT
        user_content = RAG_USER_TEMPLATE.format(
            context="\n\n---\n\n".join(context),
            question=question,
        )
    else:
        system_prompt = NAIVE_SYSTEM_PROMPT
        user_content = question

    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )
    return response.choices[0].message.content or ""
