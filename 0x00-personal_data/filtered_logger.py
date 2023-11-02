#!/usr/bin/env python3
'''
Personal data Module
'''
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''redact message of LogRecord instances'''
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)  # nopep8


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    '''returns the log message obfuscated'''
    re_pattern = f'({"|".join(fields)})=[^\\{separator}]*'
    return re.sub(re_pattern, f'\\1={redaction}', message)
