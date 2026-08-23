"""
CareerPilot AI — Placement Intelligence PDF Report Generator
Generates a downloadable, beautifully formatted PDF report summarizing candidate Placement Intelligence & Career Readiness.
Strictly consumes exact data payload from AnalyticsService to guarantee consistency.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class AnalyticsPdfReportGenerator:
    """Generates clean multi-page PDF Placement Intelligence Report using ReportLab."""

    @classmethod
    def generate_pdf(cls, intelligence: dict) -> BytesIO:
        """Renders Placement Intelligence metrics into a BytesIO PDF buffer."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

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
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=15
        )

        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
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

        # 1. Header Title & Candidate Metadata
        user_name = intelligence.get('user_name', 'Candidate')
        overall_score = intelligence.get('overall_score', 0.0)
        confidence = intelligence.get('confidence', 'Medium')
        status_name = intelligence.get('placement_status', 'Developing')
        last_updated = intelligence.get('last_updated', '')

        elements.append(Paragraph("CareerPilot AI — Placement Intelligence Report", title_style))
        elements.append(Paragraph(
            f"Candidate: <b>{user_name}</b> | Generated: {last_updated} | Data Confidence: <b>{confidence}</b>",
            subtitle_style
        ))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

        # 2. Executive Readiness Summary Table
        summary_table_data = [
            ["Metric", "Value / Rating", "Description & Guidance"],
            ["Overall Placement Readiness", f"{overall_score} / 100", f"Status: {status_name}"],
            ["Analytics Confidence", confidence, f"Based on {intelligence.get('active_modules_count', 0)} of {intelligence.get('total_modules_count', 8)} active assessment modules"],
            ["Evaluation Mode", "Provisional" if intelligence.get('is_provisional') else "Comprehensive", "Dynamic weight redistribution applied for missing modules"]
        ]

        t_summary = Table(summary_table_data, colWidths=[160, 110, 270])
        t_summary.setStyle(TableStyle([
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
        elements.append(t_summary)
        elements.append(Spacer(1, 15))

        # 3. AI Placement Career Summary
        elements.append(Paragraph("AI Placement Career Summary", h2_style))
        elements.append(Paragraph(intelligence.get("career_summary", "Evaluation complete."), body_style))
        elements.append(Spacer(1, 12))

        # 4. Multi-Module Competency Breakdown Table
        elements.append(Paragraph("Multi-Dimensional Competency Breakdown", h2_style))
        modules = intelligence.get("modules", {})
        
        comp_data = [["Assessment Domain", "Status", "Score / Rating", "Key Metrics Summary"]]
        
        for mod_key, mod_title in [
            ("resume", "Resume & ATS Analysis"),
            ("aptitude", "Aptitude & Logic"),
            ("coding", "Coding & DSA"),
            ("communication", "Communication Skills"),
            ("interview", "Mock Interview Prep"),
            ("skills", "Technical Skill Breadth"),
            ("roadmap", "Learning Roadmap"),
            ("consistency", "Preparation Consistency")
        ]:
            mod_info = modules.get(mod_key, {})
            m_status = mod_info.get("status", "N/A")
            m_score = f"{mod_info.get('score')}/100" if mod_info.get('score') is not None else "Pending"
            
            if mod_key == "resume":
                metrics_desc = f"ATS: {mod_info.get('ats_score', 0)} | Quality: {mod_info.get('quality_score', 0)}"
            elif mod_key == "aptitude":
                metrics_desc = f"Accuracy: {mod_info.get('accuracy_pct', 0)}% | Solved: {mod_info.get('total_solved', 0)}"
            elif mod_key == "coding":
                metrics_desc = f"Solved: {mod_info.get('problems_solved', 0)} | Success Rate: {mod_info.get('success_rate_pct', 0)}%"
            elif mod_key == "communication":
                metrics_desc = f"Grammar: {mod_info.get('grammar_score', 0)} | Clarity: {mod_info.get('clarity_score', 0)}"
            elif mod_key == "interview":
                metrics_desc = f"Completed Interviews: {mod_info.get('completed_interviews', 0)}"
            else:
                metrics_desc = "Activity tracked"

            comp_data.append([mod_title, m_status, m_score, metrics_desc])

        t_comp = Table(comp_data, colWidths=[150, 80, 90, 220])
        t_comp.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#FFFFFF')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        elements.append(t_comp)
        elements.append(Spacer(1, 15))

        # 5. Role Suitability & Matching Breakdown
        elements.append(Paragraph("Target Career Role Suitability Alignment", h2_style))
        roles = intelligence.get("role_suitability", [])
        
        role_lines = []
        for r in roles[:4]:
            matched_str = ", ".join(r.get("matched_skills", [])) if r.get("matched_skills") else "None"
            missing_str = ", ".join(r.get("missing_skills", [])) if r.get("missing_skills") else "None"
            role_lines.append(
                f"• <b>{r['title']}</b> (Match: <b>{r['match_pct']}%</b>)<br/>"
                f"  Matched Skills: {matched_str} | Missing Skills: {missing_str}"
            )

        elements.append(Paragraph("<br/><br/>".join(role_lines) if role_lines else "No target role data.", body_style))
        elements.append(Spacer(1, 15))

        # 6. Actionable Next Steps
        elements.append(Paragraph("Personalized High-Priority Action Plan", h2_style))
        next_steps = intelligence.get("next_steps", [])
        
        step_lines = []
        for idx, step in enumerate(next_steps[:4], 1):
            step_lines.append(f"{idx}. <b>[{step.get('priority', 'High')}] {step['title']}</b><br/>   Reason: {step['reason']}")

        elements.append(Paragraph("<br/><br/>".join(step_lines) if step_lines else "Continue current practice schedule.", body_style))
        elements.append(Spacer(1, 20))

        # Footer Notice & Disclaimer
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
        elements.append(Paragraph(
            "<b>Disclaimer:</b> This report is an internal preparation indicator generated by CareerPilot AI. "
            "It does not constitute a legal guarantee of employment or company selection.",
            subtitle_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer
