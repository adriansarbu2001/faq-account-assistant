from __future__ import annotations


def test_models_import_executes_module() -> None:
    from src.vectorstore.models import FAQItem

    assert FAQItem.__tablename__ == "faq_items"
