#!/usr/bin/env python3
"""Module that will obfusticate a given string"""


import typing
import re


def filter_datum(fields: typing.Sequence,
                 redaction: str,
                 message: str,
                 seperator: str):
    """Function to implement obfustication based
    on the redaction and field string
    """
    obfusticated_message = message
    for field in fields:
        obfusticated_message = re.sub(
            field + r'=.*?' + seperator,
            field + r'=' + redaction + seperator,
            obfusticated_message
        )
    return obfusticated_message
