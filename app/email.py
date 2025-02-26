"""
Program: Email
Author: Maya Name
Creation Date: 01/28/202
Revision Date: 
Description: Email wrapper function for Flask microblog application

Revisions:

"""

from flask import render_template, current_app
from flask_mail import Message
from app.config import Config
from app.extensions import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Flask Journal - Reset Password',
               sender=Config.MAIL_DEFAULT_SENDER,
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))