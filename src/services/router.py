"""AI Router using LangChain to classify questions as IT or NON_IT."""

from __future__ import annotations

from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.core.settings import settings

_NON_IT_HINTS = [
    "vacation",
    "holiday",
    "salary",
    "payroll",
]
_IT_HINTS = [
    "password",
    "account",
    "2fa",
    "authentication",
    "email",
]


def _keyword_gate(q: str) -> Literal["IT", "NON_IT", "AMBIG"]:
    t = q.lower()
    if any(k in t for k in _NON_IT_HINTS):
        return "NON_IT"
    if any(k in t for k in _IT_HINTS):
        return "IT"
    return "AMBIG"


_PROMPT = ChatPromptTemplate.from_template(
    """You are a router that classifies questions.
Answer only with IT or NON_IT.

Examples:
Q: How do I reset my account password? -> IT
Q: Can I take vacation next week? -> NON_IT
Q: Change my registered email address -> IT
Q: What is the company reimbursement policy? -> NON_IT

Q: {question}
Answer:"""
)


def _llm_route(q: str) -> Literal["IT", "NON_IT"]:
    llm = ChatOpenAI(model=settings.fallback_model, temperature=0, api_key=settings.openai_api_key)
    chain = _PROMPT | llm | StrOutputParser()
    result = chain.invoke({"question": q}).strip().upper()
    return "IT" if result.startswith("IT") else "NON_IT"


def route_domain(user_question: str) -> Literal["IT", "NON_IT"]:
    gate = _keyword_gate(user_question)
    if gate != "AMBIG":
        return gate
    return _llm_route(user_question)
