# -*- coding: utf-8 -*-

# RECIEVER PART

RECIEVE_SERVER_ADDRESS = "livecmt.bilibili.com"
RECIEVE_SERVER_PORT = 88
RECIEVE_INIT_DATA = '0101000c0000%04x00000000'


# LOGIN PART

LOGIN_URL = 'https://account.bilibili.com/login'
LOGIN_HEADER = {
    'Host': 'account.bilibili.com',
            'Referer': 'https://account.bilibili.com/login',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://account.bilibili.com'
}
LOGIN_DATA = {
    'act': 'login',
    'gourl': 'https://account.bilibili.com/login/dologin',
    'keeptime': 864000,
}

VDCODE_URL = 'https://account.bilibili.com/captcha'


# LOGIN PART

SEND_URL = 'http://live.bilibili.com/msg/send'
