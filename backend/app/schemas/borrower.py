from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MSMEBase(BaseModel):
    business_name: str
    owner_name: str
    business_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    gstin: str
    email: Optional[str] = None
    phone: Optional[str] = None


class MSMECreate(MSMEBase):
    pass


class MSMEResponse(MSMEBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DataSourceResponse(BaseModel):
    source_type: str
    connected: bool
    connected_at: Optional[datetime] = None

    class Config:
        from_attributes = True
