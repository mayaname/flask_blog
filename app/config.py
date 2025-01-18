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


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') 
    SECRET_KEY = os.getenv('SECRET_KEY') 

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
    # ADMIN = os.environ.get('MAIL_ADMIN')
    ADMIN = os.environ.get('MAIL_ADMIN').split(',')

