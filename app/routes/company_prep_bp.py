"""
CareerPilot AI - Company Prep Blueprint (`/company-prep`)
Controller for company profiles and interview experience insights.
"""

from flask import Blueprint, render_template
from flask_login import login_required

company_prep_bp = Blueprint('company_prep', __name__)


@company_prep_bp.route('/')
@login_required
def index():
    """Company preparation hub landing page."""
    return render_template('company_prep/index.html')
