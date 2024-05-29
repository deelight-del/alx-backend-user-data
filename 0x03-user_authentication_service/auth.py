#!/usr/bin/env python3
"""Module to auth.py functionalities"""


from typing import Union

import bcrypt
from uuid import uuid4

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Function to hash passwords with a salt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Mehod to register a given user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hased_pwd = _hash_password(password).decode()
            new_user = self._db.add_user(email, hased_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Method to verify if a given email and password is valid."""
        try:
            user_obj = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(),
                                  str(user_obj.hashed_password).encode()
                                  )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Method to create a given session ID for any login"""
        try:
            user_obj = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(int(user_obj.id), session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Method to return a user object or none based on sesion id"""
        if session_id is None:
            return None
        try:
            user_obj = self._db.find_user_by(session_id=session_id)
            return user_obj
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method to destroy the given session, and update
        the session_id to None"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Method to generate a reset password token."""
        try:
            user_obj = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user_obj.id, reset_token=new_uuid)
            return new_uuid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Method to update password field, if reset_token is valid."""
        try:
            user_obj = self._db.find_user_by(reset_token=reset_token)
            hashed_pw = _hash_password(password)
            self._db.update_user(user_obj.id,
                                 hashed_password=hashed_pw,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
