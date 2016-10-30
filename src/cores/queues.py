# -*- coding: utf-8 -*-
"""
    弹幕池
"""

class Pool(object):

    """弹幕池
    """

    def __init__(self):

        self.queue = []
        self.count = 0

    def enqueue(self, danmaku):
        """enqueue a danmaku.

        :param danmaku: a danamku.
        :return: the bool value.
        """
        self.queue.append(danmaku)
        return true

    def dequeue(self):
        """dequeue a danmaku.

        :return: the danmaku when success.
        """
        if self.queue:
            return self.queue.pop(0)
