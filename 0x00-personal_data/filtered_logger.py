#!/usr/bin/env python3
"""Module that will obfusticate a given string"""


import typing
import re


def filter_datum(fields: typing.List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """Function to implement obfustication based"""
    if fields:
        pattern = r"(" + "|".join(fields) + r")" + r"(=.*?)" + seperator
        return re.sub(pattern, r"\1=" + redaction + seperator, message)
