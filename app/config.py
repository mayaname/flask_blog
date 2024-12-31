"""
Program: Config
Author: Maya Name
Creation Date: 12/31/2024
Revision Date: 
Description: Configuration file for microblog application

Revisions:

"""

import os
from dotenv import load_dotenv
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# Temporary app to get the instance path
app = Flask(__name__)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') 