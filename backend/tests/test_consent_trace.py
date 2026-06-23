import datetime
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Consent, ConsentAuditLog

@pytest.mark.asyncio
async def test_consent_lifecycle_and_audit(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a borrower profile first
    borrower_payload = {
        "id": "borrower_test_consent",
        "name": "Rajesh Kumar",
        "business_name": "Kumar Grocery Stores",
        "pan": "ABCDE5678F",
        "gstin": "27ABCDE5678F1Z9",
        "email": "rajesh@kumarstores.com",
        "phone": "+919876543222"
    }
    create_res = await client.post("/api/v1/borrower", json=borrower_payload)
    assert create_res.status_code == 201
    
    # 2. Grant consent for a valid data source
    expiry_time = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + "Z"
    grant_payload = {
        "borrower_id": "borrower_test_consent",
        "data_source": "bank_statements",
        "purpose": "Cash Flow Stability Assessment",
        "scope": "read",
        "expiry": expiry_time
    }
    grant_res = await client.post("/api/v1/consent/grant", json=grant_payload)
    assert grant_res.status_code == 201
    grant_data = grant_res.json()
    assert grant_data["status"] == "approved"
    assert grant_data["data_source"] == "bank_statements"
    assert grant_data["purpose"] == "Cash Flow Stability Assessment"

    # Try granting for a non-existent borrower ID
    invalid_grant = grant_payload.copy()
    invalid_grant["borrower_id"] = "borrower_invalid"
    invalid_res = await client.post("/api/v1/consent/grant", json=invalid_grant)
    assert invalid_res.status_code == 404

    # 3. List active consents
    list_res = await client.get("/api/v1/consent/borrower_test_consent")
    assert list_res.status_code == 200
    consents_list = list_res.json()
    assert len(consents_list) == 1
    assert consents_list[0]["data_source"] == "bank_statements"
    assert consents_list[0]["status"] == "approved"

    # 4. Revoke consent
    revoke_payload = {
        "borrower_id": "borrower_test_consent",
        "data_source": "bank_statements"
    }
    revoke_res = await client.post("/api/v1/consent/revoke", json=revoke_payload)
    assert revoke_res.status_code == 200
    revoke_data = revoke_res.json()
    assert revoke_data["status"] == "revoked"
    assert revoke_data["revoked_at"] is not None

    # Try revoking again (no longer active)
    revoke_res_again = await client.post("/api/v1/consent/revoke", json=revoke_payload)
    assert revoke_res_again.status_code == 404

    # 5. Verify Trace Log
    trace_res = await client.get("/api/v1/consent/borrower_test_consent/trace")
    assert trace_res.status_code == 200
    trace_log = trace_res.json()
    # Should have a 'grant' action and a 'revoke' action in audit log
    actions = [log["action"] for log in trace_log]
    assert "grant" in actions
    assert "revoke" in actions

@pytest.mark.asyncio
async def test_consent_auto_expiration(client: AsyncClient, db_session: AsyncSession):
    # 1. Create a borrower
    borrower_payload = {
        "id": "borrower_test_expiry",
        "name": "Amit Shah",
        "business_name": "Shah Enterprises",
        "pan": "FGHIJ1234K",
        "gstin": "27FGHIJ1234K1Z0",
        "email": "amit@shah.com",
        "phone": "+919876543233"
    }
    await client.post("/api/v1/borrower", json=borrower_payload)

    # 2. Grant consent with an already expired date (1 hour ago)
    past_expiry = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + "Z"
    grant_payload = {
        "borrower_id": "borrower_test_expiry",
        "data_source": "gst",
        "purpose": "Business Activity Verification",
        "scope": "read",
        "expiry": past_expiry
    }
    grant_res = await client.post("/api/v1/consent/grant", json=grant_payload)
    assert grant_res.status_code == 201

    # 3. Retrieve consents list. This should trigger the auto-expiry checker!
    list_res = await client.get("/api/v1/consent/borrower_test_expiry")
    assert list_res.status_code == 200
    consents_list = list_res.json()
    assert len(consents_list) == 1
    assert consents_list[0]["status"] == "expired"

    # 4. Check that audit log recorded the expiration
    trace_res = await client.get("/api/v1/consent/borrower_test_expiry/trace")
    trace_log = trace_res.json()
    actions = [log["action"] for log in trace_log]
    assert "expire" in actions
