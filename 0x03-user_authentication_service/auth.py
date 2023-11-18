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


def _hash_password(password: str) -> bytes:
    """Returns bytes as asalted hash of the input password, hashed"""
    salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_psswd


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string."""
    new_uuid = str(uuid.uuid4())
    return new_uuid
