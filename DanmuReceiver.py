# -*- coding: utf-8 -*-

import time
import json
import gevent
import socket
from binascii import unhexlify
from datetime import datetime


class DanmuReceiver(object):

    """关于接收弹幕的类"""

    def run(self):
        """运行弹幕助手程序。"""
        room_id_str = raw_input('请输入房间号：')
        room_id = int(room_id_str)
        while True:
            event = gevent.spawn(self.get_danmus, room_id)
            gevent.joinall([event])

    def get_danmus(self, room_id):
        """ 请求获得弹幕信息。"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("livecmt.bilibili.com", 88))
        data = '0101000c0000%04x00000000' % room_id
        send_data = unhexlify(data)
        self.socket.sendall(send_data)
        while True:
            data = self.socket.recv(1024)
            if data == "": 
                self.socket.close()
                break
            try:
                print self.format_danmus(json.loads(data[4:]))
            except:
                pass

    def format_danmus(self, danmu):
        """格式化输出一条弹幕信息。

        :params: danmu: 一条弹幕信息。
        :returns: 格式化的弹幕。
        """

        string = u"用户 {0} 说：{1}".format(
            danmu['info'][2][1],
            danmu['info'][1])
        return string

if __name__ == '__main__':
    s = DanmuReceiver()
    s.run()
