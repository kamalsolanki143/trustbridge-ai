import os
from typing import Optional
from app.services.readiness_engine.coverage_meter import compute_coverage
from app.services.readiness_engine.confidence_band import compute_confidence_band
from app.services.readiness_engine.risk_signals import generate_risk_signals
from app.services.readiness_engine.reason_codes import generate_reason_codes

try:
    from app.services.ladder_engine.decision_engine import get_outcome as _get_outcome
except ImportError:

    def _get_outcome(score: int, confidence: str) -> str:
        if score >= 75 and confidence == "High":
            return "Pre-Qualified"
        elif score >= 50 and confidence in ("High", "Medium"):
            return "Starter Loan"
        elif score < 50 or confidence == "Low":
            return "Improve First"
        return "Manual Review"


GRADE_BANDS = [
    (90, "A+"), (80, "A"), (70, "A-"), (60, "B"),
    (50, "B-"), (40, "C+"), (30, "C"), (0, "D"),
]


def compute_cash_flow_score(gst_data: Optional[dict], upi_data: Optional[dict], bank_data: Optional[dict]) -> float:
    inflow_consistency = 0
    inflow_ratio_score = 0
    seasonality_penalty = 0

    if upi_data:
        monthly_transactions = upi_data.get("monthly_transactions", 0)
        inflow = upi_data.get("avg_monthly_inflow", 0)
        outflow = upi_data.get("avg_monthly_outflow", 0)

        if monthly_transactions >= 500:
            inflow_consistency = 10
        elif monthly_transactions >= 200:
            inflow_consistency = 7
        elif monthly_transactions >= 100:
            inflow_consistency = 4
        else:
            inflow_consistency = 2

        if outflow > 0:
            ratio = inflow / outflow
            if ratio >= 1.2:
                inflow_ratio_score = 8
            elif ratio >= 1.0:
                inflow_ratio_score = 6
            elif ratio >= 0.8:
                inflow_ratio_score = 4
            else:
                inflow_ratio_score = 2
        else:
            inflow_ratio_score = 4

        tx_history = upi_data.get("transaction_history", [])
        if len(tx_history) >= 6:
            inflows = [t.get("inflow", 0) for t in tx_history if isinstance(t, dict)]
            if inflows:
                avg = sum(inflows) / len(inflows)
                deviations = [abs(v - avg) / avg for v in inflows if avg > 0]
                if deviations:
                    avg_dev = sum(deviations) / len(deviations)
                    if avg_dev < 0.15:
                        inflow_consistency = max(inflow_consistency, 9)
                    elif avg_dev > 0.4:
                        seasonality_penalty = 5

    if gst_data:
        trend = gst_data.get("turnover_trend_percent", 0)
        if trend < -10:
            seasonality_penalty = max(seasonality_penalty, 4)

    if bank_data:
        stability = bank_data.get("balance_stability", "")
        if stability == "volatile":
            seasonality_penalty = max(seasonality_penalty, 3)

    score = inflow_consistency + inflow_ratio_score - seasonality_penalty
    return max(0, min(25, score))


def compute_compliance_score(gst_data: Optional[dict], business_data: Optional[dict]) -> float:
    gst_score = 0
    epfo_score = 0

    if gst_data:
        months_filed = gst_data.get("months_filed", 0)
        total_months = gst_data.get("total_months", 12)

        if total_months > 0:
            ratio = months_filed / total_months
            if ratio >= 0.9:
                gst_score = 15
            elif ratio >= 0.75:
                gst_score = 12
            elif ratio >= 0.5:
                gst_score = 8
            else:
                gst_score = 4

    if business_data:
        emp = business_data.get("employee_count", 0)
        emp_delta = business_data.get("employee_delta_6m", 0)

        if emp == 0:
            epfo_score = 2
        else:
            epfo_score = 8
            if emp_delta >= 0:
                epfo_score = 10

    return max(0, min(25, gst_score + epfo_score))


def compute_repayment_score(bank_data: Optional[dict]) -> float:
    if not bank_data:
        return 12

    emi = bank_data.get("emi_burden_percent", 0)
    bounced = bank_data.get("bounced_payments", 0)

    if emi < 30:
        emi_score = 25
    elif emi <= 40:
        emi_score = 18
    elif emi <= 50:
        emi_score = 10
    else:
        emi_score = 5

    bounced_penalty = bounced * 2
    return max(0, min(25, emi_score - bounced_penalty))


def compute_growth_score(gst_data: Optional[dict], business_data: Optional[dict]) -> float:
    revenue_trend_score = 0
    employee_delta_score = 0

    if gst_data:
        trend = gst_data.get("turnover_trend_percent", 0)
        if trend >= 20:
            revenue_trend_score = 15
        elif trend >= 10:
            revenue_trend_score = 12
        elif trend >= 5:
            revenue_trend_score = 9
        elif trend >= 0:
            revenue_trend_score = 6
        elif trend >= -10:
            revenue_trend_score = 3
        else:
            revenue_trend_score = 1

    if business_data:
        delta = business_data.get("employee_delta_6m", 0)
        if delta >= 5:
            employee_delta_score = 10
        elif delta >= 3:
            employee_delta_score = 8
        elif delta >= 1:
            employee_delta_score = 6
        elif delta == 0:
            employee_delta_score = 4
        else:
            employee_delta_score = 1

    return max(0, min(25, revenue_trend_score + employee_delta_score))


