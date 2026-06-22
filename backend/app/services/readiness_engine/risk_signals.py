from typing import Optional


def generate_risk_signals(
    gst_data: Optional[dict] = None,
    bank_data: Optional[dict] = None,
    upi_data: Optional[dict] = None,
    invoice_data: Optional[dict] = None,
    business_data: Optional[dict] = None,
) -> list[dict]:
    signals = []

    if gst_data:
        months_filed = gst_data.get("months_filed", 0)
        total_months = gst_data.get("total_months", 12)
        if months_filed < total_months * 0.5:
            signals.append({
                "type": "critical",
                "code": "LOW_GST_COMPLIANCE",
                "message": f"GST filed only {months_filed}/{total_months} months",
            })
        elif months_filed < total_months * 0.75:
            signals.append({
                "type": "warning",
                "code": "MODERATE_GST_GAP",
                "message": f"GST filed {months_filed}/{total_months} months, improvement needed",
            })

        trend = gst_data.get("turnover_trend_percent", 0)
        if trend < -10:
            signals.append({
                "type": "critical",
                "code": "REVENUE_DECLINE",
                "message": f"Revenue declining at {trend}% over 6 months",
            })
        elif trend < 0:
            signals.append({
                "type": "warning",
                "code": "SLIGHT_REVENUE_DIP",
                "message": f"Revenue slightly declined by {trend}%",
            })

        if gst_data.get("turnover_annual", 0) < 500000:
            signals.append({
                "type": "warning",
                "code": "LOW_TURNOVER",
                "message": "Annual turnover below ₹5L, limited credit capacity",
            })

    if bank_data:
        emi = bank_data.get("emi_burden_percent", 0)
        if emi > 50:
            signals.append({
                "type": "critical",
                "code": "HIGH_EMI_BURDEN",
                "message": f"EMI burden at {emi}% of inflows, severe repayment stress",
            })
        elif emi > 40:
            signals.append({
                "type": "warning",
                "code": "ELEVATED_EMI",
                "message": f"EMI burden at {emi}% of inflows, above safe threshold",
            })

        bounced = bank_data.get("bounced_payments", 0)
        if bounced >= 3:
            signals.append({
                "type": "critical",
                "code": "MULTIPLE_BOUNCES",
                "message": f"{bounced} bounced payments detected",
            })
        elif bounced > 0:
            signals.append({
                "type": "warning",
                "code": "BOUNCE_HISTORY",
                "message": f"{bounced} bounced payment(s) on record",
            })

        stability = bank_data.get("balance_stability", "")
        if stability == "volatile":
            signals.append({
                "type": "warning",
                "code": "VOLATILE_BALANCE",
                "message": "Bank balance shows high volatility",
            })

    if upi_data:
        inflow = upi_data.get("avg_monthly_inflow", 0)
        if inflow < 50000:
            signals.append({
                "type": "warning",
                "code": "LOW_UPI_INFLOW",
                "message": "Average monthly UPI inflow below ₹50,000",
            })

        txns = upi_data.get("monthly_transactions", 0)
        if txns < 100:
            signals.append({
                "type": "warning",
                "code": "LOW_UPI_VOLUME",
                "message": f"Only ~{txns} UPI transactions/month, limited digital footprint",
            })

    if invoice_data:
        pending = invoice_data.get("pending_percent", 0)
        if pending > 30:
            signals.append({
                "type": "warning",
                "code": "HIGH_PENDING_INVOICES",
                "message": f"{pending}% of invoices are pending",
            })

    if business_data:
        emp = business_data.get("employee_count", 0)
        if emp == 0:
            signals.append({
                "type": "warning",
                "code": "NO_EMPLOYEES",
                "message": "No employees registered (EPFO not applicable)",
            })
        elif emp < 3:
            signals.append({
                "type": "warning",
                "code": "SMALL_TEAM",
                "message": "Micro business with fewer than 3 employees",
            })

        years = business_data.get("years_in_business", 0)
        if years < 2:
            signals.append({
                "type": "warning",
                "code": "EARLY_STAGE",
                "message": "Business operating less than 2 years",
            })

    return signals
