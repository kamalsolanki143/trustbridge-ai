import json
import os
from typing import Optional

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sample_data")


def parse_gst_data(data: dict) -> dict:
    filings = data.get("filings", [])
    months_filed = sum(1 for f in filings if f.get("status") == "filed")

    return {
        "months_filed": months_filed,
        "total_months": data.get("total_months", 12),
        "turnover_annual": data.get("turnover_annual", 0),
        "turnover_trend_percent": data.get("turnover_trend_percent", 0),
        "filings": filings,
    }


def read_gst_data(gstin: Optional[str] = None) -> dict:
    filepath = os.path.join(SAMPLE_DATA_DIR, "gst_summary.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"GST summary not found at {filepath}")

    with open(filepath) as f:
        content = f.read().strip()
        if not content:
            raise ValueError("gst_summary.json is empty")

        data = json.loads(content)
        if gstin and data.get("gstin") != gstin:
            raise ValueError(f"GST data for GSTIN {gstin} not found")
        return parse_gst_data(data)
