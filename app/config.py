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
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.getenv('SECRET_KEY') 

# print(f'DB Path: {Config.SQLALCHEMY_DATABASE_URI}')