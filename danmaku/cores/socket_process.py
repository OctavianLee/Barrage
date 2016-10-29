# -*- coding: utf-8 -*-
"""
    Process the socket when connecting to the server for reciever.
"""
import random
import time
import struct
from contextlib import contextmanager
from gevent import socket
from danmaku.models.danmaku import DanmakuQueue
from danmaku.configs.personal_settings import MAX_RETRY, TIME_OUT
from danmaku.cores.produce_and_consume import (
    terminate, produce_danmaku
)
from danmaku.helpers import (
    send_socket_data,
    get_server
)

is_first = True

@contextmanager
def generate_socket(room_id):
    """Generate the socket to communicate with Bilibili Danmaku Server.

    :param room_id: the id of live room.
    """
    global is_first
    retry_time = 0
    socket.setdefaulttimeout(TIME_OUT)
    userid = int(100000000 * random.random())
    body = ('{"roomid": ' + str(room_id) + ', "uid": ' + str(userid) +'}')
    while True:
        try:
            sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
            address = get_server(room_id)
            sock.connect(
                (address, 788))
            send_data = send_socket_data(sock, 16 + len(body), 16,
                    1, 7, 1, body)
        except socket.error as exc:
            if retry_time == MAX_RETRY:
                if not is_first:
                    terminate()
                raise RuntimeError("重试请求过多，服务中止！")
            print "服务器连接失败..."
            retry_time += 1
            time.sleep(4)
            continue

        if is_first:
            print "开始接收弹幕。(Ctrl + C 退出)"
            is_first = False
        retry_time = 0
        try:
            yield sock
        finally:
            sock.close()


def run_recieve(room_id):
    """Run the program of recieving danmakus.

    :param room_id: the id of live room.
    """
    danmaku_queue = DanmakuQueue(room_id)
    print "请求服务器连接"
    while True:
        with generate_socket(room_id) as sock:
            try:
                produce_danmaku.switch(sock, danmaku_queue, True)
            except RuntimeError and KeyboardInterrupt:
                continue
