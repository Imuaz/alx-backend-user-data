#!/usr/bin/env python3
'''
Personal data Module
'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    '''returns the log message obfuscated'''
    for field in fields:
        regex_pattern = f'{field}=(.*?){separator}'
        message = re.sub(regex_pattern, f'{field}={redaction}{separator}', message)
    return message
