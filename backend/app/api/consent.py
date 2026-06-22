from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.schemas.consent import (
    GrantConsentRequest,
    RevokeConsentRequest,
    ConsentResponse,
    ConsentAuditLogResponse
)
from backend.app.services.consent_trace import consent_tracker

router = APIRouter(prefix="/consent", tags=["Consent Management"])

@router.post("/grant", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def grant_consent(
    request: GrantConsentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Grants consent for a borrower's specific data source.
    If borrower doesn't exist, returns 404.
    """
    try:
        consent = await consent_tracker.record_consent_grant(
            db=db,
            borrower_id=request.borrower_id,
            data_source=request.data_source,
            scope=request.scope,
            expiry=request.expiry
        )
        return consent
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/revoke", response_model=ConsentResponse)
async def revoke_consent(
    request: RevokeConsentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Revokes consent for a borrower's specific data source.
    If no active consent exists, returns 404.
    """
    consent = await consent_tracker.record_consent_revocation(
        db=db,
        borrower_id=request.borrower_id,
        data_source=request.data_source
    )
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active consent found for borrower '{request.borrower_id}' and source '{request.data_source}'."
        )
    return consent

@router.get("/{borrower_id}", response_model=List[ConsentResponse])
async def list_consents(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Lists all consents for a borrower. Automatically flags and updates expired records.
    """
    consents = await consent_tracker.get_active_consents(db, borrower_id)
    return consents

@router.get("/{borrower_id}/trace", response_model=List[ConsentAuditLogResponse])
async def get_consent_trace(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the timestamped history of grants, revocations, and usages (the Consent Trace audit log).
    """
    trace_log = await consent_tracker.get_consent_trace_log(db, borrower_id)
    return trace_log
