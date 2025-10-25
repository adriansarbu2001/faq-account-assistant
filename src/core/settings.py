from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)

    api_token: str = Field(default="dev-token")

    # OpenAI and similarity placeholders, will be used soon
    openai_api_key: str = Field(default="")
    similarity_threshold: float = Field(default=0.80)
    top_k: int = Field(default=8)
    fallback_model: str = Field(default="gpt-4o-mini")

    compliance_message: str = Field(
        default="This is not really what I was trained for, therefore I cannot answer. Try again."
    )


settings = Settings()
