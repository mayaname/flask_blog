# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

print(f"Key {os.environ.get('SENDGRID_API_KEY')}")
print(f"From {os.environ.get('MAIL_FROM')}")
print(f"To {os.environ.get('MAIL_TO')}")

message = Mail(
    from_email=os.environ.get('MAIL_FROM'),
    to_emails=os.environ.get('MAIL_TO'),
    subject='This is another test email',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)