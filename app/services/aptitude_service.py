"""
CareerPilot AI - Adaptive Aptitude Service
Core business logic for Aptitude Learning, Timed Mock Engine, Level Adaptivity, Daily Challenges, Bookmarks, and Analytics.
"""

import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import func

from app import db
from app.models.aptitude import (
    AptitudeCategory, AptitudeQuestion, AptitudeAttempt,
    AptitudeQuestionAnswer, AptitudeBookmark, AptitudeProgress,
    AptitudeTopicMastery, AptitudeTestSession, AptitudeTestResult,
    AptitudeDailyChallenge, AptitudeDailyChallengeAttempt, AptitudeStreak
)


class AptitudeService:
    """Service handling placement aptitude learning, assessment, adaptivity, and analytics."""

    LEVELS = ["foundation", "beginner", "intermediate", "advanced", "expert", "master"]

    @staticmethod
    def get_categories() -> List[AptitudeCategory]:
        """Retrieves available test categories."""
        return AptitudeCategory.query.all()

    @classmethod
    def get_or_create_user_progress(cls, user_id: int) -> AptitudeProgress:
        """Retrieves or initializes user aptitude progress record."""
        progress = AptitudeProgress.query.filter_by(user_id=user_id).first()
        if not progress:
            progress = AptitudeProgress(
                user_id=user_id,
                current_level='foundation',
                total_questions_solved=0,
                correct_count=0,
                overall_accuracy=0.0,
                avg_time_seconds=45.0,
                readiness_score=0
            )
            db.session.add(progress)
            db.session.commit()
        return progress

    @classmethod
    def get_or_create_user_streak(cls, user_id: int) -> AptitudeStreak:
        """Retrieves or initializes user streak record."""
        streak = AptitudeStreak.query.filter_by(user_id=user_id).first()
        if not streak:
            streak = AptitudeStreak(
                user_id=user_id,
                current_streak=0,
                longest_streak=0,
                questions_today=0,
                last_activity_date=None
            )
            db.session.add(streak)
            db.session.commit()
        return streak

    @classmethod
    def update_user_streak(cls, user_id: int, questions_count: int = 1):
        """Updates user daily practice streak without faking activity."""
        streak = cls.get_or_create_user_streak(user_id)
        today = date.today()

        if streak.last_activity_date == today:
            streak.questions_today += questions_count
        elif streak.last_activity_date == today - timedelta(days=1):
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.questions_today = questions_count
            streak.last_activity_date = today
        else:
            streak.current_streak = 1
            if streak.longest_streak == 0:
                streak.longest_streak = 1
            streak.questions_today = questions_count
            streak.last_activity_date = today

        streak.updated_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def calculate_readiness_score(cls, accuracy: float, avg_speed: float, total_solved: int, mock_avg: float) -> int:
        """
        Calculates a transparent Aptitude Readiness Score (0-100).
        - Accuracy Component: 40%
        - Solved Volume Component: 20%
        - Speed Component: 20%
        - Mock Performance Component: 20%
        """
        acc_score = min(100.0, accuracy) * 0.40
        vol_score = min(100.0, (total_solved / 200.0) * 100.0) * 0.20
        
        # Ideal speed ~40s, penalize if > 90s
        speed_ratio = max(0.0, 1.0 - max(0.0, (avg_speed - 40.0) / 60.0))
        speed_score = (speed_ratio * 100.0) * 0.20

        mock_score = min(100.0, mock_avg) * 0.20

        total = int(round(acc_score + vol_score + speed_score + mock_score))
        return min(100, max(0, total))

    @classmethod
    def recalculate_user_progress(cls, user_id: int):
        """Recalculates user progress, level adaptivity, and readiness score."""
        progress = cls.get_or_create_user_progress(user_id)

        # Aggregates from question answers
        stats = db.session.query(
            func.count(AptitudeQuestionAnswer.id),
            func.sum(db.case((AptitudeQuestionAnswer.is_correct == True, 1), else_=0)),
            func.avg(AptitudeQuestionAnswer.time_taken_seconds)
        ).filter(AptitudeQuestionAnswer.user_id == user_id).first()

        total_ans = stats[0] or 0
        correct_ans = stats[1] or 0
        avg_speed = float(stats[2] or 45.0)

        progress.total_questions_solved = total_ans
        progress.correct_count = correct_ans
        progress.overall_accuracy = round((correct_ans / total_ans * 100.0), 1) if total_ans > 0 else 0.0
        progress.avg_time_seconds = round(avg_speed, 1)

        # Calculate mock avg score
        mock_stats = db.session.query(func.avg(AptitudeTestResult.accuracy_percentage)).filter_by(user_id=user_id).scalar()
        mock_avg = float(mock_stats or 0.0)

        progress.readiness_score = cls.calculate_readiness_score(progress.overall_accuracy, avg_speed, total_ans, mock_avg)

        # Level Progression Logic
        if total_ans >= 15:
            if progress.overall_accuracy >= 85 and progress.current_level != 'master':
                curr_idx = cls.LEVELS.index(progress.current_level)
                if curr_idx < len(cls.LEVELS) - 1:
                    progress.current_level = cls.LEVELS[curr_idx + 1]
            elif progress.overall_accuracy < 45 and progress.current_level != 'foundation':
                curr_idx = cls.LEVELS.index(progress.current_level)
                if curr_idx > 0:
                    progress.current_level = cls.LEVELS[curr_idx - 1]

        progress.updated_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def get_practice_questions(cls, category_id: Optional[int] = None, topic: Optional[str] = None, difficulty: Optional[str] = None, limit: int = 10) -> List[AptitudeQuestion]:
        """Fetches practice questions filtered by category, topic, or difficulty with fallback relaxation."""
        # 1. Strict Query
        query = AptitudeQuestion.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        if topic and topic.strip() and topic.strip().lower() != 'all':
            query = query.filter_by(topic=topic.strip())
        if difficulty and difficulty.strip() and difficulty.strip().lower() not in ['all', 'adaptive']:
            query = query.filter_by(difficulty=difficulty.strip())

        questions = query.order_by(func.random()).limit(limit).all()
        
        # 2. Fallback 1: Relax difficulty filter if insufficient questions
        if len(questions) < limit and difficulty and difficulty.strip().lower() not in ['all', 'adaptive']:
            query_relaxed = AptitudeQuestion.query
            if category_id:
                query_relaxed = query_relaxed.filter_by(category_id=category_id)
            if topic and topic.strip() and topic.strip().lower() != 'all':
                query_relaxed = query_relaxed.filter_by(topic=topic.strip())
            questions = query_relaxed.order_by(func.random()).limit(limit).all()

        # 3. Fallback 2: Relax topic filter if insufficient questions
        if len(questions) < limit and topic and topic.strip().lower() != 'all':
            query_cat = AptitudeQuestion.query
            if category_id:
                query_cat = query_cat.filter_by(category_id=category_id)
            questions = query_cat.order_by(func.random()).limit(limit).all()

        # 4. Fallback 3: Return any available questions from the question bank
        if len(questions) < limit:
            questions = AptitudeQuestion.query.order_by(func.random()).limit(limit).all()

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Practice Filter Request -> CatID: {category_id}, Topic: '{topic}', Diff: '{difficulty}', Limit: {limit} | Retrieved: {len(questions)} questions")

        return questions

    @classmethod
    def submit_single_answer(cls, user_id: int, question_id: int, selected_option: str, time_taken: int = 0) -> Dict[str, Any]:
        """Evaluates a single question submission in practice mode."""
        question = db.session.get(AptitudeQuestion, question_id)
        if not question:
            return {"error": "Question not found"}

        is_correct = (selected_option.upper() == question.correct_option.upper())

        # Log answer
        ans_log = AptitudeQuestionAnswer(
            user_id=user_id,
            question_id=question_id,
            selected_option=selected_option.upper(),
            is_correct=is_correct,
            time_taken_seconds=time_taken
        )
        db.session.add(ans_log)

        # Update topic mastery
        mastery = AptitudeTopicMastery.query.filter_by(user_id=user_id, topic=question.topic).first()
        if not mastery:
            cat = db.session.get(AptitudeCategory, question.category_id)
            cat_name = cat.name if cat else "General"
            mastery = AptitudeTopicMastery(
                user_id=user_id,
                category_name=cat_name,
                topic=question.topic,
                mastery_percentage=0.0,
                questions_attempted=0,
                correct_count=0,
                avg_speed_seconds=0.0
            )
            db.session.add(mastery)

        mastery.questions_attempted += 1
        if is_correct:
            mastery.correct_count += 1
        mastery.mastery_percentage = round((mastery.correct_count / mastery.questions_attempted) * 100.0, 1)
        mastery.last_attempted_at = datetime.utcnow()

        db.session.commit()

        # Update streak & readiness
        cls.update_user_streak(user_id, 1)
        cls.recalculate_user_progress(user_id)

        return {
            "is_correct": is_correct,
            "correct_option": question.correct_option,
            "explanation": question.explanation,
            "formula": question.formula,
            "shortcut": question.shortcut,
            "concept": question.concept,
            "estimated_time": question.estimated_time,
            "actual_time": time_taken
        }

    @classmethod
    def start_mock_session(cls, user_id: int, test_type: str = 'standard', custom_title: Optional[str] = None) -> AptitudeTestSession:
        """Launches a timed mock test with server-side expiry security."""
        mock_configs = {
            'quick': ('Quick Placement Mock', 15, 15),
            'standard': ('Standard Placement Assessment', 30, 30),
            'placement': ('Placement Mastery Assessment', 50, 60),
            'full': ('Full Length Aptitude Mock', 100, 90),
            'master': ('Master Challenge Mock', 100, 90),
            'tcs': ('TCS Pattern-Inspired Mock', 30, 35),
            'infosys': ('Infosys Pattern-Inspired Mock', 30, 35),
            'wipro': ('Wipro Pattern-Inspired Mock', 30, 35),
            'accenture': ('Accenture Pattern-Inspired Mock', 30, 35),
        }
        title, num_q, duration_m = mock_configs.get(test_type, ('Placement Mock Test', 30, 30))
        if custom_title:
            title = custom_title

        questions = AptitudeQuestion.query.order_by(func.random()).limit(num_q).all()
        q_payload = []
        for q in questions:
            q_payload.append({
                "id": q.id,
                "topic": q.topic,
                "category": q.category.name if q.category else "Quantitative",
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty
            })

        session_id = str(uuid.uuid4())
        started_at = datetime.utcnow()
        expires_at = started_at + timedelta(minutes=duration_m)

        session = AptitudeTestSession(
            id=session_id,
            user_id=user_id,
            test_type=test_type,
            title=title,
            total_questions=len(q_payload),
            duration_minutes=duration_m,
            questions_data=json.dumps(q_payload),
            answers_data=json.dumps({}),
            started_at=started_at,
            expires_at=expires_at,
            is_completed=False
        )
        db.session.add(session)
        db.session.commit()
        return session

    @classmethod
    def get_mock_session_status(cls, session_id: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves active mock session and enforces server-side expiration logic."""
        session = db.session.get(AptitudeTestSession, session_id)
        if not session or session.user_id != user_id:
            return None

        # Server-side timer check
        now = datetime.utcnow()
        is_expired = now > session.expires_at

        if is_expired and not session.is_completed:
            cls.submit_mock_session(session_id, user_id, json.loads(session.answers_data or '{}'))
            db.session.refresh(session)

        questions = json.loads(session.questions_data)
        answers = json.loads(session.answers_data or '{}')
        remaining_seconds = max(0, int((session.expires_at - now).total_seconds())) if not session.is_completed else 0

        return {
            "session": session,
            "questions": questions,
            "answers": answers,
            "is_expired": is_expired,
            "remaining_seconds": remaining_seconds
        }

    @classmethod
    def submit_mock_session(cls, session_id: str, user_id: int, user_answers: Dict[str, Any]) -> AptitudeTestResult:
        """Evaluates completed mock test session and compiles performance analytics."""
        session = db.session.get(AptitudeTestSession, session_id)
        if not session or session.user_id != user_id:
            raise ValueError("Invalid test session")

        if session.is_completed:
            existing_res = AptitudeTestResult.query.filter_by(session_id=session_id).first()
            if existing_res:
                return existing_res

        questions = json.loads(session.questions_data)
        correct_count = 0
        incorrect_count = 0
        skipped_count = 0

        cat_scores = {}
        topic_perf = {}

        for q_item in questions:
            q_id = str(q_item['id'])
            q_obj = db.session.get(AptitudeQuestion, q_item['id'])
            if not q_obj:
                continue

            sel_opt = user_answers.get(q_id, {}).get('selected_option') if isinstance(user_answers.get(q_id), dict) else user_answers.get(q_id)
            cat_name = q_item['category']
            topic_name = q_item['topic']

            if cat_name not in cat_scores:
                cat_scores[cat_name] = {"total": 0, "correct": 0}
            cat_scores[cat_name]["total"] += 1

            if topic_name not in topic_perf:
                topic_perf[topic_name] = {"total": 0, "correct": 0}
            topic_perf[topic_name]["total"] += 1

            if not sel_opt:
                skipped_count += 1
            elif sel_opt.upper() == q_obj.correct_option.upper():
                correct_count += 1
                cat_scores[cat_name]["correct"] += 1
                topic_perf[topic_name]["correct"] += 1
                # Log question answer
                db.session.add(AptitudeQuestionAnswer(user_id=user_id, question_id=q_obj.id, selected_option=sel_opt.upper(), is_correct=True))
            else:
                incorrect_count += 1
                db.session.add(AptitudeQuestionAnswer(user_id=user_id, question_id=q_obj.id, selected_option=sel_opt.upper(), is_correct=False))

        total_q = len(questions)
        accuracy = round((correct_count / total_q * 100.0), 1) if total_q > 0 else 0.0
        now = datetime.utcnow()
        time_used = min(session.duration_minutes * 60, int((now - session.started_at).total_seconds()))

        # Categorize strong and weak topics
        strong_topics = [t for t, p in topic_perf.items() if (p['correct'] / p['total']) >= 0.70]
        weak_topics = [t for t, p in topic_perf.items() if (p['correct'] / p['total']) < 0.60]

        session.is_completed = True
        session.completed_at = now
        session.answers_data = json.dumps(user_answers)

        result = AptitudeTestResult(
            session_id=session_id,
            user_id=user_id,
            test_type=session.test_type,
            title=session.title,
            score=correct_count,
            total_questions=total_q,
            accuracy_percentage=accuracy,
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            skipped_count=skipped_count,
            time_used_seconds=time_used,
            category_scores_json=json.dumps(cat_scores),
            strong_topics_json=json.dumps(strong_topics),
            weak_topics_json=json.dumps(weak_topics)
        )
        db.session.add(result)
        db.session.commit()

        cls.update_user_streak(user_id, total_q)
        cls.recalculate_user_progress(user_id)

        return result

    @classmethod
    def get_daily_challenge(cls, user_id: int) -> Dict[str, Any]:
        """Gets or generates today's Daily 10 Challenge."""
        today = date.today()
        challenge = AptitudeDailyChallenge.query.filter_by(challenge_date=today).first()

        if not challenge:
            questions = AptitudeQuestion.query.order_by(func.random()).limit(10).all()
            q_payload = [{"id": q.id, "topic": q.topic, "question_text": q.question_text, "option_a": q.option_a, "option_b": q.option_b, "option_c": q.option_c, "option_d": q.option_d, "difficulty": q.difficulty} for q in questions]
            challenge = AptitudeDailyChallenge(
                challenge_date=today,
                questions_json=json.dumps(q_payload)
            )
            db.session.add(challenge)
            db.session.commit()

        attempt = AptitudeDailyChallengeAttempt.query.filter_by(user_id=user_id, challenge_id=challenge.id).first()
        return {
            "challenge": challenge,
            "questions": json.loads(challenge.questions_json),
            "attempt": attempt
        }

    @classmethod
    def toggle_bookmark(cls, user_id: int, question_id: int) -> bool:
        """Toggles bookmark status for a question."""
        bm = AptitudeBookmark.query.filter_by(user_id=user_id, question_id=question_id).first()
        if bm:
            db.session.delete(bm)
            db.session.commit()
            return False  # Removed
        else:
            bm = AptitudeBookmark(user_id=user_id, question_id=question_id)
            db.session.add(bm)
            db.session.commit()
            return True  # Added

    @classmethod
    def get_user_bookmarks(cls, user_id: int) -> List[AptitudeQuestion]:
        """Retrieves list of bookmarked questions for user."""
        return db.session.query(AptitudeQuestion).join(AptitudeBookmark).filter(AptitudeBookmark.user_id == user_id).order_by(AptitudeBookmark.created_at.desc()).all()

    @classmethod
    def get_personalized_practice(cls, user_id: int, limit: int = 15) -> List[AptitudeQuestion]:
        """Generates custom practice set auto-weighted towards student's weak topics."""
        masteries = AptitudeTopicMastery.query.filter_by(user_id=user_id).order_by(AptitudeTopicMastery.mastery_percentage.asc()).limit(5).all()
        weak_topics = [m.topic for m in masteries if m.mastery_percentage < 70.0]

        if weak_topics:
            questions = AptitudeQuestion.query.filter(AptitudeQuestion.topic.in_(weak_topics)).order_by(func.random()).limit(limit).all()
            if len(questions) < limit:
                fill_q = AptitudeQuestion.query.order_by(func.random()).limit(limit - len(questions)).all()
                questions.extend(fill_q)
            return questions

        return AptitudeQuestion.query.order_by(func.random()).limit(limit).all()

    @classmethod
    def get_analytics_data(cls, user_id: int) -> Dict[str, Any]:
        """Compiles analytics metrics for Chart.js visualization."""
        progress = cls.get_or_create_user_progress(user_id)
        masteries = AptitudeTopicMastery.query.filter_by(user_id=user_id).all()
        recent_results = AptitudeTestResult.query.filter_by(user_id=user_id).order_by(AptitudeTestResult.completed_at.desc()).limit(10).all()

        topic_labels = [m.topic for m in masteries] or ["Percentage", "Average", "Number Series", "Coding-Decoding", "Grammar"]
        topic_scores = [m.mastery_percentage for m in masteries] or [85, 70, 90, 65, 80]

        recent_scores = [r.accuracy_percentage for r in reversed(recent_results)] or [60, 65, 75, 80, 85]
        recent_dates = [r.completed_at.strftime("%b %d") for r in reversed(recent_results)] or ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5"]

        return {
            "progress": progress,
            "readiness_score": progress.readiness_score,
            "overall_accuracy": progress.overall_accuracy,
            "total_solved": progress.total_questions_solved,
            "avg_time": progress.avg_time_seconds,
            "topic_labels": topic_labels,
            "topic_scores": topic_scores,
            "recent_scores": recent_scores,
            "recent_dates": recent_dates
        }
