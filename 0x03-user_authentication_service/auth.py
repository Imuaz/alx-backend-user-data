#!/usr/bin/env python3
"""
Authentication Module
"""
import uuid
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user, saves to the db, and returns User object."""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Log a valid user"""
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates user session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        # Generate a new UUID for the session
        user.session_id = _generate_uuid()

        # Update the user's session_id in the database
        self._db.update_user(user.id, session_id=user.session_id)
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Takes a session_id and returns the corresponding user
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None"""
        user = self._db.update_user(user_id, session_id=None)
        return user

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)


def _hash_password(password: str) -> bytes:
    """Returns bytes as asalted hash of the input password, hashed"""
    salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_psswd


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string."""
    new_uuid = str(uuid.uuid4())
    return new_uuid
