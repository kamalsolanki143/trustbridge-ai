from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import (
    MSME, GSTRecord, UPIRecord, BankStatementRecord,
    InvoiceRecord, BusinessProfile, ConsentRecord,
    ReadinessAssessment, SubScore, RiskSignal, ReasonCode, DataSource
)
from app.schemas.readiness import (
    ReadinessAssessRequest, ReadinessResponse,
    CoverageMeterResponse, SubScoreResponse,
    RiskSignalResponse, ReasonCodeResponse, ReadinessHistoryResponse
)
from app.services.readiness_engine.readiness_grade import compute_readiness

router = APIRouter(prefix="/api/readiness", tags=["readiness"])


@router.post("/assess", response_model=ReadinessResponse)
def assess_readiness(req: ReadinessAssessRequest, db: Session = Depends(get_db)):
    msme = db.query(MSME).filter(MSME.gstin == req.gstin).first()
    if not msme:
        raise HTTPException(status_code=404, detail=f"MSME with GSTIN {req.gstin} not found")

    consent = db.query(ConsentRecord).filter(
        ConsentRecord.consent_token == req.consent_token,
        ConsentRecord.msme_id == msme.id,
    ).first()
    if not consent:
        raise HTTPException(status_code=403, detail="Invalid consent token")

    data_sources = db.query(DataSource).filter(
        DataSource.msme_id == msme.id,
        DataSource.connected == True,
    ).all()
    connected_sources = [ds.source_type for ds in data_sources]

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

    result = compute_readiness(
        gst_data=gst_data,
        bank_data=bank_data,
        upi_data=upi_data,
        invoice_data=invoice_data,
        business_data=business_data,
        business_name=msme.business_name,
        connected_sources=connected_sources,
    )

    assessment = ReadinessAssessment(
        msme_id=msme.id,
        score=result["score"],
        grade=result["grade"],
        confidence_band=result["confidence_band"],
        coverage_percent=result["coverage_meter"]["percentage"],
        coverage_connected=result["coverage_meter"]["connected"],
        coverage_total=result["coverage_meter"]["total"],
        credit_ladder_outcome=result["credit_ladder_outcome"],
        ai_summary=result["ai_summary"],
        data_sources_used=req.data_sources,
    )
    db.add(assessment)
    db.flush()

    for dim, score in result["sub_scores"].items():
        weights = {"cash_flow": 35, "compliance": 20, "repayment": 30, "growth": 15}
        db.add(SubScore(
            assessment_id=assessment.id,
            dimension=dim,
            score=score,
            max_score=25,
            weight_percent=weights.get(dim, 0),
        ))

    for signal in result["risk_signals"]:
        db.add(RiskSignal(
            assessment_id=assessment.id,
            signal_type=signal["type"],
            code=signal["code"],
            message=signal["message"],
        ))

    for code in result["reason_codes"]:
        db.add(ReasonCode(
            assessment_id=assessment.id,
            code_type=code["type"],
            code=code["code"],
            message=code["message"],
        ))

    db.commit()

    return _build_response(msme, assessment, result)


@router.get("/{msme_id}", response_model=ReadinessResponse)
def get_readiness(msme_id: str, db: Session = Depends(get_db)):
    assessment = db.query(ReadinessAssessment).filter(
        ReadinessAssessment.msme_id == msme_id
    ).order_by(ReadinessAssessment.created_at.desc()).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for this MSME")

    msme = db.query(MSME).filter(MSME.id == msme_id).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    result = _reconstruct_result(assessment, db)
    return _build_response(msme, assessment, result)


@router.get("/history/{gstin}", response_model=ReadinessHistoryResponse)
def get_readiness_history(gstin: str, db: Session = Depends(get_db)):
    msme = db.query(MSME).filter(MSME.gstin == gstin).first()
    if not msme:
        raise HTTPException(status_code=404, detail="MSME not found")

    assessments = db.query(ReadinessAssessment).filter(
        ReadinessAssessment.msme_id == msme.id
    ).order_by(ReadinessAssessment.created_at.desc()).all()

    results = []
    for assessment in assessments:
        result = _reconstruct_result(assessment, db)
        results.append(_build_response(msme, assessment, result))

    return ReadinessHistoryResponse(assessments=results)


def _build_response(msme: MSME, assessment: ReadinessAssessment, result: dict) -> ReadinessResponse:
    return ReadinessResponse(
        msme_id=msme.id,
        business_name=msme.business_name,
        readiness_grade=assessment.grade,
        score=assessment.score,
        confidence_band=assessment.confidence_band,
        coverage_meter=CoverageMeterResponse(
            connected=assessment.coverage_connected,
            total=assessment.coverage_total,
            percentage=assessment.coverage_percent,
        ),
        sub_scores=[
            SubScoreResponse(
                dimension=s.dimension, score=s.score,
                max_score=s.max_score, weight_percent=s.weight_percent,
            )
            for s in (assessment.sub_scores or [])
        ],
        risk_signals=[
            RiskSignalResponse(type=s.signal_type, code=s.code, message=s.message)
            for s in (assessment.risk_signals or [])
        ],
        reason_codes=[
            ReasonCodeResponse(type=s.code_type, code=s.code, message=s.message)
            for s in (assessment.reason_codes or [])
        ],
        credit_ladder_outcome=assessment.credit_ladder_outcome,
        ai_summary=assessment.ai_summary,
        created_at=assessment.created_at,
    )


def _reconstruct_result(assessment: ReadinessAssessment, db: Session) -> dict:
    sub_scores = {s.dimension: s.score for s in (assessment.sub_scores or [])}
    return {
        "score": assessment.score,
        "grade": assessment.grade,
        "sub_scores": sub_scores,
        "confidence_band": assessment.confidence_band,
        "coverage_meter": {
            "connected": assessment.coverage_connected,
            "total": assessment.coverage_total,
            "percentage": assessment.coverage_percent,
        },
        "risk_signals": [
            {"type": s.signal_type, "code": s.code, "message": s.message}
            for s in (assessment.risk_signals or [])
        ],
        "reason_codes": [
            {"type": s.code_type, "code": s.code, "message": s.message}
            for s in (assessment.reason_codes or [])
        ],
        "credit_ladder_outcome": assessment.credit_ladder_outcome,
        "ai_summary": assessment.ai_summary,
    }
