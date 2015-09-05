# -*- coding: utf-8 -*-
"""
    Process the danmaku data.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import ujson as json
from datetime import datetime

from danmaku.models.danmaku import DanmakuModel
from danmaku.helpers import convert_hexascii_to_int

from danmaku.configs.personal_settings import TIME_FORMAT


def process_recieve_data(socket, danmaku_queue, data):
    data_type = convert_hexascii_to_int(data)
    if data_type == 1:
        count = convert_hexascii_to_int(socket.recv(4))
        if danmaku_queue.set_count(count):
            print "当前直播人数为：{0}".format(count)
    elif data_type == 4:
        length = convert_hexascii_to_int(socket.recv(2)) - 4
        if length > 0:
            msg = socket.recv(length)
            danmaku = generate_danmaku(json.loads(msg))
            if danmaku:
                put_danmaku(danmaku_queue, danmaku)
                return True

def generate_danmaku(msg):
    """生成弹幕。

    :param msg: 从服务器获取到的消息。
    """
    recieved_time = datetime.now().strftime(TIME_FORMAT)
    try:
        danmaku = DanmakuModel(
            publisher=msg['info'][2][1],
            content=msg['info'][1],
            recieved_time=recieved_time
        )
        return danmaku
    except Exception as e:
        # b站现在新推出了msg类型，防止问题先pass，之后来处理这些新弹幕
        return None

def put_danmaku(danmaku_queue, danmaku):
    danmaku_queue.enqueue(danmaku)

def get_danmaku(danmaku_queue):
    return danmaku_queue.dequeue()
