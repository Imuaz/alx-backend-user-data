#!/usr/bin/env python3
'''
Personal data Module
'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    '''returns the log message obfuscated'''
    re_pattern = f'({"|".join(fields)})=[^\\{separator}]*'
    return re.sub(re_pattern, f'\\1={redaction}', message)
