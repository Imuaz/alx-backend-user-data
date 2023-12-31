#!/usr/bin/env python3
"""
App module
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

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
def login():
    """Log in an authenticated user and create a session"""
    email = request.form.get("email")
    password = request.form.get("password")
    log_user = AUTH.valid_login(email, password)

    if not log_user:
        abort(401)

    session_id = AUTH.create_session(email)
    payload = jsonify({"email": f"{email}", "message": "logged in"})
    payload.set_cookie("session_id", session_id)

    return payload


@app.route("/sessions"  methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout route to destroy the session."""
    if request.method == "DELETE":
        session_cookie = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_cookie)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        else:
            abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """finds user profile"""
    session_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_cookie)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Gets the reset password token"""
    email = request.form.get("email")
    try:
        psswd_token = AUTH.get_reset_password_token(email)
        if psswd_token:
            return jsonify({"email": email, "reset_token": token}), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=None)
def update_password():
    """Udates user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
