"""
CareerPilot AI Database Models Package
Exposes SQLAlchemy database entities for all 18 platform modules.
"""

from app.models.user import User, Role
from app.models.admin import AdminLog, SystemNotice
from app.models.ai_assistant import ChatSession, ChatMessage
from app.models.analytics import UserAnalytics, MetricSnapshot
from app.models.aptitude import (
    AptitudeCategory, AptitudeQuestion, AptitudeAttempt,
    AptitudeQuestionAnswer, AptitudeBookmark, AptitudeProgress,
    AptitudeTopicMastery, AptitudeTestSession, AptitudeTestResult,
    AptitudeDailyChallenge, AptitudeDailyChallengeAttempt, AptitudeStreak
)
from app.models.coding import (
    CodingProblem, CodingSubmission, CodingBookmark,
    CodingProgress, DailyChallenge, CodingBadge, UserBadge
)
from app.models.communication import CommunicationAssessment
from app.models.company_prep import CompanyProfile, PlacementPattern, InterviewExperience
from app.models.interview import InterviewSession, InterviewTurn
from app.models.job_eligibility import EligibilityCriteria, JobRequirement
from app.models.learning_roadmap import Roadmap, RoadmapMilestone
from app.models.notification import Notification
from app.models.planner import StudyPlan, StudyTask
from app.models.resume import ResumeUpload, ResumeAnalysis, ResumeQuestion, ResumeInterviewSession, ResumeInterviewMessage
from app.models.settings import UserSettings
from app.models.skill_gap import TargetRole, SkillAssessment, SkillGapReport

__all__ = [
    'User', 'Role',
    'AdminLog', 'SystemNotice',
    'ChatSession', 'ChatMessage',
    'UserAnalytics', 'MetricSnapshot',
    'AptitudeCategory', 'AptitudeQuestion', 'AptitudeAttempt',
    'AptitudeQuestionAnswer', 'AptitudeBookmark', 'AptitudeProgress',
    'AptitudeTopicMastery', 'AptitudeTestSession', 'AptitudeTestResult',
    'AptitudeDailyChallenge', 'AptitudeDailyChallengeAttempt', 'AptitudeStreak',
    'CodingProblem', 'CodingSubmission', 'CodingBookmark',
    'CodingProgress', 'DailyChallenge', 'CodingBadge', 'UserBadge',
    'CommunicationAssessment',
    'CompanyProfile', 'PlacementPattern', 'InterviewExperience',
    'InterviewSession', 'InterviewTurn',
    'EligibilityCriteria', 'JobRequirement',
    'Roadmap', 'RoadmapMilestone',
    'Notification',
    'StudyPlan', 'StudyTask',
    'ResumeUpload', 'ResumeAnalysis', 'ResumeQuestion', 'ResumeInterviewSession', 'ResumeInterviewMessage',
    'UserSettings',
    'TargetRole', 'SkillAssessment', 'SkillGapReport'
]
