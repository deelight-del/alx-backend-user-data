#!/usr/bin/env python3
"""Module that will obfusticate a given string"""


from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """Function to implement obfustication based"""
    if len(fields) > 0:
        pattern = r"(" + "|".join(fields) + r")" + r"(=.*?)" + seperator
        return re.sub(pattern, r"\1=" + redaction + seperator, message)
    return message
