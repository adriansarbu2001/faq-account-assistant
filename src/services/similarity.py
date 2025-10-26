from __future__ import annotations

from dataclasses import dataclass

from pgvector.sqlalchemy import Vector
from sqlalchemy import bindparam, text

from src.core.celery_app import compute_embedding
from src.core.settings import settings
from src.db.session import SessionLocal
from src.services.openai_embed import embed_text


@dataclass
class SimilarityResult:
    question: str
    answer: str
    score: float


def _get_query_vector(user_question: str) -> list[float]:
    """Queue embedding via Celery and wait briefly for result;
    fallback to direct embed on timeout."""
    async_result = compute_embedding.delay([user_question])
    try:
        vectors = async_result.get(timeout=4)
        return vectors[0]
    except Exception:
        return embed_text([user_question])[0]


def find_best_local_match(user_question: str) -> SimilarityResult | None:
    qvec = _get_query_vector(user_question)
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
            question=row.question, answer=row.answer, score=float(row.similarity)
        )
