# -*- coding: utf-8 -*-


class DanmakuModel(object):

    """The model of a Danmaku
    """
    DANMU_MSG = 1
    SEND_GIFT = 2
    WELCOME = 3
    GIFT_TOP = 4

    def __init__(self, publisher, content, recieved_time, danmaku_type,
                 is_admin=False, is_vip=False):
        self.publisher = publisher
        self.content = content
        self.recieved_time = recieved_time
        self.is_admin = is_admin
        self.is_vip = is_vip
        self.danmaku_type = danmaku_type

    def __str__(self):
        title = []
        if self.is_vip:
           title.append('尊贵的')
        if self.is_admin:
           title.append('管理员')
        else:
           title.append('用户')

        string = ''
        if self.danmaku_type == DanmakuModel.DANMU_MSG:
            string = "[{}] {} {} 说：{}".format(
                self.recieved_time, ''.join(title),
                self.publisher, self.content)
        elif self.danmaku_type == DanmakuModel.SEND_GIFT:
            string = "[{}] {} {} 送出了 {}".format(
                self.recieved_time, ''.join(title),
                self.publisher, self.content)
        elif self.danmaku_type == DanmakuModel.WELCOME:
            string = "[{}] 欢迎 {} {}".format(
                self.recieved_time, ''.join(title),
                self.publisher)
        elif self.danmaku_type == DanmakuModel.GIFT_TOP:
            string = "[{}] {}:\n {}".format(
                self.recieved_time,
                self.publisher,
                self.content)

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
