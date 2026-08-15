"""
CareerPilot AI - Planner Service
Manages study preparation schedules, daily tasks, and task completion states.
"""

from app.models.planner import StudyPlan, StudyTask
from app import db


class PlannerService:
    """Service handling candidate daily study plans."""

    @staticmethod
    def create_study_plan(user_id: int, title: str, tasks: list) -> StudyPlan:
        """Creates a study plan with initial daily tasks."""
        plan = StudyPlan(user_id=user_id, title=title)
        db.session.add(plan)
        db.session.commit()

        for task_name in tasks:
            t = StudyTask(plan_id=plan.id, task_name=task_name)
            db.session.add(t)

        db.session.commit()
        return plan
