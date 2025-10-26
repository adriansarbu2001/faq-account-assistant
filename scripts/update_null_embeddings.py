"""Compute embeddings for all FAQ rows that currently have NULL embeddings."""

from __future__ import annotations

from typing import TypeVar

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.db.session import engine
from src.services.openai_embed import embed_text
from src.vectorstore.models import FAQItem

T = TypeVar("T")
BATCH_SIZE = 64


def _chunks(items: list[T], n: int) -> list[list[T]]:
    """Split a list into n-sized chunks."""
    return [items[i : i + n] for i in range(0, len(items), n)]


def main() -> None:
    with Session(engine) as session:
        items = (
            session.execute(select(FAQItem).where(FAQItem.embedding_q.is_(None))).scalars().all()
        )
        if not items:
            print("No NULL embeddings to update.")
            return

        print(f"Found {len(items)} rows with NULL embeddings. Updating...")

        for batch in _chunks(items, BATCH_SIZE):
            texts = [it.question for it in batch]
            vectors = embed_text(texts)
            for it, vec in zip(batch, vectors, strict=False):
                session.execute(update(FAQItem).where(FAQItem.id == it.id).values(embedding_q=vec))
            session.commit()

        print("Embeddings updated for all NULL rows.")


if __name__ == "__main__":
    main()
