"""Business logic for database-backed, low-call mock interviews."""

from datetime import datetime
import logging
import random
import threading

from app import db
from app.ai.ai_router import AIRouter
from app.models.interview import InterviewQuestion, InterviewSession, InterviewTurn

logger = logging.getLogger(__name__)


class InterviewService:
    """Manage queued interview turns and bounded AI workflows."""

    MAX_FOLLOW_UPS = 3
    DIFFICULTY_QUESTION_COUNTS = {
        "easy": 5,
        "medium": 10,
        "hard": 15,
    }

    def __init__(self):
        self.ai = AIRouter()

    @staticmethod
    def _normalize_difficulty(value):
        if not value:
            return "Medium"
        return " ".join(part.capitalize() for part in str(value).strip().split())

    @classmethod
    def resolve_question_count(cls, difficulty, total_questions=None):
        """Return a total based on difficulty unless an explicit manual count is supplied."""
        if total_questions not in (None, "", 0):
            try:
                value = int(total_questions)
                if value > 0:
                    return value
            except (TypeError, ValueError):
                pass
        normalized = (difficulty or "Medium").strip().lower()
        return cls.DIFFICULTY_QUESTION_COUNTS.get(normalized, 7)

    @classmethod
    def _difficulty_fallback_order(cls, difficulty):
        """Return strict difficulty order (no fallback) to maintain consistent question difficulty."""
        normalized = cls._normalize_difficulty(difficulty)
        return [normalized]

    def _get_coding_challenge(self, difficulty, company, role):
        from app.models.coding import CodingProblem
        difficulty_key = (difficulty or "Medium").lower()
        candidates = CodingProblem.query.filter(CodingProblem.difficulty == difficulty_key).order_by(CodingProblem.id.asc()).all()

        if company and company.lower() != "other":
            company_matches = [c for c in candidates if company.lower() in (c.company_tags or "").lower()]
            if company_matches:
                candidates = company_matches

        if role and not candidates:
            role_keywords = role.lower()
            candidates = CodingProblem.query.filter(
                (CodingProblem.topic.ilike(f"%{role_keywords}%")) |
                (CodingProblem.company_tags.ilike(f"%{role_keywords}%"))
            ).order_by(CodingProblem.id.asc()).all()

        challenge = candidates[0] if candidates else None
        if not challenge:
            challenge = CodingProblem.query.order_by(CodingProblem.id.asc()).first()
        if not challenge:
            return None

        return {
            "question": f"Coding Challenge: {challenge.title} - {challenge.description[:180]}{'...' if len(challenge.description) > 180 else ''}",
            "question_type": "Coding Challenge",
            "topic": challenge.topic,
            "challenge_title": challenge.title,
            "challenge_slug": challenge.slug,
            "challenge_id": challenge.id,
        }

    def _insert_coding_challenge(self, queue, challenge, total_questions):
        if not challenge:
            return queue[:total_questions]
        if not queue:
            return [challenge][:total_questions]

        insertion_index = next(
            (idx for idx, item in enumerate(queue)
             if item.get("question_type") not in {"Introduction", "Resume", "Project"}),
            len(queue)
        )
        queue.insert(insertion_index, challenge)
        return queue[:total_questions]

    def _get_resume_summary(self, resume_id):
        from app.models.resume import ResumeUpload
        upload = db.session.get(ResumeUpload, resume_id)
        if not upload:
            return ""
        if upload.analyses:
            parsed = upload.analyses[0].get_parsed_data()
            summary = []
            if parsed.get("skills"):
                summary.append(f"Skills: {', '.join(parsed['skills'])}")
            if parsed.get("experience"):
                summary.append("Experience:\n" + "\n".join(
                    f"- {item.get('role', '')} at {item.get('company', '')}: {'; '.join(item.get('highlights', [])[:2])}"
                    for item in parsed["experience"]
                ))
            if parsed.get("projects"):
                summary.append("Projects:\n" + "\n".join(
                    f"- {item.get('name', '')} ({', '.join(item.get('technologies', []))}): {item.get('description', '')[:100]}"
                    for item in parsed["projects"]
                ))
            if summary:
                return "\n\n".join(summary)
        return ""

    @staticmethod
    def _get_question_order():
        """Return the formal interview progression order."""
        return ["Introduction", "Resume", "Project", "Technical", "Behavioral", "HR"]

    @staticmethod
    def _question_types(interview_type):
        if interview_type == "Technical":
            return ["Technical"]
        if interview_type == "HR / Behavioral":
            return ["Behavioral", "HR"]
        return ["Technical", "Behavioral", "HR"]

    def _bank_questions(self, role, interview_type, difficulty, count, resume_based=False):
        """Build question queue following formal interview progression with strict difficulty matching."""
        queue = []
        question_order = self._get_question_order()
        remaining_count = count
        difficulty_order = self._difficulty_fallback_order(difficulty)

        for q_type in question_order:
            if remaining_count <= 0:
                break
            for difficulty_level in difficulty_order:
                if remaining_count <= 0:
                    break
                if q_type == "Introduction":
                    intro_q = InterviewQuestion.query.filter(
                        InterviewQuestion.is_active.is_(True),
                        InterviewQuestion.interview_type == "Introduction",
                        InterviewQuestion.difficulty == difficulty_level
                    ).first()
                    if intro_q:
                        queue.append({"question": intro_q.question, "question_type": "Introduction", "topic": intro_q.topic})
                        remaining_count -= 1
                        break
                elif q_type == "Resume":
                    if resume_based:
                        resume_q = InterviewQuestion.query.filter(
                            InterviewQuestion.is_active.is_(True),
                            InterviewQuestion.interview_type == "Resume",
                            InterviewQuestion.difficulty == difficulty_level,
                            InterviewQuestion.role == role
                        ).first()
                        if not resume_q:
                            resume_q = InterviewQuestion.query.filter(
                                InterviewQuestion.is_active.is_(True),
                                InterviewQuestion.interview_type == "Resume",
                                InterviewQuestion.difficulty == difficulty_level
                            ).first()
                        if resume_q:
                            queue.append({"question": resume_q.question, "question_type": "Resume", "topic": resume_q.topic})
                            remaining_count -= 1
                            break
                elif q_type == "Project":
                    proj_q = InterviewQuestion.query.filter(
                        InterviewQuestion.is_active.is_(True),
                        InterviewQuestion.interview_type == "Project",
                        InterviewQuestion.difficulty == difficulty_level,
                        InterviewQuestion.role == role
                    ).first()
                    if not proj_q:
                        proj_q = InterviewQuestion.query.filter(
                            InterviewQuestion.is_active.is_(True),
                            InterviewQuestion.interview_type == "Project",
                            InterviewQuestion.difficulty == difficulty_level
                        ).first()
                    if proj_q:
                        queue.append({"question": proj_q.question, "question_type": "Project", "topic": proj_q.topic})
                        remaining_count -= 1
                        break
                else:
                    types_for_category = [q_type] if q_type in ["Technical"] else self._question_types(interview_type)
                    if q_type in types_for_category:
                        questions = InterviewQuestion.query.filter(
                            InterviewQuestion.is_active.is_(True),
                            InterviewQuestion.role == role,
                            InterviewQuestion.difficulty == difficulty_level,
                            InterviewQuestion.interview_type == q_type
                        ).all()
                        if not questions:
                            questions = InterviewQuestion.query.filter(
                                InterviewQuestion.is_active.is_(True),
                                InterviewQuestion.difficulty == difficulty_level,
                                InterviewQuestion.interview_type == q_type
                            ).all()
                        if questions:
                            random.shuffle(questions)
                            for q in questions:
                                if remaining_count <= 0:
                                    break
                                queue.append({"question": q.question, "question_type": q.interview_type, "topic": q.topic})
                                remaining_count -= 1
                            break

        return queue

    def create_session(self, user_id, resume_id, role, company, difficulty, interview_type, total_questions, resume_based_questions):
        from app.models.resume import ResumeUpload
        upload = db.session.get(ResumeUpload, resume_id)
        if not upload or upload.user_id != user_id:
            raise ValueError("Please select or upload a valid resume before starting the interview.")

        total_questions = self.resolve_question_count(difficulty, total_questions)
        challenge = self._get_coding_challenge(difficulty, company, role)
        should_include_challenge = bool(challenge) and total_questions >= 5

        queue = []
        bank_target = total_questions - 1 if should_include_challenge else total_questions
        if bank_target > 0:
            queue = self._bank_questions(role, interview_type, difficulty, bank_target, resume_based_questions)

        if resume_based_questions:
            try:
                generated = self.ai.generate_resume_questions(
                    role, company, interview_type, difficulty, self._get_resume_summary(resume_id)
                )
                resume_questions = [item for item in generated if isinstance(item, dict) and item.get("question")]
                if resume_questions:
                    insert_at = 1 if queue and queue[0].get("question_type") == "Introduction" else 0
                    for index, item in enumerate(resume_questions):
                        item.setdefault("question_type", "Resume")
                        item.setdefault("topic", "Resume")
                        queue.insert(min(insert_at + index, len(queue)), item)
                queue = queue[:bank_target]
            except Exception as exc:
                logger.warning("Resume question generation failed: %s", exc)

        if len(queue) < bank_target:
            extra_questions = self._bank_questions(
                role,
                interview_type,
                difficulty,
                bank_target - len(queue),
                False
            )
            seen = {item.get("question") for item in queue}
            for item in extra_questions:
                if item.get("question") in seen:
                    continue
                queue.append(item)
                seen.add(item.get("question"))
                if len(queue) >= bank_target:
                    break

        if should_include_challenge and challenge:
            queue = self._insert_coding_challenge(queue, challenge, total_questions)

        if len(queue) < total_questions:
            fallback_questions = [
                {"question": "Tell me about a project where you solved a meaningful problem.", "question_type": "Project", "topic": "Projects"},
                {"question": "How do you prioritize work when requirements are changing?", "question_type": "Behavioral", "topic": "Prioritization"},
                {"question": "Why are you interested in this role and company?", "question_type": "HR", "topic": "Motivation"},
                {"question": "Discuss a technical tradeoff you had to make in a real system.", "question_type": "Technical", "topic": "System Design"},
                {"question": "What would you do if the deadline changed mid-sprint?", "question_type": "Behavioral", "topic": "Execution"},
            ]
            seen = {item.get("question") for item in queue}
            for item in fallback_questions:
                if len(queue) >= total_questions:
                    break
                if item.get("question") in seen:
                    continue
                queue.append(item)
                seen.add(item.get("question"))
            if len(queue) < total_questions:
                logger.warning(
                    "Interview session: requested %d questions but bank had only %d at difficulty %s.",
                    total_questions, len(queue), difficulty
                )

        queue = queue[:total_questions]
        while len(queue) < total_questions:
            queue.append({
                "question": "Tell me about a project or decision that best shows your problem-solving ability.",
                "question_type": "Technical",
                "topic": "General"
            })

        if not queue:
            raise ValueError("No interview questions are available for this setup.")

        first = queue[0]
        remaining_queue = queue[1:]
        session = InterviewSession(
            user_id=user_id, resume_id=resume_id, role=role, company=company,
            difficulty=difficulty, interview_type=interview_type,
            total_questions=total_questions, current_question_no=1,
            resume_based_questions=resume_based_questions, status="In Progress",
            follow_up_count=0, question_queue=remaining_queue
        )
        db.session.add(session)
        db.session.flush()
        db.session.add(InterviewTurn(
            session_id=session.id, question=first["question"],
            question_type=first.get("question_type", "Technical"), sequence_number=1
        ))
        db.session.commit()
        return session

    @staticmethod
    def _session_context(session):
        return {"role": session.role, "company": session.company, "difficulty": session.difficulty,
                "interview_type": session.interview_type, "total_questions": session.total_questions,
                "current_question_no": session.current_question_no}

    @staticmethod
    def _needs_follow_up(turn, answer):
        if len(answer.split()) < 30:
            return True
        if turn.question_type in ("Technical", "Resume"):
            terms = ("api", "database", "python", "java", "react", "sql", "testing", "cache", "algorithm", "system")
            return not any(term in answer.lower() for term in terms)
        return False

    def _history(self, session):
        return [{"question": turn.question, "candidate_answer": turn.candidate_answer or "",
                 "question_type": turn.question_type, "scores": turn.get_scores(),
                 "evaluation": turn.get_evaluation()}
                for turn in InterviewTurn.query.filter_by(session_id=session.id)
                .order_by(InterviewTurn.sequence_number.asc()).all()]

    def submit_answer(self, session_id, answer):
        session = db.session.get(InterviewSession, session_id)
        if not session:
            raise ValueError("Interview session not found.")
        if session.status == "Completed":
            raise ValueError("This interview session has already been completed.")
        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty. Please provide a response.")
        active_turn = InterviewTurn.query.filter_by(
            session_id=session.id, sequence_number=session.current_question_no
        ).first()
        if not active_turn or active_turn.candidate_answer is not None:
            raise ValueError("Active turn record not found.")
        active_turn.candidate_answer = answer.strip()
        if session.current_question_no >= session.total_questions:
            db.session.commit()
            self.finalize_session(session.id)
            return {"success": True, "is_finished": True, "next_question": "Interview complete"}

        next_item = None
        if self._needs_follow_up(active_turn, active_turn.candidate_answer) and session.follow_up_count < self.MAX_FOLLOW_UPS:
            try:
                next_item = self.ai.generate_follow_up(
                    self._session_context(session), active_turn.question,
                    active_turn.candidate_answer, self._history(session)
                )
                session.follow_up_count += 1
                next_item.setdefault("question_type", "Follow-up")
            except Exception as exc:
                logger.warning("Follow-up generation failed: %s", exc)
        if not next_item:
            queue = session.get_question_queue()
            if not queue:
                db.session.commit()
                self.finalize_session(session.id)
                return {"success": True, "is_finished": True, "next_question": "Interview complete"}
            next_item = queue.pop(0)
            session.set_question_queue(queue)
        session.current_question_no += 1
        db.session.add(InterviewTurn(
            session_id=session.id, question=next_item["question"],
            question_type=next_item.get("question_type", "Technical"), sequence_number=session.current_question_no
        ))
        db.session.commit()
        return {"success": True, "is_finished": False, "next_question": next_item["question"],
                "next_question_type": next_item.get("question_type", "Technical"),
                "follow_up_count": session.follow_up_count}

    def finalize_session(self, session_id, force=False):
        session = db.session.get(InterviewSession, session_id)
        if not session:
            raise ValueError("Interview session not found.")
        if session.status == "Completed" and not force:
            return
        try:
            report_data = self.ai.generate_final_report(self._session_context(session), self._history(session))
        except Exception as exc:
            logger.warning("Final report generation failed: %s", exc)
            report_data = {"overall_score": 50, "dimension_scores": {}, "strengths": [],
                           "areas_for_improvement": ["Practice giving specific, structured answers."],
                           "recommended_improvements": ["Use the STAR method and include measurable results."]}
        session.overall_score = float(report_data.get("overall_score", 50))
        session.set_final_feedback(report_data)
        session.status = "Completed"
        session.completed_at = datetime.utcnow()
        db.session.commit()

    def finalize_session_async(self, session_id, flask_app):
        """Close an interrupted interview immediately and complete AI scoring off-request."""
        session = db.session.get(InterviewSession, session_id)
        if not session:
            raise ValueError("Interview session not found.")
        if session.status == "Completed":
            return

        provisional = {
            "overall_score": 0,
            "dimension_scores": {},
            "strengths": [],
            "areas_for_improvement": ["Final AI feedback is still being generated."],
            "recommended_improvements": [],
            "per_question_feedback": [],
            "report_pending": True
        }
        session.overall_score = 0
        session.set_final_feedback(provisional)
        session.status = "Completed"
        session.completed_at = datetime.utcnow()
        db.session.commit()

        def generate_report():
            with flask_app.app_context():
                try:
                    self.finalize_session(session_id, force=True)
                except Exception as exc:
                    logger.warning("Background final report generation failed: %s", exc)

        threading.Thread(target=generate_report, daemon=True).start()