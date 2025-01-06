"""
Program: Init
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 
Description: Init file for microblog application

Run app:
use run.py

Revisions:
01/02/2025 Add support for database and Flask shell
"""

from datetime import timedelta
from flask import Flask
from .config import Config
from .extensions import db, login_manager, migrate
from .models import User, Post
from .routes import pages

def create_app():
    app = Flask(__name__)

    # Sets config for development
    app.config.from_object(Config)
    # Set custom remember me duration
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Set view to login route 
    login_manager.login_view = 'pages.login'
    login_manager.login_message = "You are not authorized to modify site content."
    login_manager.login_message_category = "warning"

    # Get user by id for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(pages)

    # Add shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post}

    return app
