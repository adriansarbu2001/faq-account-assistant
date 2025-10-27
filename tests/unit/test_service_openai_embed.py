from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.services.openai_embed import embed_text


class _Resp:
    class _D:
        def __init__(self, emb: list[float]) -> None:
            self.embedding = emb

    def __init__(self, embs: list[list[float]]) -> None:
        self.data = [self._D(e) for e in embs]


def test_openai_embed_lazy_client_and_result() -> None:
    with patch("src.services.openai_embed.OpenAI") as MockOpenAI:
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.embeddings.create.return_value = _Resp([[0.1, 0.2], [0.3, 0.4]])

        out = embed_text(["a", "b"])
        assert out == [[0.1, 0.2], [0.3, 0.4]]

        mock_client.embeddings.create.return_value = _Resp([[0.5, 0.6]])
        out2 = embed_text(["c"])
        assert out2 == [[0.5, 0.6]]

        assert MockOpenAI.call_count == 1
        assert mock_client.embeddings.create.call_count == 2
