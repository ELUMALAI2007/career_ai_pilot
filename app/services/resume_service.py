"""
CareerPilot AI - Resume Service
Central coordinator for document parsing, evaluation, version tracking, questions generation, and privacy deletion.
"""

import os
import json
from typing import List, Optional, Dict, Any
from app import db
from app.models.resume import ResumeUpload, ResumeAnalysis, ResumeQuestion
from app.services.resume_parser import ResumeParser
from app.services.resume_evaluator import ResumeEvaluator
from app.services.resume_interview_service import ResumeInterviewService


class ResumeService:
    """Master service managing resume uploads, evaluations, and version history."""

    def process_and_evaluate_resume(
        self,
        user_id: int,
        file_path: str,
        filename: str,
        target_role: str = "Software Engineer",
        target_company: str = "General Placement",
        job_description: str = ""
    ) -> ResumeAnalysis:
        """Parses document, runs multidimensional evaluation, saves records, and generates resume questions."""
        
        # Calculate version number
        existing_count = ResumeUpload.query.filter_by(user_id=user_id).count()
        version_num = existing_count + 1
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

        # Extract text & document metadata
        clean_text, metadata = ResumeParser.extract_text(file_path)
        
        # Parse contact details & sections
        contact_info = ResumeParser.parse_contact_info(clean_text)
        sections_info = ResumeParser.parse_sections(clean_text)
        
        # Calculate Completeness Score
        completeness_score, _ = ResumeParser.calculate_completeness_score(contact_info, sections_info)

        # Run multidimensional evaluation engine
        eval_result = ResumeEvaluator.evaluate_all(
            text=clean_text,
            metadata=metadata,
            contact=contact_info,
            sections=sections_info,
            completeness_score=completeness_score,
            target_role=target_role,
            job_description=job_description,
            target_company=target_company
        )

        scores = eval_result["scores"]

        # Create Upload Record
        upload = ResumeUpload(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size_bytes=file_size,
            mime_type='application/pdf' if filename.lower().endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            target_role=target_role,
            target_company=target_company,
            job_description=job_description,
            version_number=version_num
        )
        db.session.add(upload)
        db.session.commit()

        # Create Analysis Record
        analysis = ResumeAnalysis(
            resume_id=upload.id,
            overall_score=scores["overall_score"],
            ats_score=scores["ats_score"],
            quality_score=scores["quality_score"],
            job_match_score=scores["job_match_score"],
            completeness_score=scores["completeness_score"],
            parsed_data_json=json.dumps(eval_result["parsed_data"]),
            keyword_analysis_json=json.dumps(eval_result["keyword_analysis"]),
            skills_analysis_json=json.dumps(eval_result["skills_analysis"]),
            bullets_analysis_json=json.dumps(eval_result["bullets_analysis"]),
            project_analysis_json=json.dumps(eval_result["project_analysis"]),
            red_flags_json=json.dumps(eval_result["red_flags"]),
            strengths_json=json.dumps(eval_result["strengths"]),
            priority_plan_json=json.dumps(eval_result["priority_plan"]),
            formatting_json=json.dumps(eval_result["formatting"]),
            language_json=json.dumps(eval_result["language"]),
            recruiter_impression=eval_result["recruiter_impression"],
            summary_rewrite=eval_result["summary_rewrite"]
        )
        db.session.add(analysis)
        db.session.commit()

        # Generate Resume-Based Interview Questions
        ResumeInterviewService.generate_resume_questions(
            user_id=user_id,
            resume_id=upload.id,
            parsed_data=eval_result["parsed_data"],
            target_role=target_role
        )

        return analysis

    @classmethod
    def get_user_resumes(cls, user_id: int) -> List[ResumeUpload]:
        """Returns all resume uploads for a user ordered by version."""
        return ResumeUpload.query.filter_by(user_id=user_id).order_by(ResumeUpload.version_number.desc()).all()

    @classmethod
    def get_latest_analysis(cls, user_id: int) -> Optional[ResumeAnalysis]:
        """Returns latest resume analysis for a user."""
        latest_upload = ResumeUpload.query.filter_by(user_id=user_id).order_by(ResumeUpload.uploaded_at.desc()).first()
        if latest_upload and latest_upload.analyses:
            return latest_upload.analyses[0]
        return None

    @classmethod
    def delete_resume(cls, user_id: int, resume_id: int) -> bool:
        """Securely deletes resume file from disk and database records."""
        upload = db.session.get(ResumeUpload, resume_id)
        if not upload or upload.user_id != user_id:
            return False

        # Remove physical file if it exists
        if upload.file_path and os.path.exists(upload.file_path):
            try:
                os.remove(upload.file_path)
            except Exception:
                pass

        db.session.delete(upload)
        db.session.commit()
        return True
