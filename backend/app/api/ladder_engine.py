from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.models import Borrower, LenderPolicy
from backend.app.schemas.recommendation import LadderDecision
from backend.app.services._stubs import get_ladder_decision

router = APIRouter(prefix="/ladder", tags=["Ladder Decision Engine"])

@router.get("/{borrower_id}", response_model=LadderDecision)
async def get_decision(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches the current Credit Ladder recommendation for a borrower,
    taking into account the active lender policy configuration.
    """
    # Verify borrower exists
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    res = await db.execute(stmt)
    if not res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile '{borrower_id}' not found."
        )

    # Get active policy preference (or default to Balanced)
    policy_stmt = select(LenderPolicy).order_by(LenderPolicy.updated_at.desc())
    policy_res = await db.execute(policy_stmt)
    latest_policy = policy_res.scalars().first()
    preference = latest_policy.preference if latest_policy else "Balanced"

    # Call Krrish/Kamal engine stub
    decision = get_ladder_decision(borrower_id, preference)
    return decision

@router.post("/{borrower_id}/recompute", response_model=LadderDecision)
async def recompute_decision(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Forces a recomputation of the Credit Ladder recommendation (e.g. after data updates).
    """
    # Verify borrower exists
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    res = await db.execute(stmt)
    if not res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile '{borrower_id}' not found."
        )

    policy_stmt = select(LenderPolicy).order_by(LenderPolicy.updated_at.desc())
    policy_res = await db.execute(policy_stmt)
    latest_policy = policy_res.scalars().first()
    preference = latest_policy.preference if latest_policy else "Balanced"

    # Recompute recommendation
    decision = get_ladder_decision(borrower_id, preference)
    return decision
