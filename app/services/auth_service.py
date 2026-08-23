import logging
from flask import current_app, url_for
from flask_mail import Message
from app.models.user import User
from app import db, mail

logger = logging.getLogger(__name__)


class AuthService:
    """Service for managing user authentication and account creation."""

    @staticmethod
    def register_user(full_name: str, email: str, password: str) -> User:
        """Registers a new user account via local credentials."""
        from sqlalchemy.exc import IntegrityError
        from app.models.user import Role

        clean_email = email.strip().lower()
        existing = User.query.filter_by(email=clean_email).first()
        if existing:
            raise ValueError("This email address is already registered. Please sign in instead.")

        student_role = Role.query.filter_by(name='student').first()
        role_id = student_role.id if student_role else None

        user = User(
            full_name=full_name.strip(),
            email=clean_email,
            status='approved',
            auth_provider='local',
            role_id=role_id,
            is_active=True,
            is_verified=True
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("This email address is already registered. Please sign in instead.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user {clean_email}: {e}")
            raise

    @staticmethod
    def authenticate(email: str, password: str) -> User:
        """Authenticates user credentials, logs diagnostic lookup status, and updates last login timestamp."""
        from datetime import datetime
        clean_email = email.strip().lower() if email else ""
        user = User.query.filter_by(email=clean_email).first()

        if not user:
            logger.info(f"Authentication lookup failed: user_not_found for email='{clean_email}'")
            return None

        if not user.is_active:
            logger.info(f"Authentication lookup failed: account_deactivated for email='{clean_email}'")
            return None

        if not user.check_password(password):
            logger.info(f"Authentication lookup failed: password_mismatch for email='{clean_email}'")
            return None

        user.last_login_at = datetime.utcnow()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.warning(f"Could not update last_login_at for {clean_email}: {e}")
        return user

    @classmethod
    def process_google_user(cls, google_id: str, email: str, full_name: str, picture: str = None) -> tuple[User, bool]:
        """
        Processes Google OAuth login. 
        Links existing accounts by email or creates a new pending candidate request.
        Returns tuple: (user, is_new_created)
        """
        # 1. Search by google_id
        user = User.query.filter_by(google_id=google_id).first()
        if user:
            if picture and not user.profile_picture:
                user.profile_picture = picture
                db.session.commit()
            return user, False

        # 2. Search by verified email (Associate with existing local account)
        user = User.query.filter_by(email=email).first()
        if user:
            user.google_id = google_id
            user.profile_picture = picture or user.profile_picture
            user.auth_provider = 'both' if user.auth_provider == 'local' else user.auth_provider
            db.session.commit()
            return user, False

        # 3. Create new user account (Default status: 'pending')
        user = User(
            full_name=full_name or email.split('@')[0],
            email=email,
            google_id=google_id,
            profile_picture=picture,
            auth_provider='google',
            status='pending'
        )
        db.session.add(user)
        db.session.commit()

        # Send notification to administrator
        cls.notify_admin_new_request(user)
        return user, True

    @staticmethod
    def notify_admin_new_request(user: User):
        """Sends an administrative alert email when a new Google user registers."""
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@careerpilot.ai')
        review_url = url_for('admin.requests', _external=True)
        
        subject = "New Career Prospects Access Request"
        body = (
            f"Subject: {subject}\n\n"
            f"New user wants access to Career Prospects.\n\n"
            f"Name: {user.full_name}\n"
            f"Email: {user.email}\n"
            f"Authentication: Google OAuth\n"
            f"Registration Time: {user.created_at.strftime('%d %B %Y, %I:%M %p')}\n"
            f"Status: {user.status.upper()}\n\n"
            f"Review request at: {review_url}\n"
        )
        
        try:
            msg = Message(
                subject=subject,
                recipients=[admin_email],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            mail.send(msg)
            logger.info(f"Admin approval email dispatched to {admin_email} for user {user.email}")
        except Exception as e:
            logger.warning(f"Could not send admin notification email via SMTP (Logged locally): {e}\n{body}")

    @staticmethod
    def notify_user_status_update(user: User, action: str):
        """Notifies user via email when their account request is approved or rejected."""
        sign_in_url = url_for('auth.login', _external=True)
        
        if action == 'approved':
            subject = "Your Career Prospects Access Has Been Approved"
            body = (
                f"Hello {user.full_name},\n\n"
                f"Your Career Prospects account has been approved!\n\n"
                f"You can now sign in using Google and access your Career Prospects dashboard.\n\n"
                f"Sign In here: {sign_in_url}\n"
            )
        else:
            subject = "Career Prospects Access Request Update"
            body = (
                f"Hello {user.full_name},\n\n"
                f"Your request to access Career Prospects was not approved at this time.\n\n"
                f"If you believe this is an error, please contact the administrator.\n"
            )

        try:
            msg = Message(
                subject=subject,
                recipients=[user.email],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            mail.send(msg)
            logger.info(f"Status update ({action}) email sent to {user.email}")
        except Exception as e:
            logger.warning(f"Could not send user status email via SMTP (Logged locally): {e}\n{body}")
