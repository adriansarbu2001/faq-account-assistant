import logging

from fastapi import APIRouter, Depends

from src.api.deps.auth import get_token
from src.core.errors import (
    UpstreamRateLimitError,
    UpstreamServiceError,
)
from src.core.settings import settings
from src.models.ask import AskRequest, AskResponse
from src.services.openai_fallback import openai_answer
from src.services.router import route_domain
from src.services.similarity import find_best_local_match

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/ask-question",
    response_model=AskResponse,
    dependencies=[Depends(get_token)],
)
def ask(payload: AskRequest) -> AskResponse:
    """
    Flow:
        1) Route to IT / NON_IT.
        2) If NON_IT -> compliance message.
        3) Else try local FAQ.
        4) If below threshold -> LangChain fallback.
    """
    domain = route_domain(payload.user_question)

    if domain == "NON_IT":
        logger.info(
            f"[NON-IT] Question='{payload.user_question}'"
            f"| Source='local' "
            f"| Matched='' | Score=None"
        )
        return AskResponse(
            source="local",
            matched_question="N/A",
            answer=settings.compliance_message,
        )

    candidate = find_best_local_match(payload.user_question)

    if candidate and candidate.score >= settings.similarity_threshold:
        logger.info(
            f"[LOCAL] Question='{payload.user_question}'"
            f"| Matched='{candidate.question}' "
            f"| Similarity={candidate.score}"
        )
        return AskResponse(
            source="local",
            matched_question=candidate.question,
            answer=candidate.answer,
        )

    try:
        fallback_answer = openai_answer(payload.user_question)
        logger.info(
            f"[OPENAI] Question='{payload.user_question}'"
            f"| Fallback used "
            f"| Similarity={f'{candidate.score}' if candidate else 'None'}"
        )
        return AskResponse(
            source="openai",
            matched_question="N/A",
            answer=fallback_answer,
        )
    except UpstreamRateLimitError:
        logger.warning("[OPENAI] rate limited")
        raise
    except UpstreamServiceError:
        logger.error("[OPENAI] upstream error")
        raise
