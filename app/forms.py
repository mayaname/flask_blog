"""
Program: Forms
Author: Maya Name
Creation Date: 12/31/2024
Revision Date: 
Description: Forms file for microblog application

Revisions:


"""

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, ValidationError
from app.extensions import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
