import pytest
from httpx import AsyncClient
from app.database.db import SessionLocal
from app.database.models import MSME
from app.database.seed import seed_database

# Guarantee that the database has seeded MSME profiles before running tests
@pytest.fixture(scope="module", autouse=True)
def ensure_db_seeded():
    db = SessionLocal()
    try:
        sharma_exists = db.query(MSME).filter(MSME.gstin == "19AABCS1429B1ZX").first()
        patel_exists = db.query(MSME).filter(MSME.gstin == "24AAACP3415G1ZK").first()
        if not sharma_exists or not patel_exists:
            seed_database()
    finally:
        db.close()

@pytest.mark.asyncio
async def test_list_scenarios(client: AsyncClient):
    res = await client.get("/api/v1/simulator/scenarios")
    assert res.status_code == 200
    scenarios = res.json()
    assert len(scenarios) >= 4
    scenario_ids = [s["id"] for s in scenarios]
    assert "clear_bounces" in scenario_ids
    assert "connect_invoices" in scenario_ids

@pytest.mark.asyncio
async def test_simulate_clear_bounces(client: AsyncClient):
    # Patel Hardware has 2 bounced checks by default. Let's project clearing them to 0.
    payload = {
        "gstin": "24AAACP3415G1ZK",
        "adjustments": {
            "bounced_payments": 0
        }
    }
    res = await client.post("/api/v1/simulator/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    
    assert data["projected_score"] > 0
    assert data["projected_grade"] is not None
    # Verify delta score is calculated and positive because clearing check bounces improves score
    assert data["delta_score"] >= 0
    assert any("bounced payment(s)" in imp for imp in data["improvements"])

@pytest.mark.asyncio
async def test_simulate_multiple_adjustments(client: AsyncClient):
    # Patel Hardware has 38% EMI burden, 312 UPI transactions, 2 bounced checks.
    # Let's project boosting their UPI transactions and clearing check bounces.
    payload = {
        "gstin": "24AAACP3415G1ZK",
        "adjustments": {
            "bounced_payments": 0,
            "monthly_transactions": 500,
            "connect_invoices": True
        }
    }
    res = await client.post("/api/v1/simulator/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    
    assert data["delta_score"] > 0
    assert len(data["improvements"]) >= 3
    # Checks for key improvements logged
    improvements_str = " ".join(data["improvements"])
    assert "invoices" in improvements_str
    assert "bounced" in improvements_str
    assert "UPI" in improvements_str

@pytest.mark.asyncio
async def test_simulate_invalid_gstin(client: AsyncClient):
    payload = {
        "gstin": "99INVALIDGSTIN999",
        "adjustments": {
            "bounced_payments": 0
        }
    }
    res = await client.post("/api/v1/simulator/simulate", json=payload)
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]
