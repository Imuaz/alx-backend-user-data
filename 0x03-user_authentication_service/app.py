#!/usr/bin/env python3
"""
App module
"""
from auth import Auth
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Returns end-point to register a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Log in an authenticated user and create a session"""
    email = request.form.get("email")
    password = request.form.get("email")

    if not AUTH.valid_login(email, password):
        abort(401)

    new_session_id = AUTH.create_session(email)
    payload = jsonify({"email": f"{email}", "message": "logged in"})
    payload.set_cookie("session_id", new_session_id)

    return payload


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
