from __future__ import annotations

from typing import Final

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.errors import (
    UpstreamRateLimitError,
    UpstreamServiceError,
    classify_exception,
)
from src.core.settings import settings

_PROMPT: Final[ChatPromptTemplate] = ChatPromptTemplate.from_template(
    "You answer end-user questions about account settings.\n"
    "If you are unsure, say so briefly and suggest the"
    "closest relevant steps.\n\n"
    "Question: {question}\n"
    "Answer in 1-3 concise sentences."
)


def _build_chain() -> StrOutputParser:
    llm = ChatOpenAI(
        model=settings.fallback_model,
        temperature=0,
        api_key=settings.openai_api_key,
        timeout=15,
        max_retries=0,
    )
    return _PROMPT | llm | StrOutputParser()


@retry(
    wait=wait_exponential(multiplier=0.5, max=4),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(
        (UpstreamRateLimitError, UpstreamServiceError)
    ),
)
def openai_answer(question: str) -> str:
    """
    Produce an answer for a user question from OpenAI.
    """
    try:
        chain = _build_chain()
        return chain.invoke({"question": question}).strip()
    except Exception as e:
        raise classify_exception(e) from e
