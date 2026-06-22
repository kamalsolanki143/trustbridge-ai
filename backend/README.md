# Backend Module: Consent, Trust Summary, Ladder API & Manual Review
**Owner:** Muskan Yeshmin Ali (Backend Lead)
**Branch:** `muskan/backend-trust-summary-consent-ladder`
**Status:** Ready for integration review

---

## 1. What This Module Does

This module covers the **decision-support and trust layer** of TrustBridge AI — the part that turns a borrower's underlying readiness data into something a lender can actually read, trust, and act on. Specifically, it implements:

1. **Consent Management & Consent Trace** — lets borrowers grant/revoke consent per data source, enforces purpose-limited usage, and keeps a full audit trail of every consent event.
2. **Underwriting Trust Summary™** — generates the lender-facing decision document: Readiness Grade, Confidence Band, Coverage %, Risk Signals, Verified Sources, Stability Indicators, an AI-written underwriting narrative (via Gemini), and the recommended lending action. Exportable as PDF.
3. **Ladder Engine API layer** — exposes the Pre-Qualified / Starter Loan / Improve First / Manual Review decision (computed by the decision engine) to borrowers and lenders, with reason codes.
4. **Manual Review queue** — lists flagged applications, lets lenders resolve them, and logs the resolution to an audit trail.
5. **Borrower & Lender API surface** — profile CRUD, borrower dashboard aggregation, lender application list, and lender policy (Conservative / Balanced / Aggressive) management.

---

## 2. Files Added/Changed in This PR

```
backend/app/api/
  ├── borrower.py
  ├── lender.py
  ├── consent.py
  ├── trust_summary.py
  ├── ladder_engine.py
  └── manual_review.py

backend/app/services/trust_summary/
  ├── summary_generator.py
  └── pdf_export.py

backend/app/services/consent_trace/
  ├── consent_tracker.py
  └── purpose_mapper.py

backend/app/prompts/
  └── underwriting_summary.txt

backend/app/main.py            (added router registrations for the 6 modules above)

backend/tests/
  ├── test_consent_trace.py
  └── test_trust_summary.py
```

**I did NOT touch:** `readiness_engine/*`, `ingestion/*`, `outcome_simulator/*`, `decision_engine.py`/`lender_policy.py`/`recommendation_engine.py` internals, any frontend file, `docs/`, `sample_data/`, or `presentations/`.

---

## 3. API Endpoints Delivered

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/consent/grant` | Grant consent for a data source |
| POST | `/api/v1/consent/revoke` | Revoke an existing consent |
| GET | `/api/v1/consent/{borrower_id}` | List consent status per source |
| GET | `/api/v1/consent/{borrower_id}/trace` | Full consent audit trail |
| POST | `/api/v1/trust-summary/generate/{borrower_id}` | Generate a new Trust Summary |
| GET | `/api/v1/trust-summary/{borrower_id}` | Get latest Trust Summary (JSON) |
| GET | `/api/v1/trust-summary/{borrower_id}/pdf` | Download Trust Summary as PDF |
| GET | `/api/v1/ladder/{borrower_id}` | Get current ladder decision + reason codes |
| POST | `/api/v1/ladder/{borrower_id}/recompute` | Force recompute decision |
| GET | `/api/v1/manual-review/queue` | List all flagged applications |
| GET | `/api/v1/manual-review/{borrower_id}` | Detail view of a flagged case |
| POST | `/api/v1/manual-review/{borrower_id}/resolve` | Lender resolves a flagged case |
| POST | `/api/v1/borrower` | Create borrower profile |
| GET | `/api/v1/borrower/{borrower_id}` | Get borrower profile |
| GET | `/api/v1/borrower/{borrower_id}/dashboard` | Aggregated borrower dashboard |
| GET | `/api/v1/lender/applications` | List applicants for lender review |
| POST | `/api/v1/lender/policy` | Set lender risk policy |
| GET | `/api/v1/lender/{lender_id}/policy` | Get lender's current policy |
| POST | `/api/v1/lender/{borrower_id}/decision` | Lender records final decision |
| GET | `/health` | Health check |

---

## 4. ⚠️ Known Stubs — What Still Needs to Connect

Because the Readiness Engine and Ladder decision logic weren't ready yet when I built this, the following are **mocked with the exact expected interface**, clearly marked `# STUB` in code (mostly isolated in `backend/app/services/_stubs.py`):

