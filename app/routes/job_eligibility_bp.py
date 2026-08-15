"""
CareerPilot AI - Job Eligibility Blueprint (`/eligibility`)
Controller for campus placement drive qualification checks.
"""

from flask import Blueprint, render_template
from flask_login import login_required

job_eligibility_bp = Blueprint('job_eligibility', __name__)


@job_eligibility_bp.route('/')
@login_required
def index():
    """Job eligibility checker view."""
    return render_template('job_eligibility/index.html')
