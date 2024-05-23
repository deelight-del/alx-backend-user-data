#!/usr/bin/python3
"""The session class persistent implementation"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """The class blueprint for the SessionDBAuth"""
    def create_session(self, user_id=None):
        """Overloading create_session"""
        session_id = super().create_session(user_id)
        if session_id:
            session_object = UserSession(**{"user_id": user_id,
                                            "session_id": session_id})
            session_object.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overloading user_id_for_session_id"""
        session_object_list = UserSession.search({"session_id": session_id})
        if len(session_object_list) > 0:
            self.user_session_object = session_object_list[0]
            return self.user_session_object.user_id
        return None

    def destroy_session(self, request=None):
        """Method to destroy an object"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if user_id_for_session_id(session_id):
            self.user_session_object.remove()
            return True
        return False
