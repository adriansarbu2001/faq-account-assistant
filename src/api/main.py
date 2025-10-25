from fastapi import FastAPI

from src.api.routers import ask
from src.core.logging import configure_logging

app = FastAPI(title="FAQ Account Assistant", version="0.1.0")
configure_logging()


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}


app.include_router(ask.router, tags=["faq"])
