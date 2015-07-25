# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import socket
import thread

from binascii import unhexlify
from datetime import datetime

from danmaku.configs.global_settings import (
    RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT,
    RECIEVE_INIT_DATA
)
from danmaku.configs.personal_settings import TIME_FORMAT
from danmaku.helpers import convert_hexascii_to_int
from danmaku.models.danmaku import DanmakuModel, DanmakuQueue


class RecieverService(object):

    """提供弹幕接收服务。
    """

    def __init__(self, room_id):
        """初始化服务。
        :params: room_id: 直播间号。
        """
        data = RECIEVE_INIT_DATA % room_id
        self.send_data = unhexlify(data)
        self.danmaku_queue = DanmakuQueue(room_id)

    def cmd_run(self):
        """启动服务(只针对命令行使用)"""
        thread.start_new_thread(self.subscribe_danmaku, ())
        self.consume_danmaku()

    def recieve_danmaku(self):    
        """接收一个弹幕"""
        return self.danmaku_queue.dequeue()

    def consume_danmaku(self):
        """获取接收到的弹幕。"""
        while True:
            danmaku = self.recieve_danmaku()
            if danmaku:
                print danmaku

    def subscribe_danmaku(self):
        """订阅接收到的弹幕。"""
        is_first = True
        print "请求服务器连接。"
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(
                    (RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT))
                self.socket.sendall(self.send_data)
                if is_first:
                    print "开始接收弹幕。(Ctrl + C 退出)"
                    is_first = False
            except:
                print "服务器连接失败。"
            self.get_danmaku()

    def get_danmaku(self):
        """ 请求获得弹幕信息。"""
        while True:
            data = self.socket.recv(2)
            if not data:
                self.socket.close()
                break
            type = convert_hexascii_to_int(data)
            if type == 1:
                count = convert_hexascii_to_int(self.socket.recv(4))
                if self.danmaku_queue.set_count(count):
                    print "当前直播人数为：{0}".format(count)
            elif type == 4:
                length = convert_hexascii_to_int(self.socket.recv(2)) - 4
                if length > 0:
                    msg = self.socket.recv(length)
                    self.store_message(json.loads(msg))

    def store_message(self, msg):
        """将信息存入弹幕队列中

        :params: msg: 从服务器获取到的消息。
        """
        recieved_time = datetime.now().strftime(TIME_FORMAT)
        danmaku = DanmakuModel(
            publisher=msg['info'][2][1],
            content=msg['info'][1],
            recieved_time=recieved_time
        )
        self.danmaku_queue.enqueue(danmaku)
