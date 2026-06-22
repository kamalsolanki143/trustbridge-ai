from typing import List
from pydantic import BaseModel, Field

# TODO: move to schemas/ once Krrish's PR lands

class ReadinessProfile(BaseModel):
    readiness_grade: str = Field(..., example="A")
    confidence_band: str = Field(..., example="High")
    coverage_pct: float = Field(..., example=95.5)
    risk_signals: List[str] = Field(default_factory=list, example=["No major defaults", "Irregular transaction activity"])
    reason_codes: List[str] = Field(default_factory=list, example=["STABLE_INFLOWS", "CONSISTENT_GST"])
    stability_indicators: List[str] = Field(default_factory=list, example=["3+ years operational history", "High customer retention"])

    class Config:
        from_attributes = True
