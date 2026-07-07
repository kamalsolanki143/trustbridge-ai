from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.database.models import (
    MSME, GSTRecord, UPIRecord, BankStatementRecord,
    InvoiceRecord, BusinessProfile, DataSource
)
from app.services.readiness_engine.readiness_grade import compute_readiness

def run_simulation(
    db: Session,
    gstin: str,
    adjustments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Loads MSME details, applies adjustments (e.g. clearing bounces, increasing UPI transactions),
    re-runs compute_readiness, and reports projected outcomes and delta improvements.
    """
    msme = db.query(MSME).filter(MSME.gstin == gstin).first()
    if not msme:
        raise ValueError(f"MSME with GSTIN {gstin} not found")

    # 1. Fetch connected sources
    data_sources = db.query(DataSource).filter(DataSource.msme_id == msme.id).all()
    connected_sources = [ds.source_type for ds in data_sources if ds.connected]

    # 2. Extract base data dictionaries
    gst_data = None
    gst_record = db.query(GSTRecord).filter(GSTRecord.msme_id == msme.id).first()
    if gst_record:
        gst_data = {
            "months_filed": gst_record.months_filed,
            "total_months": gst_record.total_months,
            "turnover_annual": gst_record.turnover_annual,
            "turnover_trend_percent": gst_record.turnover_trend_percent,
            "filings": gst_record.filings or [],
        }

    upi_data = None
    upi_record = db.query(UPIRecord).filter(UPIRecord.msme_id == msme.id).first()
    if upi_record:
        upi_data = {
            "avg_monthly_inflow": upi_record.avg_monthly_inflow,
            "avg_monthly_outflow": upi_record.avg_monthly_outflow,
            "monthly_transactions": upi_record.monthly_transactions,
            "transaction_history": upi_record.transaction_history or [],
        }

    bank_data = None
    bank_record = db.query(BankStatementRecord).filter(BankStatementRecord.msme_id == msme.id).first()
    if bank_record:
        bank_data = {
            "emi_burden_percent": bank_record.emi_burden_percent,
            "bounced_payments": bank_record.bounced_payments,
            "avg_balance": bank_record.avg_balance,
            "balance_stability": bank_record.balance_stability,
            "months_history": bank_record.months_history,
        }

    invoice_data = None
    invoice_record = db.query(InvoiceRecord).filter(InvoiceRecord.msme_id == msme.id).first()
    if invoice_record:
        invoice_data = {
            "total_invoices": invoice_record.total_invoices,
            "total_value": invoice_record.total_value,
            "avg_value": invoice_record.avg_value,
            "pending_percent": invoice_record.pending_percent,
        }

    business_data = None
    business_record = db.query(BusinessProfile).filter(BusinessProfile.msme_id == msme.id).first()
    if business_record:
        business_data = {
            "years_in_business": business_record.years_in_business,
            "employee_count": business_record.employee_count,
            "employee_delta_6m": business_record.employee_delta_6m,
            "description": business_record.description or "",
        }

    # 3. Compute baseline score first to find delta
    base_result = compute_readiness(
        gst_data=gst_data,
        bank_data=bank_data,
        upi_data=upi_data,
        invoice_data=invoice_data,
        business_data=business_data,
        business_name=msme.business_name,
        connected_sources=connected_sources,
    )
    base_score = base_result["score"]

    # 4. Apply Adjustments
    improvements = []
    
    # Connection adjustments
    if adjustments.get("connect_invoices") and "invoice" not in connected_sources:
        connected_sources.append("invoice")
        improvements.append("Integrating digital invoices increases alternative Data Coverage to 100%.")
        if not invoice_data:
            invoice_data = {
                "total_invoices": 12,
                "total_value": 300000.0,
                "avg_value": 25000.0,
                "pending_percent": 5.0
            }
            
    if adjustments.get("connect_gst") and "gst" not in connected_sources:
        connected_sources.append("gst")
        improvements.append("Connecting GST tax portal data sources.")
        
    if adjustments.get("connect_aa") and "aa" not in connected_sources:
        connected_sources.append("aa")
        improvements.append("Authorizing Account Aggregator connection.")

    # Metric adjustments
    if "bounced_payments" in adjustments and bank_data:
        old_val = bank_data["bounced_payments"]
        new_val = adjustments["bounced_payments"]
        if new_val < old_val:
            bank_data["bounced_payments"] = new_val
            diff = old_val - new_val
            improvements.append(f"Clearing {diff} bounced payment(s) from record improves Repayment Score.")

    if "turnover_trend_percent" in adjustments and gst_data:
        old_val = gst_data["turnover_trend_percent"]
        new_val = adjustments["turnover_trend_percent"]
        if new_val > old_val:
            gst_data["turnover_trend_percent"] = new_val
            improvements.append(f"Increasing revenue growth trajectory trend to +{new_val}% improves Growth Score.")

    if "monthly_transactions" in adjustments and upi_data:
        old_val = upi_data["monthly_transactions"]
        new_val = adjustments["monthly_transactions"]
        if new_val > old_val:
            upi_data["monthly_transactions"] = new_val
            improvements.append(f"Increasing monthly UPI transaction frequency to {new_val} improves Cash Flow Score.")

    if "emi_burden_percent" in adjustments and bank_data:
        old_val = bank_data["emi_burden_percent"]
        new_val = adjustments["emi_burden_percent"]
        if new_val < old_val:
            bank_data["emi_burden_percent"] = new_val
            improvements.append(f"Reducing existing debt service EMI burden to {new_val}% improves Repayment Score.")

    # 5. Recompute score
    projected_result = compute_readiness(
        gst_data=gst_data,
        bank_data=bank_data,
        upi_data=upi_data,
        invoice_data=invoice_data,
        business_data=business_data,
        business_name=msme.business_name,
        connected_sources=connected_sources,
    )

    projected_score = projected_result["score"]
    projected_grade = projected_result["grade"]
    projected_outcome = projected_result["credit_ladder_outcome"]
    delta_score = projected_score - base_score

    if not improvements:
        improvements.append("No metrics were changed. Projected readiness remains identical to baseline.")

    return {
        "projected_score": projected_score,
        "projected_grade": projected_grade,
        "projected_outcome": projected_outcome,
        "delta_score": delta_score,
        "improvements": improvements
    }
