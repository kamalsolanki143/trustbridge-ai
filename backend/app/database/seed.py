from sqlalchemy.orm import Session
from app.database.models import (
    MSME, DataSource, GSTRecord, UPIRecord, BankStatementRecord,
    InvoiceRecord, BusinessProfile, ConsentRecord
)
from app.database.db import SessionLocal, init_db


def seed_database():
    init_db()
    db = SessionLocal()
    try:
        _seed_msme_1(db)
        _seed_msme_2(db)
        _seed_msme_3(db)
        db.commit()
    finally:
        db.close()


def _get_or_create_msme(db: Session, gstin: str, defaults: dict) -> MSME:
    existing = db.query(MSME).filter(MSME.gstin == gstin).first()
    if existing:
        return existing
    msme = MSME(**defaults)
    db.add(msme)
    db.flush()
    return msme


def _seed_msme_1(db: Session):
    msme = _get_or_create_msme(db, "19AABCS1429B1ZX", {
        "business_name": "Sharma Textile Works",
        "owner_name": "Rajesh Sharma",
        "business_type": "Textile Manufacturing",
        "address": "42 Industrial Area, Sector 5",
        "city": "Kolkata",
        "state": "West Bengal",
        "gstin": "19AABCS1429B1ZX",
        "email": "rajesh@sharmatextiles.in",
        "phone": "+91-9876543210",
    })

    db.add(DataSource(msme_id=msme.id, source_type="gst", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="aa", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="upi", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="invoice", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="business", connected=True))

    db.add(GSTRecord(
        msme_id=msme.id, months_filed=11, total_months=12,
        turnover_annual=4200000, turnover_trend_percent=18,
        filings=[{"month": m, "status": "filed" if m < 11 else "pending"} for m in range(1, 13)]
    ))

    db.add(UPIRecord(
        msme_id=msme.id, avg_monthly_inflow=320000, avg_monthly_outflow=240000,
        monthly_transactions=847,
        transaction_history=[{"month": m, "inflow": 300000 + m * 3000} for m in range(1, 13)]
    ))

    db.add(BankStatementRecord(
        msme_id=msme.id, emi_burden_percent=22, bounced_payments=0,
        avg_balance=185000, balance_stability="stable", months_history=12
    ))

    db.add(InvoiceRecord(
        msme_id=msme.id, total_invoices=156, total_value=3800000,
        avg_value=24359, pending_percent=5
    ))

    db.add(BusinessProfile(
        msme_id=msme.id, years_in_business=8, employee_count=12,
        employee_delta_6m=3, description="Textile manufacturing with B2B contracts across West Bengal"
    ))

    db.add(ConsentRecord(
        msme_id=msme.id, consent_token="consent-sharma-001",
        data_sources=["gst", "aa", "upi", "invoice", "business"],
        purpose="Credit Readiness Assessment for IDBI Bank Loan Application",
        status="active"
    ))


def _seed_msme_2(db: Session):
    msme = _get_or_create_msme(db, "24AAACP3415G1ZK", {
        "business_name": "Patel Hardware Suppliers",
        "owner_name": "Amit Patel",
        "business_type": "Hardware Wholesale",
        "address": "7, Gandhi Nagar Market",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "gstin": "24AAACP3415G1ZK",
        "email": "amit@patelhardware.in",
        "phone": "+91-9876543211",
    })

    db.add(DataSource(msme_id=msme.id, source_type="gst", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="aa", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="upi", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="invoice", connected=False))
    db.add(DataSource(msme_id=msme.id, source_type="business", connected=True))

    db.add(GSTRecord(
        msme_id=msme.id, months_filed=9, total_months=12,
        turnover_annual=1800000, turnover_trend_percent=0,
        filings=[{"month": m, "status": "filed" if m <= 9 else "missed"} for m in range(1, 13)]
    ))

    db.add(UPIRecord(
        msme_id=msme.id, avg_monthly_inflow=110000, avg_monthly_outflow=95000,
        monthly_transactions=312,
        transaction_history=[{"month": m, "inflow": 100000 + (m % 3) * 15000} for m in range(1, 13)]
    ))

    db.add(BankStatementRecord(
        msme_id=msme.id, emi_burden_percent=38, bounced_payments=2,
        avg_balance=45000, balance_stability="moderate", months_history=10
    ))

    db.add(InvoiceRecord(
        msme_id=msme.id, total_invoices=48, total_value=1200000,
        avg_value=25000, pending_percent=18
    ))

    db.add(BusinessProfile(
        msme_id=msme.id, years_in_business=5, employee_count=5,
        employee_delta_6m=1, description="Hardware wholesale supplier serving retail stores in Gujarat"
    ))

    db.add(ConsentRecord(
        msme_id=msme.id, consent_token="consent-patel-001",
        data_sources=["gst", "aa", "upi", "business"],
        purpose="Credit Readiness Assessment for IDBI Bank Loan Application",
        status="active"
    ))


def _seed_msme_3(db: Session):
    msme = _get_or_create_msme(db, "27AAAFK2314H1ZM", {
        "business_name": "Khan Catering Services",
        "owner_name": "Imran Khan",
        "business_type": "Food & Catering",
        "address": "15, Hill Road, Bandra West",
        "city": "Mumbai",
        "state": "Maharashtra",
        "gstin": "27AAAFK2314H1ZM",
        "email": "imran@khancatering.in",
        "phone": "+91-9876543212",
    })

    db.add(DataSource(msme_id=msme.id, source_type="gst", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="aa", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="upi", connected=True))
    db.add(DataSource(msme_id=msme.id, source_type="invoice", connected=False))
    db.add(DataSource(msme_id=msme.id, source_type="business", connected=True))

    db.add(GSTRecord(
        msme_id=msme.id, months_filed=6, total_months=12,
        turnover_annual=800000, turnover_trend_percent=-15,
        filings=[{"month": m, "status": "filed" if m <= 6 and m % 2 == 0 else "missed"} for m in range(1, 13)]
    ))

    db.add(UPIRecord(
        msme_id=msme.id, avg_monthly_inflow=60000, avg_monthly_outflow=55000,
        monthly_transactions=98,
        transaction_history=[{"month": m, "inflow": 50000 + (m % 5) * 8000} for m in range(1, 13)]
    ))

    db.add(BankStatementRecord(
        msme_id=msme.id, emi_burden_percent=51, bounced_payments=4,
        avg_balance=12000, balance_stability="volatile", months_history=6
    ))

    db.add(BusinessProfile(
        msme_id=msme.id, years_in_business=2, employee_count=0,
        employee_delta_6m=0, description="Catering services for events and parties in Mumbai"
    ))

    db.add(ConsentRecord(
        msme_id=msme.id, consent_token="consent-khan-001",
        data_sources=["gst", "aa", "upi", "business"],
        purpose="Credit Readiness Assessment for IDBI Bank Loan Application",
        status="active"
    ))


if __name__ == "__main__":
    seed_database()
