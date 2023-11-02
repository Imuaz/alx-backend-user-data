#!/usr/bin/env python3
'''
Personal data Module
'''
import re


def filter_datum(fields: str, redaction: str, message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    re_pattern: str = f'({separator.join(fields)})=[^\\{separator}]*'
    return re.sub(re_pattern, f'\\1={redaction}', message)
