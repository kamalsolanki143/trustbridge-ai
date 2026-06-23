import datetime
import os
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TrustSummary, Borrower, LenderPolicy
from app.services._stubs import get_readiness_profile, get_ladder_decision
from app.services.consent_trace.consent_tracker import get_active_consents, record_consent_usage
from app.services import gemini_client

async def generate_trust_summary(db: AsyncSession, borrower_id: str) -> TrustSummary:
    """
    Assembles data from the Readiness Engine, Consent Tracer, and Ladder Engine.
    Uses Gemini 2.5 Pro to generate a natural language underwriting narrative.
    Records audits of consent usage and persists the summary in the database.
    """
    # 1. Fetch borrower profile details
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    res = await db.execute(stmt)
    borrower = res.scalar_one_or_none()
    if not borrower:
        raise ValueError(f"Borrower with ID '{borrower_id}' not found.")

    # 2. Get readiness profile from Krrish's engine stub
    readiness = get_readiness_profile(borrower_id)

    # 3. Fetch active consents and log their usage for audit trace compliance
    active_consents = await get_active_consents(db, borrower_id)
    verified_sources = []
    
    # Check consent and record usage for each potential source
    possible_sources = ["bank_statements", "gst", "upi", "invoices", "business_profile"]
    for source in possible_sources:
        consent = next((c for c in active_consents if c.data_source == source and c.status == "approved"), None)
        if consent:
            # Try to record consent usage (logs to audit trace and returns if allowed)
            permitted = await record_consent_usage(
                db=db,
                borrower_id=borrower_id,
                data_source=source,
                intended_purpose=consent.purpose,
                details="Accessed for generating Underwriting Trust Summary."
            )
            if permitted:
                verified_sources.append(source)

    # 4. Fetch the lender's risk policy configuration (or default to Balanced)
    policy_stmt = select(LenderPolicy).order_by(LenderPolicy.updated_at.desc())
    policy_res = await db.execute(policy_stmt)
    latest_policy = policy_res.scalars().first()
    preference = latest_policy.preference if latest_policy else "Balanced"

    # 5. Fetch ladder engine recommendation from Kamal's engine stub
    decision_profile = get_ladder_decision(borrower_id, preference)

    # 6. Load underwriting narrative template prompt
    prompt_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "prompts", "underwriting_summary.txt"
    )
    
    try:
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        # Fallback if path mapping fails during alternative runtime
        prompt_template = (
            "Borrower Name: {borrower_name}\n"
            "Business Name: {business_name}\n"
            "Readiness Grade: {readiness_grade}\n"
            "Confidence Band: {confidence_band}\n"
            "Data Coverage %: {coverage_pct}%\n"
            "Risk Signals: {risk_signals}\n"
            "Verified Data Sources: {verified_sources}\n"
            "Stability Indicators: {stability_indicators}\n"
            "Ladder Recommendation: {recommended_action}"
        )

    formatted_prompt = prompt_template.format(
        borrower_name=borrower.name,
        business_name=borrower.business_name,
        readiness_grade=readiness.readiness_grade,
        confidence_band=readiness.confidence_band,
        coverage_pct=readiness.coverage_pct,
        risk_signals=", ".join(readiness.risk_signals) if readiness.risk_signals else "None",
        verified_sources=", ".join(verified_sources) if verified_sources else "None",
        stability_indicators=", ".join(readiness.stability_indicators) if readiness.stability_indicators else "None",
        recommended_action=decision_profile.decision
    )

    # 7. Generate narrative with Gemini Pro client
    ai_summary = gemini_client.generate(formatted_prompt)

    # 8. Save trust summary to database
    summary_record = TrustSummary(
        borrower_id=borrower_id,
        readiness_grade=readiness.readiness_grade,
        confidence_band=readiness.confidence_band,
        coverage_pct=readiness.coverage_pct,
        risk_signals=readiness.risk_signals,
        reason_codes=readiness.reason_codes,
        stability_indicators=readiness.stability_indicators,
        verified_sources=verified_sources,
        ai_summary=ai_summary,
        recommended_action=decision_profile.decision,
        generated_at=datetime.datetime.utcnow()
    )
    db.add(summary_record)
    await db.flush()
    return summary_record

async def get_latest_trust_summary(db: AsyncSession, borrower_id: str) -> Optional[TrustSummary]:
    """
    Fetches the latest generated trust summary for a borrower.
    """
    stmt = select(TrustSummary).where(
        TrustSummary.borrower_id == borrower_id
    ).order_by(TrustSummary.generated_at.desc())
    
    result = await db.execute(stmt)
    return result.scalars().first()
