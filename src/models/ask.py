from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    user_question: str = Field(..., description="Question from the user.")


class AskResponse(BaseModel):
    source: str = Field(..., description='"local" or "openai"')
    matched_question: str = Field(..., description='Exact matched FAQ question or "N/A"')
    answer: str = Field(..., description="Final answer text.")
