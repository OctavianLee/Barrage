# -*- coding: utf-8 -*-

import getpass
import json
import requests
import cookielib
import urllib2

from datetime import datetime

from danmaku.configs.global_settings import (
    LOGIN_URL, LOGIN_HEADER, LOGIN_DATA,
    SEND_URL
)
from danmaku.configs.personal_settings import SEND_FORMAT

requests.packages.urllib3.disable_warnings()

class SenderService(object):

    """提供弹幕发送服务。
    """

    def __init__(self, room_id):
        """初始化服务。
        :params: room_id: 直播间号。
        """
        self.session = requests.Session()
        # 设置cookie
        self.cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(
            cookie_handler, urllib2.HTTPHandler)
        self.send_danmaku(room_id)

    def send_danmaku(self, room_id):
        """发送弹幕。
        :params: room_id: 直播间号。
        """
        self.do_login()
        self.danmaku_sender(room_id)

    def do_login(self):
        # 载入登陆设置
        self._pre_login()
        # 获取 登陆必要参数
        while 1:
            user_id = raw_input('请输入你的用户名：')
            password = getpass.getpass('请输入你的密码：')
            # 进行登录
            if not self._login(user_id, password):
                continue

    def _pre_login(self):
        """进行登录前信息配置信息。"""
        # 将页面信息加入头部
        req = urllib2.Request(LOGIN_URL)
        resp = self.opener.open(req)
        self.login_header = LOGIN_HEADER
        for i in self.cookie:
            self.login_header['Cookie'] = i.name + '=' + i.value

    def _login(self, user_id, password):
        """登陆操作。

        :params: user_id: 用户账户或邮箱。
        :params: password: 密码。
        """
        data = LOGIN_DATA
        data['userid'] = user_id
        data['pwd'] = password
        response = self.session.post(
            'https://account.bilibili.com/ajax/miniLogin/login',
            data=data,
            headers=self.login_header
        )
        if not response.json()['status']:
            print "输入的用户名或密码有误！"
            return False
        # response.raise_for_status()
        self.cookie = response.cookies
        return True

    def danmaku_sender(self, room_id):
        """不断发送弹幕。
        :params: room_id: 直播间号。
        """
        print "准备开启弹幕发射！"
        while True:
            try:
                danmaku = raw_input('输入发送的弹幕(Exit 退出)：')
                if danmaku.lower() == "exit":
                    break
            except KeyboardInterrupt:
                break
            except:
                continue
            self.send_a_danmaku(room_id, danmaku)

    def send_a_danmaku(self, room_id, danmaku):
        """发送一条弹幕。
        :params: room_id: 直播间号。
        :params: danmaku: 弹幕信息。
        """

        data = SEND_FORMAT
        data["msg"] = danmaku
        data["roomid"] = room_id
        json_data = json.dumps(data)
        response = self.session.post(
            SEND_URL,
            data=data,
            cookies=self.cookie
        )
        response.raise_for_status()
        if response.json().get('code') == 0:
            print "弹幕已发出"
        else:
            print response.json().get('msg')
        return True
