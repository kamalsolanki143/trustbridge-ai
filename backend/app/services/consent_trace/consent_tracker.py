import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Consent, ConsentAuditLog, Borrower
from app.services.consent_trace.purpose_mapper import get_purpose_for_source, is_usage_permitted

async def record_consent_grant(
    db: AsyncSession,
    borrower_id: str,
    data_source: str,
    scope: str,
    expiry: datetime.datetime
) -> Consent:
    """
    Grants consent for a borrower's specific data source. Revokes any existing
    active consent for the same source prior to granting.
    """
    # 1. Check if borrower exists. Raise ValueError if not.
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    result = await db.execute(stmt)
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise ValueError(f"Borrower with ID {borrower_id} not found.")

    # 2. Validate data source
    from app.services.consent_trace.purpose_mapper import PURPOSE_MAP
    canonical_source = data_source.strip().lower()
    if canonical_source not in PURPOSE_MAP:
        raise ValueError(f"Data source '{data_source}' is not supported. Must be one of: {list(PURPOSE_MAP.keys())}")

    # Revoke existing active consent for this source if any
    active_stmt = select(Consent).where(
        and_(
            Consent.borrower_id == borrower_id,
            Consent.data_source == data_source,
            Consent.status == "approved"
        )
    )
    existing_result = await db.execute(active_stmt)
    existing_consents = existing_result.scalars().all()
    for existing in existing_consents:
        existing.status = "revoked"
        existing.revoked_at = datetime.datetime.utcnow()
        db.add(existing)

    # 3. Create new consent record
    purpose = get_purpose_for_source(data_source)
    
    used_for_mapping = {
        "bank_statements": "Used for assessing borrower's cashflow stability and debt-service capacity.",
        "gst": "Used for verifying operational business activity and tax filing consistency.",
        "upi": "Used for measuring merchant transaction volumes and monthly velocity.",
        "invoices": "Used for checking customer billing cycles and concentration risks.",
        "business_profile": "Used for verifying merchant identity and duration of business operations."
    }
    used_for_text = used_for_mapping.get(canonical_source, "Used for credit readiness scoring.")

    new_consent = Consent(
        borrower_id=borrower_id,
        data_source=data_source,
        purpose=purpose,
        scope=scope,
        expiry=expiry,
        status="approved",
        used_for=used_for_text,
        granted_at=datetime.datetime.utcnow()
    )
    db.add(new_consent)

    # 4. Write audit log
    audit_log = ConsentAuditLog(
        borrower_id=borrower_id,
        data_source=data_source,
        action="grant",
        purpose=purpose,
        timestamp=datetime.datetime.utcnow(),
        details=f"Granted with scope '{scope}', expires at {expiry.isoformat()}."
    )
    db.add(audit_log)
    
    await db.flush()
    return new_consent

async def record_consent_revocation(
    db: AsyncSession,
    borrower_id: str,
    data_source: str
) -> Optional[Consent]:
    """
    Revokes active consent for a borrower's specific data source.
    """
    stmt = select(Consent).where(
        and_(
            Consent.borrower_id == borrower_id,
            Consent.data_source == data_source,
            Consent.status == "approved"
        )
    )
    result = await db.execute(stmt)
    active_consent = result.scalar_one_or_none()
    
    if not active_consent:
        return None
        
    active_consent.status = "revoked"
    active_consent.revoked_at = datetime.datetime.utcnow()
    db.add(active_consent)
    
    # Audit log
    audit_log = ConsentAuditLog(
        borrower_id=borrower_id,
        data_source=data_source,
        action="revoke",
        purpose=active_consent.purpose,
        timestamp=datetime.datetime.utcnow(),
        details="Consent manually revoked by borrower."
    )
    db.add(audit_log)
    
    await db.flush()
    return active_consent

async def record_consent_usage(
    db: AsyncSession,
    borrower_id: str,
    data_source: str,
    intended_purpose: str,
    details: Optional[str] = None
) -> bool:
    """
    Validates and records usage of a data source.
    Checks if active consent exists, has not expired, and complies with purpose mapping.
    """
    # 1. Enforce purpose limitation
    if not is_usage_permitted(data_source, intended_purpose):
        audit_log = ConsentAuditLog(
            borrower_id=borrower_id,
            data_source=data_source,
            action="use_denied",
            purpose=intended_purpose,
            timestamp=datetime.datetime.utcnow(),
            details=f"Usage denied: Intended purpose '{intended_purpose}' does not match canonical purpose."
        )
        db.add(audit_log)
        await db.flush()
        return False

    # 2. Check active consent
    stmt = select(Consent).where(
        and_(
            Consent.borrower_id == borrower_id,
            Consent.data_source == data_source,
            Consent.status == "approved"
        )
    )
    result = await db.execute(stmt)
    consent = result.scalar_one_or_none()

    if not consent:
        # Log unauthorized usage attempt
        audit_log = ConsentAuditLog(
            borrower_id=borrower_id,
            data_source=data_source,
            action="use_denied",
            purpose=intended_purpose,
            timestamp=datetime.datetime.utcnow(),
            details="Usage denied: No active consent record found."
        )
        db.add(audit_log)
        await db.flush()
        return False

    # 3. Check expiration
    now = datetime.datetime.utcnow()
    if consent.expiry < now:
        consent.status = "expired"
        db.add(consent)
        
        audit_log = ConsentAuditLog(
            borrower_id=borrower_id,
            data_source=data_source,
            action="use_denied",
            purpose=intended_purpose,
            timestamp=datetime.datetime.utcnow(),
            details=f"Usage denied: Consent expired at {consent.expiry.isoformat()}."
        )
        db.add(audit_log)
        await db.flush()
        return False

    # 4. Success: Record usage
    audit_log = ConsentAuditLog(
        borrower_id=borrower_id,
        data_source=data_source,
        action="use",
        purpose=intended_purpose,
        timestamp=now,
        details=details or "Authorized data access."
    )
    db.add(audit_log)
    await db.flush()
    return True

async def get_active_consents(db: AsyncSession, borrower_id: str) -> List[Consent]:
    """
    Lists all consents for a borrower. Automatically updates and flags expired consents.
    """
    stmt = select(Consent).where(Consent.borrower_id == borrower_id)
    result = await db.execute(stmt)
    consents = result.scalars().all()
    
    now = datetime.datetime.utcnow()
    modified = False
    for c in consents:
        if c.status == "approved" and c.expiry < now:
            c.status = "expired"
            db.add(c)
            modified = True
            
            # Log auto-expiration
            audit_log = ConsentAuditLog(
                borrower_id=borrower_id,
                data_source=c.data_source,
                action="expire",
                purpose=c.purpose,
                timestamp=now,
                details=f"Consent automatically marked as expired (expiry was {c.expiry.isoformat()})."
            )
            db.add(audit_log)

    if modified:
        await db.flush()
        
    return list(consents)

async def get_consent_trace_log(db: AsyncSession, borrower_id: str) -> List[ConsentAuditLog]:
    """
    Retrieves the full Consent Trace audit history log for a borrower.
    """
    stmt = select(ConsentAuditLog).where(
        ConsentAuditLog.borrower_id == borrower_id
    ).order_by(ConsentAuditLog.timestamp.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())
