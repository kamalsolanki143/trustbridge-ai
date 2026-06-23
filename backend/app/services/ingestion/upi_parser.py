import json
import os
from typing import Optional

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sample_data")


def parse_upi_data(data: dict) -> dict:
    return {
        "avg_monthly_inflow": data.get("avg_monthly_inflow", 0),
        "avg_monthly_outflow": data.get("avg_monthly_outflow", 0),
        "monthly_transactions": data.get("monthly_transactions", 0),
        "transaction_history": data.get("transaction_history", []),
    }


def read_upi_data(gstin: Optional[str] = None) -> dict:
    filepath = os.path.join(SAMPLE_DATA_DIR, "upi_transactions.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"UPI data not found at {filepath}")

    with open(filepath) as f:
        content = f.read().strip()
        if not content:
            raise ValueError("upi_transactions.json is empty")

        data = json.loads(content)
        if gstin and data.get("gstin") != gstin:
            raise ValueError(f"UPI data for GSTIN {gstin} not found")
        return parse_upi_data(data)
