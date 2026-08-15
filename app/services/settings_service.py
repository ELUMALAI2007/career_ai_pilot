"""
CareerPilot AI - Settings Service
Manages user preferences, security settings, and UI themes.
"""

from app.models.settings import UserSettings
from app import db


class SettingsService:
    """Service handling user platform settings."""

    @staticmethod
    def get_or_create_settings(user_id: int) -> UserSettings:
        """Retrieves user settings record, instantiating defaults if missing."""
        settings = UserSettings.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserSettings(user_id=user_id)
            db.session.add(settings)
            db.session.commit()
        return settings
