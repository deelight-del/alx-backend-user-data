#!/usr/bin/env python3
"""Implementation of the Basic Authenticaion
class
"""


from api.v1.auth.auth import Auth


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
