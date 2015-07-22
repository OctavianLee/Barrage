# -*- coding: utf-8 -*-

import json
import socket

from binascii import unhexlify
from datetime import datetime

from danmaku.configs.global_settings import (
    RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT,
    RECIEVE_INIT_DATA
)
from danmaku.configs.personal_settings import TIME_FORMAT


class RecieverService(object):

    """提供弹幕接收服务。
    """

    def __init__(self, room_id):
        """初始化服务。
        :params: room_id: 直播间号。
        """
        self.recieve_danmaku(room_id)

    def recieve_danmaku(self, room_id):
        """接受弹幕。
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
            self.socket.connect((RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT))
            data = RECIEVE_INIT_DATA % room_id
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
                except Exception as e:
                    print e
                    pass
        except Exception:
            print "服务器连接失败。"

    def format_danmaku(self, danmaku):
        """格式化输出一条弹幕信息。

        :params: danmaku: 一条弹幕信息。
        :returns: 格式化的弹幕。
        """
        now = datetime.now().strftime(TIME_FORMAT)
        string = u"[{0}] 用户 {1} 说：{2}".format(
            now,
            danmaku['info'][2][1],
            danmaku['info'][1])
        return string
