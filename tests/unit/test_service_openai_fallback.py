from __future__ import annotations

from unittest.mock import MagicMock, patch

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
