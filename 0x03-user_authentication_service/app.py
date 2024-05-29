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
def logout():
    """Logout method"""
    session_id = request.cookies.get("session_id")
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj:
        AUTH.destroy_session(int(user_obj.id))
        return redirect(url_for("login"))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
