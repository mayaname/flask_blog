"""
Program: App
Author: Maya Name
Creation Date: 08/29/2024
Revision Date: 12/29/2024
Description: File that launches the microblog application

Revisions:
12/29/2024 Update to work w/ app factory
"""


from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)