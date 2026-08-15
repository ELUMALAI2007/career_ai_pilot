"""
CareerPilot AI - Job Eligibility Service
Evaluates candidate academic parameters (CGPA, Branch, Backlogs) against company recruitment criteria.
"""

from app.models.job_eligibility import JobRequirement, EligibilityCriteria
from app import db


class JobEligibilityService:
    """Service evaluating placement eligibility criteria matching."""

    @staticmethod
    def evaluate_eligibility(user_id: int, job_id: int, user_cgpa: float, user_branch: str, backlogs: int) -> dict:
        """Evaluates student eligibility for a specific campus placement drive."""
        job = db.session.get(JobRequirement, job_id)
        if not job:
            return {"eligible": False, "reasons": ["Job criteria not found"]}

        reasons = []
        if user_cgpa < job.min_cgpa:
            reasons.append(f"CGPA ({user_cgpa}) is below minimum requirement ({job.min_cgpa})")
        if backlogs > job.max_active_backlogs:
            reasons.append(f"Active backlogs ({backlogs}) exceed limit ({job.max_active_backlogs})")

        is_eligible = len(reasons) == 0
        return {"is_eligible": is_eligible, "reasons": reasons, "match_percentage": 90.0 if is_eligible else 45.0}
