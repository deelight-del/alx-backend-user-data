#!/usr/bin/env python3
"""Class implementation of SessionExpAuth
that inherits from SessionAuth"""


from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """The SessionExpAuth class blueprint.
    """
    def __init__(self):
        """Overloading the init method.
        """
        session_duration = os.getenv("SESSION_DURATION")
        if (session_duration is None
           or not session_duration.isdigit()):
            self.session_duration = 0
        else:
            self.session_duration = int(session_duration)

    def create_session(self, user_id=None):
        """Overloading create_session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overloading user_id_for_session_id
        """
        if (session_id is None
           or self.user_id_by_session_id.get(session_id) is None):
            return None
        session_d = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_d.get("user_id")
        if ("created_at" not in session_d.keys()
           or session_d.get("created_at") +
                timedelta(seconds=self.session_duration) < datetime.now()):
            return None
        return session_d.get("user_id")
