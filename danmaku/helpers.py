# -*- coding: utf-8 -*-
from gevent import socket
from binascii import unhexlify, hexlify


def convert_hexascii_to_int(string):
    if isinstance(string, str):
        return int(hexlify(string), 16)
    else:
        return None

def recieve_sock_data(sock, length):
    try:
        return sock.recv(length)
    except socket.error:
        return None
