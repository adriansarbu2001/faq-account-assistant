from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.core.settings import settings


def test_non_it_returns_compliance(client: TestClient) -> None:
    with patch("src.api.routers.ask.route_domain", return_value="NON_IT"):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "Can I take free day next week?"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body == {
        "source": "local",
        "matched_question": "N/A",
        "answer": settings.compliance_message,
    }
