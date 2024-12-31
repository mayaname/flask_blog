"""
Program: Init
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 
Description: Init file for Flask Video Catalog application

Run app:
use run.py

Revisions:

"""


from flask import Blueprint, flash, render_template, redirect,  url_for
from app.forms import LoginForm

pages = Blueprint('pages', __name__)

@pages.route('/')
@pages.route('/index/')
def index():
    head_title = 'Home'
    page_title = 'Blog Posts'
    user = {'username': 'Maya'}

    posts = [
        {
            'title': 'Using the Python Interpreter in Linux',
            'author': {'username': 'John'},
            'body': 'For Python interpreter, the open a terminal window and type python3,  To exit the interactive prompt, you can type exit() and press Enter or by pressing Ctrl-D. ',
            'posted': '12/30/2024'

        },
        {
            'title': 'Creating a Virtual Environment with Python',
            'author': {'username': 'Susan'},
            'body': 'In the Linux terminal window, type python3 -m venv venv and press Enter. This creates a virtual environment called venv. To activate, type source venv/bin/activate and press Enter.',
            'posted': '12/30/2024'
        },
        {
            'title': 'Installing the Flask Package',
            'author': {'username': 'Maya'},
            'body': 'Be sure that you have the virtual environment activates. Type pip install flask. Note the lowercase f is user for the package name. Confirm the install by typing import flask in the Python interpreter window.',
            'posted': '12/30/2024'
        },
        {
            'title': 'Creating a Python Package',
            'author': {'username': 'Bob'},
            'body': 'In the application folder, create a subfolder called app. In the app subfolder, create an __init__.py file. This file will make the contents of the app subfolder into a package.',
            'posted': '12/30/2024'
        }
    ]
    return render_template('index.html',
                           head_title=head_title,
                           page_title=page_title,
                           posts=posts,
                           user = user)

@pages.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    head_title = 'Login'
    page_title = 'Sign In'

    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}' , 'success')
        return redirect(url_for('pages.index'))

    return render_template('login.html', 
                               head_title=head_title,
                               page_title=page_title, 
                               form=form)