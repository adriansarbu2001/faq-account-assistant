from fastapi import APIRouter, Depends

from src.api.deps.auth import get_token
from src.models.ask import AskRequest, AskResponse

router = APIRouter()


@router.post("/ask-question", response_model=AskResponse, dependencies=[Depends(get_token)])
def ask(payload: AskRequest) -> AskResponse:
    """
    Decision flow per spec:
      - Temporary: always treat as IT domain (router added later).
      - No vector DB yet: return fallback placeholder below threshold.
      - If later routed NON_IT, return exact compliance_message.
    """
    return AskResponse(
        source="openai",
        matched_question="N/A",
        answer="Fallback not yet implemented. This is a temporary scaffold.",
        similarity_score=None,
        collection=payload.collection,
        routing_domain="IT",
        top_candidate=None,
    )
