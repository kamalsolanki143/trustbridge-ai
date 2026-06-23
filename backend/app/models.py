import datetime
from sqlalchemy import String, Integer, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

# TODO: Coordinate with Krrish to merge these models into the unified models.py once his data ingestion PR lands.

class Borrower(Base):
    __tablename__ = "borrowers"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True) # Usually a UUID or external ID
    name: Mapped[str] = mapped_column(String, nullable=False)
    business_name: Mapped[str] = mapped_column(String, nullable=False)
    pan: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    gstin: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )


class Consent(Base):
    __tablename__ = "consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borrower_id: Mapped[str] = mapped_column(String, ForeignKey("borrowers.id"), index=True)
    data_source: Mapped[str] = mapped_column(String, nullable=False) # e.g. bank_statements, gst, upi, invoices, business_profile
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    scope: Mapped[str] = mapped_column(String, nullable=False)
    expiry: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String, default="approved") # approved, revoked, expired
    used_for: Mapped[str] = mapped_column(String, nullable=True) # Description of what the data was used for
    granted_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    revoked_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)


class ConsentAuditLog(Base):
    __tablename__ = "consent_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borrower_id: Mapped[str] = mapped_column(String, ForeignKey("borrowers.id"), index=True)
    data_source: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False) # grant, revoke, use
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    details: Mapped[str] = mapped_column(String, nullable=True) # Any extra context (e.g. API endpoint accessed)


class LenderPolicy(Base):
    __tablename__ = "lender_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lender_id: Mapped[str] = mapped_column(String, unique=True, index=True) # e.g. "lender_abc"
    preference: Mapped[str] = mapped_column(String, default="Balanced") # Conservative, Balanced, Aggressive
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class LenderDecision(Base):
    __tablename__ = "lender_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borrower_id: Mapped[str] = mapped_column(String, ForeignKey("borrowers.id"), index=True)
    lender_id: Mapped[str] = mapped_column(String, index=True)
    decision: Mapped[str] = mapped_column(String, nullable=False) # approved, rejected, escalated
    notes: Mapped[str] = mapped_column(String, nullable=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )


class ManualReview(Base):
    __tablename__ = "manual_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borrower_id: Mapped[str] = mapped_column(String, ForeignKey("borrowers.id"), unique=True, index=True)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, resolved, escalated
    assigned_to: Mapped[str] = mapped_column(String, nullable=True)
    risk_signals: Mapped[list] = mapped_column(JSON, default=list) # List of risk flags
    anomaly_flags: Mapped[list] = mapped_column(JSON, default=list) # List of anomaly reasons
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    resolved_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    resolution_notes: Mapped[str] = mapped_column(String, nullable=True)


class TrustSummary(Base):
    __tablename__ = "trust_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    borrower_id: Mapped[str] = mapped_column(String, ForeignKey("borrowers.id"), index=True)
    readiness_grade: Mapped[str] = mapped_column(String, nullable=False)
    confidence_band: Mapped[str] = mapped_column(String, nullable=False)
    coverage_pct: Mapped[float] = mapped_column(Float, nullable=False)
    risk_signals: Mapped[list] = mapped_column(JSON, default=list)
    reason_codes: Mapped[list] = mapped_column(JSON, default=list)
    stability_indicators: Mapped[list] = mapped_column(JSON, default=list)
    verified_sources: Mapped[list] = mapped_column(JSON, default=list)
    ai_summary: Mapped[str] = mapped_column(String, nullable=False)
    recommended_action: Mapped[str] = mapped_column(String, nullable=False)
    generated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
