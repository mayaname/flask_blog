"""
Program: Extensions
Author: Maya Name
Creation Date: 01/01/2025
Revision Date: 
Description: Extensions file for microblog application

Revisions:


"""


from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()