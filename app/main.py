# app/main.py
from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings

logger = logging.getLogger(__name__)
from app.core.logging import configure_logging
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Central place for startup/shutdown logic:
    - initialize DB connections/pools
    - init clients (redis, kafka, http)
    - warm caches
    - start background tasks
    """
    logger.info("Starting service: %s", settings.service_name)

    # Example:
    # await init_db()
    # app.state.http = httpx.AsyncClient(timeout=...)

    yield

    logger.info("Shutting down service: %s", settings.service_name)

    # Example:
    # await app.state.http.aclose()
    # await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.service_name,
        version=settings.version,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs" if settings.enable_docs else None,
        redoc_url=f"{settings.api_prefix}/redoc" if settings.enable_docs else None,
        lifespan=lifespan,
    )

    # ---- Middleware ----

    # CORS (only if you actually need browser-based cross-origin requests)
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Request ID + basic request logging (minimal but useful)
    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000.0
        response.headers["x-request-id"] = request_id

        logger.info(
            "request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )
        return response

    # ---- Routers ----
    app.include_router(v1_router, prefix=settings.api_prefix)

    # ---- Root / Health ----
    @app.get("/", include_in_schema=False)
    async def root():
        return {"service": settings.service_name, "version": settings.version}

    return app


app = create_app()
