import json
import os
from typing import Optional

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sample_data")


def parse_invoice_data(data: dict) -> dict:
    return {
        "total_invoices": data.get("total_invoices", 0),
        "total_value": data.get("total_value", 0),
        "avg_value": data.get("avg_value", 0),
        "pending_percent": data.get("pending_percent", 0),
    }


def read_invoice_data(gstin: Optional[str] = None) -> dict:
    filepath = os.path.join(SAMPLE_DATA_DIR, "invoices.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Invoice data not found at {filepath}")

    with open(filepath) as f:
        content = f.read().strip()
        if not content:
            raise ValueError("invoices.json is empty")

        data = json.loads(content)
        if gstin and data.get("gstin") != gstin:
            raise ValueError(f"Invoice data for GSTIN {gstin} not found")
        return parse_invoice_data(data)
