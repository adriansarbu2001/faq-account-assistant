"""Similarity search using pgvector cosine distance."""

from __future__ import annotations

from dataclasses import dataclass

from pgvector.sqlalchemy import Vector
from sqlalchemy import bindparam, text

from src.core.settings import settings
from src.db.session import SessionLocal
from src.services.openai_embed import embed_text


@dataclass
class SimilarityResult:
    question: str
    answer: str
    score: float


def find_best_local_match(user_question: str) -> SimilarityResult | None:
    [qvec] = embed_text([user_question])

    sql = """
        SELECT question, answer, (1 - (embedding_q <=> :qvec)) AS similarity
        FROM faq_items
        ORDER BY embedding_q <=> :qvec
        LIMIT 1
    """
    stmt = text(sql).bindparams(bindparam("qvec", qvec, type_=Vector(dim=settings.embedding_dim)))

    with SessionLocal() as s:
        row = s.execute(stmt).fetchone()
        if not row:
            return None
        return SimilarityResult(
            question=row.question,
            answer=row.answer,
            score=float(row.similarity),
        )
