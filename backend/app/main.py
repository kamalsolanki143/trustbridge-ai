from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import init_db
from app.database.seed import seed_database
from app.api.readiness import router as readiness_router

app = FastAPI(
    title="TrustBridge AI — MSME Credit Ladder Engine",
    description="REST API for credit readiness assessment of Indian MSMEs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(readiness_router)


@app.on_event("startup")
def on_startup():
    init_db()
    seed_database()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "TrustBridge AI"}
