"""
CareerPilot AI - Profile Service
Manages candidate academic info, contact links, and experience records.
"""

from app.models.user import User
from app import db


class ProfileService:
    """Service managing candidate profile details."""

    @staticmethod
    def update_user_profile(user_id: int, profile_data: dict) -> User:
        """Updates user profile attributes."""
        user = db.session.get(User, user_id)
        if user:
            for key, val in profile_data.items():
                if hasattr(user, key):
                    setattr(user, key, val)
            db.session.commit()
        return user
