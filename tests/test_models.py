# -*- coding: utf-8 -*-
import pytest
from mock import Mock
from datetime import datetime

from constants import TEST_STRING, TEST_NUMBER
from danmaku.models import DanmakuModel, DanmakuQueue
from danmaku.configs.personal_settings import TIME_FORMAT


def test_danmakumodel():
    publisher = TEST_STRING
    content = TEST_STRING
    recieved_time = datetime.now().strftime(TIME_FORMAT)
    test_string = u"[{0}] 用户 {1} 说：{2}".format(
        recieved_time, publisher, content)
    danmaku = DanmakuModel(publisher, content, recieved_time)
    assert danmaku.to_string() == test_string


class TestDanmakuQueue(object):

    room_id = TEST_NUMBER

    def test_set_count(self):
        count = TEST_NUMBER
        test_danmaku_queue = DanmakuQueue(self.room_id)
        assert test_danmaku_queue.set_count(count) == True
        assert test_danmaku_queue.set_count(count) == False

    def test_get_count(self):
        test_danmaku_queue = DanmakuQueue(self.room_id)
        assert test_danmaku_queue.get_count() == 0
        count = TEST_NUMBER
        assert test_danmaku_queue.set_count(count) == True
        assert test_danmaku_queue.get_count() == count

    def test_enqueue(self):
        test_danmaku_queue = DanmakuQueue(self.room_id)
        assert test_danmaku_queue.enqueue([]) == False
        danmaku = Mock(spec=DanmakuModel)
        assert test_danmaku_queue.enqueue(danmaku) == True

    def test_dequeue(self):
        test_danmaku_queue = DanmakuQueue(self.room_id)
        assert test_danmaku_queue.dequeue() == None
        danmaku = Mock(spec=DanmakuModel)
        test_danmaku_queue.enqueue(danmaku)
        assert test_danmaku_queue.dequeue() == danmaku
