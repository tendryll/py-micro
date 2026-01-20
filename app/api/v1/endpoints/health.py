# app/api/v1/endpoints/health.py
from __future__ import annotations

from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/health",
    summary="Liveness check",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Liveness probe.

    Used by:
    - Kubernetes livenessProbe
    - Load balancers
    - Basic uptime checks

    Should return OK if the process is running.
    """
    return {"status": "ok"}


@router.get(
    "/health/ready",
    summary="Readiness check",
    status_code=status.HTTP_200_OK,
)
async def readiness_check():
    """
    Readiness probe.

    Used by:
    - Kubernetes readinessProbe
    - Traffic gating during startup

    Extend this to check:
    - Database connectivity
    - Cache availability
    - External dependencies
    """
    checks = {
        "database": "ok",   # replace with real check
        "cache": "ok",      # replace with real check
    }

    all_ok = all(value == "ok" for value in checks.values())

    return {
        "status": "ok" if all_ok else "degraded",
        "checks": checks,
    }