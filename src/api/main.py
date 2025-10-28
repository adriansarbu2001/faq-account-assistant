from fastapi import FastAPI

from src.api.routers import ask, health
from src.core.errors import (
    RequestValidationError,
    UpstreamRateLimitError,
    UpstreamServiceError,
    handle_rate_limit,
    handle_unexpected,
    handle_upstream_error,
    validation_handler,
)
from src.core.logging import configure_logging
from src.core.settings import settings

configure_logging(settings.log_level)
app = FastAPI(title="FAQ Account Assistant")

app.add_exception_handler(UpstreamRateLimitError, handle_rate_limit)
app.add_exception_handler(UpstreamServiceError, handle_upstream_error)
app.add_exception_handler(Exception, handle_unexpected)
app.add_exception_handler(RequestValidationError, validation_handler)

app.include_router(health.router)
app.include_router(ask.router)
