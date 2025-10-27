"""OpenAI embeddings."""

from __future__ import annotations

from langchain_openai import OpenAIEmbeddings

from src.core.settings import settings


def embed_text(texts: list[str]) -> list[list[float]]:
    """
    Return embeddings for input texts.

    Args:
        texts: List of strings to embed.

    Returns:
        List of vector embeddings, one per input.
    """
    if not texts:
        return []

    inputs = [t.strip() for t in texts]
    embeddings = OpenAIEmbeddings(
        api_key=settings.openai_api_key,
        model=settings.embedding_model,
    )
    return embeddings.embed_documents(inputs)
