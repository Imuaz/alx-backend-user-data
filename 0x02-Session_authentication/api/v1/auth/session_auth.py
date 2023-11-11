#!/usr/bin/env python3
"""
SessionAuth Module
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session Authorization class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""

        # Gets session ID from the session cookie
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        return user
