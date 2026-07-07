import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_credit_ladder_policy_mapping(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a qualified borrower profile (Grade A by default in stubs)
    borrower_a = {
        "id": "borrower_ladder_a",
        "name": "Karan Johar",
        "business_name": "Dharma Productions",
        "pan": "ABCDE1234F",
        "gstin": "27ABCDE1234F1Z5",
        "email": "karan@dharma.com",
        "phone": "+919876543210"
    }
    create_res = await client.post("/api/v1/borrower", json=borrower_a)
    assert create_res.status_code == 201

    # 2. Test default policy (Balanced) recommendation
    res = await client.get("/api/v1/ladder/borrower_ladder_a")
    assert res.status_code == 200
    assert res.json()["decision"] == "Pre-Qualified"

    # 3. Modify lender policy to Conservative and re-query
    set_policy_res = await client.post("/api/v1/lender/policy", json={"preference": "Conservative"})
    assert set_policy_res.status_code == 200
    assert set_policy_res.json()["preference"] == "Conservative"

    res_cons = await client.get("/api/v1/ladder/borrower_ladder_a")
    assert res_cons.json()["decision"] == "Pre-Qualified"

@pytest.mark.asyncio
async def test_credit_ladder_starter_loan_routing(client: AsyncClient, db_session: AsyncSession):
    # Create a borrower profile that resolves to Grade C (simulated by having 'manual' in borrower_id in stubs)
    borrower_c = {
        "id": "borrower_manual_ladder_c",
        "name": "Manmohan Singh",
        "business_name": "Singh Logistics",
        "pan": "ABCDE2222B",
        "gstin": "27ABCDE2222B1Z2",
        "email": "manmohan@singh.com",
        "phone": "+919876543212"
    }
    await client.post("/api/v1/borrower", json=borrower_c)

    # Under Balanced Policy, Grade C routes to Manual Review
    await client.post("/api/v1/lender/policy", json={"preference": "Balanced"})
    res_bal = await client.get("/api/v1/ladder/borrower_manual_ladder_c")
    assert res_bal.json()["decision"] == "Manual Review"

    # Under Aggressive Policy, Grade C routes to Starter Loan
    await client.post("/api/v1/lender/policy", json={"preference": "Aggressive"})
    res_aggr = await client.get("/api/v1/ladder/borrower_manual_ladder_c")
    assert res_aggr.json()["decision"] == "Starter Loan"

    # Under Conservative Policy, Grade C routes to Manual Review
    await client.post("/api/v1/lender/policy", json={"preference": "Conservative"})
    res_cons = await client.get("/api/v1/ladder/borrower_manual_ladder_c")
    assert res_cons.json()["decision"] == "Manual Review"

@pytest.mark.asyncio
async def test_ladder_recompute_endpoint(client: AsyncClient, db_session: AsyncSession):
    borrower = {
        "id": "borrower_recompute_test",
        "name": "Rajesh Kumar",
        "business_name": "Kumar Stores",
        "pan": "ABCDE5678F",
        "gstin": "27ABCDE5678F1Z9",
        "email": "rajesh@kumarstores.com",
        "phone": "+919876543222"
    }
    await client.post("/api/v1/borrower", json=borrower)

    # Force recomputation via POST
    recomp_res = await client.post("/api/v1/ladder/borrower_recompute_test/recompute")
    assert recomp_res.status_code == 200
    assert "decision" in recomp_res.json()

@pytest.mark.asyncio
async def test_ladder_invalid_borrower(client: AsyncClient, db_session: AsyncSession):
    # Query for borrower that does not exist
    res = await client.get("/api/v1/ladder/nonexistent_borrower_uuid")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]
