import datetime
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import ManualReview, LenderDecision

@pytest.mark.asyncio
async def test_trust_summary_and_lender_flows(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a borrower profile
    borrower_payload = {
        "id": "borrower_trust_test",
        "name": "Sonia Gandhi",
        "business_name": "National Traders Co",
        "pan": "ABCDE1111A",
        "gstin": "27ABCDE1111A1Z1",
        "email": "sonia@national.com",
        "phone": "+919876543211"
    }
    create_res = await client.post("/api/v1/borrower", json=borrower_payload)
    assert create_res.status_code == 201

    # 2. Grant consents for bank statements and GST
    expiry_time = (datetime.datetime.utcnow() + datetime.timedelta(days=10)).isoformat() + "Z"
    
    await client.post("/api/v1/consent/grant", json={
        "borrower_id": "borrower_trust_test",
        "data_source": "bank_statements",
        "purpose": "Cash Flow Stability Assessment",
        "scope": "read",
        "expiry": expiry_time
    })
    await client.post("/api/v1/consent/grant", json={
        "borrower_id": "borrower_trust_test",
        "data_source": "gst",
        "purpose": "Business Activity Verification",
        "scope": "read",
        "expiry": expiry_time
    })

    # 3. Generate Trust Summary
    gen_res = await client.post("/api/v1/trust-summary/generate/borrower_trust_test")
    assert gen_res.status_code == 201
    summary_data = gen_res.json()
    assert summary_data["readiness_grade"] == "A"
    assert summary_data["confidence_band"] == "High"
    # Consents utilized and verified
    assert "bank_statements" in summary_data["verified_sources"]
    assert "gst" in summary_data["verified_sources"]
    assert summary_data["ai_summary"] is not None
    assert summary_data["recommended_action"] == "Pre-Qualified"

    # Verify that consent usage was recorded in the trace audit log
    trace_res = await client.get("/api/v1/consent/borrower_trust_test/trace")
    trace_log = trace_res.json()
    use_logs = [log for log in trace_log if log["action"] == "use"]
    assert len(use_logs) == 2
    sources_used = [log["data_source"] for log in use_logs]
    assert "bank_statements" in sources_used
    assert "gst" in sources_used

    # 4. Fetch the latest Trust Summary as JSON
    get_res = await client.get("/api/v1/trust-summary/borrower_trust_test")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == summary_data["id"]

    # 5. Fetch the Trust Summary PDF
    pdf_res = await client.get("/api/v1/trust-summary/borrower_trust_test/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert "attachment" in pdf_res.headers["content-disposition"]
    # PDF files start with the "%PDF" magic header bytes
    assert pdf_res.content.startswith(b"%PDF")

    # 6. Fetch Borrower Dashboard
    dash_res = await client.get("/api/v1/borrower/borrower_trust_test/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["latest_readiness_grade"] == "A"
    assert dash_data["active_ladder_outcome"] == "Pre-Qualified"
    assert dash_data["consent_status_overview"]["bank_statements"] == "approved"
    assert dash_data["consent_status_overview"]["upi"] == "missing"
    assert "current_stage" in dash_data["growth_roadmap"]

@pytest.mark.asyncio
async def test_manual_review_routing_and_lender_actions(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a borrower configured to trigger Manual Review recommendation
    # (By putting "manual" in borrower_id, our _stubs return Grade C -> outcome "Manual Review")
    borrower_id = "borrower_manual_test"
    borrower_payload = {
        "id": borrower_id,
        "name": "Manmohan Singh",
        "business_name": "Singh Logistics",
        "pan": "ABCDE2222B",
        "gstin": "27ABCDE2222B1Z2",
        "email": "manmohan@singh.com",
        "phone": "+919876543212"
    }
    await client.post("/api/v1/borrower", json=borrower_payload)

    # 2. Querying the dashboard should automatically trigger Manual Review insertion
    dash_res = await client.get(f"/api/v1/borrower/{borrower_id}/dashboard")
    assert dash_res.status_code == 200
    assert dash_res.json()["active_ladder_outcome"] == "Manual Review"

    # Verify manual review record is present in DB queue
    queue_res = await client.get("/api/v1/manual-review/queue")
    assert queue_res.status_code == 200
    queue = queue_res.json()
    assert len(queue) == 1
    assert queue[0]["borrower_id"] == borrower_id
    assert queue[0]["status"] == "pending"
    assert len(queue[0]["risk_signals"]) > 0

    # Fetch detail case view
    detail_res = await client.get(f"/api/v1/manual-review/{borrower_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["borrower_id"] == borrower_id

    # 3. Resolve the manual review
    resolve_payload = {
        "resolution": "resolved",
        "notes": "Lender verified manual tax documentation and resolved pending flags."
    }
    resolve_res = await client.post(f"/api/v1/manual-review/{borrower_id}/resolve", json=resolve_payload)
    assert resolve_res.status_code == 200
    resolved_data = resolve_res.json()
    assert resolved_data["status"] == "resolved"
    assert resolved_data["resolution_notes"] == resolve_payload["notes"]

    # Verify borrower is no longer in pending/escalated queue
    queue_res_after = await client.get("/api/v1/manual-review/queue")
    assert len(queue_res_after.json()) == 0

    # Verify a LenderDecision audit entry was logged
    stmt = select(LenderDecision).where(LenderDecision.borrower_id == borrower_id)
    res = await db_session.execute(stmt)
    lender_dec = res.scalar_one_or_none()
    assert lender_dec is not None
    assert lender_dec.decision == "approved"
    assert lender_dec.notes == resolve_payload["notes"]

@pytest.mark.asyncio
async def test_lender_policy_settings(client: AsyncClient, db_session: AsyncSession):
    # Retrieve default policy
    get_pol = await client.get("/api/v1/lender/lender_default/policy")
    assert get_pol.status_code == 200
    assert get_pol.json()["preference"] == "Balanced"

    # Set policy to Aggressive
    set_pol = await client.post("/api/v1/lender/policy", json={"preference": "Aggressive"})
    assert set_pol.status_code == 200
    assert set_pol.json()["preference"] == "Aggressive"

    # Verify updated policy
    get_pol_updated = await client.get("/api/v1/lender/lender_default/policy")
    assert get_pol_updated.json()["preference"] == "Aggressive"
