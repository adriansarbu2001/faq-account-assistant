"""Recompute embeddings for ALL rows (should be called only when the embedding model changed).

Flow:
  1) Ensure pgvector extension exists
  2) Drop temp column if present
  3) Add temp column 'embedding_q_new' with current settings.embedding_dim
  4) Re-embed every row in batches and UPDATE by id
  5) Drop old 'embedding_q' and rename 'embedding_q_new' -> 'embedding_q'
  6) ANALYZE for fresh planner stats
"""

from __future__ import annotations

from typing import TypeVar

from pgvector.sqlalchemy import Vector
from sqlalchemy import bindparam, select, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Session

from src.core.settings import settings
from src.db.session import engine
from src.services.openai_embed import embed_text
from src.vectorstore.models import FAQItem

T = TypeVar("T")
BATCH_SIZE = 64


def _chunks(items: list[T], n: int) -> list[list[T]]:
    """Split a list into n-sized chunks."""
    return [items[i : i + n] for i in range(0, len(items), n)]


def _prepare_new_column() -> None:
    """Create extension, drop any old temp column, add the new temp column."""
    dim = settings.embedding_dim
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("ALTER TABLE faq_items DROP COLUMN IF EXISTS embedding_q_new;"))
        conn.execute(text(f"ALTER TABLE faq_items ADD COLUMN embedding_q_new VECTOR({dim});"))


def _reembed_all_rows_into_new() -> int:
    """Compute embeddings for all rows and write them to embedding_q_new."""
    # Pre-compiled typed UPDATE statement (uses pgvector bind)
    stmt = text("UPDATE faq_items SET embedding_q_new = :vec WHERE id = :id").bindparams(
        bindparam("vec", type_=Vector(dim=settings.embedding_dim)),
        bindparam("id", type_=PGUUID(as_uuid=True)),
    )

    updated = 0
    with Session(engine) as session:
        rows: list[FAQItem] = list(session.execute(select(FAQItem)).scalars().all())
        if not rows:
            return 0

        for batch in _chunks(rows, BATCH_SIZE):
            texts = [r.question for r in batch]
            vectors = embed_text(texts)
            for row_obj, vec in zip(batch, vectors, strict=False):
                session.execute(stmt, {"id": row_obj.id, "vec": vec})
            session.commit()
            updated += len(batch)

    return updated


def _swap_columns() -> None:
    """Swap embedding_q_new into embedding_q and analyze."""
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE faq_items DROP COLUMN IF EXISTS embedding_q;"))
        conn.execute(text("ALTER TABLE faq_items RENAME COLUMN embedding_q_new TO embedding_q;"))
        conn.execute(text("ANALYZE faq_items;"))


def main() -> None:
    _prepare_new_column()
    count = _reembed_all_rows_into_new()
    _swap_columns()
    print(f"Re-embedded {count} rows and switched embedding_q " f"to dim={settings.embedding_dim}.")


if __name__ == "__main__":
    main()
