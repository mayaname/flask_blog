"""
Program: Init
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 
Description: Init file for Flask microblog application

Revisions:

"""

import sqlalchemy as sa
from flask import Blueprint, flash, render_template, redirect,  request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from urllib.parse import urlparse, urljoin
from app.forms import LoginForm, SignupForm
from app.extensions import db
from app.models import User, Post

pages = Blueprint('pages', __name__)

def is_safe_redirect_url(target):
    # Check if the url is safe for redirects 
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
        redirect_url.scheme in ('http', 'https') and
        host_url.netloc == redirect_url.netloc
    )

# Application routes

@pages.route('/')
@pages.route('/index/')
def index():
    head_title = 'Home'
    page_title = 'Journal Posts'
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
    page_title = 'Journal Login'

    # Reroute to index if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid login. Check your username and password.', 
                    'error')
            return redirect(url_for('pages.login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'{form.username.data} successfully logged in' , 'success')
        # return redirect(url_for('pages.index'))

        # Check the 'next' parameter for safe redirection
        next_page = request.form.get('next') or request.args.get('next') 

        if next_page and is_safe_redirect_url(next_page):
            # Redirect safely
            return redirect(next_page)
        # Fallback to a default page
        return redirect(url_for('pages.index'))


    return render_template('login.html', 
                               head_title=head_title,
                               page_title=page_title, 
                               form=form)

@pages.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')

    next_page = request.form.get('next') or request.args.get('next') 
    if next_page and is_safe_redirect_url(next_page):
        return redirect(next_page)
    return redirect(url_for('pages.index'))

@pages.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    head_title = 'Sign Up'
    page_title = 'Journal Sign Up'

    # Reroute to index if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        print(f'Entered password: {form.password.data}')

        user.set_password(form.password.data)

        # Debug print to check the hashed password
        print(f'Hashed password: {user.password}')

        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} successfully signed up' , 'success')
        return redirect(url_for('pages.login'))



    return render_template('signup.html', 
                               head_title=head_title,
                               page_title=page_title, 
                               form=form)