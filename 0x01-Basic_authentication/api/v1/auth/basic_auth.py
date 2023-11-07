#!/usr/bin/env python3
"""
Basic auth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # nopep8
        """
        Extract the Base64 part of the Authorization header for
        Basic Authentication.
        """
        if authorization_header is None or not isinstance(authorization_header, str):  # nopep8
            return None

        if not authorization_header.startswith('Basic '):
            return None

        # Extract the value after 'Basic ' (after the space)
        base64_part = authorization_header.split(' ')[1]

        return base64_part
