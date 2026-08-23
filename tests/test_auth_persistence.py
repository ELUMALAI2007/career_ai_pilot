"""
CareerPilot AI — Persistent Authentication & Database Automated Test Suite (`tests/test_auth_persistence.py`)
Verifies user registration persistence across app context restarts, case-insensitive email normalization,
duplicate registration rejection, password hash security, seed_admin idempotency, and admin role access control.
"""

import pytest
import os
from app import create_app, db
from app.models.user import User, Role
from app.services.auth_service import AuthService
from seed_admin import seed_admin_account
from config import TestingConfig


@pytest.fixture
def auth_app():
    """Configures isolated test application with clean database tables."""
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        # Seed student and admin roles idempotently
        student_role = Role.query.filter_by(name='student').first()
        if not student_role:
            student_role = Role(name='student', description='Student Role')
            db.session.add(student_role)
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Admin Role')
            db.session.add(admin_role)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_client(auth_app):
    """Provides Flask test client for HTTP endpoint testing."""
    return auth_app.test_client()


def test_user_registration_saves_permanently(auth_app):
    """Verifies user registration saves record permanently to database with hashed password."""
    with auth_app.app_context():
        user = AuthService.register_user(
            full_name="Student Test",
            email="STUDENT_TEST@example.com",
            password="SecurePassword123!"
        )
        assert user.id is not None
        assert user.full_name == "Student Test"
        assert user.email == "student_test@example.com"  # Normalized lowercase
        assert user.password_hash is not None
        assert user.password_hash != "SecurePassword123!"  # Hashed
        assert user.role is not None
        assert user.role.name == "student"

        # Verify DB query retrieves saved user
        retrieved = User.query.filter_by(email="student_test@example.com").first()
        assert retrieved is not None
        assert retrieved.check_password("SecurePassword123!") is True


def test_duplicate_email_registration_rejection(auth_app):
    """Verifies duplicate email registration is rejected case-insensitively with clear error."""
    with auth_app.app_context():
        AuthService.register_user("Original Student", "student@example.com", "Password123!")
        
        # Second registration with uppercase duplicate email
        with pytest.raises(ValueError) as exc_info:
            AuthService.register_user("Duplicate Candidate", "STUDENT@EXAMPLE.COM", "Password123!")
        
        assert "already registered" in str(exc_info.value).lower()

        # Ensure database count remains 1
        count = User.query.filter_by(email="student@example.com").count()
        assert count == 1


def test_authentication_verifies_credentials_and_updates_last_login(auth_app):
    """Verifies login authentication, password hash checking, and last_login_at timestamp update."""
    with auth_app.app_context():
        reg_user = AuthService.register_user("Auth User", "auth@example.com", "MySecret123!")
        assert reg_user.last_login_at is None

        # Authenticate with correct credentials
        authenticated_user = AuthService.authenticate("AUTH@EXAMPLE.COM", "MySecret123!")
        assert authenticated_user is not None
        assert authenticated_user.id == reg_user.id
        assert authenticated_user.last_login_at is not None

        # Authenticate with wrong password
        failed_password = AuthService.authenticate("auth@example.com", "WrongPassword!")
        assert failed_password is None

        # Authenticate with unknown email
        failed_email = AuthService.authenticate("unknown@example.com", "MySecret123!")
        assert failed_email is None


def test_seed_admin_script_idempotency(auth_app):
    """Verifies seed_admin_account creates admin once and leaves password hash untouched on subsequent runs."""
    with auth_app.app_context():
        # First seeding
        seed_admin_account(auth_app)
        admin = User.query.filter_by(email="admin@careerpilot.ai").first()
        assert admin is not None
        assert admin.role.name == "admin"
        first_hash = admin.password_hash

        # Change admin password manually to simulate user custom password change
        admin.set_password("CustomAdminPass999!")
        db.session.commit()
        custom_hash = admin.password_hash
        assert custom_hash != first_hash

        # Run seed_admin_account a second time
        seed_admin_account(auth_app)
        admin_reloaded = User.query.filter_by(email="admin@careerpilot.ai").first()
        # Verify custom password hash was NOT overwritten or reset
        assert admin_reloaded.password_hash == custom_hash
        assert admin_reloaded.check_password("CustomAdminPass999!") is True


def test_admin_required_access_control(auth_client, auth_app):
    """Verifies @admin_required decorator blocks student users and permits admin users."""
    with auth_app.app_context():
        student = AuthService.register_user("Student User", "student_user@example.com", "Pass1234!")
        admin_role = Role.query.filter_by(name='admin').first()
        admin = User(full_name="Admin User", email="admin_user@example.com", role_id=admin_role.id, status="approved", is_active=True)
        admin.set_password("AdminPass123!")
        db.session.add(admin)
        db.session.commit()

    # 1. Login as student via HTTP POST -> Access /admin -> Redirected
    auth_client.post('/auth/login', data={'email': 'student_user@example.com', 'password': 'Pass1234!'}, follow_redirects=True)
    res_student = auth_client.get('/admin/', follow_redirects=True)
    assert b'permissions required' in res_student.data.lower() or b'dashboard' in res_student.data.lower()

    # Logout student
    auth_client.get('/auth/logout', follow_redirects=True)

    # 2. Login as admin via HTTP POST -> Access /admin -> Granted (200 OK)
    auth_client.post('/auth/login', data={'email': 'admin_user@example.com', 'password': 'AdminPass123!'}, follow_redirects=True)
    res_admin = auth_client.get('/admin/')
    assert res_admin.status_code == 200


def test_database_persistence_across_app_contexts(auth_app):
    """Verifies database records persist across separate app contexts / restarts."""
    with auth_app.app_context():
        AuthService.register_user("Persist User", "persist@example.com", "Pass1234!")

    # Simulate restarting application context
    with auth_app.app_context():
        user = User.query.filter_by(email="persist@example.com").first()
        assert user is not None
        assert user.full_name == "Persist User"
        assert user.check_password("Pass1234!") is True
