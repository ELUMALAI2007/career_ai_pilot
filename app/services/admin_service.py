"""
CareerPilot AI - Admin Service
Orchestrates administrative tasks, user role management, system metrics, and audit logging.
"""

from app.models.user import User
from app.models.admin import AdminLog, SystemNotice
from app import db


class AdminService:
    """Service handling platform admin operations."""

    @staticmethod
    def get_system_stats() -> dict:
        """Retrieves real system statistics across all database tables."""
        from app.models.user import User, Role
        from app.models.aptitude import AptitudeQuestion, AptitudeAttempt, AptitudeTestResult
        from app.models.coding import CodingSubmission
        from app.models.interview import MockInterview
        from app.models.resume import ResumeAnalysis

        student_role = Role.query.filter_by(name='student').first()
        student_role_id = student_role.id if student_role else None

        return {
            "total_users": User.query.count(),
            "total_students": User.query.filter_by(role_id=student_role_id).count() if student_role_id else User.query.count(),
            "active_students": User.query.filter_by(is_active=True, status='approved').count(),
            "pending_requests": User.query.filter_by(status='pending').count(),
            "approved_users": User.query.filter_by(status='approved').count(),
            "rejected_users": User.query.filter_by(status='rejected').count(),
            "total_aptitude_questions": AptitudeQuestion.query.count(),
            "total_aptitude_attempts": AptitudeAttempt.query.count(),
            "total_mock_tests": AptitudeTestResult.query.count(),
            "total_resume_analyses": ResumeAnalysis.query.count(),
            "total_coding_submissions": CodingSubmission.query.count(),
            "total_interview_sessions": MockInterview.query.count()
        }

    @staticmethod
    def get_user_requests(status_filter: str = None, search_query: str = None) -> list:
        """Retrieves user access requests with optional status and search filtering."""
        query = User.query
        if status_filter and status_filter != 'all':
            query = query.filter_by(status=status_filter)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(User.full_name.ilike(term) | User.email.ilike(term))
        return query.order_by(User.created_at.desc()).all()

    @staticmethod
    def get_request_counts() -> dict:
        """Returns request counts broken down by status."""
        return {
            "pending": User.query.filter_by(status='pending').count(),
            "approved": User.query.filter_by(status='approved').count(),
            "rejected": User.query.filter_by(status='rejected').count(),
            "total": User.query.count()
        }

    @classmethod
    def update_user_status(cls, admin_id: int, user_id: int, new_status: str) -> User:
        """Updates user approval status (approved/rejected) and sends email alert."""
        from app.services.auth_service import AuthService
        user = db.session.get(User, user_id)
        if not user:
            return None

        old_status = user.status
        user.status = new_status
        db.session.commit()

        # Audit Log
        cls.log_action(admin_id, f"USER_STATUS_CHANGE", f"Changed status for {user.email} from {old_status} to {new_status}")

        # Dispatch email notification to candidate
        AuthService.notify_user_status_update(user, new_status)
        return user

    @staticmethod
    def log_action(admin_id: int, action: str, details: str = None):
        """Creates an audit log entry."""
        log = AdminLog(admin_id=admin_id, action=action, details=details)
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_aptitude_questions(search_query: str = None, category_id: int = None, topic: str = None, difficulty: str = None, page: int = 1, per_page: int = 20):
        """Paginated retrieval of aptitude questions for admin management."""
        from app.models.aptitude import AptitudeQuestion
        query = AptitudeQuestion.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        if topic and topic != 'all':
            query = query.filter_by(topic=topic)
        if difficulty and difficulty != 'all':
            query = query.filter_by(difficulty=difficulty)
        if search_query:
            term = f"%{search_query.strip()}%"
            query = query.filter(AptitudeQuestion.question_text.ilike(term) | AptitudeQuestion.topic.ilike(term))
        return query.order_by(AptitudeQuestion.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

