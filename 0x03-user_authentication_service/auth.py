#!/usr/bin/env python3
"""
Authentication Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns bytes as asalted hash of the input password, hashed"""
    salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_psswd
