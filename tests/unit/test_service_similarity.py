from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

from src.services.similarity import _get_query_vector, find_best_local_match


def test_similarity_best_match_maps_fields() -> None:
    dummy_vec = [[0.1, 0.2, 0.3]]
    fake_row = SimpleNamespace(
        question="How can I restore my account settings?",
        answer="Go to settings and click on 'restore default'.",
        similarity=0.9234,
    )

    mock_session = MagicMock()
    mock_session.__enter__.return_value = mock_session
    mock_session.execute.return_value.fetchone.return_value = fake_row

    with (
        patch("src.services.similarity.embed_text", return_value=dummy_vec),
        patch("src.services.similarity.SessionLocal", return_value=mock_session),
    ):
        res = find_best_local_match("How do I reset my account?")
    assert res is not None
    assert res.question == fake_row.question
    assert res.answer == fake_row.answer
    assert abs(res.score - 0.9234) < 1e-9


def test_similarity_returns_none_when_no_rows() -> None:
    mock_session = MagicMock()
    mock_session.__enter__.return_value = mock_session
    mock_session.execute.return_value.fetchone.return_value = None

    with (
        patch("src.services.similarity._get_query_vector", return_value=[0.0]),
        patch("src.services.similarity.SessionLocal", return_value=mock_session),
    ):
        res = find_best_local_match("q")
    assert res is None


def test_get_query_vector_uses_celery_result() -> None:
    """Covers the happy path where Celery returns a vector before timeout."""

    class FakeAsyncResult:
        def get(self, timeout: int) -> list[list[float]]:
            return [[0.1, 0.2, 0.3]]

    with (
        patch("src.services.similarity.compute_embedding") as task,
        patch("src.services.similarity.embed_text") as embed_direct,
    ):
        task.delay.return_value = FakeAsyncResult()
        vec = _get_query_vector("hello")
        assert vec == [0.1, 0.2, 0.3]
        task.delay.assert_called_once()
        embed_direct.assert_not_called()


def test_get_query_vector_timeout_fallback() -> None:
    """Covers the exception path: fallback to direct embed_text()."""

    class FakeAsyncResult:
        def get(self, timeout: int) -> Any:
            raise TimeoutError("pretend celery slow")

    with (
        patch("src.services.similarity.compute_embedding") as task,
        patch("src.services.similarity.embed_text", return_value=[[9.9, 9.8, 9.7]]) as embed_direct,
    ):
        task.delay.return_value = FakeAsyncResult()
        vec = _get_query_vector("hello")
        assert vec == [9.9, 9.8, 9.7]
        task.delay.assert_called_once()
        embed_direct.assert_called_once_with(["hello"])
