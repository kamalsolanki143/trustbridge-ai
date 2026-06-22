from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ConsentGrantRequest(BaseModel):
    msme_id: str
    data_sources: list[str]
    purpose: str = "Credit Readiness Assessment for IDBI Bank Loan Application"


class ConsentResponse(BaseModel):
    id: str
    msme_id: str
    consent_token: str
    data_sources: list[str]
    purpose: str
    status: str
    granted_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConsentCheckRequest(BaseModel):
    consent_token: str
    gstin: str
    data_sources: list[str]
