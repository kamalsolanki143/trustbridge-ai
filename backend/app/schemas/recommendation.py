import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# ==============================================================================
# Kamal's Growth Roadmap & Scenario Schemas (from main branch)
# ==============================================================================

class Milestone(BaseModel):
    title: str
    description: str
    impact: str
    timeline: str
    effort: str


class GrowthRoadmapResponse(BaseModel):
    current_grade: str
    target_grade: str
    milestones: List[Milestone]
    progress_percent: float


class ScenarioInput(BaseModel):
    gstin: str
    adjustments: Dict[str, Any]


class ScenarioResult(BaseModel):
    projected_score: int
    projected_grade: str
    projected_outcome: str
    delta_score: int
    improvements: List[str]


# ==============================================================================
# Muskan's Credit Ladder, Lender & Manual Review Schemas
# ==============================================================================

class LadderDecision(BaseModel):
    decision: str = Field(..., example="Starter Loan") # Pre-Qualified | Starter Loan | Improve First | Manual Review
    reason_codes: List[str] = Field(default_factory=list, example=["GOOD_TILL_NOW", "LOW_INFLOW_HISTORY"])
    borrower_id: str

class LenderPolicyRequest(BaseModel):
    preference: str = Field(..., example="Balanced") # Conservative | Balanced | Aggressive

class LenderPolicyResponse(BaseModel):
    lender_id: str
    preference: str
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class LenderDecisionRecordRequest(BaseModel):
    decision: str = Field(..., example="approved") # approved | rejected | escalated
    notes: Optional[str] = Field(None, example="Borrower showed solid alternative cashflows, approved for starter tier.")

class LenderDecisionRecordResponse(BaseModel):
    id: int
    borrower_id: str
    lender_id: str
    decision: str
    notes: Optional[str]
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class ManualReviewResponse(BaseModel):
    id: int
    borrower_id: str
    status: str # pending, resolved, escalated
    assigned_to: Optional[str]
    risk_signals: List[str]
    anomaly_flags: List[str]
    created_at: datetime.datetime
    resolved_at: Optional[datetime.datetime]
    resolution_notes: Optional[str]

    class Config:
        from_attributes = True

class ManualReviewResolveRequest(BaseModel):
    resolution: str = Field(..., example="resolved") # resolved | escalated | rejected
    notes: str = Field(..., example="Verified manual documents, cleared warning signals.")

class TrustSummaryResponse(BaseModel):
    id: int
    borrower_id: str
    readiness_grade: str
    confidence_band: str
    coverage_pct: float
    risk_signals: List[str]
    reason_codes: List[str]
    stability_indicators: List[str]
    verified_sources: List[str]
    ai_summary: str
    recommended_action: str
    generated_at: datetime.datetime

    class Config:
        from_attributes = True

class LenderApplicationResponse(BaseModel):
    borrower_id: str
    name: str
    business_name: str
    readiness_grade: str
    ladder_outcome: str
    risk_signals: List[str]

    class Config:
        from_attributes = True
