# TrustBridge AI: API Documentation

All endpoints in the TrustBridge AI backend engine are REST-based, returning JSON payloads. Development and local server default endpoint prefix: `http://localhost:8000`.

---

## 1. System Health Endpoint

### 1.1 `GET /health`
Verifies service availability.
*   **Method**: `GET`
*   **Request Body**: None
*   **Headers**: None
*   **Response (200 OK)**:
    ```json
    {
      "status": "healthy",
      "service": "TrustBridge AI Backend Engine",
      "api_version": "1.0.0"
    }
    ```

---

## 2. Borrower Management API

### 2.1 `POST /api/v1/borrower`
Registers a new MSME borrower profile.
*   **Method**: `POST`
*   **Request Body (`BorrowerCreate`)**:
    ```json
    {
      "id": "borrower_uuid_123",
      "name": "Karan Johar",
      "business_name": "Dharma Productions Private Limited",
      "pan": "ABCDE1234F",
      "gstin": "27ABCDE1234F1Z5",
      "email": "contact@dharma.com",
      "phone": "+919876543210"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
      "id": "borrower_uuid_123",
      "name": "Karan Johar",
      "business_name": "Dharma Productions Private Limited",
      "pan": "ABCDE1234F",
      "gstin": "27ABCDE1234F1Z5",
      "email": "contact@dharma.com",
      "phone": "+919876543210",
      "created_at": "2026-07-07T12:00:00.000000"
    }
    ```
*   **Error Responses**:
    *   **400 Bad Request**: If borrower ID, PAN, or GSTIN already exists, or request payload has format validation failures.
        ```json
        { "detail": "Borrower with this ID, PAN, or GSTIN already exists." }
        ```

### 2.2 `GET /api/v1/borrower/{borrower_id}`
Retrieves details of a borrower profile.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    {
      "id": "borrower_uuid_123",
      "name": "Karan Johar",
      "business_name": "Dharma Productions Private Limited",
      "pan": "ABCDE1234F",
      "gstin": "27ABCDE1234F1Z5",
      "email": "contact@dharma.com",
      "phone": "+919876543210",
      "created_at": "2026-07-07T12:00:00.000000"
    }
    ```
*   **Error Responses**:
    *   **404 Not Found**: If the borrower profile doesn't exist.

### 2.3 `GET /api/v1/borrower/{borrower_id}/dashboard`
Aggregates and retrieves borrower-facing statistics (scores, outcomes, consents, and improvement roadmaps).
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    {
      "borrower_id": "borrower_uuid_123",
      "latest_readiness_grade": "A",
      "coverage_pct": 95.0,
      "active_ladder_outcome": "Pre-Qualified",
      "consent_status_overview": {
        "bank_statements": "approved",
        "gst": "approved",
        "upi": "approved",
        "invoices": "approved",
        "business_profile": "approved"
      },
      "growth_roadmap": {
        "current_stage": "Pre-Qualified",
        "next_goal": "Premium Tier Interest Rate Reductions",
        "milestones": [
          { "title": "Maintain GST consistency for next 3 months", "completed": true },
          { "title": "Increase digital invoicing to 100%", "completed": false, "impact": "High" }
        ],
        "tips": ["Ensure your UPI volume does not drop during seasonal fluctuations."]
      }
    }
    ```

---

## 3. Consent Management API

### 3.1 `POST /api/v1/consent/grant`
Registers borrower consent for a specific alternative data source.
*   **Method**: `POST`
*   **Request Body (`GrantConsentRequest`)**:
    ```json
    {
      "borrower_id": "borrower_uuid_123",
      "data_source": "bank_statements",
      "purpose": "Cash Flow Stability Assessment",
      "scope": "read",
      "expiry": "2027-07-07T12:00:00Z"
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
      "id": 1,
      "borrower_id": "borrower_uuid_123",
      "data_source": "bank_statements",
      "purpose": "Cash Flow Stability Assessment",
      "scope": "read",
      "expiry": "2027-07-07T12:00:00Z",
      "status": "approved",
      "used_for": "Used for assessing borrower's cashflow stability and debt-service capacity.",
      "granted_at": "2026-07-07T12:30:00Z",
      "revoked_at": null
    }
    ```
