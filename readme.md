# Flask Journal

## Description

This is a micro-blog/journal application loosely based on the 2024 version of the Flask Mega Tutorial series by Miguel Grinberg and several other tutorials. You can view a stripped down version of this application on PythonAnywhere.

I have modified the application structure to suit my preferences, but still avoid circular imports. As I am still learning about Flask, I plan to use the app as a journal of sorts for short posts on Flask topics I find useful. I will also try to address some of the issues I encountered when deploying to PythonAnywhere. While these are mostly for my reference, it is my hope that others will also find them along with the application code of some use.

View a streamlined version of this Flask application on 
<a href="https://mayajournal.pythonanywhere.com/" target="_blank">PythonAnywhere</a>.



## Resources

### Tutorial

- [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) series
- [GitHub](https://github.com/miguelgrinberg/microblog)

### Package Documentation

- [Flask-Babel](https://python-babel.github.io/flask-babel/)
- [Bleach](https://bleach.readthedocs.io/en/latest/)
- [Dotenv](https://pypi.org/project/python-dotenv/) 
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) 
- [Flask Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-Mail 0.10.0](https://flask-mail.readthedocs.io/en/latest/)
- [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Moment](https://flask-moment.readthedocs.io/en/latest/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)
- [Flask with SendGrid](https://sendgrid.com/en-us/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid)
- [logging](https://docs.python.org/3/library/logging.html)
- [MarkupSafe](https://markupsafe.palletsprojects.com/en/stable/)
- [unittest](https://docs.python.org/3/library/unittest.html)
- [WTForms](https://wtforms.readthedocs.io/en/3.2.x/) 

### Database Documentation

- [MySQL](https://dev.mysql.com/doc/) For PythonAnywhere
- [SQLite3](https://www.sqlite.org/docs.html) For development

### Deployment

- [PythonAnywhere](https://help.pythonanywhere.com/pages/)

### Tools and Services

- [.gitignore Generator](https://toptal.com/developers/gitignore)
- [GitHub](https://github.com/)
- [GitHub Docs](https://docs.github.com/en)
- [Gravatar](https://docs.gravatar.com/)
- [SendGrid](https://sendgrid.com/en-us)
- [WWW SQL Designer](https://sql.toad.cz/?) Application
- [WWW SQL Designer](https://github.com/ondras/wwwsqldesigner/wiki/Manual) Documentation

## Changes from Flask Mega Tutorial

- Define extensions like SQLAlchemy, Flash-Login, and Flask-Migrate in extensions.py
- Used standard CSS rather than Bootstrap
- Add Script to dismiss flash notification after 30 seconds in main.js
- Add Script to show/hide login password in login.js
- Define post column in Post class to support larger text content (more journal like)
- Used a somewhat different code for errors.py to support common error.html file
- Used modified code from SendGrid for logging and password reset emails
- Changed index route to not require login, shows all journal entries in descending order
- Changed User profile page shows both user and following entries in descending order
- Moved the Add Journal Entry link to the User profile page
- Used Bleach and Markupsafe modules to securely allow formatting of post body content
- Used Babel to translation to German rather than Spanish
- Used googletrans as no credit card is required, Display entire translated post on separate page
- Used SQLAlchemy for navbar search form that searches the entry titles
- Added author mini-profiles (no journal entries) that are not restricted by login requirement
- Updated the author profile to be a modal popup (original route and pages were retained)
- Added an About page
