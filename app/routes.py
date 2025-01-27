"""
Program: Routes
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 
Description: Routes file for Flask microblog application

Revisions:

"""

import bleach
import sqlalchemy as sa
from datetime import datetime, timezone
from flask import Blueprint, flash, render_template, redirect,  request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from markupsafe import Markup
from sqlalchemy import desc
from urllib.parse import urlparse, urljoin
from app.config import Config
from app.forms import LoginForm, SignupForm, EditProfileForm, FollowForm, PostForm
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

@pages.before_request
def before_request():
    # Set date/time of last page view
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# Application routes

@pages.route('/', methods=['GET', 'POST'])
@pages.route('/index/', methods=['GET', 'POST'])
def index():
    head_title = 'Home'
    page_title = 'Journal Posts'
    page = request.args.get('page', 1, type=int)

    # posts = db.session.scalars(db.select(Post).order_by(desc(Post.timestamp))).all()
    posts = db.paginate(db.select(Post).order_by(desc(Post.timestamp)),
                        page=page,
                        per_page=Config.POSTS_PER_PAGE,
                        error_out=False
                        )

    # Mark the sanitized HTML as safe
    for post in posts:
        post.body = Markup(post.body)

    # Navigate posts list
    next_url = url_for('pages.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('pages.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html',
                           head_title=head_title,
                           page_title=page_title,
                           posts=posts.items, 
                           next_url=next_url,
                           prev_url=prev_url
                           )

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
        flash(f'{form.username.data} successfully logged in', 'success')

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
        
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} successfully signed up' , 'success')

        # Check the 'next' parameter for safe redirection
        next_page = request.form.get('next') or request.args.get('next') 

        if next_page and is_safe_redirect_url(next_page):
            # Redirect safely
            return redirect(next_page)
        # Fallback to a default page
        return redirect(url_for('pages.login'))
    

    return render_template('signup.html', 
                               head_title=head_title,
                               page_title=page_title, 
                               form=form)

@pages.route('/user/<username>')
@login_required
def user(username):
    head_title = 'User Profile'
    page = request.args.get('page', 1, type=int)

    user = db.first_or_404(sa.select(User).where(User.username == username))

    posts = db.paginate(current_user.following_posts().order_by(Post.timestamp.desc()),
                        page=page,
                        per_page=Config.POSTS_PER_PAGE,
                        error_out=False
                        )

    # Mark the sanitized HTML as safe
    for post in posts:
        post.body = Markup(post.body)

    # Navigate posts list
    next_url = url_for('pages.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('pages.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    # Set for follower/following form buttons
    form = FollowForm()

    return render_template('user.html', 
                           head_title=head_title,
                           user=user, 
                           posts=posts.items, 
                           next_url=next_url,
                           prev_url=prev_url,
                           form=form)

@pages.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    head_title = 'Edit Profile'
    page_title = 'Edit Profile'
    form = EditProfileForm()
    # Handles valid submit
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
    
        # Check the 'next' parameter for safe redirection
        next_page = request.form.get('next') or request.args.get('next') 

        if next_page and is_safe_redirect_url(next_page):
            # Redirect safely
            return redirect(next_page)
        # Fallback to a default page
        return redirect(url_for('pages.edit_profile'))

    # Handles initial form display w/ current data
    elif request.method == 'GET':
        # Populate form with current data from database
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', 
                           head_title=head_title,
                           page_title=page_title,
                           form=form)

@pages.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.', 
                    'error')
            return redirect(url_for('pages.index'))
        if user == current_user:
            flash('You cannot follow yourself!', 
                    'error')
            return redirect(url_for('pages.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!', 
                    'success')
        return redirect(url_for('pages.user', username=username))
    else:
        return redirect(url_for('pages.index'))

@pages.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.', 
                    'error')
            return redirect(url_for('pages.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!', 
                    'error')
            return redirect(url_for('pages.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.', 
                    'success')
        return redirect(url_for('pages.user', username=username))
    else:
        return redirect(url_for('pages.index'))
    
@pages.route('/add_entry/', methods=['GET', 'POST'])
@login_required
def add_entry():
    head_title = 'Add Entry'
    page_title = 'Add Journal Entry'

    # Allowed elements for sanitized the entry input
    ALLOWED_TAGS = ['p', 'br', 'code' 'strong', 'em', 'ul', 'ol', 'li']
    ALLOWED_ATTRIBUTES = {}
    
    form = PostForm()
    if form.validate_on_submit():
        sanitized_body = bleach.clean(form.post.data, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        post = Post(
            title=form.title.data,           
            body=sanitized_body, 
            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Journal entry successfully added', 'success')
        return redirect(url_for('pages.index'))
    
    return render_template('add_entry.html',
                           head_title=head_title,
                           page_title=page_title,
                           form=form
                           )