*   **Error Responses**:
    *   **404 Not Found**: If the borrower does not exist, or data source is invalid.
        ```json
        { "detail": "Borrower with ID borrower_uuid_123 not found." }
        ```

### 3.2 `POST /api/v1/consent/revoke`
Manually revokes active consent for a source.
*   **Method**: `POST`
*   **Request Body (`RevokeConsentRequest`)**:
    ```json
    {
      "borrower_id": "borrower_uuid_123",
      "data_source": "bank_statements"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "id": 1,
      "borrower_id": "borrower_uuid_123",
      "data_source": "bank_statements",
      "purpose": "Cash Flow Stability Assessment",
      "scope": "read",
      "expiry": "2027-07-07T12:00:00Z",
      "status": "revoked",
      "used_for": "Used for assessing borrower's cashflow stability and debt-service capacity.",
      "granted_at": "2026-07-07T12:30:00Z",
      "revoked_at": "2026-07-07T12:35:00Z"
    }
    ```
*   **Error Responses**:
    *   **404 Not Found**: If no active approved consent is found for the borrower and source.

### 3.3 `GET /api/v1/consent/{borrower_id}`
Lists all consents for a borrower. Automatically flags and updates expired records.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "borrower_id": "borrower_uuid_123",
        "data_source": "bank_statements",
        "purpose": "Cash Flow Stability Assessment",
        "scope": "read",
        "expiry": "2027-07-07T12:00:00Z",
        "status": "approved",
        "used_for": "Used for assessing borrower's cashflow stability.",
        "granted_at": "2026-07-07T12:30:00Z",
        "revoked_at": null
      }
    ]
    ```

### 3.4 `GET /api/v1/consent/{borrower_id}/trace`
Retrieves the timestamped history of consent grants, revocations, and usages.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 2,
        "borrower_id": "borrower_uuid_123",
        "data_source": "bank_statements",
        "action": "use",
        "purpose": "Cash Flow Stability Assessment",
        "timestamp": "2026-07-07T12:34:00Z",
        "details": "Accessed for generating Underwriting Trust Summary."
      },
      {
        "id": 1,
        "borrower_id": "borrower_uuid_123",
        "data_source": "bank_statements",
        "action": "grant",
        "purpose": "Cash Flow Stability Assessment",
        "timestamp": "2026-07-07T12:30:00Z",
        "details": "Granted with scope 'read', expires at 2027-07-07T12:00:00Z."
      }
    ]
    ```

---

## 4. Underwriting Trust Summary API

### 4.1 `POST /api/v1/trust-summary/generate/{borrower_id}`
Triggers trust summary compilation, calls Gemini AI for the narrative, logs consent audit accesses, and saves the summary.
*   **Method**: `POST`
*   **Response (201 Created)**:
    ```json
    {
      "id": 1,
      "borrower_id": "borrower_uuid_123",
      "readiness_grade": "A",
      "confidence_band": "High",
      "coverage_pct": 95.0,
      "risk_signals": ["No major defaults"],
      "reason_codes": ["STABLE_INFLOWS", "CONSISTENT_GST", "HIGH_UPI_VOLUME"],
      "stability_indicators": ["3+ years operational history", "Consistent quarterly revenue growth"],
      "verified_sources": ["bank_statements", "gst", "upi"],
      "ai_summary": "The borrower demonstrates strong cashflow stability with consistent digital transactions across UPI and verified bank statements...",
      "recommended_action": "Pre-Qualified",
      "generated_at": "2026-07-07T12:36:00Z"
    }
    ```

