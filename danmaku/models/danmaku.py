# -*- coding: utf-8 -*-


class DanmakuModel(object):

    """弹幕的数据模型。
    """

    def __init__(self, publisher, content, recieved_time):
        self.publisher = publisher
        self.content = content
        self.recieved_time = recieved_time

    def __str__(self):
        string = u"[{0}] 用户 {1} 说：{2}".format(
            self.recieved_time, self.publisher, self.content)
        return string


class DanmakuQueue(object):

    """弹幕队列。
    当获取到弹幕信息，加入队列中，此时接收器可以通过取出内容获取弹幕信息。

    """

    def __init__(self):
        self.__queue = []

    def enqueue(self, danmaku):
        """将一个弹幕数据放入队列中。
        :params: danmaku_model: 弹幕数据类型。
        """
        if isinstance(danmaku, DanmakuModel):
            self.__queue.append(danmaku)
        else:
            print "获取到错误的数据类型！"

    def dequeue(self):
        """弹出一个弹幕数据类型。
        """
        if self.__queue:
            return self.__queue.pop(0)


danmaku_queue = DanmakuQueue()
