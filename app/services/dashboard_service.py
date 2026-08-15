"""
CareerPilot AI - Dashboard Service
Aggregates personalized user stats, upcoming study items, and readiness metrics for dashboard rendering.
"""

from app.services.analytics_service import AnalyticsService


class DashboardService:
    """Service serving candidate dashboard summaries."""

    @staticmethod
    def get_dashboard_summary(user_id: int) -> dict:
        """Constructs aggregated overview data for the primary user dashboard."""
        analytics = AnalyticsService.get_user_analytics_summary(user_id)
        return {
            "analytics": analytics,
            "recent_activities": [
                {"title": "Completed Quantitative Test", "time": "2 hours ago", "status": "80%"},
                {"title": "Resume Parsed", "time": "Yesterday", "status": "ATS Score: 78"}
            ],
            "recommended_actions": [
                "Practice Binary Search coding problem",
                "Review System Architecture mock questions"
            ]
        }
