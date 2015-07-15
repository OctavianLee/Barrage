# -*- coding: utf-8 -*-

import getpass
import json
import requests
import cookielib
import urllib2
import socket
from binascii import unhexlify
from datetime import datetime


class DanmakuHelper(object):

    """在直播中发送弹幕。

    登陆后在直播中发送弹幕信息。
    """

    def __init__(self):
        self.session = requests.Session()

        print (
            """欢迎使用直播弹幕小助手，选择当前服务：\n
            本助手由Octavian开发，邮箱：Octavianlee1@gmail.com\n
        \t 1: 选择 1 接收直播间弹幕信息；  \n
        \t 2: 选择 2 在直播间发送弹幕信息（需要登录）。\n
        """)
        option = None
        room_id = None
        while True:
            option = raw_input("请输入你的选择(Exit 退出):")
            if option in ["1", "2", "Exit"]:
                break
        if option != "Exit":
            while True:
                try:
                    room_id_str = raw_input('您所在直播间(Exit 退出助手)：')
                    if room_id_str == "Exit":
                        break
                    room_id = int(room_id_str)
                    if option == "1":
                        self.receiver_service(room_id)
                    elif option == "2":
                        self.sender_service(room_id)
                    break
                except:
                    print "您输入的直播间有误，请重新输入！"
        print "感谢使用本助手！"

    def sender_service(self, room_id):
        """弹幕发送服务。
        :params: room_id: 直播间号。
        """
        self.do_login()
        self.danmaku_sender(room_id)

    def do_login(self):
        login_url = 'https://account.bilibili.com/login'
        # 载入登陆设置
        self._pre_login(login_url)
        # 获取 登陆必要参数
        user_id = raw_input('请输入你的用户名：')
        password = getpass.getpass('请输入你的密码：')
        self._get_vdcode()
        vdcode = raw_input('请打开当前路径下名为vdcode.png的图片，输入验证码：')
        # 进行登录
        self._login(login_url, user_id, password, vdcode)

    def _pre_login(self, login_url):
        """进行登录前信息配置信息。

        :params: login_url: 登录地址。
        """
        # 设置cookie
        self.cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(
            cookie_handler, urllib2.HTTPHandler)
        # 将页面信息加入头部
        req = urllib2.Request(login_url)
        resp = self.opener.open(req)
        self.login_headers = {
            'Host': 'account.bilibili.com',
            'Referer': 'https://account.bilibili.com/login',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://account.bilibili.com'
        }
        for i in self.cookie:
            self.login_headers['Cookie'] = i.name + '=' + i.value

    def _get_vdcode(self):
        """获取验证码。"""
        vdcode_url = 'https://account.bilibili.com/captcha'
        req = urllib2.Request(vdcode_url)
        resp = self.opener.open(req)
        html = resp.read()
        with open('./vdcode.png', 'w') as f:
            f.write(html)
            f.close()

    def _login(self, login_url, user_id, password, vdcode):
        """登陆操作。
        :params: login_url: 登录地址。
        :params: user_id: 用户账户或邮箱。
        :params: password: 密码。
        :params: vdcode: 验证码。
        """
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
        print self.cookie
        return True

    def danmaku_sender(self, room_id):
        """不断发送弹幕。
        :params: room_id: 直播间号。
        """
        print "准备开启弹幕发射！"
        while True:
            try:
                danmaku = raw_input('输入发送的弹幕(Exit 退出)：')
                if danmaku == "Exit":
                    break
            except:
                pass
            self.send_a_danmaku(room_id, danmaku)

    def send_a_danmaku(self, room_id, danmaku):
        """发送一条弹幕。
        :params: room_id: 直播间号。
        :params: danmaku: 弹幕信息。
        """

        data = {
            "color": "1111111",
            "fontsize": "11",
            "mode": "1",
            "msg": danmaku,
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
            print "弹幕已发出"
        else:
            print response.json().get('msg')
        return True

    def receiver_service(self, room_id):
        """接受弹幕服务。
        :params: room_id: 直播间号。
        """
        is_first = True
        while True:
            self.get_danmaku(room_id, is_first)
            is_first = False

    def get_danmaku(self, room_id, is_first):
        """ 请求获得弹幕信息。
        :params: room_id: 直播间号。
        :params: is_first: 判断是否是第一次连接弹幕服务器。
        """
        if is_first:
            print "请求服务器连接。"
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("livecmt.bilibili.com", 88))
            data = '0101000c0000%04x00000000' % room_id
            send_data = unhexlify(data)
            self.socket.sendall(send_data)
            while True:
                if is_first:
                    print "开始接收弹幕。(Ctrl + C 退出)"
                    is_first = False
                data = self.socket.recv(1024)
                if data == "":
                    self.socket.close()
                    break
                try:
                    print self.format_danmaku(json.loads(data[4:]))
                except:
                    pass
        except Exception:
            print "服务器连接失败。"

    def format_danmaku(self, danmaku):
        """格式化输出一条弹幕信息。

        :params: danmaku: 一条弹幕信息。
        :returns: 格式化的弹幕。
        """
        now = datetime.now().strftime("%H:%M:%S")
        string = u"[{0}] 用户 {1} 说：{2}".format(
            now,
            danmaku['info'][2][1],
            danmaku['info'][1])
        return string

if __name__ == '__main__':
    helper = DanmakuHelper()
