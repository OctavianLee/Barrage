# -*- coding: utf-8 -*-

"""
The gobal data of danamku hime.
"""

# RECIEVER PART

RECIEVE_SERVER_ADDRESS = "livecmt-1.bilibili.com"
RECIEVE_SERVER_PORT = 88
RECIEVE_INIT_DATA = '0101000c0000%04x00000000'

HEARTBEAT_STR = '01020004'
HEARTBEAT_KEEP_TIME = 30


# LOGIN PART

LOGIN_URL = 'https://account.bilibili.com/ajax/miniLogin/minilogin'
LOGIN_HEADER = {
    'Host': 'account.bilibili.com',
            'Referer': 'https://account.bilibili.com/ajax/miniLogin/minilogin',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://account.bilibili.com'
}
LOGIN_DATA = {
    'keep': 0,
    'captcha': ''
}


# LOGIN PART

SEND_URL = 'http://live.bilibili.com/msg/send'
