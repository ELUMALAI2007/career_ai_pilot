"""
CareerPilot AI HTTP Error Handlers
Renders custom user-friendly error templates for HTTP 400, 403, 404, and 500 status codes.
"""

from flask import render_template

def register_error_handlers(app):
    """Registers custom error handlers with the Flask app."""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(500)
    def internal_error(error):
        # TODO: Implement automated error alerting or db rollback if needed
        return render_template('errors/500.html', error=error), 500
