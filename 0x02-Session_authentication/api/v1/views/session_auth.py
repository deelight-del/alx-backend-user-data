#!/usr/bin/env python3
"""view for login authentication.
"""


import os
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def login():
    """Method to route to auth_session login"""
    from api.v1.app import auth

    email = request.form.get("email")
    pwd = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pwd is None:
        return jsonify({"error": "password missing"}), 400
    user_object_list = User.search({"email": email})
    if not user_object_list:
        return jsonify({"error": "no user found for this email"}), 404
    user_object = user_object_list[0]
    if not user_object.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user_object.id)
    cookie_name = os.getenv("SESSION_NAME")
    resp = jsonify(user_object.to_json())
    resp.set_cookie(cookie_name, session_id)
    return resp
