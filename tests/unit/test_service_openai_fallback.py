from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from tenacity import RetryError

from src.core.errors import UpstreamRateLimitError, UpstreamServiceError
from src.services.openai_fallback import openai_answer


def test_openai_fallback_chain_returns_text() -> None:
    fake_chain = MagicMock()
    fake_chain.invoke.return_value = "Final answer"
    with (
        patch("src.services.openai_fallback.ChatOpenAI") as _llm,
        patch("src.services.openai_fallback._PROMPT") as _prompt,
        patch("src.services.openai_fallback.StrOutputParser") as _parser,
    ):

        _prompt.__or__.return_value.__or__.return_value = fake_chain
        out = openai_answer("question?")
    assert out == "Final answer"


def test_fallback_success() -> None:
    fake_chain = MagicMock()
    fake_chain.invoke.return_value = "ok"
    with patch(
        "src.services.openai_fallback._build_chain", return_value=fake_chain
    ):
        out = openai_answer("q")
    assert out == "ok"
    fake_chain.invoke.assert_called_once()


def test_fallback_classifies_rate_limit() -> None:
    fake_chain = MagicMock()
    fake_chain.invoke.side_effect = Exception("Rate limit exceeded (429)")
    with patch(
        "src.services.openai_fallback._build_chain", return_value=fake_chain
    ):
        with pytest.raises(RetryError) as exc:
            openai_answer("q")
        inner = exc.value.last_attempt.exception()
        assert isinstance(inner, UpstreamRateLimitError)


def test_fallback_classifies_generic_upstream() -> None:
    fake_chain = MagicMock()
    fake_chain.invoke.side_effect = Exception("network timeout")
    with patch(
        "src.services.openai_fallback._build_chain", return_value=fake_chain
    ):
        with pytest.raises(RetryError) as exc:
            openai_answer("q")
        inner = exc.value.last_attempt.exception()
        assert isinstance(inner, UpstreamServiceError)
