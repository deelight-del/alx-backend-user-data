#!/usr/bin/env python3
"""Authentication Base Class"""


from flask import request
from typing import (List, TypeVar)


class Auth:
    """The base Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method that checks if a given path require Authentication
        """
        if path is None or not excluded_paths:
            return True
        if path.endswith("/"):
            if path in excluded_paths:
                return False
        else:
            if (path + "/") in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """pulic method that checks the request header for the authorization
        field
        """
        if request is None:
            return None
        return request.authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """The method to retrieve the user info at a given session
        """
        return None
