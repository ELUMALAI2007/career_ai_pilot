"""
CareerPilot AI - Resume PDF Report Generator
Generates a downloadable, beautifully formatted PDF report summarizing Resume Intelligence & ATS analysis.
"""

import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.models.resume import ResumeAnalysis


class ResumePdfReportGenerator:
    """Generates clean PDF analysis report using ReportLab."""

    @classmethod
    def generate_pdf(cls, analysis: ResumeAnalysis) -> BytesIO:
        """Renders analysis details into a BytesIO PDF buffer."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        
        styles = getSampleStyleSheet()
        
        # Custom Paragraph Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=8
        )
        
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=15
        )

        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2563EB'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#334155')
        )

        elements = []

        # Header Title
        elements.append(Paragraph("CareerPilot AI — Resume Intelligence Report", title_style))
        elements.append(Paragraph(f"Candidate Resume: {analysis.resume.filename} | Target Role: {analysis.resume.target_role} | Evaluated: {analysis.evaluated_at.strftime('%Y-%m-%d')}", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

        # Score Overview Table
        score_data = [
            ["Metric", "Score", "Evaluation Summary"],
            ["Overall Readiness Score", f"{analysis.overall_score}/100", "Weighted Composite Evaluation"],
            ["ATS Compatibility Score", f"{analysis.ats_score}/100", "Machine Readability & Keyword Density"],
            ["Resume Quality Score", f"{analysis.quality_score}/100", "Action Verbs, Metrics & Structure"],
            ["Job Match Score", f"{analysis.job_match_score}/100", f"Target Role Skill Overlap ({analysis.resume.target_role})"],
            ["Completeness Score", f"{analysis.completeness_score}/100", "Section Coverage & Contact Information"]
        ]

        t_scores = Table(score_data, colWidths=[180, 80, 280])
        t_scores.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#FFFFFF')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('FONTNAME', (0, 1), (1, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 1), (1, -1), colors.HexColor('#2563EB')),
        ]))
        elements.append(t_scores)
        elements.append(Spacer(1, 15))

        # Recruiter First Impression
        elements.append(Paragraph("Recruiter First Impression", h2_style))
        elements.append(Paragraph(analysis.recruiter_impression or "Solid profile with good technical structure.", body_style))
        elements.append(Spacer(1, 12))

        # Priority Improvement Plan ("Fix These First")
        elements.append(Paragraph("Priority Improvement Plan (Fix These First)", h2_style))
        priority_data = analysis.get_priority_plan()
        high_p = priority_data.get("high_priority", [])
        med_p = priority_data.get("medium_priority", [])
        
        plan_lines = []
        for item in high_p:
            plan_lines.append(f"• <b>[HIGH PRIORITY]</b> {item}")
        for item in med_p:
            plan_lines.append(f"• <b>[MEDIUM PRIORITY]</b> {item}")

        elements.append(Paragraph("<br/>".join(plan_lines) if plan_lines else "No critical changes needed.", body_style))
        elements.append(Spacer(1, 12))

        # Keywords & Skill Gaps
        elements.append(Paragraph("Keyword & Skill Gap Breakdown", h2_style))
        kw_data = analysis.get_keyword_analysis()
        missing_kw = kw_data.get("top_10_to_add", [])
        
        kw_text = f"<b>Top Recommended Keywords to Add Naturally:</b> {', '.join(missing_kw) if missing_kw else 'All key role keywords present.'}"
        elements.append(Paragraph(kw_text, body_style))
        elements.append(Spacer(1, 15))

        # Recruiter Red Flags & Strengths
        elements.append(Paragraph("Strengths & Recruiter Red Flags", h2_style))
        strengths = analysis.get_strengths()
        red_flags = analysis.get_red_flags()

        sf_lines = [f"✅ <b>Strength:</b> {s}" for s in strengths]
        rf_lines = [f"⚠️ <b>Red Flag:</b> {r}" for r in red_flags]

        elements.append(Paragraph("<br/>".join(sf_lines + rf_lines) if (sf_lines or rf_lines) else "Balanced profile.", body_style))
        elements.append(Spacer(1, 20))

        # Footer Notice
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
        elements.append(Paragraph("Generated automatically by CareerPilot AI Resume Intelligence Engine.", subtitle_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer
