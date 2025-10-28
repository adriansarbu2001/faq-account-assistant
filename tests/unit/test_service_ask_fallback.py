from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.core.settings import settings


@dataclass
class _SimLow:
    question: str
    answer: str
    score: float


def test_openai_fallback_when_below_threshold(client: TestClient) -> None:
    sim = _SimLow(
        question="Q",
        answer="A",
        score=max(0.0, float(settings.similarity_threshold) - 0.2),
    )
    with (
        patch("src.api.routers.ask.route_domain", return_value="IT"),
        patch("src.api.routers.ask.find_best_local_match", return_value=sim),
        patch(
            "src.api.routers.ask.openai_answer",
            return_value="Mocked generated answer",
        ),
    ):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "different wording"},
        )
    assert r.status_code == 200
    assert r.json() == {
        "source": "openai",
        "matched_question": "N/A",
        "answer": "Mocked generated answer",
    }
