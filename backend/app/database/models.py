import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utcnow():
    return datetime.now(timezone.utc)


class MSME(Base):
    __tablename__ = "msmes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String(255), nullable=False)
    owner_name = Column(String(255), nullable=False)
    business_type = Column(String(100))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    gstin = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(255))
    phone = Column(String(20))
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    data_sources = relationship("DataSource", back_populates="msme", cascade="all, delete-orphan")
    assessments = relationship("ReadinessAssessment", back_populates="msme", cascade="all, delete-orphan")
    gst_records = relationship("GSTRecord", back_populates="msme", cascade="all, delete-orphan")
    upi_records = relationship("UPIRecord", back_populates="msme", cascade="all, delete-orphan")
    bank_records = relationship("BankStatementRecord", back_populates="msme", cascade="all, delete-orphan")
    invoice_records = relationship("InvoiceRecord", back_populates="msme", cascade="all, delete-orphan")
    business_profiles = relationship("BusinessProfile", back_populates="msme", cascade="all, delete-orphan")
    consent_records = relationship("ConsentRecord", back_populates="msme", cascade="all, delete-orphan")


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    source_type = Column(String(50), nullable=False)
    connected = Column(Boolean, default=False)
    connected_at = Column(DateTime)

    msme = relationship("MSME", back_populates="data_sources")


class GSTRecord(Base):
    __tablename__ = "gst_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    months_filed = Column(Integer, default=0)
    total_months = Column(Integer, default=12)
    turnover_annual = Column(Float, default=0)
    turnover_trend_percent = Column(Float, default=0)
    filings = Column(JSON, default=list)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="gst_records")


class UPIRecord(Base):
    __tablename__ = "upi_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    avg_monthly_inflow = Column(Float, default=0)
    avg_monthly_outflow = Column(Float, default=0)
    monthly_transactions = Column(Integer, default=0)
    transaction_history = Column(JSON, default=list)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="upi_records")


class BankStatementRecord(Base):
    __tablename__ = "bank_statement_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    emi_burden_percent = Column(Float, default=0)
    bounced_payments = Column(Integer, default=0)
    avg_balance = Column(Float, default=0)
    balance_stability = Column(String(20))
    months_history = Column(Integer, default=0)
    statement_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="bank_records")


class InvoiceRecord(Base):
    __tablename__ = "invoice_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    total_invoices = Column(Integer, default=0)
    total_value = Column(Float, default=0)
    avg_value = Column(Float, default=0)
    pending_percent = Column(Float, default=0)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="invoice_records")


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    years_in_business = Column(Float, default=0)
    employee_count = Column(Integer, default=0)
    employee_delta_6m = Column(Integer, default=0)
    description = Column(Text)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="business_profiles")


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    consent_token = Column(String(255), unique=True, nullable=False, index=True)
    data_sources = Column(JSON, default=list)
    purpose = Column(String(255))
    status = Column(String(50), default="active")
    granted_at = Column(DateTime, default=utcnow)
    expires_at = Column(DateTime)

    msme = relationship("MSME", back_populates="consent_records")


class ReadinessAssessment(Base):
    __tablename__ = "readiness_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    msme_id = Column(String, ForeignKey("msmes.id"), nullable=False)
    score = Column(Integer, default=0)
    grade = Column(String(3))
    confidence_band = Column(String(10))
    coverage_percent = Column(Float, default=0)
    coverage_connected = Column(Integer, default=0)
    coverage_total = Column(Integer, default=5)
    credit_ladder_outcome = Column(String(50))
    ai_summary = Column(Text)
    data_sources_used = Column(JSON, default=list)
    created_at = Column(DateTime, default=utcnow)

    msme = relationship("MSME", back_populates="assessments")
    sub_scores = relationship("SubScore", back_populates="assessment", cascade="all, delete-orphan")
    risk_signals = relationship("RiskSignal", back_populates="assessment", cascade="all, delete-orphan")
    reason_codes = relationship("ReasonCode", back_populates="assessment", cascade="all, delete-orphan")


class SubScore(Base):
    __tablename__ = "sub_scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("readiness_assessments.id"), nullable=False)
    dimension = Column(String(50), nullable=False)
    score = Column(Float, default=0)
    max_score = Column(Float, default=25)
    weight_percent = Column(Float, default=0)

    assessment = relationship("ReadinessAssessment", back_populates="sub_scores")


class RiskSignal(Base):
    __tablename__ = "risk_signals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("readiness_assessments.id"), nullable=False)
    signal_type = Column(String(20), nullable=False)
    code = Column(String(100))
    message = Column(Text)

    assessment = relationship("ReadinessAssessment", back_populates="risk_signals")


class ReasonCode(Base):
    __tablename__ = "reason_codes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("readiness_assessments.id"), nullable=False)
    code_type = Column(String(20), nullable=False)
    code = Column(String(100))
    message = Column(Text)

    assessment = relationship("ReadinessAssessment", back_populates="reason_codes")
