from __future__ import annotations

import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.settings import settings


class Base(DeclarativeBase):
    """Declarative base."""


class FAQItem(Base):
    """FAQ item stored with an optional vector embedding."""

    __tablename__ = "faq_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_q = Column(Vector(dim=settings.embedding_dim), nullable=True)
