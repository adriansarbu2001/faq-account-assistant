"""Seed FAQ items from JSON, computing embeddings."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import insert

from src.db.session import SessionLocal
from src.services.openai_embed import embed_text
from src.vectorstore.models import FAQItem

SEED_PATH = Path("data/faq_seed.json")


def main() -> None:
    if not SEED_PATH.exists():
        raise SystemExit(f"Seed file not found: {SEED_PATH}")

    payload = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    questions = [row["question"] for row in payload]
    qa_texts = [f"{row['question']}\n\n{row['answer']}" for row in payload]

    emb_q = embed_text(questions)
    emb_qa = embed_text(qa_texts)

    records = []
    for row, vq, vqa in zip(payload, emb_q, emb_qa, strict=False):
        records.append(
            {
                "question": row["question"],
                "answer": row["answer"],
                "embedding_q": vq,
                "embedding_qa": vqa,
            }
        )

    with SessionLocal() as s:
        s.execute(insert(FAQItem).values(records))
        s.commit()


if __name__ == "__main__":
    main()
