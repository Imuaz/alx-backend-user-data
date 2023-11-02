#!/usr/bin/env python3
'''
Personal data Module
'''
import os
import re
from logging import StreamHandler
from typing import List
import logging
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    '''returns the log message obfuscated'''
    re_pattern = f'({"|".join(fields)})=[^\\{separator}]*'
    return re.sub(re_pattern, f'\\1={redaction}', message)


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


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector:
    '''connects to the secure database'''
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection
