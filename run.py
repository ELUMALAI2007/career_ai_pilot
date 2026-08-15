"""
CareerPilot AI Assistant Entry Point Script
Initializes the Flask application via the Application Factory pattern.
"""

import os
from app import create_app
from config import config_by_name

env_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_by_name[env_name])

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug = app.config.get('DEBUG', True)
    
    app.run(host=host, port=port, debug=debug)
