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
from .routes import pages

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(pages)

    return app
