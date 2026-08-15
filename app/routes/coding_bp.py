"""
CareerPilot AI - Coding Blueprint (`/coding`)
Controller for Data Structures and Algorithm coding challenges.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.services.coding_service import CodingService

coding_bp = Blueprint('coding', __name__)


@coding_bp.route('/')
@login_required
def index():
    """Coding problems list view."""
    problems = CodingService.get_problems()
    return render_template('coding/index.html', problems=problems)
