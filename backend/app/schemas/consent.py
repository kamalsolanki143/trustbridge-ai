import datetime
from typing import Optional
from pydantic import BaseModel, Field

# TODO: move to schemas/ once Krrish's PR lands

class GrantConsentRequest(BaseModel):
    borrower_id: str = Field(..., example="borrower_uuid_123")
    data_source: str = Field(..., example="bank_statements") # bank_statements, gst, upi, invoices, business_profile
    purpose: str = Field(..., example="Cash Flow Stability Assessment")
    scope: str = Field(..., example="read")
    expiry: datetime.datetime = Field(..., example="2027-06-22T11:20:00Z")

class RevokeConsentRequest(BaseModel):
    borrower_id: str = Field(..., example="borrower_uuid_123")
    data_source: str = Field(..., example="bank_statements")

class ConsentResponse(BaseModel):
    id: int
    borrower_id: str
    data_source: str
    purpose: str
    scope: str
    expiry: datetime.datetime
    status: str # approved, revoked, expired
    used_for: Optional[str] = None
    granted_at: datetime.datetime
    revoked_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class ConsentAuditLogResponse(BaseModel):
    id: int
    borrower_id: str
    data_source: str
    action: str # grant, revoke, use
    purpose: str
    timestamp: datetime.datetime
    details: Optional[str] = None

    class Config:
        from_attributes = True
