"""
Program: Init
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 
Description: Init file for microblog application

Run app:
use run.py

Revisions:

"""

from flask import Flask
from .config import Config
from .extensions import db, migrate
from .models import User, Post
from .routes import pages

def create_app():
    app = Flask(__name__)

    # Sets config for development
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(pages)

    return app
