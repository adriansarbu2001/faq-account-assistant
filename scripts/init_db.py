"""Initialize database schema and indexes for pgvector search."""

from __future__ import annotations

from sqlalchemy import text

from src.db.session import engine
from src.vectorstore.models import Base


def main() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        Base.metadata.create_all(bind=conn)
        # IVF Flat index with cosine distance
        conn.execute(
            text(
                """
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE schemaname = 'public'
                AND indexname = 'idx_faq_items_embedding_q_ivfflat'
              ) THEN
                CREATE INDEX idx_faq_items_embedding_q_ivfflat
                ON faq_items USING ivfflat (embedding_q vector_cosine_ops)
                WITH (lists = 100);
              END IF;
            END$$;
        """
            )
        )


if __name__ == "__main__":
    main()
