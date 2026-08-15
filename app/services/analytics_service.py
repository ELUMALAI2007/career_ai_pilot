"""
CareerPilot AI - Analytics Service
Aggregates user score metrics across aptitude, coding, and mock interviews for Chart.js rendering.
"""

from app.models.analytics import UserAnalytics, MetricSnapshot
from app import db


class AnalyticsService:
    """Service handling performance analytics and metric snapshots."""

    @staticmethod
    def get_user_analytics_summary(user_id: int) -> dict:
        """Retrieves user performance radar chart data and readiness score."""
        # TODO: Compute real metric averages from test attempts
        return {
            "aptitude_score": 82.5,
            "coding_score": 78.0,
            "communication_score": 85.0,
            "interview_score": 80.0,
            "overall_readiness": 81.4
        }
