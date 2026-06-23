from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from app.models import TrustSummary

# NOTE: Dependency on 'reportlab' library. Added to requirements.txt.

def export_trust_summary_pdf(summary: TrustSummary, borrower_name: str, business_name: str) -> BytesIO:
    """
    Generates a beautifully styled PDF document of the Underwriting Trust Summary.
    Returns a BytesIO stream containing the PDF binary.
    """
    buffer = BytesIO()
    
    # Set page margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom color palette matching the premium trust theme
    primary_color = colors.HexColor("#1A365D")   # Deep navy
    secondary_color = colors.HexColor("#2B6CB0") # Medium blue
    text_color = colors.HexColor("#2D3748")      # Charcoal text
    bg_light = colors.HexColor("#F7FAFC")        # Warm off-white
    border_color = colors.HexColor("#E2E8F0")    # Slate borders
    
    # Base paragraph styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=6
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=primary_color
    )
    
    # Center aligned styles for readiness metrics table
    readiness_header_style = ParagraphStyle(
        'ReadinessHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.white,
        alignment=1 # Center
    )
    
    readiness_val_style = ParagraphStyle(
        'ReadinessVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        alignment=1 # Center
    )
    
    ai_narrative_style = ParagraphStyle(
        'AINarrativeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#2C5282") # Dark slate blue
    )

    story = []
    
    # 1. Document Title
    story.append(Paragraph("Underwriting Trust Summary™", title_style))
    story.append(Spacer(1, 5))
    
    # 2. Borrower Metadata Grid
    metadata_data = [
        [
            Paragraph("Borrower Name:", meta_label_style), Paragraph(borrower_name, body_style),
            Paragraph("Business Name:", meta_label_style), Paragraph(business_name, body_style)
        ],
        [
            Paragraph("Report Date:", meta_label_style), Paragraph(summary.generated_at.strftime("%Y-%m-%d %H:%M:%S UTC"), body_style),
            Paragraph("Borrower ID:", meta_label_style), Paragraph(summary.borrower_id, body_style)
        ]
    ]
    
    meta_table = Table(metadata_data, colWidths=[100, 165, 100, 165])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('GRID', (0,0), (-1,-1), 1, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # 3. Core Risk Readiness Profile Table
    story.append(Paragraph("Credit Readiness Profile", h2_style))
    
    grade_html = f"<font size=14 color='#1A365D'><b>{summary.readiness_grade}</b></font>"
    readiness_data = [
        [
            Paragraph("Readiness Grade", readiness_header_style), 
            Paragraph("Confidence Band", readiness_header_style), 
            Paragraph("Data Coverage", readiness_header_style), 
            Paragraph("Lending Action", readiness_header_style)
        ],
        [
            Paragraph(grade_html, readiness_val_style),
            Paragraph(summary.confidence_band, readiness_val_style),
            Paragraph(f"{summary.coverage_pct}%", readiness_val_style),
            Paragraph(f"<b>{summary.recommended_action}</b>", readiness_val_style)
        ]
    ]
    
    readiness_table = Table(readiness_data, colWidths=[132, 132, 132, 132])
    readiness_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, border_color),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(readiness_table)
    story.append(Spacer(1, 10))
    
    # 4. AI Underwriting Narrative Callout Box
    story.append(Paragraph("AI Underwriting Narrative (Gemini 2.5 Pro)", h2_style))
    ai_box_data = [[Paragraph(summary.ai_summary, ai_narrative_style)]]
    ai_table = Table(ai_box_data, colWidths=[530])
    ai_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")), # Very light ice-blue
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ai_table)
    story.append(Spacer(1, 10))
    
    # 5. Verified Sources & Detail Flags Table
    story.append(Paragraph("Detailed Risk & Verification Analysis", h2_style))
    
    detail_data = [
        [
            Paragraph("Verified Data Sources", meta_label_style), 
            Paragraph(", ".join(summary.verified_sources) if summary.verified_sources else "None", body_style)
        ],
        [
            Paragraph("Risk Signals Flagged", meta_label_style), 
            Paragraph(", ".join(summary.risk_signals) if summary.risk_signals else "None", body_style)
        ],
        [
            Paragraph("Stability Indicators", meta_label_style), 
            Paragraph(", ".join(summary.stability_indicators) if summary.stability_indicators else "None", body_style)
        ],
        [
            Paragraph("Reason Codes", meta_label_style), 
            Paragraph(", ".join(summary.reason_codes) if summary.reason_codes else "None", body_style)
        ]
    ]
    
    detail_table = Table(detail_data, colWidths=[140, 390])
    detail_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, border_color),
        ('BACKGROUND', (0,0), (0,-1), bg_light),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(detail_table)
    
    # Build the document flow
    doc.build(story)
    buffer.seek(0)
    return buffer
