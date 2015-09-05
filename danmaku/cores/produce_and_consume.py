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


@greenlet
def produce_danmaku(sock, danmaku_queue, is_health=True):
    start = time.time()
    while True:
        end = time.time()
        if end - start > HEARTBEAT_KEEP_TIME:
            start = time.time()
            heartbeat.switch(sock, danmaku_queue, is_health)
        try:
            data = sock.recv(2)
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
def consume_danmaku(socket, danmaku_queue, is_health):
    while True:
        danmaku = get_danmaku(danmaku_queue)
        print danmaku
        produce_danmaku.switch(socket, danmaku_queue, is_health)


@greenlet
def heartbeat(sock, danmaku_queue, is_health):
    send_data = unhexlify(HEARTBEAT_STR)
    while True:
        try:
            sock.sendall(send_data)
        except socket.timeout:
            is_health = False
        produce_danmaku.switch(socket, danmaku_queue, is_health)


def terminate():
    gevent.kill(produce_danmaku)
    gevent.kill(consume_danmaku)
    gevent.kill(heartbeat)
