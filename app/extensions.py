"""
Program: Extensions
Author: Maya Name
Creation Date: 01/01/2025
Revision Date: 
Description: Extensions file for microblog application

Revisions:


"""


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()