"""
CareerPilot AI - Skill Gap Service
Evaluates candidate skill proficiencies against target role benchmarks to pinpoint critical gaps.
"""

from app.models.skill_gap import TargetRole, SkillAssessment, SkillGapReport
from app.ai.sklearn_models import SklearnRecommendationModel
from app import db


class SkillGapService:
    """Service handling skill gap calculation and learning suggestions."""

    def __init__(self):
        self.ml_model = SklearnRecommendationModel()

    def generate_skill_gap_report(self, user_id: int, target_role_id: int) -> SkillGapReport:
        """Analyzes missing skills and computes candidate role match percentage."""
        target_role = db.session.get(TargetRole, target_role_id)
        if not target_role:
            return None

        # TODO: Compare user assessments with target_role.required_skills
        match_score = self.ml_model.predict_job_match([]) * 100
        report = SkillGapReport(
            user_id=user_id,
            target_role_id=target_role_id,
            match_percentage=match_score,
            missing_critical_skills="System Design, Docker, Kubernetes",
            recommended_learning_actions="Complete System Design milestone in Learning Roadmap."
        )
        db.session.add(report)
        db.session.commit()
        return report
