"""
Program: Routes
Author: Maya Name
Creation Date: 12/30/2024
Revision Date: 02/03/2025
Description: Routes file for Flask microblog application

Revisions:
02/03/2025 Update text to support German translation

"""

import asyncio
import bleach
import sqlalchemy as sa
from datetime import datetime, timezone
from flask import Blueprint, current_app, flash, g, render_template, redirect, request, url_for
from flask_babel import _, get_locale
from flask_login import current_user, login_required, login_user, logout_user
from langdetect import detect, LangDetectException
from markupsafe import Markup
from sqlalchemy import desc
from urllib.parse import urlparse, urljoin
from app.config import Config
from app.forms import (LoginForm, SignupForm, EditProfileForm,
                       FollowForm, PostForm, ResetPasswordRequestForm,
                       ResetPasswordForm, SearchForm
                       )
from app.email import send_password_reset_email
from app.extensions import db
from app.models import User, Post
from app.trans import translate_text

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
    # Set local formatting for date/time
    g.locale = str(get_locale())

# Application routes

@pages.route('/', methods=['GET', 'POST'])
@pages.route('/index/', methods=['GET', 'POST'])
def index():
    head_title = _('Home')
    page_title = _('Journal Posts')
    page = request.args.get('page', 1, type=int)

    # posts = db.session.scalars(db.select(Post).order_by(desc(Post.timestamp))).all()
    posts = db.paginate(db.select(Post).order_by(desc(Post.timestamp)),
                        page=page,
                        per_page = current_app.config['POSTS_PER_PAGE'],
                        # per_page=Config.POSTS_PER_PAGE,
                        error_out=False
                        )

    # Mark the sanitized HTML as safe
    for post in posts:
        post.body = Markup(post.body)


    return render_template('index.html',
                           head_title=head_title,
                           page_title=page_title,
                           posts=posts.items, 
                           pagination=posts,
                           )

@pages.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    head_title = _('Login')
    page_title = _('Journal Login')

    # Reroute to index if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid login. Check your username and password.'), 
                    'error')
            return redirect(url_for('pages.login'))
        login_user(user, remember=form.remember_me.data)
        # flash(f'{form.username.data} successfully logged in', 'success')
        flash(_('%(username)s successfully logged in' , username=form.username.data), 'success')

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
    flash(_('Logged out successfully!'), 'success')

    next_page = request.form.get('next') or request.args.get('next') 
    if next_page and is_safe_redirect_url(next_page):
        return redirect(next_page)
    return redirect(url_for('pages.index'))

@pages.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    head_title = _('Sign Up')
    page_title = _('Journal Sign Up')

    # Reroute to index if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        # flash(f'{form.username.data} successfully signed up' , 'success')
        flash(_('%(username)s successfully signed up' , username=form.username.data), 'success')

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
    head_title = _('User Profile')
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

    # Set for follower/following form buttons
    form = FollowForm()

    return render_template('user.html', 
                           head_title=head_title,
                           user=user, 
                           posts=posts.items, 
                           pagination=posts,
                           form=form)

@pages.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    head_title = _('Edit Profile')
    page_title = _('Edit Profile')
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
    head_title = _('Add Entry')
    page_title = _('Add Journal Entry')

    # Allowed elements for sanitized the entry input
    ALLOWED_TAGS = ['p', 'br', 'code', 'strong', 'em', 'ul', 'ol', 'li']
    ALLOWED_ATTRIBUTES = {}
    
    form = PostForm()
    if form.validate_on_submit():
        # Try to determine language of post
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''

        # Only allow safe text to be added to database
        sanitized_body = bleach.clean(form.post.data, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        
        post = Post(
            title=form.title.data,           
            body=sanitized_body, 
            author=current_user,
            language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Journal entry successfully added'), 'success')
        return redirect(url_for('pages.index'))
    
    return render_template('add_entry.html',
                           head_title=head_title,
                           page_title=page_title,
                           form=form
                           )

@pages.route('/reset_password_request/', methods=['GET', 'POST'])
# @login_required
def reset_password_request():
    head_title = _('Password Reset')
    page_title = _('Reset Password Request')
    form = ResetPasswordRequestForm()

    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'), 'success')
        return redirect(url_for('pages.login'))
    

    return render_template('reset_password_request.html',
                           head_title=head_title,
                           page_title=page_title,
                           form=form
                           )

@pages.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('pages.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'), 'success')
        return redirect(url_for('pages.login'))
    return render_template('reset_password.html', form=form)

@pages.route('/trans_text/<int:post_id>', methods=['GET', 'POST'])
# @login_required
def trans_text(post_id):
    head_title = _('Translate')
    page_title = _('Translated Journal Entry')

    post = db.session.scalars(db.select(Post).where(Post.id==post_id)).first()

    src_lang = post.language
    dest_lang = g.locale
    trans_title = post.title
    trans_body = post.body

    # Get the existing event loop or create a new one if none exists
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run both translations concurrently
    translated_title, translated_body = loop.run_until_complete(
        asyncio.gather(
            translate_text(text=trans_title, src=src_lang, dest=dest_lang),
            translate_text(text=trans_body, src=src_lang, dest=dest_lang)
        )
    )


    return render_template('trans_text.html', 
                           head_title=head_title,
                           page_title=page_title,
                           post=post,
                           translated_title=translated_title,
                           translated_body=translated_body
                           )

@pages.route('/search/', methods=['GET', 'POST'])
def search():
    head_title = _('Search Results')
    page_title = _('Search Results')
    page = request.args.get('page', 1, type=int)

    form = SearchForm()

    if form.validate_on_submit():
        searched = form.searched.data
        
        posts = db.paginate(db.select(Post).filter(Post.title.contains(searched)).order_by(desc(Post.timestamp)),
                    page=page,
                    per_page=Config.POSTS_PER_PAGE,
                    error_out=False
                    )

        # Mark the sanitized HTML as safe
        for post in posts:
            post.body = Markup(post.body)

        return render_template('search.html', 
                               head_title=head_title,
                               page_title=page_title,
                               form=form,
                               searched=searched,
                               posts=posts.items, 
                               pagination=posts)
    
    return render_template('search.html', form=form)

@pages.route('/profile/<username>')
def profile(username):
    head_title = _('Author Profile')
    page_title = _('Author Profile')

    user = db.first_or_404(sa.select(User).where(User.username == username))

    return render_template('_profile.html', 
                           head_title=head_title,
                           page_title=page_title,
                           user=user, 
)

@pages.route('/profile_popup/<username>')
def profile_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('_profile_content.html', user=user)

@pages.route('/about/')
def about():
    head_title = 'About Site'
    page_title = 'About this Site'

    return render_template('about.html',
                           head_title=head_title,
                           page_title=page_title
                           )