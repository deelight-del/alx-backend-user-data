#!/usr/bin/env python3
"""Authentication Base Class"""


from flask import request
from typing import (List, TypeVar)
import re


class Auth:
    """The base Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method that checks if a given path require Authentication
        """
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                pattern = r"" + (excluded_path[:-1] + r".*")
            else:
                pattern = r"" + excluded_path
            if path.endswith("/"):
                if re.match(pattern, path):
                    return False
            else:
                path_with_slash = path + "/"
                if re.match(pattern, path_with_slash):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """pulic method that checks the request header for the authorization
        field
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """The method to retrieve the user info at a given session
        """
        return None
