from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.core.settings import settings


@dataclass
class _Sim:
    question: str
    answer: str
    score: float


def test_local_match_above_threshold(client: TestClient) -> None:
    sim = _Sim(
        question="How can I restore my account settings?",
        answer="Go to settings and click on 'restore default'.",
        score=max(0.9, float(settings.similarity_threshold) + 0.01),
    )
    with (
        patch("src.api.routers.ask.route_domain", return_value="IT"),
        patch("src.api.routers.ask.find_best_local_match", return_value=sim),
    ):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "How do I reset my account?"},
        )
    assert r.status_code == 200
    assert r.json() == {
        "source": "local",
        "matched_question": sim.question,
        "answer": sim.answer,
    }
