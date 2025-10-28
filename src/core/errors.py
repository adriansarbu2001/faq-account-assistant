from __future__ import annotations

import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

logger = logging.getLogger(__name__)


class UpstreamRateLimitError(RuntimeError):
    """OpenAI rate limit or quota exhausted."""


class UpstreamServiceError(RuntimeError):
    """Any other upstream error (timeouts, network, 5xx)."""


def classify_exception(e: Exception) -> Exception:
    msg = str(e).lower()
    if "rate limit" in msg or "quota" in msg or "429" in msg:
        return UpstreamRateLimitError(msg)
    return UpstreamServiceError(msg)


async def handle_rate_limit(
    _: Request, exc: UpstreamRateLimitError
) -> JSONResponse:
    logger.warning("UpstreamRateLimitError: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "rate_limited",
            "detail": "OpenAI temporarily rate limited.",
        },
    )


async def handle_upstream_error(
    _: Request, exc: UpstreamServiceError
) -> JSONResponse:
    logger.error("UpstreamServiceError: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "upstream_error",
            "detail": "Upstream service failed.",
        },
    )


async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_error",
            "detail": "Unexpected server error.",
        },
    )


async def validation_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": "validation_error", "detail": exc.errors()},
    )
