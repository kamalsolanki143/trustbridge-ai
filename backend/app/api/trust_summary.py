from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.models import Borrower
from backend.app.schemas.recommendation import TrustSummaryResponse
from backend.app.services.trust_summary import summary_generator, pdf_export

router = APIRouter(prefix="/trust-summary", tags=["Underwriting Trust Summary"])

@router.post("/generate/{borrower_id}", response_model=TrustSummaryResponse, status_code=status.HTTP_201_CREATED)
async def generate_summary(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Triggers the generation of the Underwriting Trust Summary for a borrower.
    Aggregates findings, calls Gemini for an underwriting narrative, and logs consent usage.
    """
    try:
        summary = await summary_generator.generate_trust_summary(db, borrower_id)
        return summary
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{borrower_id}", response_model=TrustSummaryResponse)
async def get_summary(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the latest generated Underwriting Trust Summary as JSON.
    """
    summary = await summary_generator.get_latest_trust_summary(db, borrower_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_444_NOT_FOUND if False else status.HTTP_404_NOT_FOUND, # Standard 404
            detail=f"No trust summary found for borrower '{borrower_id}'. Please generate one first."
        )
    return summary

@router.get("/{borrower_id}/pdf")
async def get_summary_pdf(
    borrower_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Exports the latest generated Underwriting Trust Summary as a downloadable PDF.
    """
    summary = await summary_generator.get_latest_trust_summary(db, borrower_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trust summary found for borrower '{borrower_id}'. Please generate one first."
        )
        
    stmt = select(Borrower).where(Borrower.id == borrower_id)
    res = await db.execute(stmt)
    borrower = res.scalar_one_or_none()
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Borrower profile for '{borrower_id}' not found."
        )

    # Generate the PDF file buffer
    pdf_buffer = pdf_export.export_trust_summary_pdf(
        summary=summary,
        borrower_name=borrower.name,
        business_name=borrower.business_name
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=trust_summary_{borrower_id}.pdf"
        }
    )
