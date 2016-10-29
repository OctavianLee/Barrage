# -*- coding: utf-8 -*-

"""
The gobal data of danamku hime.
"""

# RECIEVER PART
HEARTBEAT_STR = '01020004'
HEARTBEAT_KEEP_TIME = 20


# LOGIN PART

LOGIN_URL = 'https://passport.bilibili.com/ajax/miniLogin/minilogin'
LOGIN_HEADER = {
    'Host': 'passport.bilibili.com',
            'Referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://passport.bilibili.com'
}
LOGIN_DATA = {
    'keep': 0,
    'captcha': ''
}


# LOGIN PART

SEND_URL = 'http://live.bilibili.com/msg/send'
