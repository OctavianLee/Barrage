# -*- coding: utf-8 -*-
"""
    搬运弹幕
"""
import time
import struct
from src.utils import generate_send_data

class Worker(object):

    """弹幕搬运工
    """

    def __init__(self, sock):
        """初始化工人
        """
        self.sock = sock
        self.is_health = True

    def recieve_data(self):
        """接受数据
        """
        data = self.sock.recv(10240)
        return data

    def process_data(self, data):
        """提取弹幕
        """
        data_length = len(data)
        if data_length < 16:
            return False
        info = struct.unpack(
            "!ihhii" + str(data_length - 16) + "s",
            data
        )
        info_length = info[0]

        if info_length < 16:
            return False
        elif 16 < info_length < data_length:
            # 在高人气直播间，弹幕一次接受可能多条
            # 需要切片处理
            first_data = data[0:info_length]
            self.recieve_data(first_data)
            other_data = data[info_length:data_length]
            self.recieve_data(other_data)
            return True
        elif info_length == data_length:
            #TODO: 增加对有效弹幕处理
            print info
            return True
        return False

    def beat(self):
        """保持连接

        工人有点懒，需要来一鞭子
        """
        send_data = generate_send_data(
            16, 16, 1, 2)
        self.sock.send(send_data)

    def work(self):
        """干活
        """
        start = time.time()
        while True:
            end = time.time()
            # 20s打一下
            if end - start > 20:
                start = time.time()
                self.beat()
            data = self.recieve_data()
            self.process_data(data)

