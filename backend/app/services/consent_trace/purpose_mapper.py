# Canonical purpose-per-source mapping as defined in product specification
PURPOSE_MAP = {
    "bank_statements": "Cash Flow Stability Assessment",
    "gst": "Business Activity Verification",
    "upi": "Revenue Consistency Analysis",
    "invoices": "Customer Concentration & Collection Analysis",
    "business_profile": "Identity & Stability Verification"
}

def get_purpose_for_source(data_source: str) -> str:
    """
    Returns the canonical purpose for a given data source.
    """
    key = data_source.strip().lower()
    return PURPOSE_MAP.get(key, "General Credit Assessment")

def is_usage_permitted(data_source: str, intended_purpose: str) -> bool:
    """
    Checks if a given data source is permitted to be used for the intended purpose.
    Ensures purpose-limited data usage.
    """
    key = data_source.strip().lower()
    canonical_purpose = PURPOSE_MAP.get(key)
    if not canonical_purpose:
        return False
    return canonical_purpose.lower() == intended_purpose.strip().lower()
