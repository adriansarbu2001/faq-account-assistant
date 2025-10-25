from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_ask_requires_auth() -> None:
    resp = client.post("/ask-question", json={"user_question": "hi"})
    assert resp.status_code == 401


def test_ask_scaffold_ok() -> None:
    resp = client.post(
        "/ask-question",
        headers={"Authorization": "Bearer dev-token"},
        json={"user_question": "How do I reset my password?"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["source"] == "openai"
    assert body["matched_question"] == "N/A"
