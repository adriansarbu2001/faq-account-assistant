"""Append all FAQ rows from a JSON file with NULL embeddings.

Usage:
  python scripts/seed_faq.py --file data/faq_seed.json
"""

from __future__ import annotations

import json
from argparse import ArgumentParser
from pathlib import Path

from sqlalchemy import insert
from sqlalchemy.orm import Session

from src.db.session import engine
from src.vectorstore.models import FAQItem


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--file", "-f", default="data/faq_seed.json", help="Path to JSON file")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"Seed file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))

    rows = [
        {"question": row["question"], "answer": row["answer"], "embedding_q": None}
        for row in payload
    ]

    with Session(engine) as session:
        session.execute(insert(FAQItem).values(rows))
        session.commit()

    print(f"Inserted {len(rows)} rows from {path}.")


if __name__ == "__main__":
    main()
