import pytest
from app.services.readiness_engine.readiness_grade import (
    compute_readiness,
    compute_cash_flow_score,
    compute_compliance_score,
    compute_repayment_score,
    compute_growth_score
)

def test_compute_cash_flow_score():
    # Good cash flow: high transaction counts, positive ratio, low deviation
    upi_good = {
        "monthly_transactions": 600,
        "avg_monthly_inflow": 120000.0,
        "avg_monthly_outflow": 100000.0,
        "transaction_history": [
            {"inflow": 120000}, {"inflow": 122000}, {"inflow": 118000},
            {"inflow": 125000}, {"inflow": 121000}, {"inflow": 119000}
        ]
    }
    score = compute_cash_flow_score(gst_data=None, upi_data=upi_good, bank_data=None)
    assert score == 18.0 # 10 (txn count) + 8 (ratio >= 1.2) - 0 (no penalty)

    # Volatile cash flow with penalties
    upi_volatile = {
        "monthly_transactions": 50,
        "avg_monthly_inflow": 50000.0,
        "avg_monthly_outflow": 70000.0,
        "transaction_history": [
            {"inflow": 90000}, {"inflow": 20000}, {"inflow": 80000},
            {"inflow": 15000}, {"inflow": 70000}, {"inflow": 25000}
        ] # highly volatile
    }
    gst_declining = {"turnover_trend_percent": -15}
    bank_volatile = {"balance_stability": "volatile"}
    score_bad = compute_cash_flow_score(gst_data=gst_declining, upi_data=upi_volatile, bank_data=bank_volatile)
    # 2 (low txn) + 2 (ratio < 0.8) - 5 (deviation > 0.4 penalty) - 4 (GST decline penalty) -> min score is 0
    assert score_bad == 0.0

def test_compute_compliance_score():
    # Perfect compliance: 100% GST files, active EPFO workforce
    gst_good = {"months_filed": 12, "total_months": 12}
    biz_good = {"employee_count": 10, "employee_delta_6m": 2}
    score = compute_compliance_score(gst_good, biz_good)
    assert score == 25.0 # 15 (GST ratio >= 0.9) + 10 (EPFO stable/growing)

    # Low compliance: missed filing, no employees
    gst_bad = {"months_filed": 5, "total_months": 12} # ratio < 0.5
    biz_bad = {"employee_count": 0, "employee_delta_6m": 0}
    score_bad = compute_compliance_score(gst_bad, biz_bad)
    assert score_bad == 6.0 # 4 (GST) + 2 (EPFO)

def test_compute_repayment_score():
    # Strong repayment: low debt service, no bounces
    bank_good = {"emi_burden_percent": 15, "bounced_payments": 0}
    score = compute_repayment_score(bank_good)
    assert score == 25.0

    # Risky repayment: high debt, multiple bounces
    bank_bad = {"emi_burden_percent": 45, "bounced_payments": 3}
    score_bad = compute_repayment_score(bank_bad)
    assert score_bad == 4.0 # 10 (EMI > 40) - 6 (3 bounces * 2)

def test_compute_growth_score():
    # High growth
    gst_good = {"turnover_trend_percent": 25}
    biz_good = {"employee_delta_6m": 6}
    score = compute_growth_score(gst_good, biz_good)
    assert score == 25.0 # 15 (trend >= 20) + 10 (delta >= 5)

    # Declining growth
    gst_bad = {"turnover_trend_percent": -15}
    biz_bad = {"employee_delta_6m": -2}
    score_bad = compute_growth_score(gst_bad, biz_bad)
    assert score_bad == 2.0 # 1 (trend) + 1 (headcount drop)

def test_complete_readiness_good_business():
    # Simulates Sharma Textile Works (A+ profile)
    res = compute_readiness(
        gst_data={"months_filed": 11, "total_months": 12, "turnover_annual": 4200000, "turnover_trend_percent": 18},
        bank_data={"emi_burden_percent": 22, "bounced_payments": 0, "avg_balance": 185000, "balance_stability": "stable", "months_history": 12},
        upi_data={"avg_monthly_inflow": 320000, "avg_monthly_outflow": 240000, "monthly_transactions": 847, "transaction_history": [{"inflow": 320000} for _ in range(12)]},
        invoice_data={"total_invoices": 156, "total_value": 3800000, "avg_value": 24359, "pending_percent": 5},
        business_data={"years_in_business": 8, "employee_count": 12, "employee_delta_6m": 3},
        business_name="Sharma Textile Works",
        connected_sources=["gst", "aa", "upi", "invoice", "business"]
    )
    assert res["score"] >= 80
    assert res["grade"] in ("A", "A+", "A-")
    assert res["confidence_band"] == "High"
    assert res["credit_ladder_outcome"] == "Pre-Qualified"
    assert len(res["risk_signals"]) == 0

def test_complete_readiness_high_risk():
    # Simulates Khan Catering Services (D profile)
    res = compute_readiness(
        gst_data={"months_filed": 6, "total_months": 12, "turnover_annual": 800000, "turnover_trend_percent": -15},
        bank_data={"emi_burden_percent": 51, "bounced_payments": 4, "avg_balance": 12000, "balance_stability": "volatile", "months_history": 6},
        upi_data={"avg_monthly_inflow": 60000, "avg_monthly_outflow": 55000, "monthly_transactions": 98, "transaction_history": [{"inflow": 60000} for _ in range(6)]},
        invoice_data=None,
        business_data={"years_in_business": 2, "employee_count": 0, "employee_delta_6m": 0},
        business_name="Khan Catering Services",
        connected_sources=["gst", "aa", "upi", "business"]
    )
    assert res["score"] < 50
    assert res["grade"] in ("C", "D")
    assert res["confidence_band"] == "Medium"
    # Auto-routes to Manual Review due to bounces & high EMI
    assert res["credit_ladder_outcome"] == "Manual Review"
    
    # Assert presence of critical risk signals
    signal_codes = [s["code"] for s in res["risk_signals"]]
    assert "LOW_GST_COMPLIANCE" in signal_codes or "MODERATE_GST_GAP" in signal_codes
    assert "MULTIPLE_BOUNCES" in signal_codes
    assert "HIGH_EMI_BURDEN" in signal_codes

def test_readiness_edge_cases_empty():
    # All data missing or disconnected
    res = compute_readiness(
        gst_data=None,
        bank_data=None,
        upi_data=None,
        invoice_data=None,
        business_data=None,
        business_name="New Business Inc",
        connected_sources=[]
    )
    assert res["score"] <= 50
    assert res["confidence_band"] == "Low"
    assert res["credit_ladder_outcome"] == "Manual Review" # overrides to manual review due to missing bank statement data
