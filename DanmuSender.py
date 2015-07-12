# -*- coding: utf-8 -*-

import getpass
import json
import requests
import cookielib
import urllib2
import gevent


class DanmuSender(object):

    """在直播中发送弹幕。

    登陆后在直播中发送弹幕信息。
    """

    def __init__(self):
        self.login_headers = {
            'Host': 'account.bilibili.com',
            'Referer': 'https://account.bilibili.com/login',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://account.bilibili.com'
        }

        # 设置cookie
        self.cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(
            cookie_handler, urllib2.HTTPHandler)
        self.session = requests.Session()
        self.__login()

    def __login(self):
        """登陆操作。"""
        login_url = 'https://account.bilibili.com/login'
        req = urllib2.Request(login_url)
        resp = self.opener.open(req)
        for i in self.cookie:
            self.login_headers['Cookie'] = i.name + '=' + i.value
        self.__get_vdcode()
        user_id = raw_input('请输入你的用户名：')
        password = getpass.getpass('请输入你的密码：')
        vdcode = raw_input('请打开当前路径下名为vdcode.png的图片，输入验证码：')
        data = {
            'act': 'login',
            'gourl': 'https://account.bilibili.com/login/dologin',
            'keeptime': 864000,
            'userid': user_id,
            'pwd': password,
            'vdcode': vdcode,
        }
        response = self.session.post(
            login_url,
            data=data,
            headers=self.login_headers
        )
        response.raise_for_status()
        self.cookie = response.cookies
        return True

    def run(self):
        event = gevent.spawn(self.danmu_sender)
        gevent.joinall([event])

    def danmu_sender(self):
        """不断发送弹幕。"""
        room_id = raw_input('您所在直播间：')
        while True:
            message = raw_input('弹幕(Ctrl+C 结束)：')
            self.send_a_danmu(room_id, message)

    def send_a_danmu(self, room_id, message):
        """发送一条弹幕。
        """

        data = {
            "color": "1111111",
            "fontsize": "11",
            "mode": "1",
            "msg": message,
            "roomid": room_id
        }
        json_data = json.dumps(data)
        response = self.session.post(
            'http://live.bilibili.com/msg/send',
            data=data,
            cookies=self.cookie
        )
        response.raise_for_status()
        if response.json().get('code') == 0:
            print "已发出"
        else:
            print response.json.get('msg')
        return True

    def __get_vdcode(self):
        '''
        获取验证码
        '''
        vdcode_url = 'https://account.bilibili.com/captcha'
        req = urllib2.Request(vdcode_url)
        resp = self.opener.open(req)
        html = resp.read()
        f = open('./vdcode.png', 'w')
        f.write(html)
        f.close()

if __name__ == '__main__':
    bili = DanmuSender()
    bili.run()
