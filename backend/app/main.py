import json
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text

# Local database and router imports
from app.db import engine as async_engine, Base as async_base
from app.database.db import init_db
from app.database.seed import seed_database

from app.api.borrower import router as borrower_router
from app.api.lender import router as lender_router
from app.api.consent import router as consent_router
from app.api.readiness import router as readiness_router
from app.api.trust_summary import router as trust_summary_router
from app.api.ladder_engine import router as ladder_router
from app.api.manual_review import router as manual_review_router
from app.api.simulator import router as simulator_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("trustbridge")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup banner print
    print("====================================")
    print("TrustBridge AI Backend Started")
    print("Version: 1.0.0")
    print("Docs: /docs")
    print("====================================")

    # Startup: Initialize Muskan's async DB tables for trust summaries/consents
    async with async_engine.begin() as conn:
        await conn.run_sync(async_base.metadata.create_all)
        
    # Initialize Krrish's sync DB tables and run seed data
    init_db()
    try:
        seed_database()
    except Exception as e:
        logger.warning(f"Database seeding bypassed or failed: {e}")
        
    yield

app = FastAPI(
    title="TrustBridge AI Backend API",
    description="Explainable MSME Credit Ladder Engine powered by Credit Readiness API.",
    version="1.0.0",
    contact={"name": "Compass Crew Team"},
    license_info={"name": "MIT"},
    lifespan=lifespan
)

# CORS Configuration supporting localhost and Vercel subdomains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for structured logging of request start and completion
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(json.dumps({
        "event": "request_start",
        "method": request.method,
        "path": request.url.path,
        "client": request.client.host if request.client else None
    }))
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(json.dumps({
            "event": "request_completed",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(process_time, 2)
        }))
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(json.dumps({
            "event": "request_failed",
            "method": request.method,
            "path": request.url.path,
            "duration_ms": round(process_time, 2),
            "error": str(e)
        }), exc_info=True)
        raise e

# Global Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(json.dumps({
        "event": "http_exception",
        "method": request.method,
        "path": request.url.path,
        "status_code": exc.status_code,
        "detail": exc.detail
    }))
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_details = []
    for error in errors:
        loc = " -> ".join(str(item) for item in error.get("loc", []))
        msg = error.get("msg", "Invalid value")
        error_details.append(f"{loc}: {msg}")
    detail_str = "Validation Error: " + "; ".join(error_details)
    
    logger.error(json.dumps({
        "event": "validation_error",
        "method": request.method,
        "path": request.url.path,
        "detail": detail_str
    }))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": detail_str}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(json.dumps({
        "event": "unhandled_exception",
        "method": request.method,
        "path": request.url.path,
        "error": str(exc)
    }), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

# Root route
@app.get("/")
async def root_route():
    return {
        "project": "TrustBridge AI Backend",
        "status": "Running",
        "version": "1.0.0",
        "documentation": "/docs"
    }

# Health Check route
@app.get("/health", tags=["Health"])
async def health_check():
    database_status = "connected"
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        database_status = "disconnected"

    return {
        "status": "healthy" if database_status == "connected" else "unhealthy",
        "service": "TrustBridge AI",
        "database": database_status,
        "version": "1.0.0"
    }

# Register API Routers under prefixes and with correct tags
app.include_router(borrower_router, prefix="/api/v1")
app.include_router(lender_router, prefix="/api/v1")
app.include_router(consent_router, prefix="/api/v1")
app.include_router(trust_summary_router, prefix="/api/v1")
app.include_router(ladder_router, prefix="/api/v1")
app.include_router(manual_review_router, prefix="/api/v1")
app.include_router(readiness_router)
app.include_router(simulator_router, prefix="/api/v1")
