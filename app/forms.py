"""
Program: Forms
Author: Maya Name
Creation Date: 12/31/2024
Revision Date: 02/03/2025
Description: Forms file for microblog application

Revisions:
02/03/2025 Update text to support German translation

"""

import sqlalchemy as sa
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError
from app.extensions import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[InputRequired()])
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class SignupForm(FlaskForm):
    firstname = StringField(_l('First name'), validators=[InputRequired()])
    lastname = StringField(_l('Last name'), validators=[InputRequired()])
    username = StringField(_l('Username'), validators=[InputRequired()])
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[InputRequired(), EqualTo('password')])
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    submit = SubmitField(_l('Sign Up'))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))


class EditProfileForm(FlaskForm):
    firstname = StringField(_l('First name'), validators=[InputRequired()])
    lastname = StringField(_l('Last name'), validators=[InputRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))


class FollowForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField(_l('Title'), validators=[InputRequired()])
    post = TextAreaField(_l('Entry'), validators=[
        InputRequired(), Length(min=1, max=1024)])
    submit = SubmitField(_l('Post'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[InputRequired(), Email()])
    submit = SubmitField(_l('Request Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[InputRequired()])
    submit = SubmitField("Submit")