# -*- coding: utf-8 -*-

from binascii import unhexlify, hexlify


def convert_hexascii_to_int(string):
    if isinstance(string, str):
        return int(hexlify(string), 16)
    else:
        return None
