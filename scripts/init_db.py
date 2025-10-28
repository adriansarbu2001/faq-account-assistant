"""Initialize Postgres schema."""

from __future__ import annotations

from sqlalchemy import text

from src.db.session import engine
from src.vectorstore.models import Base


def main() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)
        conn.execute(text("ANALYZE"))
    print("Schema ready.")


if __name__ == "__main__":
    main()
