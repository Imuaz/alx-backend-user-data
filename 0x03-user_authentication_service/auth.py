#!/usr/bin/env python3
"""
Authentication Module
"""
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
        """Registers a new user,save to the db, and return User object"""
        try:  # checks wheather a user with the same email exists
            self._db.find_user_by(email=email)
        except NoResultFound:  # User doesn't exists
            hashed_passwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_passwd)
            return new_user

        raise ValueError(f"User {email} already exists")


def _hash_password(password: str) -> bytes:
    """Returns bytes as asalted hash of the input password, hashed"""
    salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_psswd
