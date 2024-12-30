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

pages = Blueprint('pages', __name__)

@pages.route('/')
@pages.route('/index')
def index():
    head_title = 'Home'
    page_title = 'Blog Posts'
    user = {'username': 'Maya'}

    posts = [
        {
            'title': 'Seasons Greetings',
            'author': {'username': 'John'},
            'body': 'Merry Christmas everyone!',
            'posted': '12/25/2024'

        },
        {
            'title': 'Seasons Greetings',
            'author': {'username': 'Susan'},
            'body': 'A merry Christmas to you too!',
            'posted': '12/25/2024'
        },
        {
            'title': 'Seasons Greetings',
            'author': {'username': 'Maya'},
            'body': 'And a happy Ney Year!',
            'posted': '12/25/2024'
        },
        {
            'title': 'Seasons Greetings',
            'author': {'username': 'Bob'},
            'body': 'Happy holidays',
            'posted': '12/26/2024'
        }
    ]
    return render_template('index.html',
                           head_title=head_title,
                           page_title=page_title,
                           posts=posts,
                           user = user)