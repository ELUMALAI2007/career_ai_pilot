"""
CareerPilot AI - Profile Blueprint (`/profile`)
Controller for managing personal candidate credentials and academic details.
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.forms.profile_forms import UserProfileForm
from app.services.profile_service import ProfileService

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """User profile overview and management view."""
    form = UserProfileForm()
    if form.validate_on_submit():
        ProfileService.update_user_profile(current_user.id, {
            'phone': form.phone.data,
            'headline': form.headline.data,
            'bio': form.bio.data,
            'target_role': form.target_role.data,
            'linkedin_url': form.linkedin_url.data,
            'github_url': form.github_url.data
        })
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.index'))
        
    return render_template('profile/index.html', form=form)
