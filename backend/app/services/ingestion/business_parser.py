import json
import os
from typing import Optional

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sample_data")


def parse_business_profile(data: dict) -> dict:
    return {
        "years_in_business": data.get("years_in_business", 0),
        "employee_count": data.get("employee_count", 0),
        "employee_delta_6m": data.get("employee_delta_6m", 0),
        "description": data.get("description", ""),
        "business_type": data.get("business_type", ""),
        "address": data.get("address", ""),
        "city": data.get("city", ""),
        "state": data.get("state", ""),
    }


def read_business_profile(gstin: Optional[str] = None) -> dict:
    filepath = os.path.join(SAMPLE_DATA_DIR, "business_profile.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Business profile not found at {filepath}")

    with open(filepath) as f:
        content = f.read().strip()
        if not content:
            raise ValueError("business_profile.json is empty")

        data = json.loads(content)
        if gstin:
            if data.get("gstin") != gstin:
                raise ValueError(f"Business profile for GSTIN {gstin} not found")
        return parse_business_profile(data)
