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

    # Initialize logging & security headers
    configure_logging(app)
    configure_security_headers(app)

    # Initialize extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Ensure all database models are registered and tables created automatically
    with app.app_context():
        import app.models as _models  # noqa: F401
        db.create_all()

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
