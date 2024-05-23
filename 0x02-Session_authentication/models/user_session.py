#!/usr/bin/env python3
"""User SEssion Class for persisting a
Users session"""


from models.base import Base


class UserSession(Base):
    """Class blueprint for the UserSession Class"""
    def __init__(self, *args: list, **kwargs: dict):
        """The init method.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
