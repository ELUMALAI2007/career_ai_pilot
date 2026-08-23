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
    AptitudeDailyChallenge, AptitudeDailyChallengeAttempt, AptitudeStreak,
    AptitudeGenerationLog, AptitudeCategoryPerformance, AptitudeDifficultyPerformance,
    AptitudeRecommendation, AptitudeReadinessScore, AptitudeLevelProgress
)
from app.models.coding import CodingProblem, CodingSubmission
from app.models.communication import CommunicationAssessment
from app.models.company_prep import CompanyProfile, PlacementPattern, InterviewExperience
from app.models.interview import MockInterview, InterviewQuestion, InterviewFeedback
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
    'AptitudeGenerationLog', 'AptitudeCategoryPerformance', 'AptitudeDifficultyPerformance',
    'AptitudeRecommendation', 'AptitudeReadinessScore', 'AptitudeLevelProgress',
    'CodingProblem', 'CodingSubmission',
    'CommunicationAssessment',
    'CompanyProfile', 'PlacementPattern', 'InterviewExperience',
    'MockInterview', 'InterviewQuestion', 'InterviewFeedback',
    'EligibilityCriteria', 'JobRequirement',
    'Roadmap', 'RoadmapMilestone',
    'Notification',
    'StudyPlan', 'StudyTask',
    'ResumeUpload', 'ResumeAnalysis', 'ResumeQuestion', 'ResumeInterviewSession', 'ResumeInterviewMessage',
    'UserSettings',
    'TargetRole', 'SkillAssessment', 'SkillGapReport'
]
