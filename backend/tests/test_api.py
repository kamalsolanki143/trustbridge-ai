import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    res = await client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "TrustBridge AI" in data["service"]
    assert "api_version" in data

@pytest.mark.asyncio
async def test_cors_headers_configured(client: AsyncClient):
    # Hit health check with CORS origin request headers
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    }
    res = await client.options("/health", headers=headers)
    assert res.status_code in (200, 204)
    # Check that Access-Control-Allow-Origin header is present
    assert "access-control-allow-origin" in res.headers

@pytest.mark.asyncio
async def test_unmapped_route_returns_404(client: AsyncClient):
    res = await client.get("/api/v1/non_existent_endpoint_path")
    assert res.status_code == 404
    # FastAPI returns detail: Not Found by default
    assert "detail" in res.json()

@pytest.mark.asyncio
async def test_global_exception_handler_returns_500(client: AsyncClient):
    # Trigger an internal backend error to test the global exception handler
    # We patch the summary generator inside trust_summary router to raise an unexpected Exception
    with patch("app.services.trust_summary.summary_generator.generate_trust_summary", side_effect=RuntimeError("Unhandled Server Error Mock")):
        # Generate trust summary endpoint will trigger the patched method
        res = await client.post("/api/v1/trust-summary/generate/borrower_error_trigger")
        assert res.status_code == 500
        data = res.json()
        assert "detail" in data
        assert "Internal Server Error" in data["detail"]
        assert "Unhandled Server Error Mock" in data["detail"]
