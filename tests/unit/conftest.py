from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture(autouse=True)
def _env() -> Iterator[None]:
    os.environ.setdefault("OPENAI_API_KEY", "sk-test")
    os.environ.setdefault("SIMILARITY_THRESHOLD", "0.8")
    yield


@pytest.fixture(autouse=True)
def _no_celery_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.services.similarity._get_query_vector", lambda q: [0.0], raising=True)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