### 4.2 `GET /api/v1/trust-summary/{borrower_id}`
Fetches the latest generated Trust Summary details.
*   **Method**: `GET`
*   **Response (200 OK)**: (Same structure as `POST` generation endpoint response).
*   **Error Responses**:
    *   **404 Not Found**: If no summary has been generated yet for this borrower.

### 4.3 `GET /api/v1/trust-summary/{borrower_id}/pdf`
Downloads the latest underwriting trust summary as a formatted PDF file.
*   **Method**: `GET`
*   **Response (200 OK)**: Binary stream of PDF data.
*   **Headers**:
    *   `Content-Type: application/pdf`
    *   `Content-Disposition: attachment; filename=trust_summary_borrower_uuid_123.pdf`

---

## 5. Lender Operations & Settings API

### 5.1 `GET /api/v1/lender/applications`
Retrieves a list of borrower applications with credit readiness profiles (underwriter overview).
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    [
      {
        "borrower_id": "borrower_uuid_123",
        "name": "Karan Johar",
        "business_name": "Dharma Productions Private Limited",
        "readiness_grade": "A",
        "ladder_outcome": "Pre-Qualified",
        "risk_signals": ["No major defaults"]
      }
    ]
    ```

### 5.2 `POST /api/v1/lender/policy`
Sets risk appetite preferences globally for the lender.
*   **Method**: `POST`
*   **Request Body (`LenderPolicyRequest`)**:
    ```json
    {
      "preference": "Aggressive"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "lender_id": "lender_default",
      "preference": "Aggressive",
      "updated_at": "2026-07-07T12:40:00Z"
    }
    ```

### 5.3 `GET /api/v1/lender/{lender_id}/policy`
Gets the active policy settings for a specific lender.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    {
      "lender_id": "lender_default",
      "preference": "Aggressive",
      "updated_at": "2026-07-07T12:40:00Z"
    }
    ```

### 5.4 `POST /api/v1/lender/{borrower_id}/decision`
Records the final lender audit decision (approve/reject/escalate) and underwriter notes.
*   **Method**: `POST`
*   **Request Body (`LenderDecisionRecordRequest`)**:
    ```json
    {
      "decision": "approved",
      "notes": "Verified high transaction volume. Recommended for starter loan limit."
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
      "id": 1,
      "borrower_id": "borrower_uuid_123",
      "lender_id": "lender_default",
      "decision": "approved",
      "notes": "Verified high transaction volume. Recommended for starter loan limit.",
      "timestamp": "2026-07-07T12:42:00Z"
    }
    ```

---

## 6. Manual Review Queue API

