"""
Pytest Fixtures for CareerPilot AI
Provides test app client and database session setup.
"""

import pytest
from app import create_app, db
from config import TestingConfig
from app.models.user import User


@pytest.fixture
def app():
    """Creates a testing app context."""
    app_instance = create_app(TestingConfig)
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Creates a test HTTP client."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Seeds a sample test candidate user."""
    user = User(full_name="Test Student", email="student@example.com")
    user.set_password("StudentPassword123!")
    db.session.add(user)
    db.session.commit()
    return user
