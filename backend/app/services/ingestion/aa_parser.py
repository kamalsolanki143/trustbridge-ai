import json
import os
from typing import Optional

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "sample_data")


def parse_bank_statement(data: dict) -> dict:
    return {
        "emi_burden_percent": data.get("emi_burden_percent", 0),
        "bounced_payments": data.get("bounced_payments", 0),
        "avg_balance": data.get("avg_balance", 0),
        "balance_stability": data.get("balance_stability", "unknown"),
        "months_history": data.get("months_history", 0),
        "statement_data": data,
    }


def read_bank_statement(gstin: Optional[str] = None) -> dict:
    filepath = os.path.join(SAMPLE_DATA_DIR, "bank_statement.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Bank statement not found at {filepath}")

    with open(filepath) as f:
        content = f.read().strip()
        if not content:
            raise ValueError("bank_statement.json is empty")

        data = json.loads(content)
        if gstin and data.get("gstin") != gstin:
            raise ValueError(f"Bank statement for GSTIN {gstin} not found")
        return parse_bank_statement(data)
