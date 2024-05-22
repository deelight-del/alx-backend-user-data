#!/usr/bin/env python3
"""Class implementation of the Session Authentication"""


import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """The implementation of the SessionAuth
    class that inherits from the base Auth class"""
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """Method to create a session_id from a given user_id
        """
        if (user_id is None
           or not isinstance(user_id, str)):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        # print("dictionary here, when creating session",
        #     self.__class__.user_id_by_session_id)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method to obtain the given user_id for a given session id.
        """
        if (session_id is None
           or not isinstance(session_id, str)):
            return None
        # print("dictionary here", self.__class__.user_id_by_session_id)
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Instance method of SessionAuth to return a given
        user, based on their ID.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        print("user_id from session_auth.py is", user_id)
        if user_id:
            return User.get(user_id)
        return None
