# -*- coding: utf-8 -*-
from unittest import TestCase
from nose.tools import eq_
from mock import Mock

from constants import STRING, NUMBER, DATE
from danmaku.models import DANMU_MSG, SEND_GIFT, WELCOME, GIFT_TOP
from danmaku.models import STRING_DICT, DanmakuModel, DanmakuQueue
from danmaku.configs.personal_settings import TIME_FORMAT


class TestDanmakuModel(TestCase):

    def setUp(self):
        self.publisher = STRING
        self.content = STRING
        self.recieved_time = DATE
        self.danmaku = DanmakuModel(
            self.publisher, self.content,
            self.recieved_time, DANMU_MSG)

    def test_title(self):
        eq_(self.danmaku.title, DanmakuModel.USER)
        self.danmaku.is_vip = True
        eq_(self.danmaku.title,
            ''.join([DanmakuModel.VIP, DanmakuModel.USER]))
        self.danmaku.is_admin = True
        eq_(self.danmaku.title,
            ''.join([DanmakuModel.VIP, DanmakuModel.ADMIN]))
        self.danmaku.is_vip = False
        eq_(self.danmaku.title, DanmakuModel.ADMIN)

    def test_to_string(self):
        string = STRING_DICT.get(DANMU_MSG).format(
            self.recieved_time, self.danmaku.title,
            self.publisher, self.content)
        eq_(self.danmaku.to_string(), string)
        self.danmaku.danmaku_type = SEND_GIFT
        string = STRING_DICT.get(SEND_GIFT).format(
            self.recieved_time, self.danmaku.title,
            self.publisher, self.content)
        eq_(self.danmaku.to_string(), string)
        self.danmaku.danmaku_type = WELCOME
        string = STRING_DICT.get(WELCOME).format(
            self.recieved_time, self.danmaku.title,
            self.publisher)
        eq_(self.danmaku.to_string(), string)
        self.danmaku.danmaku_type = GIFT_TOP
        string = STRING_DICT.get(WELCOME).format(
            self.recieved_time,
            self.publisher,
            self.content)


class TestDanmakuQueue(TestCase):

    def setUp(self):
        room_id = NUMBER
        self.danmaku_queue = DanmakuQueue(room_id)

    def test_count(self):
        count = NUMBER
        self.count = count
        eq_(self.count, count)

    def test_enqueue(self):
        self.assertFalse(self.danmaku_queue.enqueue([]))
        danmaku = Mock(DanmakuModel)
        self.assertTrue(self.danmaku_queue.enqueue(danmaku))

    def test_dequeue(self):
        self.assertIsNone(self.danmaku_queue.dequeue())
        danmaku = Mock(spec=DanmakuModel)
        self.danmaku_queue._queue.append(danmaku)
        eq_(self.danmaku_queue.dequeue(), danmaku)
