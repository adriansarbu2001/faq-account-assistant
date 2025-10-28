from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.core.errors import UpstreamRateLimitError, UpstreamServiceError


def test_api_rate_limited_returns_429(client: TestClient) -> None:
    with (
        patch("src.api.routers.ask.route_domain", return_value="IT"),
        patch("src.api.routers.ask.find_best_local_match", return_value=None),
        patch(
            "src.api.routers.ask.openai_answer",
            side_effect=UpstreamRateLimitError("rate limit"),
        ),
    ):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "any"},
        )
    assert r.status_code == 429
    body = r.json()
    assert body["error"] == "rate_limited"


def test_api_upstream_error_returns_502(client: TestClient) -> None:
    with (
        patch("src.api.routers.ask.route_domain", return_value="IT"),
        patch("src.api.routers.ask.find_best_local_match", return_value=None),
        patch(
            "src.api.routers.ask.openai_answer",
            side_effect=UpstreamServiceError("some bad error"),
        ),
    ):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "any"},
        )
    assert r.status_code == 502
    body = r.json()
    assert body["error"] == "upstream_error"


def test_validation_error_returns_422_problem_shape(
    client: TestClient,
) -> None:
    r = client.post(
        "/ask-question",
        headers={"Authorization": "Bearer dev-token"},
        json={},
    )
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "validation_error"
    assert isinstance(body["detail"], list)


def test_unexpected_error_returns_500_problem_shape(
    client: TestClient,
) -> None:
    with patch(
        "src.api.routers.ask.route_domain",
        side_effect=Exception("some really bad error"),
    ):
        r = client.post(
            "/ask-question",
            headers={"Authorization": "Bearer dev-token"},
            json={"user_question": "hi"},
        )
    assert r.status_code == 500
    body = r.json()
    assert body["error"] == "internal_error"
    assert body["detail"] == "Unexpected server error."
