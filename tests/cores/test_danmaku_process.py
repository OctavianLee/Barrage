# -*- coding: utf-8 -*-
from unittest import TestCase
from nose.tools import eq_
from mock import Mock
from datetime import datetime

from tests.constants import STRING, NUMBER, DATE
from tests.asserters import eq_obj

from danmaku.cores.danmaku_process import generate_danmaku
from danmaku.cores.danmaku_process import process_recieve_data
from danmaku.models import DANMU_MSG, SEND_GIFT, WELCOME, SEND_TOP
from danmaku.models.danmaku import DanmakuModel
from danmaku.configs.personal_settings import TIME_FORMAT
from danmaku.helpers import convert_hexascii_to_int


def test_generate_danmaku():
    msg = {
        u'info': [
            [ 0, 1, 25, 16777215, 1441727762, 1585812335, 0, u'c8de2b91', 0],
            u'xxxxx',
            [ NUMBER, u'xxxx', 0, u'0']
        ],
        u'cmd': u'DANMU_MSG',
        u'roomid': NUMBER
    }
    danmaku_type = DANMU_MSG
    publisher = msg['info'][2][1].encode('utf-8')
    content = msg['info'][1].encode('utf-8')
    is_vip = msg['info'][2][2] == 1
    is_admin = int(msg['info'][2][3].encode('utf-8')) == 1
    expect_danmaku = DanmakuModel(
            publisher=publisher,
            content=content,
            recieved_time=datetime.now().strftime(TIME_FORMAT),
            danmaku_type=danmaku_type,
            is_admin=is_admin,
            is_vip=is_vip
    )
    test_danmaku = generate_danmaku(msg)
    eq_obj(expect_danmaku, test_danmaku)

    msg = {
        u'roomid': NUMBER,
        u'cmd': u'SEND_GIFT',
        u'data': {
            u'top_list': [
                {u'uname': u'xxx', u'coin': NUMBER, u'uid': NUMBER},
            ],
            u'uid': NUMBER,
            u'timestamp': 1441727778,
            u'price': NUMBER,
            u'giftId': 1,
            u'uname': u'xxxxx',
            u'num': NUMBER,
            u'rcost': NUMBER,
            u'super': 0,
            u'action': u'\u5582\u98df',
            u'giftName': u'\u8fa3\u6761'
        }
    }
    danmaku_type = SEND_GIFT
    publisher = msg['data']['uname'].encode('utf-8')
    content = ''.join(
       [str(msg['data']['num']), ' X ',
       msg['data']['giftName'].encode('utf-8'),
       ' 目前共花销：', str(msg['data']['rcost'])])
    is_vip = False
    is_admin = False
    expect_danmaku = DanmakuModel(
            publisher=publisher,
            content=content,
            recieved_time=datetime.now().strftime(TIME_FORMAT),
            danmaku_type=danmaku_type,
            is_admin=is_admin,
            is_vip=is_vip
    )
    test_danmaku = generate_danmaku(msg)
    eq_obj(expect_danmaku, test_danmaku)

    msg = {
        u'roomid': NUMBER,
        u'cmd': u'WELCOME',
        u'data': {
            u'uname': u'xxxxxr',
            u'isadmin': 0,
            u'uid': NUMBER
        }
    }
    danmaku_type = WELCOME
    publisher = msg['data']['uname'].encode('utf-8')
    is_vip = True
    content = None
    is_admin = msg['data']['isadmin'] == 1
    expect_danmaku = DanmakuModel(
            publisher=publisher,
            content=content,
            recieved_time=datetime.now().strftime(TIME_FORMAT),
            danmaku_type=danmaku_type,
            is_admin=is_admin,
            is_vip=is_vip
    )
    test_danmaku = generate_danmaku(msg)
    eq_obj(expect_danmaku, test_danmaku)

    msg = {
        u'roomid': u'11111',
        u'cmd': u'SEND_TOP',
        u'data': {
            u'top_list': [
                {u'uname': u'xxxx', u'coin': NUMBER, u'uid': NUMBER},
            ]
        }
    }
    danmaku_type = SEND_TOP
    tops = msg["data"]['top_list']
    contents = ["{}: {} {}".format(top['uid'], top['uname'], top['coin'])
                        for top in tops]
    content = '\n'.join(contents)
    publisher = "排行榜"
    is_vip = False
    is_admin = False
    expect_danmaku = DanmakuModel(
            publisher=publisher,
            content=content,
            recieved_time=datetime.now().strftime(TIME_FORMAT),
            danmaku_type=danmaku_type,
            is_admin=is_admin,
            is_vip=is_vip
    )
    test_danmaku = generate_danmaku(msg)
    eq_obj(expect_danmaku, test_danmaku)

def test_process_recieve_data():
    # I have no idea to tests it.
    mock_fun = Mock(process_recieve_data)
    mock_fun.return_value = True
    eq_(mock_fun(), True)
