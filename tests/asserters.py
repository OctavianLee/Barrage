#! /usr/bin/env python
# -*- coding: utf-8 -*-

def eq_obj(left, right, msg=None):
    """Assert the value of the left object is equal to the right.

    :param: left: the left element in the assert.
    :param: right: the right element in the assert.
    :param: msg: the message of assert.

    :except: AssertionError.
    """

    assert left.__dict__ == right.__dict__, msg

