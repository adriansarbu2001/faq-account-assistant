from fastapi import APIRouter, Depends

from src.api.deps.auth import get_token
from src.core.settings import settings
from src.models.ask import AskRequest, AskResponse
from src.services.router import route_domain
from src.services.similarity import find_best_local_match

router = APIRouter()


@router.post("/ask-question", response_model=AskResponse, dependencies=[Depends(get_token)])
def ask(payload: AskRequest) -> AskResponse:
    """
    Decision flow per spec:
      1) Local similarity search in pgvector.
      2) If score >= threshold -> return FAQ answer.
      3) Else -> OpenAI fallback (placeholder for now).
    Compliance message is enforced when we add routing (IT vs NON_IT).
    """
    domain = route_domain(payload.user_question)

    if domain == "NON_IT":
        return AskResponse(
            source="compliance",
            matched_question="N/A",
            answer=settings.compliance_message,
            routing_domain="NON_IT",
            similarity_score=None,
            top_candidate=None,
        )

    candidate = find_best_local_match(payload.user_question)

    if candidate and candidate.score >= settings.similarity_threshold:
        return AskResponse(
            source="faq",
            matched_question=candidate.question,
            answer=candidate.answer,
            similarity_score=candidate.score,
            routing_domain=domain,
            top_candidate=candidate.question,
        )

    return AskResponse(
        source="openai",
        matched_question="N/A",
        answer="Fallback not yet implemented. Local match below threshold.",
        similarity_score=candidate.score if candidate else None,
        routing_domain=domain,
        top_candidate=candidate.question if candidate else None,
    )
