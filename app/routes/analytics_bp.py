"""
CareerPilot AI - Analytics Blueprint (`/analytics`)
Controller for candidate performance charts and readiness metrics.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService
from app.services.analytics_pdf_report import AnalyticsPdfReportGenerator

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/', methods=['GET'])
@login_required
def index():
    """Detailed Placement Intelligence Dashboard View."""
    intelligence = AnalyticsService.compute_placement_intelligence(current_user.id)
    return render_template('analytics/index.html', intelligence=intelligence)


@analytics_bp.route('/refresh', methods=['POST'])
@login_required
def refresh():
    """Recalculates user performance metrics and records historical snapshot."""
    intelligence = AnalyticsService.compute_placement_intelligence(current_user.id)
    flash('Placement Intelligence metrics refreshed successfully!', 'success')
    return redirect(url_for('analytics.index'))


@analytics_bp.route('/download-report', methods=['GET'])
@login_required
def download_report():
    """Generates and downloads personalized Candidate Placement Intelligence PDF Report."""
    intelligence = AnalyticsService.compute_placement_intelligence(current_user.id)
    pdf_buffer = AnalyticsPdfReportGenerator.generate_pdf(intelligence)
    
    filename = f"CareerPilot_Placement_Report_{current_user.full_name.replace(' ', '_')}.pdf"
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
