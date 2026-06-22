from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.models import Borrower, LenderPolicy, ManualReview
from backend.app.schemas.borrower import BorrowerCreate, BorrowerResponse, BorrowerDashboardResponse
from backend.app.services._stubs import get_readiness_profile, get_ladder_decision, get_growth_roadmap
from backend.app.services.consent_trace import consent_tracker

router = APIRouter(prefix="/borrower", tags=["Borrower Profile & Dashboard"])

@router.post("", response_model=BorrowerResponse, status_code=status.HTTP_201_CREATED)
async def create_borrower(
    request: BorrowerCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registers a new borrower profile in the database.
    """
    # Check if PAN or GSTIN already exists
    stmt = select(Borrower).where(
        (Borrower.id == request.id) | 
        (Borrower.pan == request.pan) | 
        (Borrower.gstin == request.gstin)
    )
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Borrower with this ID, PAN, or GSTIN already exists."
        )

    new_borrower = Borrower(
        id=request.id,
        name=request.name,
        business_name=request.business_name,
        pan=request.pan,
        gstin=request.gstin,
        email=request.email,
        phone=request.phone
    )
    db.add(new_borrower)
    await db.flush()
    return new_borrower

@router.get("/{borrower_id}", response_model=BorrowerResponse)
async def get_borrower(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches the borrower profile.
    """
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    result = await db.execute(stmt)
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile '{borrower_id}' not found."
        )
    return borrower

@router.get("/{borrower_id}/dashboard", response_model=BorrowerDashboardResponse)
async def get_dashboard(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Aggregates borrower-facing dashboard: credit readiness grade, coverage metrics,
    ladder outcome, consent checklists, and growth milestones.
    Routes to the Manual Review queue automatically if needed.
    """
    # 1. Verify borrower exists
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    result = await db.execute(stmt)
    borrower = result.scalar_one_or_none()
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile '{borrower_id}' not found."
        )

    # 2. Get readiness details from Krrish's engine stub
    readiness = get_readiness_profile(borrower_id)

    # 3. Get lender policy preference (or default Balanced)
    policy_stmt = select(LenderPolicy).order_by(LenderPolicy.updated_at.desc())
    policy_res = await db.execute(policy_stmt)
    latest_policy = policy_res.scalars().first()
    preference = latest_policy.preference if latest_policy else "Balanced"

    # 4. Fetch decision recommendation from Kamal's engine stub
    ladder = get_ladder_decision(borrower_id, preference)

    # 5. Route to Manual Review queue automatically if decision is Manual Review
    if ladder.decision == "Manual Review":
        mr_stmt = select(ManualReview).where(ManualReview.borrower_id == borrower_id)
        mr_res = await db.execute(mr_stmt)
        if not mr_res.scalar_one_or_none():
            new_mr = ManualReview(
                borrower_id=borrower_id,
                status="pending",
                assigned_to="lender_default",
                risk_signals=readiness.risk_signals,
                anomaly_flags=readiness.reason_codes
            )
            db.add(new_mr)
            # Auto-flush to ensure manual review record is created
            await db.flush()

    # 6. Fetch consent status map from DB
    consents = await consent_tracker.get_active_consents(db, borrower_id)
    consent_status_overview = {}
    possible_sources = ["bank_statements", "gst", "upi", "invoices", "business_profile"]
    
    for source in possible_sources:
        match = next((c for c in consents if c.data_source == source), None)
        consent_status_overview[source] = match.status if match else "missing"

    # 7. Get Roadmap
    growth_roadmap = get_growth_roadmap(borrower_id)

    return BorrowerDashboardResponse(
        borrower_id=borrower_id,
        latest_readiness_grade=readiness.readiness_grade,
        coverage_pct=readiness.coverage_pct,
        active_ladder_outcome=ladder.decision,
        consent_status_overview=consent_status_overview,
        growth_roadmap=growth_roadmap
    )
