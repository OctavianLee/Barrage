# -*- coding: utf-8 -*-
"""
    Process the danmaku data.
"""
import ujson
from datetime import datetime

from danmaku.models import DANMU_MSG, SEND_GIFT, WELCOME, SEND_TOP
from danmaku.models.danmaku import DanmakuModel
from danmaku.helpers import convert_hexascii_to_int
from danmaku.configs.personal_settings import TIME_FORMAT
from danmaku.helpers import recieve_sock_data


def process_recieve_data(sock, danmaku_queue, data):
    """Process recieving data.

    :param sock: the socket object.
    :param danmaku_queue: the queue to recieve danmaku.
    :param data: the recieved data.
    """
    data_type = convert_hexascii_to_int(data)
    if data_type == 1:
        hexascii_data = recieve_sock_data(sock, 4)
        if not hexascii_data:
            return False
        count = convert_hexascii_to_int(hexascii_data)
        if danmaku_queue.count != count:
            danmaku_queue.count = count
            print "当前直播人数为：{}".format(count)
    elif data_type == 4:
        hexascii_data = recieve_sock_data(sock, 2)
        if not hexascii_data:
            return False
        length = convert_hexascii_to_int(hexascii_data) - 4
        if length > 0:
            data = recieve_sock_data(sock, length)
            if not data:
                return False
            msg = ujson.loads(data)
            danmaku = generate_danmaku(msg)
            if danmaku:
                put_danmaku(danmaku_queue, danmaku)
                return True


def generate_danmaku(msg):
    u"""Generate a danmaku.

    the format of msg (Coz the format is closed source, it could be changed):

    # 1 DANMU_MSG send a danmaku
    {
        u'info': [
            [ 0, 1, 25, 16777215, 1441727762, 1585812335, 0, u'c8de2b91', 0],
            u'xxxxx',
            [ 11111, u'xxxx', 0, u'0']
        ],
        u'cmd': u'DANMU_MSG',
        u'roomid': 1111
    }
    # 2 SEND_GIFT send a gift
    {
        u'roomid': 11111,
        u'cmd': u'SEND_GIFT',
        u'data': {
            u'top_list': [
                {u'uname': u'xxx', u'coin': 22222, u'uid': 222222},
                ...
            ],
            u'uid': 1111,
            u'timestamp': 1441727778,
            u'price': 100,
            u'giftId': 1,
            u'uname': u'xxxxx',
            u'num': 1,
            u'rcost': 99999,
            u'super': 0,
            u'action': u'\u5582\u98df',
            u'giftName': u'\u8fa3\u6761'
        }
    }
    # 3 WELCOME welcome a vip.
    {
        u'roomid': 111,
        u'cmd': u'WELCOME',
        u'data': {
            u'uname': u'xxxxxr',
            u'isadmin': 0,
            u'uid': 1111
        }
    }
    # 4 SEND_TOP Top list.
    {
        u'roomid': u'11111',
        u'cmd': u'SEND_TOP',
        u'data': {
            u'top_list': [
                {u'uname': u'xxxx', u'coin': 693300, u'uid': 11111},
                ...
            ]
        }
    }

    :param msg: the message from Bilibili Danmaku Server.
    """
    recieved_time = datetime.now().strftime(TIME_FORMAT)
    cmd = msg.get('cmd')
    publisher = None
    content = None
    is_vip = False
    is_admin = False
    danmaku_type = None
    try:
        if cmd == "DANMU_MSG":
            danmaku_type = DANMU_MSG
            publisher = msg['info'][2][1].encode('utf-8')
            content = msg['info'][1].encode('utf-8')
            is_vip = msg['info'][2][2] == 1
            is_admin = int(msg['info'][2][3].encode('utf-8')) == 1
        elif cmd == "SEND_GIFT":
            danmaku_type = SEND_GIFT
            publisher = msg['data']['uname'].encode('utf-8')
            content = ''.join(
                [str(msg['data']['num']), ' X ',
                 msg['data']['giftName'].encode('utf-8'),
                 ' 目前共花销：', str(msg['data']['rcost'])])
        elif cmd == "WELCOME":
            danmaku_type = WELCOME
            publisher = msg['data']['uname'].encode('utf-8')
            is_vip = True
            is_admin = msg['data']['isadmin'] == 1
        elif cmd == "SEND_TOP":
            danmaku_type = SEND_TOP
            tops = msg["data"]['top_list']
            contents = ["{}: {} {}".format(top['uid'], top['uname'], top['coin'])
                        for top in tops]
            content = '\n'.join(contents)
            publisher = "排行榜"

        danmaku = DanmakuModel(
            publisher=publisher,
            content=content,
            recieved_time=recieved_time,
            danmaku_type=danmaku_type,
            is_admin=is_admin,
            is_vip=is_vip
        )
        return danmaku
    except KeyError:
        # pass the unknown danamku.
        return None


def put_danmaku(danmaku_queue, danmaku):
    """Put a danmaku into a danamku queue.

    :param danmaku_queue: the queue to recieve danmaku.
    :param danmaku: a danmaku
    """
    danmaku_queue.enqueue(danmaku)


def get_danmaku(danmaku_queue):
    """Get a danmaku from a danamku queue.

    :param danmaku_queue: the queue to recieve danmaku.
    """
    return danmaku_queue.dequeue()