### 6.1 `GET /api/v1/manual-review/queue`
Lists manual review cases that are currently pending or escalated.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "borrower_id": "borrower_manual_test",
        "status": "pending",
        "assigned_to": "lender_default",
        "risk_signals": ["High debt-to-income ratio", "Irregular transaction activity"],
        "anomaly_flags": ["DEBT_SPIKE", "INCONSISTENT_DEPOSITS"],
        "created_at": "2026-07-07T12:00:00Z",
        "resolved_at": null,
        "resolution_notes": null
      }
    ]
    ```

### 6.2 `GET /api/v1/manual-review/{borrower_id}`
Fetches the detail view of an individual manual review case.
*   **Method**: `GET`
*   **Response (200 OK)**: (Same structure as queue item).

### 6.3 `POST /api/v1/manual-review/{borrower_id}/resolve`
Resolves a manual review case, saving notes and logging a lender decision entry.
*   **Method**: `POST`
*   **Request Body (`ManualReviewResolveRequest`)**:
    ```json
    {
      "resolution": "resolved",
      "notes": "Verified offline ledger. Confirmed irregular transaction was a capital refund."
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "id": 1,
      "borrower_id": "borrower_manual_test",
      "status": "resolved",
      "assigned_to": "lender_default",
      "risk_signals": ["High debt-to-income ratio", "Irregular transaction activity"],
      "anomaly_flags": ["DEBT_SPIKE", "INCONSISTENT_DEPOSITS"],
      "created_at": "2026-07-07T12:00:00Z",
      "resolved_at": "2026-07-07T12:45:00Z",
      "resolution_notes": "Verified offline ledger. Confirmed irregular transaction was a capital refund."
    }
    ```

---

## 7. Credit Readiness Engine API (Krrish's Models)

### 7.1 `POST /api/readiness/assess`
Performs alternative data ingestion and computes credit readiness.
*   **Method**: `POST`
*   **Request Body (`ReadinessAssessRequest`)**:
    ```json
    {
      "gstin": "19AABCS1429B1ZX",
      "consent_token": "consent-sharma-001",
      "data_sources": ["gst", "aa", "upi", "invoice", "business"]
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "msme_id": "9a7522d1-21c6-455a-aa70-658b122709e1",
      "business_name": "Sharma Textile Works",
      "readiness_grade": "A+",
      "score": 96,
      "confidence_band": "High",
      "coverage_meter": {
        "connected": 5,
        "total": 5,
        "percentage": 100.0
      },
      "sub_scores": [
        { "dimension": "cash_flow", "score": 23.0, "max_score": 25.0, "weight_percent": 35.0 },
        { "dimension": "compliance", "score": 25.0, "max_score": 25.0, "weight_percent": 20.0 },
        { "dimension": "repayment", "score": 25.0, "max_score": 25.0, "weight_percent": 30.0 },
        { "dimension": "growth", "score": 22.0, "max_score": 25.0, "weight_percent": 15.0 }
      ],
      "risk_signals": [],
      "reason_codes": [
        { "type": "positive", "code": "STRONG_CASH_FLOW", "message": "Consistent and healthy cash flow from business operations" },
        { "type": "positive", "code": "STRONG_COMPLIANCE", "message": "Regular GST filings and EPFO contributions demonstrate compliance" }
      ],
      "credit_ladder_outcome": "Pre-Qualified",
      "ai_summary": "Sharma Textile Works has a credit readiness grade of A+ (Score: 96/100). The business demonstrates high scores across all alternative parameters...",
      "created_at": "2026-07-07T12:00:00Z"
    }
    ```

### 7.2 `GET /api/readiness/{msme_id}`
Retrieves the latest readiness assessment details for an MSME.
*   **Method**: `GET`
*   **Response (200 OK)**: (Same structure as assessment output).

### 7.3 `GET /api/readiness/history/{gstin}`
Retrieves a list of all historical assessments for a GSTIN.
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    {
      "assessments": [
        {
          "msme_id": "9a7522d1-21c6-455a-aa70-658b122709e1",
          "business_name": "Sharma Textile Works",
          "readiness_grade": "A+",
          "score": 96,
          "confidence_band": "High",
          "coverage_meter": { "connected": 5, "total": 5, "percentage": 100.0 },
          "sub_scores": [...],
          "risk_signals": [],
          "reason_codes": [...],
          "credit_ladder_outcome": "Pre-Qualified",
          "ai_summary": "...",
          "created_at": "2026-07-07T12:00:00Z"
        }
      ]
    }
    ```

---

## 8. Credit Scenario Simulator API

### 8.1 `POST /api/v1/simulator/simulate`
Simulates the impact of business operational improvements on credit scoring.
*   **Method**: `POST`
*   **Request Body (`ScenarioInput`)**:
    ```json
    {
      "gstin": "24AAACP3415G1ZK",
      "adjustments": {
        "bounced_payments": 0,
        "turnover_trend_percent": 15,
        "monthly_transactions": 500,
        "connect_invoices": true
      }
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "projected_score": 82,
      "projected_grade": "A",
      "projected_outcome": "Pre-Qualified",
      "delta_score": 24,
      "improvements": [
        "Clearing bounced check record improves Repayment Score (+8 points)",
        "Increasing UPI transaction volume to 500/mo improves Cash Flow Score (+3 points)",
        "Integrating digital invoices increases alternative Data Coverage to 100%"
      ]
    }
    ```
