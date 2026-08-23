"""
Auth Flow & Admin Approval Unit Tests
Tests login, registration, Google user processing, status access control, and admin approval workflow.
"""

from app.models.user import User, Role
from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app import db


def test_login_page_status(client):
    """Verifies login page renders successfully with CAREER PROSPECTS title."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'CAREER PROSPECTS' in response.data
    assert b'Welcome Back' in response.data


def test_registration_flow(client):
    """Verifies new user registration endpoint."""
    response = client.post('/auth/register', data={
        'full_name': 'New Candidate',
        'email': 'new_candidate@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_google_user_creation_and_pending_status(app):
    """Verifies new Google OAuth sign-in creates a user with pending status."""
    with app.app_context():
        user, is_new = AuthService.process_google_user(
            google_id="google_123456789",
            email="google_candidate@example.com",
            full_name="Google Candidate",
            picture="https://example.com/avatar.jpg"
        )
        assert is_new is True
        assert user.status == 'pending'
        assert user.auth_provider == 'google'
        assert user.google_id == "google_123456789"
        assert user.is_pending is True
        assert user.is_approved is False


def test_google_account_linking(app):
    """Verifies existing local user logging in with Google gets linked safely."""
    with app.app_context():
        # Create existing local user
        local_user = User(
            full_name="Existing Local User",
            email="existing@example.com",
            auth_provider="local",
            status="approved"
        )
        local_user.set_password("LocalPassword123!")
        db.session.add(local_user)
        db.session.commit()

        # Google login with same verified email
        linked_user, is_new = AuthService.process_google_user(
            google_id="google_999999",
            email="existing@example.com",
            full_name="Existing Local User",
            picture=None
        )
        assert is_new is False
        assert linked_user.id == local_user.id
        assert linked_user.auth_provider == "both"
        assert linked_user.google_id == "google_999999"


def test_admin_approval_and_rejection_workflow(app):
    """Verifies admin status transitions and access control logic."""
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
            db.session.commit()

        admin_user = User(full_name="System Admin", email="admin_test@example.com", role_id=admin_role.id, status='approved')
        admin_user.set_password("AdminPass123!")
        db.session.add(admin_user)

        # Create Pending Candidate
        candidate = User(full_name="Pending Candidate", email="pending_cand@example.com", status='pending', auth_provider='google')
        db.session.add(candidate)
        db.session.commit()

        assert candidate.is_pending is True

        # Admin Approves Candidate
        updated_cand = AdminService.update_user_status(admin_user.id, candidate.id, 'approved')
        assert updated_cand.status == 'approved'
        assert updated_cand.is_approved is True

        # Admin Rejects Candidate
        rejected_cand = AdminService.update_user_status(admin_user.id, candidate.id, 'rejected')
        assert rejected_cand.status == 'rejected'
        assert rejected_cand.is_rejected is True


def test_duplicate_email_registration_prevention(client):
    """Verifies that attempting to register an existing email is prevented with a clean message."""
    client.post('/auth/register', data={
        'full_name': 'Original User',
        'email': 'duplicate@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    })

    # Second registration with same email
    response = client.post('/auth/register', data={
        'full_name': 'Duplicate User',
        'email': 'DUPLICATE@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'already registered' in response.data.lower()


def test_google_callback_route_handling(client, app, monkeypatch):
    """Verifies end-to-end /auth/google/callback POST route using mocked Google TokenInfo API."""
    import json
    from io import BytesIO

    mock_google_response = json.dumps({
        "sub": "mock_google_user_777",
        "email": "mock_google@example.com",
        "email_verified": "true",
        "name": "Mock Google User",
        "picture": "https://lh3.googleusercontent.com/a/mock_avatar",
        "aud": app.config.get("GOOGLE_CLIENT_ID", "")
    }).encode('utf-8')

    class MockResponse:
        def read(self):
            return mock_google_response
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    def mock_urlopen(req):
        return MockResponse()

    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    response = client.post('/auth/google/callback', data={
        'credential': 'mock_jwt_credential_string'
    }, follow_redirects=False)

    # New user should be redirected to pending
    assert response.status_code == 302
    assert '/auth/pending' in response.location


