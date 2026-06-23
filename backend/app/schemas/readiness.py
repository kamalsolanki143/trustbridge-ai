from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# ==============================================================================
# Krrish's Readiness Schemas (from main branch)
# ==============================================================================

class RiskSignalResponse(BaseModel):
    type: str
    code: str
    message: str


class ReasonCodeResponse(BaseModel):
    type: str
    code: str
    message: str


class SubScoreResponse(BaseModel):
    dimension: str
    score: float
    max_score: float
    weight_percent: float


class CoverageMeterResponse(BaseModel):
    connected: int
    total: int
    percentage: float


class ReadinessAssessRequest(BaseModel):
    gstin: str
    consent_token: str
    data_sources: list[str] = ["gst", "aa", "upi", "invoice", "business"]


class ReadinessResponse(BaseModel):
    msme_id: str
    business_name: str
    readiness_grade: str
    score: int
    confidence_band: str
    coverage_meter: CoverageMeterResponse
    sub_scores: list[SubScoreResponse]
    risk_signals: list[RiskSignalResponse]
    reason_codes: list[ReasonCodeResponse]
    credit_ladder_outcome: str
    ai_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReadinessHistoryResponse(BaseModel):
    assessments: list[ReadinessResponse]


# ==============================================================================
# Muskan's ReadinessProfile Schema
# ==============================================================================

class ReadinessProfile(BaseModel):
    readiness_grade: str = Field(..., example="A")
    confidence_band: str = Field(..., example="High")
    coverage_pct: float = Field(..., example=95.5)
    risk_signals: List[str] = Field(default_factory=list, example=["No major defaults", "Irregular transaction activity"])
    reason_codes: List[str] = Field(default_factory=list, example=["STABLE_INFLOWS", "CONSISTENT_GST"])
    stability_indicators: List[str] = Field(default_factory=list, example=["3+ years operational history", "High customer retention"])

    class Config:
        from_attributes = True
