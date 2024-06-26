#!/usr/bin/env python3.8
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPES = {
    "auth": Auth,
    "basic_auth": BasicAuth
}
if os.getenv("AUTH_TYPE"):
    auth_class = AUTH_TYPES.get(
        os.getenv("AUTH_TYPE")
    )
    if auth_class:
        auth = auth_class()


def before_request_handler() -> None:
    """Method to handle before any request is made"""
    if auth is None:
        return None
    excluded_list = ['/api/v1/status/',
                     '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_list):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


app.before_request(before_request_handler)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized error handler.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_handler(error) -> str:
    """Handler for the forbidden
    Error.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
