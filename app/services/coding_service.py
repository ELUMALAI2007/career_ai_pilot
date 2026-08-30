"""
CareerPilot AI - Coding Service Module
Manages problem catalog querying, code execution orchestration, test evaluation,
submission recording, progress tracking, daily challenge scheduling, and gamification.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import func, desc, or_
from app import db
from app.models.coding import (
    CodingProblem, CodingSubmission, CodingBookmark,
    CodingProgress, DailyChallenge, CodingBadge, UserBadge
)
from app.models.user import User
from app.services.code_runner import CodeRunnerService, LocalRunner


class CodingService:
    """Service handling coding problems, code grading, and candidate analytics."""

    def __init__(self, runner_service: CodeRunnerService = None):
        self.runner = runner_service or CodeRunnerService(LocalRunner())

    def get_problems(
        self,
        topic: str = None,
        difficulty: str = None,
        company: str = None,
        status: str = None,  # 'solved', 'attempted', 'unsolved', 'bookmarked'
        search: str = None,
        user_id: int = None
    ) -> List[Dict[str, Any]]:
        """Retrieves and filters coding problems with candidate metadata."""
        query = CodingProblem.query

        if topic and topic.lower() != 'all':
            query = query.filter(CodingProblem.topic.ilike(f"%{topic}%"))

        if difficulty and difficulty.lower() != 'all':
            query = query.filter(CodingProblem.difficulty == difficulty.lower())

        if company and company.lower() != 'all':
            query = query.filter(CodingProblem.company_tags.ilike(f"%{company}%"))

        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    CodingProblem.title.ilike(s),
                    CodingProblem.topic.ilike(s),
                    CodingProblem.company_tags.ilike(s),
                    CodingProblem.description.ilike(s)
                )
            )

        problems = query.order_by(CodingProblem.id.asc()).all()
        result = []

        # Solved and bookmarked problem sets for fast lookup
        solved_ids = set()
        attempted_ids = set()
        bookmarked_ids = set()

        if user_id:
            solved_subs = db.session.query(CodingSubmission.problem_id).filter_by(
                user_id=user_id, status='Accepted'
            ).distinct().all()
            solved_ids = {s[0] for s in solved_subs}

            attempted_subs = db.session.query(CodingSubmission.problem_id).filter_by(
                user_id=user_id
            ).distinct().all()
            attempted_ids = {s[0] for s in attempted_subs if s[0] not in solved_ids}

            bms = db.session.query(CodingBookmark.problem_id).filter_by(user_id=user_id).all()
            bookmarked_ids = {b[0] for b in bms}

        for p in problems:
            p_dict = p.to_public_dict(user_id=user_id)
            p_dict['is_bookmarked'] = p.id in bookmarked_ids

            if p.id in solved_ids:
                p_dict['user_status'] = 'Solved'
            elif p.id in attempted_ids:
                p_dict['user_status'] = 'Attempted'
            else:
                p_dict['user_status'] = 'Unsolved'

            # Filter by candidate status if requested
            if status and status.lower() != 'all':
                st = status.lower()
                if st == 'solved' and p_dict['user_status'] != 'Solved':
                    continue
                elif st == 'attempted' and p_dict['user_status'] != 'Attempted':
                    continue
                elif st == 'unsolved' and p_dict['user_status'] != 'Unsolved':
                    continue
                elif st == 'bookmarked' and not p_dict['is_bookmarked']:
                    continue

            result.append(p_dict)

        return result

    def get_problem_by_slug(self, slug: str, user_id: int = None) -> Optional[Dict[str, Any]]:
        """Retrieves single problem public payload by slug."""
        problem = CodingProblem.query.filter_by(slug=slug).first()
        if not problem:
            return None
        return problem.to_public_dict(user_id=user_id)

    def toggle_bookmark(self, user_id: int, problem_id: int) -> bool:
        """Toggles user bookmark for a problem and returns new bookmark state."""
        existing = CodingBookmark.query.filter_by(user_id=user_id, problem_id=problem_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return False
        else:
            bm = CodingBookmark(user_id=user_id, problem_id=problem_id)
            db.session.add(bm)
            db.session.commit()
            return True

    def run_code(
        self,
        problem_slug: str,
        language: str,
        code_body: str,
        custom_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs candidate code against sample tests or custom stdin."""
        problem = CodingProblem.query.filter_by(slug=slug_clean(problem_slug)).first()
        if not problem:
            return {'status': 'System Error', 'error_log': f"Problem '{problem_slug}' not found."}

        if custom_input is not None and custom_input.strip() != "":
            # Run with custom input
            res = self.runner.run_single(code_body, language, custom_input.strip())
            return {
                'status': res.status,
                'stdout': res.stdout,
                'error_log': res.stderr,
                'execution_time_ms': res.execution_time_ms,
                'is_custom': True,
                'test_results': [
                    {
                        'test_num': 1,
                        'passed': res.status == 'Success',
                        'status': res.status,
                        'execution_time_ms': res.execution_time_ms,
                        'is_sample': True,
                        'input': custom_input,
                        'expected_output': None,
                        'actual_output': res.stdout,
                        'error': res.stderr
                    }
                ]
            }

        # Run against public sample test cases
        sample_tests = problem.sample_test_cases or []
        for tc in sample_tests:
            tc['is_sample'] = True

        return self.runner.evaluate_test_suite(
            code_body,
            language,
            sample_tests,
            is_submission=False
        )

    def submit_solution(
        self,
        user_id: int,
        problem_slug: str,
        language: str,
        code_body: str
    ) -> Dict[str, Any]:
        """
        Grades solution against the full test suite (sample + hidden).
        Records submission and updates XP, streaks, and badges.
        """
        problem = CodingProblem.query.filter_by(slug=slug_clean(problem_slug)).first()
        if not problem:
            return {'status': 'System Error', 'error_log': f"Problem '{problem_slug}' not found."}

        # Assemble full test suite (sample + hidden)
        full_suite = []
        for tc in (problem.sample_test_cases or []):
            full_suite.append({
                'input': tc.get('input', ''),
                'expected_output': tc.get('expected_output', ''),
                'is_sample': True
            })
        for tc in (problem.hidden_test_cases or []):
            full_suite.append({
                'input': tc.get('input', ''),
                'expected_output': tc.get('expected_output', ''),
                'is_sample': False
            })

        # Evaluate test suite
        eval_result = self.runner.evaluate_test_suite(
            code_body,
            language,
            full_suite,
            is_submission=True
        )

        # Update problem metrics
        problem.total_submissions = (problem.total_submissions or 0) + 1
        if eval_result['status'] == 'Accepted':
            problem.accepted_submissions = (problem.accepted_submissions or 0) + 1

        # Record submission
        submission = CodingSubmission(
            user_id=user_id,
            problem_id=problem.id,
            language=language,
            code_body=code_body,
            status=eval_result['status'],
            execution_time_ms=eval_result['execution_time_ms'],
            memory_mb=eval_result.get('memory_mb'),
            passed_tests=eval_result['passed_tests'],
            total_tests=eval_result['total_tests'],
            stdout=eval_result.get('stdout', ''),
            error_log=eval_result.get('error_log', '')
        )
        submission.test_results = eval_result.get('test_results', [])
        db.session.add(submission)
        db.session.commit()

        # Gamification & Progress updates
        xp_earned = 0
        newly_solved = False
        unlocked_badges = []

        if user_id:
            progress = self._get_or_create_progress(user_id)
            progress.total_attempts = (progress.total_attempts or 0) + 1

            if eval_result['status'] == 'Accepted':
                # Check if user already solved this problem prior to this submission
                prior_solves = CodingSubmission.query.filter(
                    CodingSubmission.user_id == user_id,
                    CodingSubmission.problem_id == problem.id,
                    CodingSubmission.status == 'Accepted',
                    CodingSubmission.id != submission.id
                ).count()

                if prior_solves == 0:
                    newly_solved = True
                    progress.total_solved = (progress.total_solved or 0) + 1
                    diff = (problem.difficulty or 'medium').lower()
                    if diff == 'easy':
                        progress.easy_solved = (progress.easy_solved or 0) + 1
                    elif diff == 'hard':
                        progress.hard_solved = (progress.hard_solved or 0) + 1
                    else:
                        progress.medium_solved = (progress.medium_solved or 0) + 1

                    # Award XP
                    xp_earned = problem.xp_reward or 20
                    progress.total_xp = (progress.total_xp or 0) + xp_earned

                    # Update topic stats
                    topic_data = progress.topic_stats or {}
                    t_name = problem.topic or 'General'
                    if t_name not in topic_data:
                        topic_data[t_name] = {'solved': 0, 'total': 0}
                    topic_data[t_name]['solved'] = topic_data[t_name].get('solved', 0) + 1
                    progress.topic_stats = topic_data

                    # Update Streak
                    today = date.today()
                    if progress.last_solved_date:
                        diff_days = (today - progress.last_solved_date).days
                        if diff_days == 1:
                            progress.current_streak = (progress.current_streak or 0) + 1
                        elif diff_days > 1:
                            progress.current_streak = 1
                    else:
                        progress.current_streak = 1

                    if (progress.current_streak or 1) > (progress.longest_streak or 0):
                        progress.longest_streak = progress.current_streak

                    progress.last_solved_date = today

                    # Check Badges
                    unlocked_badges = self._check_and_award_badges(user_id, progress, diff)

            db.session.commit()

        return {
            'submission_id': submission.id,
            'status': eval_result['status'],
            'passed_tests': eval_result['passed_tests'],
            'total_tests': eval_result['total_tests'],
            'execution_time_ms': eval_result['execution_time_ms'],
            'memory_mb': eval_result.get('memory_mb'),
            'error_log': eval_result.get('error_log', ''),
            'test_results': eval_result.get('test_results', []),
            'xp_earned': xp_earned,
            'newly_solved': newly_solved,
            'unlocked_badges': unlocked_badges
        }

    def _get_or_create_progress(self, user_id: int) -> CodingProgress:
        """Retrieves or initializes user coding progress."""
        progress = CodingProgress.query.filter_by(user_id=user_id).first()
        if not progress:
            progress = CodingProgress(user_id=user_id)
            db.session.add(progress)
            db.session.flush()
        return progress

    def _check_and_award_badges(self, user_id: int, progress: CodingProgress, difficulty: str) -> List[Dict[str, str]]:
        """Evaluates badge milestones and awards newly unlocked achievements."""
        unlocked = []
        earned_badge_ids = {
            ub.badge_id for ub in UserBadge.query.filter_by(user_id=user_id).all()
        }

        milestones = [
            ('first_solve', progress.total_solved >= 1),
            ('solve_10', progress.total_solved >= 10),
            ('solve_50', progress.total_solved >= 50),
            ('solve_100', progress.total_solved >= 100),
            ('streak_7', (progress.current_streak or 0) >= 7),
            ('hard_crusher', difficulty == 'hard')
        ]

        for code, condition in milestones:
            if condition:
                badge = CodingBadge.query.filter_by(code=code).first()
                if badge and badge.id not in earned_badge_ids:
                    user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                    db.session.add(user_badge)
                    progress.total_xp = (progress.total_xp or 0) + (badge.xp_bonus or 50)
                    unlocked.append({
                        'name': badge.name,
                        'description': badge.description,
                        'icon': badge.icon,
                        'xp_bonus': badge.xp_bonus
                    })

        return unlocked

    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Calculates rich progress analytics, difficulty breakdown, and topic mastery."""
        progress = self._get_or_create_progress(user_id)
        
        # Calculate total problems in system
        total_problems = CodingProblem.query.count()
        easy_total = CodingProblem.query.filter_by(difficulty='easy').count()
        medium_total = CodingProblem.query.filter_by(difficulty='medium').count()
        hard_total = CodingProblem.query.filter_by(difficulty='hard').count()

        # Topic breakdown
        all_topics = db.session.query(
            CodingProblem.topic, func.count(CodingProblem.id)
        ).group_by(CodingProblem.topic).all()
        
        user_topics = progress.topic_stats or {}
        topic_breakdown = []
        for t_name, t_count in all_topics:
            solved_in_topic = user_topics.get(t_name, {}).get('solved', 0)
            pct = round((solved_in_topic / max(1, t_count)) * 100, 1)
            topic_breakdown.append({
                'topic': t_name,
                'solved': solved_in_topic,
                'total': t_count,
                'percentage': pct
            })

        # Sort topics by total problems descending
        topic_breakdown.sort(key=lambda x: x['total'], reverse=True)

        easy_pct = round(((progress.easy_solved or 0) / max(1, total_problems)) * 100, 1)
        medium_pct = round(((progress.medium_solved or 0) / max(1, total_problems)) * 100, 1)
        hard_pct = round(((progress.hard_solved or 0) / max(1, total_problems)) * 100, 1)

        return {
            'total_solved': progress.total_solved or 0,
            'total_problems': total_problems,
            'solve_percentage': round(((progress.total_solved or 0) / max(1, total_problems)) * 100, 1),
            'easy_solved': progress.easy_solved or 0,
            'easy_total': easy_total,
            'easy_pct': easy_pct,
            'medium_solved': progress.medium_solved or 0,
            'medium_total': medium_total,
            'medium_pct': medium_pct,
            'hard_solved': progress.hard_solved or 0,
            'hard_total': hard_total,
            'hard_pct': hard_pct,
            'total_attempts': progress.total_attempts or 0,
            'accuracy': progress.accuracy or 0.0,
            'total_xp': progress.total_xp or 0,
            'current_streak': progress.current_streak or 0,
            'longest_streak': progress.longest_streak or 0,
            'proctor_flags': progress.proctor_flags or 0,
            'topic_breakdown': topic_breakdown
        }

    def get_daily_challenge(self, user_id: int = None) -> Optional[Dict[str, Any]]:
        """Retrieves today's featured challenge problem."""
        today = date.today()
        dc = DailyChallenge.query.filter_by(challenge_date=today).first()
        
        # If no challenge exists for today, select one deterministically
        if not dc:
            all_probs = CodingProblem.query.order_by(CodingProblem.id.asc()).all()
            if not all_probs:
                return None
            idx = (today.toordinal()) % len(all_probs)
            selected_prob = all_probs[idx]
            dc = DailyChallenge(challenge_date=today, problem_id=selected_prob.id)
            db.session.add(dc)
            db.session.commit()

        prob_dict = dc.problem.to_public_dict(user_id=user_id)
        is_completed = False
        if user_id:
            today_start = datetime.combine(today, datetime.min.time())
            solved_today = CodingSubmission.query.filter(
                CodingSubmission.user_id == user_id,
                CodingSubmission.problem_id == dc.problem_id,
                CodingSubmission.status == 'Accepted',
                CodingSubmission.submitted_at >= today_start
            ).first()
            is_completed = bool(solved_today)

        return {
            'date': today.strftime('%B %d, %Y'),
            'problem': prob_dict,
            'is_completed': is_completed
        }

    def get_user_submissions(
        self,
        user_id: int,
        problem_id: int = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Retrieves user submission history with problem details."""
        query = CodingSubmission.query.filter_by(user_id=user_id)
        if problem_id:
            query = query.filter_by(problem_id=problem_id)
        
        submissions = query.order_by(CodingSubmission.submitted_at.desc()).limit(limit).all()
        return [s.to_dict() for s in submissions]

    def get_leaderboard(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns leaderboard sorted by XP and problems solved."""
        progress_rows = CodingProgress.query.order_by(
            CodingProgress.total_xp.desc(),
            CodingProgress.total_solved.desc()
        ).limit(limit).all()

        leaderboard = []
        for rank, p in enumerate(progress_rows, 1):
            leaderboard.append({
                'rank': rank,
                'user_id': p.user_id,
                'user_name': p.user.full_name if p.user else f"User #{p.user_id}",
                'total_xp': p.total_xp,
                'total_solved': p.total_solved,
                'easy_solved': p.easy_solved,
                'medium_solved': p.medium_solved,
                'hard_solved': p.hard_solved,
                'current_streak': p.current_streak,
                'proctor_flags': p.proctor_flags or 0
            })
        return leaderboard

    def deduct_proctor_penalty(self, user_id: int, penalty_xp: int = 50) -> Dict[str, Any]:
        """Deducts XP points from a user's progress for proctoring violations."""
        progress = self._get_or_create_progress(user_id)
        old_xp = progress.total_xp or 0
        new_xp = max(0, old_xp - penalty_xp)
        progress.total_xp = new_xp
        progress.proctor_flags = (progress.proctor_flags or 0) + 2
        db.session.commit()
        return {
            'old_xp': old_xp,
            'new_xp': new_xp,
            'deducted': old_xp - new_xp,
            'proctor_flags': progress.proctor_flags
        }


def slug_clean(slug: str) -> str:
    """Sanitizes slug string."""
    return (slug or '').strip().lower()
