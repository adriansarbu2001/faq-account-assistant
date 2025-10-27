from __future__ import annotations

from unittest.mock import patch

from src.core.celery_app import compute_embedding


def test_core_celery_compute_embedding_task() -> None:
    with patch("src.core.celery_app.embed_text", return_value=[[0.1, 0.2, 0.3]]):
        res = compute_embedding(["hello"])
    assert res == [[0.1, 0.2, 0.3]]
