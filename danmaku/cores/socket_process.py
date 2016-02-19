# -*- coding: utf-8 -*-
"""
    Process the socket when connecting to the server for reciever.
"""
import time
from binascii import unhexlify
from contextlib import contextmanager
from gevent import socket
from danmaku.models.danmaku import DanmakuQueue
from danmaku.configs.global_settings import (
    RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT,
    RECIEVE_INIT_DATA
)
from danmaku.configs.personal_settings import MAX_RETRY, TIME_OUT
from danmaku.cores.produce_and_consume import (
    terminate, produce_danmaku
)


@contextmanager
def generate_socket(room_id):
    """Generate the socket to communicate with Bilibili Danmaku Server.

    :param room_id: the id of live room.
    """
    is_first = True
    print "请求服务器连接"
    retry_time = 0
    socket.setdefaulttimeout(TIME_OUT)
    data = RECIEVE_INIT_DATA % room_id
    send_data = unhexlify(data)
    while True:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        try:
            sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
            sock.connect(
                (RECIEVE_SERVER_ADDRESS, RECIEVE_SERVER_PORT))
            sock.sendall(send_data)
        except socket.error:
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
    try:
        with generate_socket(room_id) as sock:
            produce_danmaku.switch(sock, danmaku_queue, True)
    except RuntimeError and KeyboardInterrupt:
        pass
