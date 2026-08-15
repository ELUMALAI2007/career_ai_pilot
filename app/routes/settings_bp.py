"""
CareerPilot AI - Settings Blueprint (`/settings`)
Controller for candidate settings, notification preferences, and password updates.
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.forms.settings_forms import AccountSettingsForm, NotificationSettingsForm
from app.services.settings_service import SettingsService

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """User account settings view."""
    account_form = AccountSettingsForm()
    notif_form = NotificationSettingsForm()
    
    settings = SettingsService.get_or_create_settings(current_user.id)
    return render_template('settings/index.html', account_form=account_form, notif_form=notif_form, settings=settings)
