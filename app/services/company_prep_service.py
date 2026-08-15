"""
CareerPilot AI - Company Prep Service
Manages target company insights, placement test patterns, and candidate experiences.
"""

from app.models.company_prep import CompanyProfile, PlacementPattern, InterviewExperience
from app import db


class CompanyPrepService:
    """Service handling company preparation intelligence."""

    @staticmethod
    def get_company_details(company_id: int) -> dict:
        """Fetches detailed profile and interview breakdown for a target company."""
        company = db.session.get(CompanyProfile, company_id)
        if not company:
            return None
        return {
            "company": company,
            "patterns": company.patterns.all(),
            "experiences": company.experiences.all()
        }
