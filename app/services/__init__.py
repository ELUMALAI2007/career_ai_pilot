"""
CareerPilot AI Services Layer Package
Decouples application routes from models and AI services.
"""

from app.services.admin_service import AdminService
from app.services.ai_assistant_service import AIAssistantService
from app.services.analytics_service import AnalyticsService
from app.services.aptitude_service import AptitudeService
from app.services.auth_service import AuthService
from app.services.coding_service import CodingService
from app.services.communication_service import CommunicationService
from app.services.company_prep_service import CompanyPrepService
from app.services.dashboard_service import DashboardService
from app.services.interview_service import InterviewService
from app.services.job_eligibility_service import JobEligibilityService
from app.services.learning_roadmap_service import LearningRoadmapService
from app.services.notification_service import NotificationService
from app.services.planner_service import PlannerService
from app.services.profile_service import ProfileService
from app.services.resume_service import ResumeService
from app.services.settings_service import SettingsService
from app.services.skill_gap_service import SkillGapService

__all__ = [
    'AdminService', 'AIAssistantService', 'AnalyticsService', 'AptitudeService',
    'AuthService', 'CodingService', 'CommunicationService', 'CompanyPrepService',
    'DashboardService', 'InterviewService', 'JobEligibilityService',
    'LearningRoadmapService', 'NotificationService', 'PlannerService',
    'ProfileService', 'ResumeService', 'SettingsService', 'SkillGapService'
]
