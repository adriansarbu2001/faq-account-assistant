from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.services.openai_embed import embed_text


def test_openai_embed() -> None:
    emb1 = MagicMock()
    emb2 = MagicMock()
    emb1.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]
    emb2.embed_documents.return_value = [[0.5, 0.6]]

    with patch("src.services.openai_embed.OpenAIEmbeddings") as MockEmb:
        MockEmb.side_effect = [emb1, emb2]

        out1 = embed_text(["a ", " b"])
        assert out1 == [[0.1, 0.2], [0.3, 0.4]]
        emb1.embed_documents.assert_called_once_with(["a", "b"])

        out2 = embed_text([" c"])
        assert out2 == [[0.5, 0.6]]
        emb2.embed_documents.assert_called_once_with(["c"])

        assert MockEmb.call_count == 2


def test_openai_embed_empty_input() -> None:
    with patch("src.services.openai_embed.OpenAIEmbeddings") as MockEmb:
        out = embed_text([])
        assert out == []
        MockEmb.assert_not_called()
