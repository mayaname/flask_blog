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
02/06/2025 Updated to support German translations
"""


import logging
import os
from datetime import timedelta
from flask import Flask, request
from flask_babel import lazy_gettext as _l
from flask_mail import Mail, Message
from logging.handlers import SMTPHandler, RotatingFileHandler
from .config import Config
from . import errors
from .extensions import db, login_manager, mail, migrate, moment, babel
from .models import User, Post
from .routes import pages

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def create_app():
    app = Flask(__name__)

    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])
        # return 'de'

    # Sets config for development
    app.config.from_object(Config)
    # Set custom remember me duration
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

    # Initialize extensions
    babel.init_app(app, locale_selector=get_locale)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)

    # Set view to login route 
    login_manager.login_view = 'pages.login'
    login_manager.login_message = _l("You are not authorized to modify site content.")
    login_manager.login_message_category = "warning"

    # Get user by id for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(pages)

    # Error handlers
    app.register_error_handler(403, errors.forbidden)
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(500, errors.internal_server_error)   

    # Add shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post}
    
    # Set up logging abd email error notification
    # mail = Mail(app)

    # Create Email Logging Handler
    class SendGridHandler(logging.Handler):
        def emit(self, record):
            try:
                msg = Message(
                    subject='Flash Journal Failure',
                    body=self.format(record),  
                    recipients=app.config['ADMIN']
                )
                mail.send(msg)
            except Exception:
                self.handleError(record)   

    # Configure the logger mail and file handlers
    if not app.debug:  
        # Same log format for both email and file
        MESSAGE_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

        app.logger.setLevel(logging.INFO)

        mail_handler = SendGridHandler()
        mail_handler.setLevel(logging.ERROR) 
        
        # Formatter same for both email and 
        formatter = logging.Formatter(
            MESSAGE_FORMAT
        )
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

        # Create directory for log files
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Configure log file handler
        file_handler = RotatingFileHandler('logs/journal.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            MESSAGE_FORMAT
            ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)  

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask Journal startup')              


    # Test the Logging:
    # TODO: Remove when done testing
    @app.route('/email_test/')
    def email_test():
        app.logger.error('Something went amok.') 
        return 'Email Test'

    return app
