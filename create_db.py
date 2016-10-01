import re
import sys
from getpass import getpass

from app import current_app
from app.models import db

from app.helpers.data import DataManager
from populate_db import populate


def _validate_email(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print('\nInvalid email address')
        sys.exit(1)


def _validate_password(password):
    if len(password) < 4:
        print('\nPassword should have minimum 4 characters')
        sys.exit(1)


def create_default_user():
    print("Your login is 'super_admin'.")
    email = input("Enter email for super_admin    : ")
    _validate_email(email)
    password = getpass("Enter password for super_admin : ")
    _validate_password(password)
    DataManager.create_super_admin(email, password)


if __name__ == "__main__":
    with current_app.app_context():
        db.create_all()
        create_default_user()
        populate()
