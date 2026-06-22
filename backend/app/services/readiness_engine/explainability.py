def explain_grade(grade: str, score: int) -> str:
    explanations = {
        "A+": "Exceptional credit readiness. The business demonstrates outstanding financial health across all dimensions.",
        "A": "Strong credit readiness. The business is well-positioned for lending with healthy financial indicators.",
        "A-": "Good credit readiness. Minor areas for improvement but overall a solid candidate for credit.",
        "B": "Adequate credit readiness. The business meets basic thresholds but has identifiable areas for strengthening.",
        "B-": "Below-average credit readiness. Several areas need attention before the business is optimally positioned.",
        "C+": "Limited credit readiness. Significant gaps exist in financial behavior that need to be addressed.",
        "C": "Weak credit readiness. Major concerns across multiple dimensions of credit health.",
        "D": "Poor credit readiness. Substantial improvements required across all financial areas.",
    }
    return explanations.get(grade, "Unable to determine readiness level.")


def explain_dimension(dimension: str, score: float, max_score: float = 25) -> str:
    ratio = score / max_score if max_score > 0 else 0
    descriptions = {
        "cash_flow": {
            "high": "Strong cash flow with consistent inflows and healthy surplus.",
            "medium": "Adequate cash flow but some inconsistency or narrow margins.",
            "low": "Weak cash flow with irregular inflows or high outflows relative to income.",
        },
        "compliance": {
            "high": "Excellent compliance — timely GST filings and EPFO contributions.",
            "medium": "Moderate compliance — some gaps in filing or contribution regularity.",
            "low": "Poor compliance — significant gaps in GST or EPFO obligations.",
        },
        "repayment": {
            "high": "Strong repayment capacity with low EMI burden and clean payment history.",
            "medium": "Moderate repayment capacity — some EMI stress or minor bounce history.",
            "low": "Weak repayment capacity — high debt burden or multiple bounced payments.",
        },
        "growth": {
            "high": "Strong growth trajectory with rising revenue and expanding team.",
            "medium": "Stable but modest growth — room for expansion.",
            "low": "Limited or declining growth indicators.",
        },
    }

    dim = descriptions.get(dimension, {})
    if ratio >= 0.7:
        return dim.get("high", "Good performance in this area.")
    elif ratio >= 0.4:
        return dim.get("medium", "Adequate performance with room for improvement.")
    else:
        return dim.get("low", "Significant improvement needed in this area.")


def explain_outcome(outcome: str) -> str:
    outcomes = {
        "Pre-Qualified": (
            "The borrower meets all key criteria for a standard loan product. "
            "Proceed with full application processing."
        ),
        "Starter Loan": (
            "The borrower qualifies for a starter/product-trial loan with "
            "adjusted terms. Consider lower ticket size or higher monitoring."
        ),
        "Improve First": (
            "The borrower does not meet minimum readiness thresholds. "
            "Recommend borrower follows the growth roadmap before reapplying."
        ),
        "Manual Review": (
            "Anomaly flags or missing critical data require human underwriter "
            "review before proceeding."
        ),
    }
    return outcomes.get(outcome, "Recommendation pending further analysis.")
