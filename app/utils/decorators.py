"""
CareerPilot AI Custom Decorators
Decorators for role-based access control and profile completeness enforcement.
"""

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator restricting access strictly to Administrator users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Administrator permissions required to access this area.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function



def profile_completed_required(f):
    """Decorator enforcing completed profile setup prior to accessing placement features."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Check candidate academic/profile completion state
        return f(*args, **kwargs)
    return decorated_function
