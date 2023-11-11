#!/usr/bin/env python3
"""
Session Auth view Module
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ Returns dictionary representation of user if found"""
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email and passwor is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    users = User.search({"email": email})

    # If no User found, return error
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assuming there's only one user with a given email

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # Create a Session ID for the User ID
    session_id = auth.create_session(user.id)

    # Return the dictionary representation of the User
    user_json = jsonify(user.to_json())

    # Set the cookie to the response
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    response = make_response(user_json)
    response.set_cookie(session_name, session_id)

    return response
