from typing import List, Dict, Any

def get_predefined_scenarios() -> List[Dict[str, Any]]:
    """
    Returns a list of structured credit improvement scenario templates.
    """
    return [
        {
            "id": "clear_bounces",
            "name": "Clear Bounced Checks",
            "description": "Demonstrates the score increase if the borrower has zero bounced checks.",
            "adjustments": {
                "bounced_payments": 0
            }
        },
        {
            "id": "connect_invoices",
            "name": "Integrate Digital Invoicing",
            "description": "Connects accounts receivable billing software to maximize data density.",
            "adjustments": {
                "connect_invoices": True
            }
        },
        {
            "id": "boost_upi",
            "name": "Increase UPI Velocity",
            "description": "Models a boost in digital business payments to 500+ transactions monthly.",
            "adjustments": {
                "monthly_transactions": 550
            }
        },
        {
            "id": "reduce_debt",
            "name": "De-leverage / Paydown EMI",
            "description": "Simulates paying down outstanding credits to reduce monthly EMI burden below 30%.",
            "adjustments": {
                "emi_burden_percent": 20.0
            }
        }
    ]
