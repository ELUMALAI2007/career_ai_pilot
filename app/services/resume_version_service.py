"""
CareerPilot AI - Resume Version Service
Handles version tracking across uploaded resumes and generates side-by-side version comparison matrices.
"""

from typing import Dict, Any, List
from app.models.resume import ResumeUpload, ResumeAnalysis


class ResumeVersionService:
    """Service for resume versioning and delta comparisons."""

    @classmethod
    def compare_versions(cls, v1_analysis: ResumeAnalysis, v2_analysis: ResumeAnalysis) -> Dict[str, Any]:
        """
        Generates detailed side-by-side comparison between two resume versions.
        v1 = Baseline (older), v2 = Updated (newer).
        """
        v1_parsed = v1_analysis.get_parsed_data()
        v2_parsed = v2_analysis.get_parsed_data()

        v1_skills = set(v1_parsed.get("extracted_skills", []))
        v2_skills = set(v2_parsed.get("extracted_skills", []))

        added_skills = list(v2_skills - v1_skills)
        removed_skills = list(v1_skills - v2_skills)

        v1_kw = v1_analysis.get_keyword_analysis()
        v2_kw = v2_analysis.get_keyword_analysis()

        return {
            "version_1": {
                "id": v1_analysis.resume.id,
                "version_number": v1_analysis.resume.version_number,
                "filename": v1_analysis.resume.filename,
                "uploaded_at": v1_analysis.evaluated_at.strftime("%Y-%m-%d %H:%M"),
                "scores": {
                    "overall": v1_analysis.overall_score,
                    "ats": v1_analysis.ats_score,
                    "quality": v1_analysis.quality_score,
                    "job_match": v1_analysis.job_match_score,
                    "completeness": v1_analysis.completeness_score
                }
            },
            "version_2": {
                "id": v2_analysis.resume.id,
                "version_number": v2_analysis.resume.version_number,
                "filename": v2_analysis.resume.filename,
                "uploaded_at": v2_analysis.evaluated_at.strftime("%Y-%m-%d %H:%M"),
                "scores": {
                    "overall": v2_analysis.overall_score,
                    "ats": v2_analysis.ats_score,
                    "quality": v2_analysis.quality_score,
                    "job_match": v2_analysis.job_match_score,
                    "completeness": v2_analysis.completeness_score
                }
            },
            "deltas": {
                "overall_delta": round(v2_analysis.overall_score - v1_analysis.overall_score, 1),
                "ats_delta": round(v2_analysis.ats_score - v1_analysis.ats_score, 1),
                "quality_delta": round(v2_analysis.quality_score - v1_analysis.quality_score, 1),
                "job_match_delta": round(v2_analysis.job_match_score - v1_analysis.job_match_score, 1),
                "added_skills": sorted(added_skills),
                "removed_skills": sorted(removed_skills),
                "keyword_match_delta": round(v2_kw.get("keyword_match_pct", 0) - v1_kw.get("keyword_match_pct", 0), 1)
            }
        }
