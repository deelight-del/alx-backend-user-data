#!/usr/bin/env python3
"""Hashing password module with the bcrypt tool"""


import bcrypt
import typing


def hash_password(password: str) -> bytes:
    """Function to return a salted, hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function to check if hashed_password and password are same"""
    return bcrypt.checkpw(password.encode(), hashed_password)
