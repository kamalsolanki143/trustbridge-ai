from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Muskan's imports
from app.db import engine as async_engine, Base as async_base
from app.api.borrower import router as borrower_router
from app.api.lender import router as lender_router
from app.api.consent import router as consent_router
from app.api.trust_summary import router as trust_summary_router
from app.api.ladder_engine import router as ladder_router
from app.api.manual_review import router as manual_review_router

# Krrish's imports
from app.database.db import init_db
from app.database.seed import seed_database
from app.api.readiness import router as readiness_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Muskan's async DB tables for trust summaries/consents
    async with async_engine.begin() as conn:
        await conn.run_sync(async_base.metadata.create_all)
        
    # Initialize Krrish's sync DB tables and run seed data
    init_db()
    try:
        seed_database()
    except Exception:
        pass # Avoid crashing if database is already seeded
        
    yield

app = FastAPI(
    title="TrustBridge AI - Backend API",
    description="MSME Credit Ladder Engine powered by an Explainable Credit Readiness API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Register Krrish's router
app.include_router(readiness_router)

# ==============================================================================
# TODO(team): Kamal register your simulator.py router here
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
