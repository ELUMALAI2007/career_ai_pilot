"""
CareerPilot AI - Interview Service
Orchestrates AI mock interview sessions, turn-by-turn evaluations, and final scorecard compilation.
"""

from datetime import datetime
import logging
from app import db
from app.models.interview import InterviewSession, InterviewTurn
from app.ai.ai_router import AIRouter

logger = logging.getLogger(__name__)


class InterviewService:
    """Service handling mock interview session lifecycle, state, and evaluation workflows."""

    def __init__(self):
        self.ai = AIRouter()

    def _get_resume_summary(self, resume_id: int) -> str:
        """Retrieves a summarized context of the candidate's resume from parsed database analysis."""
        from app.models.resume import ResumeUpload
        upload = db.session.get(ResumeUpload, resume_id)
        if not upload:
            return ""

        # Attempt to load from resume analyses to avoid large document payloads
        if upload.analyses:
            analysis = upload.analyses[0]
            parsed_data = analysis.get_parsed_data()
            summary = []
            if "skills" in parsed_data and parsed_data["skills"]:
                summary.append(f"Skills: {', '.join(parsed_data['skills'])}")
            if "experience" in parsed_data and parsed_data["experience"]:
                exp_list = []
                for exp in parsed_data["experience"]:
                    role = exp.get("role", "")
                    company = exp.get("company", "")
                    highlights = exp.get("highlights", [])
                    exp_list.append(f"- {role} at {company}: {'; '.join(highlights[:2])}")
                summary.append("Experience:\n" + "\n".join(exp_list))
            if "projects" in parsed_data and parsed_data["projects"]:
                proj_list = []
                for proj in parsed_data["projects"]:
                    name = proj.get("name", "")
                    tech = proj.get("technologies", [])
                    desc = proj.get("description", "")
                    proj_list.append(f"- {name} ({', '.join(tech)}): {desc[:100]}")
                summary.append("Projects:\n" + "\n".join(proj_list))

            if summary:
                return "\n\n".join(summary)

        # Fallback to raw text extraction (first 2000 chars) if analysis not present
        from app.services.resume_parser import ResumeParser
        try:
            if upload.file_path:
                clean_text, _ = ResumeParser.extract_text(upload.file_path)
                return clean_text[:2000]
        except Exception as e:
            logger.error(f"Error extracting raw text for resume {resume_id}: {e}")
        return ""

    def create_session(
        self,
        user_id: int,
        resume_id: int,
        role: str,
        company: str,
        difficulty: str,
        interview_type: str,
        total_questions: int,
        resume_based_questions: bool
    ) -> InterviewSession:
        """Validates inputs, initializes database record, generates first question, and stores first turn."""
        from app.models.resume import ResumeUpload
        upload = db.session.get(ResumeUpload, resume_id)
        if not upload or upload.user_id != user_id:
            raise ValueError("Please select or upload a valid resume before starting the interview.")

        session = InterviewSession(
            user_id=user_id,
            resume_id=resume_id,
            role=role,
            company=company,
            difficulty=difficulty,
            interview_type=interview_type,
            total_questions=total_questions,
            resume_based_questions=resume_based_questions,
            current_question_no=1,
            status='In Progress'
        )
        db.session.add(session)
        db.session.commit()

        # Build resume context if enabled
        resume_summary = ""
        if resume_based_questions:
            resume_summary = self._get_resume_summary(resume_id)

        try:
            first_q_data = self.ai.generate_first_question(
                role=role,
                company=company,
                difficulty=difficulty,
                interview_type=interview_type,
                resume_summary=resume_summary,
                ask_resume=resume_based_questions
            )
        except Exception as e:
            logger.error(f"Error generating first question: {e}")
            # Graceful fallback
            first_q_data = {
                "question": f"Welcome! Let's start by introducing yourself and discussing your background relevant to {role}.",
                "question_type": "HR"
            }

        turn = InterviewTurn(
            session_id=session.id,
            question=first_q_data["question"],
            question_type=first_q_data["question_type"],
            sequence_number=1
        )
        db.session.add(turn)
        db.session.commit()

        return session

    def submit_answer(self, session_id: int, answer: str) -> dict:
        """Saves candidate answer, runs AI turn evaluation, creates next turn, and advances count."""
        session = db.session.get(InterviewSession, session_id)
        if not session:
            raise ValueError("Interview session not found.")

        if session.status == 'Completed':
            raise ValueError("This interview session has already been completed.")

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty. Please provide a response.")

        # Find the active turn based on the session's counter (not user input ID)
        active_turn = InterviewTurn.query.filter_by(
            session_id=session.id,
            sequence_number=session.current_question_no
        ).first()

        if not active_turn:
            raise ValueError("Active turn record not found.")

        # Save candidate answer
        active_turn.candidate_answer = answer.strip()
        db.session.commit()

        # Build previous conversation history
        turns_history = []
        past_turns = InterviewTurn.query.filter(
            InterviewTurn.session_id == session.id,
            InterviewTurn.sequence_number < session.current_question_no
        ).order_by(InterviewTurn.sequence_number.asc()).all()

        for pt in past_turns:
            turns_history.append({
                "question": pt.question,
                "candidate_answer": pt.candidate_answer,
                "question_type": pt.question_type
            })

        # Get resume summary context if enabled
        resume_summary = ""
        if session.resume_based_questions:
            resume_summary = self._get_resume_summary(session.resume_id)

        session_info = {
            "role": session.role,
            "company": session.company,
            "difficulty": session.difficulty,
            "interview_type": session.interview_type,
            "total_questions": session.total_questions,
            "current_question_no": session.current_question_no,
            "resume_based_questions": session.resume_based_questions
        }

        try:
            eval_data = self.ai.evaluate_turn_and_generate_next(
                session_info=session_info,
                turns_history=turns_history,
                current_question=active_turn.question,
                current_question_type=active_turn.question_type or "Technical",
                candidate_answer=active_turn.candidate_answer,
                resume_summary=resume_summary
            )
        except Exception as e:
            logger.error(f"Error evaluating turn response: {e}")
            # Graceful fallback response
            eval_data = {
                "evaluation": {
                    "what_went_well": "Response received.",
                    "areas_for_improvement": "Feedback unavailable due to service error."
                },
                "scores": {},
                "follow_up_required": False,
                "next_question": "Interview complete" if session.current_question_no >= session.total_questions else "Tell me about another challenging project you completed.",
                "next_question_type": "HR"
            }

        # Save turn scores and evaluation metrics
        active_turn.set_evaluation(eval_data.get("evaluation", {}))
        active_turn.set_scores(eval_data.get("scores", {}))
        db.session.commit()

        # Check if limits reached
        if session.current_question_no >= session.total_questions:
            self.finalize_session(session.id)
            return {
                "success": True,
                "is_finished": True,
                "next_question": "Interview complete"
            }
        else:
            session.current_question_no += 1
            next_turn = InterviewTurn(
                session_id=session.id,
                question=eval_data.get("next_question", "Could you elaborate on another project?"),
                question_type=eval_data.get("next_question_type", "Follow-up"),
                sequence_number=session.current_question_no
            )
            db.session.add(next_turn)
            db.session.commit()

            return {
                "success": True,
                "is_finished": False,
                "next_question": next_turn.question
            }

    def finalize_session(self, session_id: int):
        """Compiles final report scorecard and updates session status to Completed."""
        session = db.session.get(InterviewSession, session_id)
        if not session or session.status == 'Completed':
            return

        turns = InterviewTurn.query.filter_by(session_id=session.id).order_by(InterviewTurn.sequence_number.asc()).all()
        turns_data = []
        for t in turns:
            turns_data.append({
                "question": t.question,
                "candidate_answer": t.candidate_answer or "",
                "scores": t.get_scores(),
                "evaluation": t.get_evaluation()
            })

        session_info = {
            "role": session.role,
            "company": session.company,
            "difficulty": session.difficulty,
            "interview_type": session.interview_type
        }

        try:
            report_data = self.ai.generate_final_report(session_info, turns_data)
        except Exception as e:
            logger.error(f"Error generating final report: {e}")
            # Build aggregate fallback
            report_data = {
                "overall_score": 60,
                "dimension_scores": {},
                "strengths": ["Completed all mock interview questions."],
                "areas_for_improvement": ["Review individual questions for detailed feedback."],
                "recommended_improvements": ["Check study planner daily tasks for interview practice."]
            }

        session.overall_score = float(report_data.get("overall_score", 50.0))
        session.set_final_feedback(report_data)
        session.status = 'Completed'
        session.completed_at = datetime.utcnow()
        db.session.commit()
