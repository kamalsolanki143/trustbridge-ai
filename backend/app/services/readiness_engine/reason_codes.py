from typing import Optional


def generate_reason_codes(
    cash_flow_score: float,
    compliance_score: float,
    repayment_score: float,
    growth_score: float,
    gst_data: Optional[dict] = None,
    bank_data: Optional[dict] = None,
    upi_data: Optional[dict] = None,
    business_data: Optional[dict] = None,
) -> list[dict]:
    reasons = []

    if cash_flow_score >= 18:
        reasons.append({
            "type": "positive",
            "code": "STRONG_CASH_FLOW",
            "message": "Consistent and healthy cash flow from business operations",
        })
    elif cash_flow_score >= 12:
        reasons.append({
            "type": "neutral",
            "code": "MODERATE_CASH_FLOW",
            "message": "Cash flow is adequate but has room for improvement",
        })
    else:
        reasons.append({
            "type": "negative",
            "code": "WEAK_CASH_FLOW",
            "message": "Irregular or low cash flow impacts credit capacity",
        })

    if compliance_score >= 18:
        reasons.append({
            "type": "positive",
            "code": "STRONG_COMPLIANCE",
            "message": "Regular GST filings and EPFO contributions demonstrate compliance",
        })
    elif compliance_score >= 12:
        reasons.append({
            "type": "neutral",
            "code": "MODERATE_COMPLIANCE",
            "message": "Compliance is acceptable but filing regularity can improve",
        })
    else:
        reasons.append({
            "type": "negative",
            "code": "WEAK_COMPLIANCE",
            "message": "GST filing gaps and/or EPFO irregularities detected",
        })

    if repayment_score >= 18:
        reasons.append({
            "type": "positive",
            "code": "STRONG_REPAYMENT",
            "message": "Low EMI burden with no bounced payments — strong repayment capacity",
        })
    elif repayment_score >= 12:
        reasons.append({
            "type": "neutral",
            "code": "MODERATE_REPAYMENT",
            "message": "Repayment history shows some stress but manageable",
        })
    else:
        reasons.append({
            "type": "negative",
            "code": "WEAK_REPAYMENT",
            "message": "High EMI burden or bounced payments indicate repayment risk",
        })

    if growth_score >= 18:
        reasons.append({
            "type": "positive",
            "code": "STRONG_GROWTH",
            "message": "Business showing solid revenue and team growth trajectory",
        })
    elif growth_score >= 12:
        reasons.append({
            "type": "neutral",
            "code": "STABLE_GROWTH",
            "message": "Business is stable with modest growth indicators",
        })
    else:
        reasons.append({
            "type": "negative",
            "code": "STAGNANT_GROWTH",
            "message": "Limited growth signals — revenue or headcount not expanding",
        })

    if upi_data:
        monthly_txns = upi_data.get("monthly_transactions", 0)
        if monthly_txns > 500:
            reasons.append({
                "type": "positive",
                "code": "HIGH_DIGITAL_FOOTPRINT",
                "message": f"Strong digital transaction history with ~{monthly_txns} monthly UPI payments",
            })

    if bank_data:
        if bank_data.get("emi_burden_percent", 0) < 25:
            reasons.append({
                "type": "positive",
                "code": "LOW_DEBT_BURDEN",
                "message": "Existing debt obligations are well within safe limits",
            })

    if gst_data:
        months_filed = gst_data.get("months_filed", 0)
        total_months = gst_data.get("total_months", 12)
        if months_filed == total_months:
            reasons.append({
                "type": "positive",
                "code": "PERFECT_GST_RECORD",
                "message": "All GST filings completed on time for the past year",
            })

    if business_data:
        emp = business_data.get("employee_count", 0)
        if emp >= 10:
            reasons.append({
                "type": "positive",
                "code": "ESTABLISHED_WORKFORCE",
                "message": f"Business employs {emp} people, indicating scale and stability",
            })

    return reasons