| Stub | Real owner | Expected real function | Where it's used |
|---|---|---|---|
| `get_readiness_profile(borrower_id)` | Krrish | Returns `{readiness_grade, confidence_band, coverage_pct, risk_signals, reason_codes, stability_indicators}` | `summary_generator.py`, `borrower.py` dashboard |
| `get_ladder_decision(borrower_id, lender_policy)` | Kamal | Returns one of `Pre-Qualified / Starter Loan / Improve First / Manual Review` + reason codes | `ladder_engine.py`, `trust_summary.py` |
| Growth Roadmap pointer | Kamal | Returns next-step recommendations | `borrower.py` dashboard (currently returns placeholder text) |

**Action needed from Krrish & Kamal:** once your real functions are ready, replace the stub import in `_stubs.py` with your actual module — function names and return shapes already match what I built against, so it should be a near drop-in swap. Please ping me if your final return shape differs even slightly (e.g. field name changes) so I can adjust the consumers.

---

## 5. Dependencies Added

- PDF export uses **`reportlab`** (lightweight, no system dependencies). Add to `requirements.txt`:
  ```
  reportlab>=4.0
  ```
- Gemini calls go through the shared `backend/app/ai/gemini_client.py`. If this file doesn't exist yet in `main`, I added a minimal stub version — **whoever owns the real Gemini integration should overwrite it**, the interface (`generate(prompt: str) -> str`) should stay the same so my code doesn't break.

---

## 6. How to Pull Everything Together (For the Team)

1. **Everyone merges to `main` via Pull Request, never direct push.** Branch naming convention: `<name>/<short-description>` (e.g. `krrish/readiness-engine`, `kamal/ladder-decision-logic`).
2. **Merge order matters less than communication** — but ideally:
   - Krrish's readiness engine + DB models/schemas merge first (everything else reads from these).
   - Kamal's decision engine + lender policy logic next.
   - My module (consent, trust summary, ladder API, manual review) merges next — once merged, go into `backend/app/services/_stubs.py` and swap each stub for the real import.
   - Saloni's tests/sample data can merge anytime and should be run against the integrated branch before final submission.
3. **After merging my branch**, run:
   ```
   cd backend
   pip install -r requirements.txt
   pytest
   uvicorn app.main:app --reload
   ```
   Hit `GET /health` to confirm the app boots, then `GET /docs` (FastAPI auto Swagger UI) to see all endpoints across everyone's merged routers in one place.
4. **Integration smoke test checklist** (do this together once everyone's merged):
   - [ ] Create a borrower → grant consent for all 5 sources → confirm `/consent/{id}/trace` shows all grants
   - [ ] Generate a Trust Summary → confirm it pulls REAL readiness data (not the stub) → download PDF and open it
   - [ ] Check `/ladder/{id}` returns a real decision under all 3 lender policies (Conservative/Balanced/Aggressive) and that the outcome actually changes with policy
   - [ ] Force a case into Manual Review → confirm it shows in `/manual-review/queue` → resolve it → confirm it disappears from queue
   - [ ] Confirm frontend (Krrish's dashboards) can successfully call all of the above endpoints with no CORS or schema-shape errors
5. **If your real function's return shape differs from what's documented in section 4 above**, please don't silently change it — message the team or open a small "interface fix" PR so consumers (my code, frontend) get updated together.

---

## 7. Questions / Issues

Tag **@captainramen35-lgtm** on the PR for anything related to consent, trust summary, ladder API exposure, or manual review. For decision-logic correctness (why a borrower got a particular grade/outcome), tag Kamal or Krrish — that logic lives outside this module.
