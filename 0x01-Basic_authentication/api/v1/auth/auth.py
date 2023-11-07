#!/usr/bin/env python3
"""
Auth Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def __init__(self, excluded_paths: List[str] = []):
        self.excluded_paths = excluded_paths

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        if not excluded_paths:
            return True

        if path in excluded_paths or path.rstrip('/') in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and path.startswith(excluded_path[:-1]):  # nopep8
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header from the request."""
        if request and 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('user'):
        """Get the current user (placeholder)."""
        return None