def determine_grade(score: int) -> str:
    for threshold, grade in GRADE_BANDS:
        if score >= threshold:
            return grade
    return "D"


def generate_ai_summary(
    business_name: str,
    grade: str,
    score: int,
    sub_scores: dict,
    risk_signals: list,
    reason_codes: list,
    outcome: str,
) -> str:
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return _fallback_summary(business_name, grade, score, sub_scores, outcome)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are an AI underwriting assistant for IDBI Bank. Generate a concise credit underwriting summary (2-3 paragraphs) for an MSME loan applicant.

Business: {business_name}
Credit Readiness Grade: {grade} (Score: {score}/100)
Sub-Scores: Cash Flow {sub_scores.get('cash_flow', 0)}/25, Compliance {sub_scores.get('compliance', 0)}/25, Repayment {sub_scores.get('repayment', 0)}/25, Growth {sub_scores.get('growth', 0)}/25
Risk Signals: {[s['message'] for s in risk_signals]}
Positive Factors: {[r['message'] for r in reason_codes if r['type'] == 'positive']}
Credit Ladder Outcome: {outcome}

Write in professional banking language. Include: key strengths, key risks, recommendation rationale, and suggested loan approach."""
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text if resp.content else _fallback_summary(business_name, grade, score, sub_scores, outcome)
    except Exception:
        return _fallback_summary(business_name, grade, score, sub_scores, outcome)


def _fallback_summary(
    business_name: str, grade: str, score: int, sub_scores: dict, outcome: str
) -> str:
    return (
        f"{business_name} has a credit readiness grade of {grade} (Score: {score}/100). "
        f"The business demonstrates {sub_scores.get('cash_flow', 0)}/25 in cash flow strength, "
        f"{sub_scores.get('compliance', 0)}/25 in compliance, "
        f"{sub_scores.get('repayment', 0)}/25 in repayment capacity, and "
        f"{sub_scores.get('growth', 0)}/25 in growth trajectory. "
        f"Recommended outcome: {outcome}."
    )


def compute_readiness(
    gst_data: Optional[dict] = None,
    bank_data: Optional[dict] = None,
    upi_data: Optional[dict] = None,
    invoice_data: Optional[dict] = None,
    business_data: Optional[dict] = None,
    business_name: str = "",
    connected_sources: Optional[list] = None,
) -> dict:
    if connected_sources is None:
        connected_sources = []

    cash_flow = compute_cash_flow_score(gst_data, upi_data, bank_data)
    compliance = compute_compliance_score(gst_data, business_data)
    repayment = compute_repayment_score(bank_data)
    growth = compute_growth_score(gst_data, business_data)

    total_score = round(
        (cash_flow * 0.35 + compliance * 0.20 + repayment * 0.30 + growth * 0.15) * 4
    )
    grade = determine_grade(total_score)

    coverage = compute_coverage(connected_sources)

    months_history = 0
    if bank_data:
        months_history = max(months_history, bank_data.get("months_history", 0))
    if upi_data:
        tx_history = upi_data.get("transaction_history", [])
        months_history = max(months_history, len(tx_history))
    if gst_data:
        months_history = max(months_history, gst_data.get("months_filed", 0))

    confidence = compute_confidence_band(connected_sources, months_history)
    risk_signals = generate_risk_signals(gst_data, bank_data, upi_data, invoice_data, business_data)
    reason_codes = generate_reason_codes(cash_flow, compliance, repayment, growth, gst_data, bank_data, upi_data, business_data)

    outcome = _get_outcome(total_score, confidence)
    has_anomaly = any(s["type"] == "critical" for s in risk_signals)
    missing_gst = "gst" not in connected_sources
    missing_aa = "aa" not in connected_sources
    missing_bank_stmt = bank_data is None
    if (has_anomaly or missing_gst or missing_aa or missing_bank_stmt) and outcome != "Manual Review":
        outcome = "Manual Review"

    ai_summary = generate_ai_summary(
        business_name, grade, total_score,
        {"cash_flow": cash_flow, "compliance": compliance, "repayment": repayment, "growth": growth},
        risk_signals, reason_codes, outcome,
    )

    return {
        "score": total_score,
        "grade": grade,
        "sub_scores": {
            "cash_flow": cash_flow,
            "compliance": compliance,
            "repayment": repayment,
            "growth": growth,
        },
        "confidence_band": confidence,
        "coverage_meter": coverage,
        "risk_signals": risk_signals,
        "reason_codes": reason_codes,
        "credit_ladder_outcome": outcome,
        "ai_summary": ai_summary,
    }
