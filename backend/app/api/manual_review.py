import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.models import ManualReview, LenderDecision
from backend.app.schemas.recommendation import ManualReviewResponse, ManualReviewResolveRequest

router = APIRouter(prefix="/manual-review", tags=["Manual Review Queue"])

@router.get("/queue", response_model=List[ManualReviewResponse])
async def get_queue(
    db: AsyncSession = Depends(get_db)
):
    """
    Lists all borrower applications currently routed to the Manual Review queue
    (status is 'pending' or 'escalated').
    """
    stmt = select(ManualReview).where(
        or_(ManualReview.status == "pending", ManualReview.status == "escalated")
    ).order_by(ManualReview.created_at.desc())
    
    result = await db.execute(stmt)
    return list(result.scalars().all())

@router.get("/{borrower_id}", response_model=ManualReviewResponse)
async def get_review_details(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches the detail view for a single manual review case.
    """
    stmt = select(ManualReview).where(ManualReview.borrower_id == borrower_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No manual review record found for borrower '{borrower_id}'."
        )
    return review

@router.post("/{borrower_id}/resolve", response_model=ManualReviewResponse)
async def resolve_review(
    borrower_id: str,
    request: ManualReviewResolveRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Lender resolves a manual review case, submitting a decision (resolved/escalated/rejected) and notes.
    Saves to the manual review state and logs a lender decision audit entry.
    """
    stmt = select(ManualReview).where(ManualReview.borrower_id == borrower_id)
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No manual review record found for borrower '{borrower_id}'."
        )
        
    # Update manual review status
    review.status = request.resolution # e.g. resolved, escalated
    review.resolved_at = datetime.datetime.utcnow()
    review.resolution_notes = request.notes
    db.add(review)

    # Convert resolution status to LenderDecision equivalent (approved/rejected/escalated)
    lender_decision_map = {
        "resolved": "approved",
        "rejected": "rejected",
        "escalated": "escalated"
    }
    decision_val = lender_decision_map.get(request.resolution, "escalated")

    # Record final lender decision
    lender_decision = LenderDecision(
        borrower_id=borrower_id,
        lender_id=review.assigned_to or "lender_default",
        decision=decision_val,
        notes=request.notes,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(lender_decision)
    
    await db.flush()
    return review
