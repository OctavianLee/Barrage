# -*- coding: utf-8 -*-
"""
    The core algorithm of reciever.
    Definitely, it's the model of producer and consumer.
    Coroutine is a better way of implementing that model.
    However, when connecting to the server,
    it also needs to keep alive by heartbeat.
"""
import time
import gevent
import struct
from gevent import socket
from greenlet import greenlet

from danmaku.configs.global_settings import (
    HEARTBEAT_KEEP_TIME
)
from danmaku.cores.danmaku_process import (
    process_recieve_data,
    get_danmaku
)
from danmaku.helpers import send_socket_data


@greenlet
def produce_danmaku(sock, danmaku_queue, is_health=True):
    """Produce danmakus.

    :param sock: the socket object.
    :param danmaku_queue: the queue to recieve danmaku.
    :param is_health: the status of connection
    """
    start = time.time()
    while True:
        end = time.time()
        if end - start > HEARTBEAT_KEEP_TIME:
            start = time.time()
            heartbeat.switch(sock, danmaku_queue, is_health)
        try:
            data = sock.recv(10240)
            if not data:
                break
        except socket.timeout:
            if not is_health:
                print "连接超时，准备重连服务器。。。"
                break
        except socket.error:
            break
        status = process_recieve_data(danmaku_queue, data)
        if status:
            consume_danmaku.switch(sock, danmaku_queue, is_health)


@greenlet
def consume_danmaku(sock, danmaku_queue, is_health):
    """Consume danmakus.

    :param sock: the socket object.
    :param danmaku_queue: the queue to recieve danmaku.
    :param is_health: the status of connection
    """
    while True:
        danmaku = get_danmaku(danmaku_queue)
        try:
            print danmaku
        except TypeError:
            pass # 测试过这玩意返回 NoneType 的时候b站直播间也不行
        produce_danmaku.switch(sock, danmaku_queue, is_health)


@greenlet
def heartbeat(sock, danmaku_queue, is_health):
    """Keep the connection alive.

    :param sock: the socket object.
    :param danmaku_queue: the queue to recieve danmaku.
    :param is_health: the status of connection
    """
    
    while True:
        try:
            send_data = send_socket_data(sock, 16, 16, 1, 2)
        except socket.timeout:
            is_health = False
        produce_danmaku.switch(sock, danmaku_queue, is_health)


def terminate():
    """Terminate all greenlets.
    """
    gevent.kill(produce_danmaku)
    gevent.kill(consume_danmaku)
    gevent.kill(heartbeat)
