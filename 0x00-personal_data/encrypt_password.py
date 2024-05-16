#!/usr/bin/env python3
"""Hashing password module with the bcrypt tool"""


import bcrypt


def hash_password(password: str) -> str:
    """Function to return a salted, hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
