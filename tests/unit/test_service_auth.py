from __future__ import annotations

from fastapi.testclient import TestClient


def test_auth_missing_token(client: TestClient) -> None:
    r = client.post("/ask-question", json={"user_question": "hi"})
    assert r.status_code == 401
    assert r.json()["detail"] in {"missing_or_invalid_token", "Unauthorized", "invalid_token"}


def test_auth_invalid_token(client: TestClient) -> None:
    r = client.post(
        "/ask-question",
        headers={"Authorization": "Bearer WRONG"},
        json={"user_question": "hi"},
    )
    assert r.status_code == 401
    assert r.json()["detail"] in {"missing_or_invalid_token", "Unauthorized", "invalid_token"}
