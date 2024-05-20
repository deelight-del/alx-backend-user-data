#!/usr/bin/env python3
""" Main 1
    """
from api.v1.auth.auth import Auth

a = Auth()

print("Expect True", a.require_auth(None, None))
print("Expect True", a.require_auth("abc", None))
print("Expect True", a.require_auth("abc", []))
print("Expect True", a.require_auth(None, []))
print("Expect True", a.require_auth("/api/v1/status/", []))
print("Expect False", a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print("Expect False", a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print("Expect True", a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print("Expect True", a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))
