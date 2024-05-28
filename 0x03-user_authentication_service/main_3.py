#!/usr/bin/env python3
"""
    Main file
    """
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
    print("The new password is", user.hashed_password)
except ValueError:
    print("Error")
try:
    my_db.update_user("inalid", invalid='invalid')
    print("Inavlid updated")
    print("The new invalid is", user.invalid)
except ValueError:
    print("Error")