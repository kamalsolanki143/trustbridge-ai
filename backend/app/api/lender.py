import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Borrower, LenderPolicy, LenderDecision
from app.schemas.recommendation import (
    LenderPolicyRequest,
    LenderPolicyResponse,
    LenderDecisionRecordRequest,
    LenderDecisionRecordResponse,
    LenderApplicationResponse
)
from app.services._stubs import get_readiness_profile, get_ladder_decision

router = APIRouter(prefix="/lender", tags=["Lender Actions & Settings"])

@router.get("/applications", response_model=List[LenderApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(get_db)
):
    """
    List of borrower applications with readiness grade, ladder outcome recommendation,
    and risk signals (lender-facing pipeline view).
    """
    stmt = select(Borrower)
    res = await db.execute(stmt)
    borrowers = res.scalars().all()
    
    # Get active policy preference (or default Balanced)
    policy_stmt = select(LenderPolicy).order_by(LenderPolicy.updated_at.desc())
    policy_res = await db.execute(policy_stmt)
    latest_policy = policy_res.scalars().first()
    preference = latest_policy.preference if latest_policy else "Balanced"

    applications = []
    for borrower in borrowers:
        readiness = get_readiness_profile(borrower.id)
        ladder = get_ladder_decision(borrower.id, preference)
        applications.append({
            "borrower_id": borrower.id,
            "name": borrower.name,
            "business_name": borrower.business_name,
            "readiness_grade": readiness.readiness_grade,
            "ladder_outcome": ladder.decision,
            "risk_signals": readiness.risk_signals
        })
        
    return applications

@router.post("/policy", response_model=LenderPolicyResponse)
async def set_policy(
    request: LenderPolicyRequest,
    lender_id: str = "lender_default",
    db: AsyncSession = Depends(get_db)
):
    """
    Sets the risk preference policy for a lender (Conservative | Balanced | Aggressive).
    """
    # Check if policy already exists for lender
    stmt = select(LenderPolicy).where(LenderPolicy.lender_id == lender_id)
    result = await db.execute(stmt)
    policy = result.scalar_one_or_none()
    
    if not policy:
        policy = LenderPolicy(
            lender_id=lender_id,
            preference=request.preference,
            updated_at=datetime.datetime.utcnow()
        )
        db.add(policy)
    else:
        policy.preference = request.preference
        policy.updated_at = datetime.datetime.utcnow()
        db.add(policy)
        
    await db.flush()
    return policy

@router.get("/{lender_id}/policy", response_model=LenderPolicyResponse)
async def get_policy(
    lender_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the current risk preference policy config for a lender.
    """
    stmt = select(LenderPolicy).where(LenderPolicy.lender_id == lender_id)
    result = await db.execute(stmt)
    policy = result.scalar_one_or_none()
    
    if not policy:
        # Default policy if none configured
        policy = LenderPolicy(
            lender_id=lender_id,
            preference="Balanced",
            updated_at=datetime.datetime.utcnow()
        )
        db.add(policy)
        await db.flush()
        
    return policy

@router.post("/{borrower_id}/decision", response_model=LenderDecisionRecordResponse, status_code=status.HTTP_201_CREATED)
async def record_decision(
    borrower_id: str,
    request: LenderDecisionRecordRequest,
    lender_id: str = "lender_default",
    db: AsyncSession = Depends(get_db)
):
    """
    Lender records their final audit action (approve/reject/escalate) taken on a borrower profile.
    """
    # Verify borrower exists
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    result = await db.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile '{borrower_id}' not found."
        )
        
    decision_record = LenderDecision(
        borrower_id=borrower_id,
        lender_id=lender_id,
        decision=request.decision,
        notes=request.notes,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(decision_record)
    await db.flush()
    return decision_record
