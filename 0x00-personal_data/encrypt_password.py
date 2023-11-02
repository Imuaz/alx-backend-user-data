#!/usr/bin/env python3
'''
Valid password Module
'''
import bcrypt


def hash_password(password: str) -> bytes:
    "Hash password using bcrypt"
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
