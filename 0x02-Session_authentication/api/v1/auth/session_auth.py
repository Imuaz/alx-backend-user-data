#!/usr/bin/env python3
"""
SessionAuth Module
"""
from models.user import User
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

        session_id = self.session_cookie(request)

        try:
            # Get the User ID based on the session ID
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                # Retrieve a User instance from the db based on the User ID
                return User.get(user_id)
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        # If Session ID is not present, return False
        if not session_cookie:
            return False

        # Get the User ID associated with the Session ID
        user_id = self.user_id_for_session_id(session_cookie)

        # If no User ID is linked, return False
        if not user_id:
            return False

        # Delete the Session ID from user_id_by_session_id
        del self.user_id_by_session_id[session_cookie]
        return True
