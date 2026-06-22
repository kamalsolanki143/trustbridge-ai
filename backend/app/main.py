from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.db import engine, Base
from backend.app.api.borrower import router as borrower_router
from backend.app.api.lender import router as lender_router
from backend.app.api.consent import router as consent_router
from backend.app.api.trust_summary import router as trust_summary_router
from backend.app.api.ladder_engine import router as ladder_router
from backend.app.api.manual_review import router as manual_review_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the DB schema automatically for local development and testing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Clean up resources if necessary

app = FastAPI(
    title="TrustBridge AI - Backend API",
    description="MSME Credit Ladder Engine powered by an Explainable Credit Readiness API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
# Allows requests from standard Next.js dev server origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler for generic errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

# Register Muskan's routers under the v1 API prefix
app.include_router(borrower_router, prefix="/api/v1")
app.include_router(lender_router, prefix="/api/v1")
app.include_router(consent_router, prefix="/api/v1")
app.include_router(trust_summary_router, prefix="/api/v1")
app.include_router(ladder_router, prefix="/api/v1")
app.include_router(manual_review_router, prefix="/api/v1")

# ==============================================================================
# TODO(team): Krrish/Kamal register your routers here — readiness.py, simulator.py
# Example:
# from backend.app.api.readiness import router as readiness_router
# from backend.app.api.simulator import router as simulator_router
# app.include_router(readiness_router, prefix="/api/v1")
# app.include_router(simulator_router, prefix="/api/v1")
# ==============================================================================

@app.get("/health", tags=["System Health"])
async def health_check():
    """
    Standard health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "TrustBridge AI Backend Engine",
        "api_version": "1.0.0"
    }
