#!/usr/bin/env python3
"""
Basic auth module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode, binascii


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


def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # nopep8
    """
    Decode a Base64 Authorization header and return as a UTF-8 string.
    """
    if not base64_authorization_header:
        return None
    if type(base64_authorization_header) is not str:
        return None
    try:
        decoded_string = base64.b64decode(base64_authorization_header)
        return decoded_string.decode('utf-8')
    except Exception:
        return None
