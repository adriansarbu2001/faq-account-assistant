"""Initialize Postgres schema for production (with IVFFlat index)."""

from sqlalchemy import text

from src.db.session import engine
from src.vectorstore.models import Base


def main() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)
        conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_faq_items_embedding_q_ivfflat
            ON faq_items
            USING ivfflat (embedding_q vector_cosine_ops)
            WITH (lists = 100);
        """
            )
        )
        conn.execute(text("ANALYZE"))


if __name__ == "__main__":
    main()
