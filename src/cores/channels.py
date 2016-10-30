# -*- coding: utf-8 -*-
"""
    连接到频道上
"""
import ujson
import random
import urllib
import struct
from gevent import socket
from src.configs.globals import Info
from src.utils import generate_send_data


class Channel(object):

    """ 频道工作
    """

    def __init__(self, room_id, user_id=0):
        """初始化你要登陆的房间号

        Args:
            room_id (i32): 房间号
            user_id (i32): 用户号
        """
        self.room_id = room_id
        self.is_first = True
        self.retry_times = 0
        if user_id == 0:
            # 如果没有的话，随机生成一个大号用户
            self.user_id = int(100000000 * random.random())
        else:
            self.user_id = user_id
        self.danmaku_server = self.get_danmaku_server()

    def get_danmaku_server(self):
        """获取弹幕服务器信息.
        """
        url = (Info.INFO_API + str(self.room_id))
        # 获取用户相关信息
        info = urllib.urlopen(url).read()
        # 截取文本(可以用正则优化这块)
        start = info.find("<server>") + len("<server>")
        end = info.find("</server>", start)

        if 0 < start < end:
            server_url = info[start:end]
            return server_url
        else:
            # 获取不到通过默认备选服务器拿弹幕
            return random.choice([nfo.SERVER_LIST])

    def connect(self):
        """连接服务器

        TODO: 用retrying优化这部分体验 
        """
        try:
            body_data = self.auth_data
            self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM)
            self.sock.connect(
                (self.danmaku_server, Info.SERVER_PORT))
            send_data = generate_send_data(
                16 + len(body_data), 16,
                1, 7, 1, body_data
            )
            self.sock.send(send_data)
            return self.sock
        except socket.error as exc:
            print "服务器连接失败..."

    @property
    def auth_data(self):
        body = {
            "roomid": self.room_id,
            "uid": self.user_id
        }
        body_data = ujson.dumps(body)
        return body_data

