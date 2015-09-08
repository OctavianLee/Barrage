"""
The Definitions of Basic Constants.
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import string
import random
from datetime import datetime


def get_random_str(length=8):
    """Get a random string.

    :param length: the length of letters. By default 8
    :return: the random string.
    """
    elements = string.letters
    result = random.sample(elements, length)
    return ''.join(result)


def get_random_int(length=8):
    """Get a random integer.

    :param length: the max len of letters. By default 8
    :return: the random integer.
    """
    num_list = ['9'] * length
    max_num = int(''.join(num_list))
    return random.randint(0, max_num)


def get_random_date(date_format="%Y-%m-%dT%H:%M:SZ"):
    """Get a random date.

    Attetion: the range of year is 1900 to 9999.

    :param date_format: the format of date. By default %Y-%m-%dT%H:%M:SZ.
    :return: the random date.
    """
    year = random.randint(1900, 9999)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    date = datetime(year, month, day,
                    hour, minute, second).strftime(date_format)
    return date
