#!/usr/bin/env python3
"""Main method to test for our
application.
"""

import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Function to test the user registeration
    enpoint."""
    resp = requests.post("http://127.0.0.1:5000/users",
                         {
                            "email": email, "password": password
                         })
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}
    resp = requests.post("http://localhost:5000/users",
                         {
                            "email": email, "password": password})
    assert resp.json() == {"message": "email already registered"}
    assert resp.status_code == 400


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
