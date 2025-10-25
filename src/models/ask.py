from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    user_question: str = Field(..., description="Question from the user.")


class AskResponse(BaseModel):
    source: str = Field(..., description="faq | openai | compliance")
    matched_question: str = Field(..., description="Matched FAQ question or 'N/A'.")
    answer: str = Field(..., description="Final answer text.")
    similarity_score: float | None = Field(
        default=None, description="Cosine similarity if from FAQ."
    )
    routing_domain: str | None = Field(
        default=None, description="IT or NON_IT when routing is enabled."
    )
    top_candidate: str | None = Field(default=None, description="Best candidate question, if any.")
