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
from binascii import unhexlify
from gevent import socket
from greenlet import greenlet

from danmaku.configs.global_settings import (
    HEARTBEAT_STR,
    HEARTBEAT_KEEP_TIME
)
from danmaku.cores.danmaku_process import (
    process_recieve_data,
    get_danmaku
)
from danmaku.helpers import recieve_sock_data


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
            data = recieve_sock_data(sock, 2)
            if not data:
                break
        except socket.timeout:
            if not is_health:
                print "连接超时，准备重连服务器。。。"
                break
        except socket.error:
            break
        status = process_recieve_data(sock, danmaku_queue, data)
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
        print danmaku
        produce_danmaku.switch(sock, danmaku_queue, is_health)


@greenlet
def heartbeat(sock, danmaku_queue, is_health):
    """Keep the connection alive.

    :param sock: the socket object.
    :param danmaku_queue: the queue to recieve danmaku.
    :param is_health: the status of connection
    """
    send_data = unhexlify(HEARTBEAT_STR)
    while True:
        try:
            sock.sendall(send_data)
        except socket.timeout:
            is_health = False
        produce_danmaku.switch(sock, danmaku_queue, is_health)


def terminate():
    """Terminate all greenlets.
    """
    gevent.kill(produce_danmaku)
    gevent.kill(consume_danmaku)
    gevent.kill(heartbeat)
