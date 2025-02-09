"""
Program: Extensions
Author: Maya Name
Creation Date: 01/01/2025
Revision Date: 
Description: Extensions file for microblog application

Revisions:


"""

from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from googletrans import Translator


babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
moment = Moment()
translator = Translator()
