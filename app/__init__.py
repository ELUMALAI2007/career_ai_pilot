"""
CareerPilot AI Application Factory Package
Initializes extensions and registers 18 feature blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from config import DevelopmentConfig
from app.logging_config import configure_logging
from app.security import configure_security_headers

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=DevelopmentConfig):
    """
    Application Factory function creating and configuring Flask instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register helper functions in Jinja environment
    def get_field(obj, key, default=''):
        if obj is None:
            return default
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    app.jinja_env.filters['get_field'] = get_field
    app.jinja_env.globals['get_field'] = get_field
    app.jinja_env.globals['attribute'] = get_field
    app.jinja_env.globals['getattr'] = get_field

    # Initialize logging & security headers
    configure_logging(app)
    configure_security_headers(app)

    # Initialize extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Ensure all database models are registered, tables created, and default roles/admin account seeded automatically
    with app.app_context():
        import app.models as _models  # noqa: F401
        db.create_all()
        try:
            from app.models.user import User, Role
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(name='admin', description='Platform Administrator')
                db.session.add(admin_role)
            student_role = Role.query.filter_by(name='student').first()
            if not student_role:
                student_role = Role(name='student', description='Placement Candidate Student')
                db.session.add(student_role)
            db.session.commit()

            admin_email = "admin@careerpilot.ai"
            admin_user = User.query.filter_by(email=admin_email).first()
            if not admin_user:
                admin_user = User(
                    full_name='System Administrator',
                    email=admin_email,
                    role_id=admin_role.id,
                    status='approved',
                    auth_provider='local',
                    is_active=True,
                    is_verified=True
                )
                admin_user.set_password('AdminSecure123!')
                db.session.add(admin_user)
                db.session.commit()
        except Exception:
            db.session.rollback()

        import os
        import sys
        is_testing = 'pytest' in sys.modules or 'PYTEST_CURRENT_TEST' in os.environ or app.config.get('TESTING')

        if not is_testing:
            # Safely apply schema migrations for any columns added later (e.g. is_verified)
            try:
                from sqlalchemy import inspect, text
                inspector = inspect(db.engine)
                
                if 'users' in inspector.get_table_names():
                    columns = [c['name'] for c in inspector.get_columns('users')]
                    with db.engine.connect() as conn:
                        needs_commit = False
                        if 'google_id' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN google_id VARCHAR(100)"))
                            needs_commit = True
                        if 'profile_picture' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"))
                            needs_commit = True
                        if 'auth_provider' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local'"))
                            needs_commit = True
                        if 'status' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'approved'"))
                            needs_commit = True
                        if 'is_verified' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0"))
                            needs_commit = True
                        if 'last_login_at' not in columns:
                            conn.execute(text("ALTER TABLE users ADD COLUMN last_login_at DATETIME"))
                            needs_commit = True
                        if needs_commit:
                            conn.commit()

                if 'interview_sessions' in inspector.get_table_names():
                    interview_cols = [c['name'] for c in inspector.get_columns('interview_sessions')]
                    with db.engine.connect() as conn:
                        needs_commit = False
                        if 'question_queue' not in interview_cols:
                            conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN question_queue JSON"))
                            needs_commit = True
                        if 'follow_up_count' not in interview_cols:
                            conn.execute(text("ALTER TABLE interview_sessions ADD COLUMN follow_up_count INTEGER DEFAULT 0"))
                            needs_commit = True
                        if needs_commit:
                            conn.commit()

                if 'interview_questions' in inspector.get_table_names():
                    question_cols = [c['name'] for c in inspector.get_columns('interview_questions')]
                    if 'question' not in question_cols:
                        with db.engine.connect() as conn:
                            conn.execute(text("ALTER TABLE interview_questions RENAME TO interview_questions_legacy"))
                            conn.commit()
                        db.create_all()
                        with db.engine.begin() as conn:
                            if 'question_text' in question_cols:
                                conn.execute(text(
                                    "INSERT INTO interview_questions "
                                    "(question, role, interview_type, difficulty, topic, company, is_active) "
                                    "SELECT question_text, 'Software Developer', 'Technical', 'Medium', "
                                    "'General', NULL, 1 FROM interview_questions_legacy "
                                    "WHERE question_text IS NOT NULL AND question_text != ''"
                                ))

                if 'aptitude_questions' in inspector.get_table_names():
                    apt_cols = [c['name'] for c in inspector.get_columns('aptitude_questions')]
                    with db.engine.connect() as conn:
                        needs_commit = False
                        if 'is_active' not in apt_cols:
                            conn.execute(text("ALTER TABLE aptitude_questions ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                            needs_commit = True
                        if 'updated_at' not in apt_cols:
                            conn.execute(text("ALTER TABLE aptitude_questions ADD COLUMN updated_at DATETIME"))
                            needs_commit = True
                        if needs_commit:
                            conn.commit()
            except Exception as e:
                app.logger.warning(f"Error applying automatic schema migrations: {e}")

            try:
                from app.models.user import User, Role
                admin_role = Role.query.filter_by(name='admin').first()
                if not admin_role:
                    admin_role = Role(name='admin', description='Platform Administrator')
                    db.session.add(admin_role)
                student_role = Role.query.filter_by(name='student').first()
                if not student_role:
                    student_role = Role(name='student', description='Placement Candidate Student')
                    db.session.add(student_role)
                db.session.commit()

                admin_email = "admin@careerpilot.ai"
                admin_user = User.query.filter_by(email=admin_email).first()
                if not admin_user:
                    admin_user = User(
                        full_name='System Administrator',
                        email=admin_email,
                        role_id=admin_role.id,
                        status='approved',
                        auth_provider='local',
                        is_active=True,
                        is_verified=True
                    )
                    admin_user.set_password('AdminSecure123!')
                    db.session.add(admin_user)
                    db.session.commit()
            except Exception:
                db.session.rollback()

        # Seed required question banks when empty, unless the app is running under pytest.
        if not is_testing:
            try:
                from app.models.aptitude import AptitudeQuestion
                if AptitudeQuestion.query.count() == 0:
                    app.logger.info("Aptitude questions not found. Seeding verified Aptitude questions into database...")
                    from generate_question_bank import _do_generate_batch
                    _do_generate_batch()
            except Exception as e:
                app.logger.warning(f"Error seeding aptitude questions: {e}")

            try:
                from app.models.interview import InterviewQuestion
                if InterviewQuestion.query.count() == 0:
                    from scripts.seed_interview_questions import seed_questions
                    app.logger.info("Interview questions not found. Seeding question bank...")
                    seed_questions()
            except Exception as e:
                app.logger.warning(f"Error seeding interview questions: {e}")

            try:
                from app.models.coding import CodingProblem
                if CodingProblem.query.count() == 0:
                    from database.seed_coding import seed_coding_database
                    app.logger.info("Coding problems not found. Seeding challenge bank...")
                    seed_coding_database(app)
            except Exception as e:
                app.logger.warning(f"Error seeding coding problems: {e}")

    # Login Manager Configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    # Register Global HTTP Error Handlers
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)

    # Register All 18 Feature Blueprints
    from app.routes.admin_bp import admin_bp
    from app.routes.ai_assistant_bp import ai_assistant_bp
    from app.routes.analytics_bp import analytics_bp
    from app.routes.aptitude_bp import aptitude_bp
    from app.routes.auth_bp import auth_bp
    from app.routes.coding_bp import coding_bp
    from app.routes.communication_bp import communication_bp
    from app.routes.company_prep_bp import company_prep_bp
    from app.routes.dashboard_bp import dashboard_bp
    from app.routes.interview_bp import interview_bp
    from app.routes.job_eligibility_bp import job_eligibility_bp
    from app.routes.learning_roadmap_bp import learning_roadmap_bp
    from app.routes.notification_bp import notification_bp
    from app.routes.planner_bp import planner_bp
    from app.routes.profile_bp import profile_bp
    from app.routes.resume_bp import resume_bp
    from app.routes.settings_bp import settings_bp
    from app.routes.skill_gap_bp import skill_gap_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ai_assistant_bp, url_prefix='/assistant')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(aptitude_bp, url_prefix='/aptitude')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(coding_bp, url_prefix='/coding')
    app.register_blueprint(communication_bp, url_prefix='/communication')
    app.register_blueprint(company_prep_bp, url_prefix='/company-prep')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(interview_bp, url_prefix='/interview')
    app.register_blueprint(job_eligibility_bp, url_prefix='/eligibility')
    app.register_blueprint(learning_roadmap_bp, url_prefix='/roadmap')
    app.register_blueprint(notification_bp, url_prefix='/notifications')
    app.register_blueprint(planner_bp, url_prefix='/planner')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(resume_bp, url_prefix='/resume')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(skill_gap_bp, url_prefix='/skill-gap')

    # Global Account Status & Security Enforcement Middleware
    @app.before_request
    def check_user_access_status():
        from flask import request, redirect, url_for
        from flask_login import current_user

        if current_user.is_authenticated:
            # Exempt routes: static files, logout, pending view, rejected view
            exempt_endpoints = {'auth.logout', 'auth.pending', 'auth.rejected', 'static'}
            if request.endpoint and request.endpoint not in exempt_endpoints:
                if current_user.is_pending:
                    return redirect(url_for('auth.pending'))
                elif current_user.is_rejected:
                    return redirect(url_for('auth.rejected'))

    # Main index fallback redirecting to dashboard or login
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.is_pending:
                return redirect(url_for('auth.pending'))
            elif current_user.is_rejected:
                return redirect(url_for('auth.rejected'))
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    return app
