import os
import logging

logger = logging.getLogger(__name__)

# STUB — replace with real Gemini client or integration once shared client exists

def generate(prompt: str, **kwargs) -> str:
    """
    Call Gemini 2.5 Pro to generate text. Falls back to a structured mock
    if the API key or library is not available.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment. Falling back to mock narrative.")
        return generate_mock_underwriting_summary(prompt)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # Using gemini-2.5-pro or similar model
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}. Falling back to mock narrative.")
        return generate_mock_underwriting_summary(prompt)

def generate_mock_underwriting_summary(prompt: str) -> str:
    """
    Parses the prompt text for key metrics to return a highly realistic mock narrative.
    """
    if "Readiness Grade: A" in prompt or "Readiness Grade: B" in prompt:
        return (
            "The borrower demonstrates strong cashflow stability with consistent digital transactions "
            "across UPI and verified bank statements. GST activity is regular, indicating active operational "
            "business standing. Due to the high data coverage and absence of negative risk signals, "
            "the merchant is recommended for pre-qualification or a standard starter tier loan."
        )
    elif "Readiness Grade: C" in prompt:
        return (
            "The business shows moderate transactional activity, but displays risk signals such as "
            "irregular deposit patterns and an elevated debt-to-income ratio. While GST filings are present, "
            "cashflow volatility remains a concern. A manual underwriting review is recommended to assess "
            "collateral eligibility and seasonal cash constraints before extending credit."
        )
    else:
        return (
            "The borrower has low data coverage and multiple risk flags, including overdue invoices and "
            "recent bank ledger anomalies. Verification of business stability remains incomplete. It is "
            "recommended to defer credit approval and outline a clear roadmap for data connection and "
            "repayment discipline."
        )
