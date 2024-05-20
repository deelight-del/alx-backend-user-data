#!/usr/bin/env python3
"""Implementation of the Basic Authenticaion
class
"""


from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii


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
        except binascii.Error:
            return None
