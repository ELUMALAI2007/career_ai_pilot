"""
CareerPilot AI - Learning Roadmap Service
Generates structured multi-week career learning paths and milestone schedules.
"""

from app.models.learning_roadmap import Roadmap, RoadmapMilestone
from app import db


class LearningRoadmapService:
    """Service handling dynamic career learning roadmaps."""

    @staticmethod
    def generate_roadmap(user_id: int, target_role: str, weeks: int = 8) -> Roadmap:
        """Generates a step-by-step milestone roadmap for a candidate."""
        roadmap = Roadmap(user_id=user_id, title=f"8-Week Prep Plan for {target_role}", target_role=target_role, total_weeks=weeks)
        db.session.add(roadmap)
        db.session.commit()

        # Generate default weekly milestones
        for w in range(1, weeks + 1):
            m = RoadmapMilestone(
                roadmap_id=roadmap.id,
                week_number=w,
                title=f"Week {w}: Core Competencies & Practice",
                description=f"Focus on foundational skills and exercises for {target_role}."
            )
            db.session.add(m)

        db.session.commit()
        return roadmap
