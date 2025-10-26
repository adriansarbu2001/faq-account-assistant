"""OpenAI embedding client."""

from __future__ import annotations

from openai import OpenAI

from src.core.settings import settings

_client: OpenAI | None = None


def _client_lazy() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def embed_text(texts: list[str]) -> list[list[float]]:
    """
    Return embeddings for input texts using the configured model.
    Text is normalized lightly.
    """
    # Basic normalization; expand later if needed
    inputs = [t.strip() for t in texts]
    resp = _client_lazy().embeddings.create(model=settings.embedding_model, input=inputs)
    return [d.embedding for d in resp.data]
