#!/usr/bin/env python3
"""Implementation of the Basic Authenticaion
class
"""


from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authenticaion class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Method to extract the authorization header
        in base64 encoding from <authorization_header>
        """
        if (authorization_header is None
           or not isinstance(authorization_header, str)
           or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Method to decode a base64 encoding to utf-8"""
        if (base64_authorization_header is None
           or not isinstance(base64_authorization_header, str)):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Function to extract the user extract user
        credentials from the decoded string
        """
        if (decoded_base64_authorization_header is None
           or not isinstance(decoded_base64_authorization_header, str)
           or ":" not in decoded_base64_authorization_header):
            return None, None
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """The method to construct a user object from given credentials
        if the credentials are valid
        """
        if (user_email is None or
           not isinstance(user_email, str)
           or user_pwd is None
           or not isinstance(user_pwd, str)):
            return None
        User.load_from_file()
        users_with_user_email = User.search({"email": user_email})
        if not users_with_user_email:
            return None
        if not users_with_user_email[0].is_valid_password(user_pwd):
            return None
        return users_with_user_email[0]

    def current_user(self, request=None) -> TypeVar('User'):
        if not self.authorization_header(request):
            return None
        auth_header = self.authorization_header(request)
        base64_auth_header = (
            self.extract_base64_authorization_header(auth_header)
        )
        decoded_header = (
            self.decode_base64_authorization_header(base64_auth_header)
        )
        email, pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, pwd)
