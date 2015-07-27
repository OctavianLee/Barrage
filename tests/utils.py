# -*- coding: utf-8 -*-
import string
import random


def constant(func):
    def fset(self, value):
        raise SyntaxError

    def fget(self):
        return func()
    return property(fget, fset)


def get_random_str(num):
    elements = string.letters + string.digits
    result = random.sample(elements, num)
    if result[0].isdigit():
        result = result[1:]
    return ''.join(result)


def get_random_int():
    return random.randint(0, 999999)
