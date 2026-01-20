# app/dependencies/auth.py
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)


async def require_bearer_token(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> str:
    """
    Minimal auth dependency.
    Replace with real JWT validation (decode token, check claims, etc.).
    """
    if creds is None or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    return creds.credentials