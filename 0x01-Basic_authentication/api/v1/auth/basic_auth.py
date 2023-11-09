#!/usr/bin/env python3
"""
Basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):  # nopep8
            return None

        try:
            # Attempt to decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            # Invalid Base64 or decoding error
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # nopep8
        """Extract user email and password from a decoded Base64 header."""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):  # nopep8
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(':', 1)  # nopep8
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # nopep8
        """Retrieve the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})

        if not users:
            return None  # No user with the provided email found

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None  # Password does not match
