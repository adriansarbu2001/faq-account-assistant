"""Celery application factory."""

from __future__ import annotations

import os

from celery import Celery

from src.services.openai_embed import embed_text

app = Celery(
    "faq_account_assistant",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_time_limit=30,
    worker_prefetch_multiplier=4,
    broker_transport_options={"visibility_timeout": 3600},
)


@app.task(name="compute_embedding")
def compute_embedding(texts: list[str]) -> list[list[float]]:
    """Compute OpenAI embeddings in the background."""
    return embed_text(texts)
