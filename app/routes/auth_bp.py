"""
CareerPilot AI - Auth Blueprint (`/auth`)
Controller for login, registration, logout, and password management.
"""

import json
import urllib.request
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth_forms import LoginForm, RegisterForm
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Login View."""
    if current_user.is_authenticated:
        if current_user.is_pending:
            return redirect(url_for('auth.pending'))
        elif current_user.is_rejected:
            return redirect(url_for('auth.rejected'))
        return redirect(url_for('dashboard.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            if user.is_pending:
                return redirect(url_for('auth.pending'))
            elif user.is_rejected:
                return redirect(url_for('auth.rejected'))
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        flash('Invalid email or password.', 'danger')
        
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration View."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            AuthService.register_user(form.full_name.data, form.email.data, form.password.data)
            flash('Account created successfully! Please log in with your credentials.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as val_err:
            flash(str(val_err), 'danger')
        except Exception as err:
            from app import db
            db.session.rollback()
            current_app.logger.error(f"Registration Exception: {err}")
            flash('Failed to create account due to a system error. Please try again.', 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/google/callback', methods=['POST'])
def google_callback():
    """
    Google OAuth 2.0 Credential Verification Endpoint.
    Verifies Google ID Token server-side and manages user status.
    """
    # Accept token either from form post or JSON body
    credential = request.form.get('credential') or (request.get_json() or {}).get('credential')
    
    if not credential:
        flash('Google authentication failed. No credential received.', 'danger')
        return redirect(url_for('auth.login'))

    try:
        # Server-side verification via Google TokenInfo API
        token_info_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
        req = urllib.request.Request(token_info_url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        google_id = data.get('sub')
        email = data.get('email')
        email_verified = data.get('email_verified', False)
        if isinstance(email_verified, str):
            email_verified = email_verified.lower() == 'true'

        full_name = data.get('name')
        picture = data.get('picture')

        # Security check: Validate Client ID / audience if configured
        configured_client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        if configured_client_id and data.get('aud') != configured_client_id:
            current_app.logger.warning(f"Google Token audience mismatch: {data.get('aud')} vs {configured_client_id}")
            flash('Invalid authentication token payload.', 'danger')
            return redirect(url_for('auth.login'))

        if not email or not email_verified:
            flash('Unverified Google email account. Login denied.', 'danger')
            return redirect(url_for('auth.login'))

        # Process user creation/linking via AuthService
        user, is_new = AuthService.process_google_user(google_id, email, full_name, picture)
        login_user(user, remember=True)

        if user.is_pending:
            flash('Your Google account has been verified. Access request submitted for admin approval.', 'info')
            return redirect(url_for('auth.pending'))
        elif user.is_rejected:
            flash('Your access request was not approved.', 'warning')
            return redirect(url_for('auth.rejected'))

        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('dashboard.index'))

    except Exception as e:
        current_app.logger.error(f"Google Token Verification Error: {e}")
        flash('Failed to verify Google login token. Please try again.', 'danger')
        return redirect(url_for('auth.login'))


@auth_bp.route('/pending')
def pending():
    """Access Pending Waiting Room Screen."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('auth/pending.html')


@auth_bp.route('/rejected')
def rejected():
    """Access Rejected Screen."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('auth/rejected.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User Logout View."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
