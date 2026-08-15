"""
CareerPilot AI - Communication Blueprint (`/communication`)
Controller for soft skills assessment and writing feedback.
"""

from flask import Blueprint, render_template
from flask_login import login_required

communication_bp = Blueprint('communication', __name__)


@communication_bp.route('/')
@login_required
def index():
    """Communication skills landing page."""
    return render_template('communication/index.html')
