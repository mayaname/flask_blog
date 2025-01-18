# Flask Journal

## Description

This is a micro-blog/journal application loosely based the Flask Mega Tutorial series by Miguel Grinberg and several other tutorials. I have modified the application structure to suit my preferences, but still avoid circular import. As I am still learning about Flask, I plan to use the app as a journal of sorts for short posts on Flask topics I find useful. I will also try to address some of the issues I encountered when deploying to PythonAnywhere. While these are mostly for my reference, it is my hope that others will also find them along with the application code of some use.

## Resources

### Tutorial

- [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) series

- [GitHub](https://github.com/miguelgrinberg/microblog)

### Package Documentation

- [Flask](https://flask.palletsprojects.com/en/3.0.x/) 

- [Dotenv](https://pypi.org/project/python-dotenv/) 

- [WTForms](https://wtforms.readthedocs.io/en/3.2.x/) 

- [Flask Login](https://flask-login.readthedocs.io/en/latest/)

- [Flask-Mail 0.10.0](https://flask-mail.readthedocs.io/en/latest/)

- [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/)

- [Flask SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)

- [logging](https://docs.python.org/3/library/logging.html)

- [Flask with SendGrid](https://sendgrid.com/en-us/blog/sending-emails-from-python-flask-applications-with-twilio-sendgrid)

### Database Documentation

- [SQLite3](https://www.sqlite.org/docs.html) For development
- [MySQL](https://dev.mysql.com/doc/) For PythonAnywhere

### Deployment

- [PythonAnywhere](https://help.pythonanywhere.com/pages/)

### Tools and Services

- [.gitignore Generator](https://toptal.com/developers/gitignore)

- [WWW SQL Designer](https://sql.toad.cz/?) Application

- [WWW SQL Designer](https://github.com/ondras/wwwsqldesigner/wiki/Manual) Documentation

- [Gravatar](https://docs.gravatar.com/)

- [SendGrid](https://sendgrid.com/en-us)


## Changes from Flask Mega Tutorial

- Define extensions like SQLAlchemy, Flash-Login, and Flask-Migrate in extensions.py
- Script to dismiss flash notification after 30 seconds in main.js
- Script to show/hide login password in login.js
- Define post column in Post class to support larger text content (more journal like)
- Used a somewhat different code for errors.py to support common error.html file
- Used modified code from SendGrid for logging emails

