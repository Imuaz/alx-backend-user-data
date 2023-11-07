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
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Make paths slash-tolerant by checking without trailing slashes
        path_without_trailing_slash = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                # Remove trailing slash from excluded paths for comparison
                excluded_path = excluded_path.rstrip('/')
                if path_without_trailing_slash == excluded_path:
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
