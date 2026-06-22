from backend.app.schemas.readiness import ReadinessProfile
from backend.app.schemas.recommendation import LadderDecision

# STUB — replace with real implementation from Krrish/Kamal's modules during integration

def get_readiness_profile(borrower_id: str) -> ReadinessProfile:
    """
    STUB - Fetches the credit readiness profile for a borrower.
    Matches Krrish's expected interface.
    """
    # Provide different profiles for testing different states
    if borrower_id == "borrower_review_abc" or "manual" in borrower_id:
        return ReadinessProfile(
            readiness_grade="C",
            confidence_band="Medium",
            coverage_pct=72.5,
            risk_signals=["High debt-to-income ratio", "Irregular transaction activity"],
            reason_codes=["DEBT_SPIKE", "INCONSISTENT_DEPOSITS"],
            stability_indicators=["GST active for 1 year", "Sole proprietorship status verified"]
        )
    elif "improve" in borrower_id:
        return ReadinessProfile(
            readiness_grade="D",
            confidence_band="Low",
            coverage_pct=50.0,
            risk_signals=["Multiple unpaid invoices", "Recent loan default indicator"],
            reason_codes=["OVERDUE_INVOICES", "LOW_BANK_COVERAGE"],
            stability_indicators=["Business active for 2+ years"]
        )
    else:
        # Standard qualified borrower
        return ReadinessProfile(
            readiness_grade="A",
            confidence_band="High",
            coverage_pct=95.0,
            risk_signals=["No major defaults"],
            reason_codes=["STABLE_INFLOWS", "CONSISTENT_GST", "HIGH_UPI_VOLUME"],
            stability_indicators=["3+ years operational history", "Consistent quarterly revenue growth"]
        )

def get_ladder_decision(borrower_id: str, lender_policy: str = "Balanced") -> LadderDecision:
    """
    STUB - Recomputes or fetches the ladder engine recommendation.
    Matches Kamal's expected interface.
    """
    profile = get_readiness_profile(borrower_id)
    
    # Simple rule-based mock matching lender policy & readiness grade
    grade = profile.readiness_grade
    
    if lender_policy == "Conservative":
        if grade == "A":
            decision = "Pre-Qualified"
        elif grade == "B":
            decision = "Starter Loan"
        elif grade == "C":
            decision = "Manual Review"
        else:
            decision = "Improve First"
    elif lender_policy == "Aggressive":
        if grade in ["A", "B"]:
            decision = "Pre-Qualified"
        elif grade == "C":
            decision = "Starter Loan"
        else:
            decision = "Manual Review"
    else: # Balanced
        if grade == "A":
            decision = "Pre-Qualified"
        elif grade == "B":
            decision = "Starter Loan"
        elif grade in ["C", "D"] and "manual" in borrower_id:
            decision = "Manual Review"
        elif grade == "C":
            decision = "Manual Review"
        else:
            decision = "Improve First"
            
    reason_codes = profile.reason_codes
    if decision == "Manual Review":
        reason_codes = reason_codes + ["MANUAL_REVIEW_ROUTING"]
    elif decision == "Improve First":
        reason_codes = reason_codes + ["IMPROVEMENT_REQUIRED"]
        
    return LadderDecision(
        decision=decision,
        reason_codes=reason_codes,
        borrower_id=borrower_id
    )

def get_growth_roadmap(borrower_id: str) -> dict:
    """
    STUB - Fetches the Dynamic Credit Growth Roadmap for the borrower.
    Matches Kamal's expected interface.
    """
    profile = get_readiness_profile(borrower_id)
    
    if profile.readiness_grade == "A":
        return {
            "current_stage": "Pre-Qualified",
            "next_goal": "Premium Tier Interest Rate Reductions",
            "milestones": [
                {"title": "Maintain GST consistency for next 3 months", "completed": True},
                {"title": "Increase digital invoicing to 100%", "completed": False, "impact": "High"}
            ],
            "tips": ["Ensure your UPI volume does not drop during seasonal fluctuations."]
        }
    else:
        return {
            "current_stage": "Starter Loan / Review Needed",
            "next_goal": "Qualify for Starter Loan with Standard Rates",
            "milestones": [
                {"title": "Clear any overdue invoices", "completed": False, "impact": "High"},
                {"title": "Submit additional bank statements via Account Aggregator", "completed": False, "impact": "Medium"}
            ],
            "tips": ["Connect your secondary UPI account to capture all revenue streams."]
        }
