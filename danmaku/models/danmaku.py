# -*- coding: utf-8 -*-


class DanmakuModel(object):

    """弹幕的数据模型。
    """

    def __init__(self, publisher, content, recieved_time):
        self.publisher = publisher
        self.content = content
        self.recieved_time = recieved_time

    def __str__(self):
        string = "[{0}] 用户 {1} 说：{2}".format(
            self.recieved_time, self.publisher, self.content)
        return string
    
    def to_string(self):
        return self.__str__()


class DanmakuQueue(object):

    """弹幕队列。
    当获取到弹幕信息，加入队列中，此时接收器可以通过取出内容获取弹幕信息。

    """

    def __init__(self, room_id):
        self.__queue = []
        self.room_id = room_id
        self.__count = 0

    def set_count(self, count):
        """设置当前直播间人数。
        :params: count: 当前直播间人数。
        """
        if self.__count != count:
            self.__count = count
            return True
        return False

    def get_count(self):
        """获取当前直播间人数。"""
        return self.__count

    def enqueue(self, danmaku):
        """将一个弹幕数据放入队列中。
        :params: danmaku_model: 弹幕数据类型。
        """
        if isinstance(danmaku, DanmakuModel):
            self.__queue.append(danmaku)
            return True
        return False

    def dequeue(self):
        """弹出一个弹幕数据类型。
        """
        if self.__queue:
            return self.__queue.pop(0)
        return None
