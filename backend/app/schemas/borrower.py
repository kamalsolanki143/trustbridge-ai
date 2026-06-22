import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field

# TODO: move to schemas/ once Krrish's PR lands

class BorrowerBase(BaseModel):
    name: str = Field(..., example="Karan Johar")
    business_name: str = Field(..., example="Dharma Productions Private Limited")
    pan: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", example="ABCDE1234F")
    gstin: str = Field(..., pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", example="27ABCDE1234F1Z5")
    email: EmailStr = Field(..., example="contact@dharma.com")
    phone: str = Field(..., pattern=r"^\+91[6-9]\d{9}$", example="+919876543210")

class BorrowerCreate(BorrowerBase):
    id: str = Field(..., example="borrower_uuid_123")

class BorrowerResponse(BorrowerBase):
    id: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class BorrowerDashboardResponse(BaseModel):
    borrower_id: str
    latest_readiness_grade: Optional[str] = None
    coverage_pct: Optional[float] = None
    active_ladder_outcome: Optional[str] = None
    consent_status_overview: Dict[str, str] # data_source -> status (approved, revoked, expired, missing)
    growth_roadmap: Optional[Dict[str, Any]] = None
