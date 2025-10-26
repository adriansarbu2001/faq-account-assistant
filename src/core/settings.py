from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)

    api_token: str = Field(default="dev-token")

    db_url: str = Field(default="postgresql+psycopg://postgres:postgres@db:5432/faqdb")

    openai_api_key: str = Field(default="")
    embedding_model: str = Field(default="text-embedding-3-small")
    embedding_dim: int = Field(default=1536)

    similarity_threshold: float = Field(default=0.80)
    fallback_model: str = Field(default="gpt-4o-mini")

    compliance_message: str = Field(
        default="This is not really what I was trained for, therefore I cannot answer. Try again."
    )


settings = Settings()
