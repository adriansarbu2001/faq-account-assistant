from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import src.services.router as router
from src.services.router import route_domain


def test_keyword_gate_forced_it(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router, "_IT_HINTS", ["yyy"], raising=True)
    monkeypatch.setattr(router, "_NON_IT_HINTS", [], raising=True)
    assert router._keyword_gate("please help with yyy login") == "IT"


def test_keyword_gate_forced_non_it(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router, "_NON_IT_HINTS", ["zzz"], raising=True)
    monkeypatch.setattr(router, "_IT_HINTS", [], raising=True)
    assert router._keyword_gate("I talk about zzz benefits") == "NON_IT"


def test_keyword_gate_ambig_when_hints_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(router, "_IT_HINTS", [], raising=True)
    monkeypatch.setattr(router, "_NON_IT_HINTS", [], raising=True)
    assert router._keyword_gate("ambiguous question") == "AMBIG"


def test_router_non_llm_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(router, "_IT_HINTS", [], raising=True)
    monkeypatch.setattr(router, "_NON_IT_HINTS", [], raising=True)
    with patch("src.services.router._keyword_gate", return_value="NON_IT"):
        assert route_domain("ambiguous question") == "NON_IT"


def test_router_llm_path() -> None:
    with patch("src.services.router._keyword_gate", return_value="AMBIG"):
        fake_chain = MagicMock()
        fake_chain.invoke.return_value = "IT"
        with (
            patch("src.services.router.ChatOpenAI") as _llm,
            patch("src.services.router._PROMPT") as _prompt,
            patch("src.services.router.StrOutputParser") as _parser,
        ):
            _prompt.__or__.return_value.__or__.return_value = fake_chain
            assert route_domain("ambiguous question") == "IT"
            fake_chain.invoke.assert_called_once()


def test_router_llm_path_non_it() -> None:
    with patch("src.services.router._keyword_gate", return_value="AMBIG"):
        fake_chain = MagicMock()
        fake_chain.invoke.return_value = "NON_IT"
        with (
            patch("src.services.router.ChatOpenAI") as _llm,
            patch("src.services.router._PROMPT") as _prompt,
            patch("src.services.router.StrOutputParser") as _parser,
        ):
            _prompt.__or__.return_value.__or__.return_value = fake_chain
            assert (
                route_domain("ambiguous question about holidays") == "NON_IT"
            )
            fake_chain.invoke.assert_called_once()
