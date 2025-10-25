from fastapi import Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from src.core.settings import settings


def get_token(authorization: str | None = Header(default=None)) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="missing_or_invalid_token")
    token = authorization.split(" ", 1)[1]
    if token != settings.api_token:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail="invalid_token")
