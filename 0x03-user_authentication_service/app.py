#!/usr/bin/env python3
"""The app.py module"""


from flask import (Flask, jsonify, request,
                   abort, redirect, url_for)

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def default() -> str:
    """Method to go to the default route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Method to post to the users route."""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Login Method"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Logout method"""
    session_id = request.cookies.get("session_id")
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj:
        AUTH.destroy_session(int(user_obj.id))
        return redirect(url_for("login"))
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """The profile method"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user_obj = AUTH.get_user_from_session_id(session_id)
        if user_obj:
            return jsonify({"email": user_obj.email}), 200
        abort(403)
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """Route method to get a reset token."""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """Route method to reset passowrd."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password Updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
