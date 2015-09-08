# -*- coding: utf-8 -*-
"""
    The models of the danmaku hime.
"""

DANMU_MSG = 1
SEND_GIFT = 2
WELCOME = 3
SEND_TOP = 4

STRING_DICT = {
    DANMU_MSG: "[{}] {} {} 说：{}",
    SEND_GIFT: "[{}] {} {} 送出了 {}",
    WELCOME: "[{}] 欢迎 {} {}",
    SEND_TOP: "[{}] {}:\n {}",
}


class DanmakuModel(object):

    """The model of a Danmaku
    """

    VIP = '尊贵的'
    ADMIN = '管理员'
    USER = '用户'

    def __init__(self, publisher, content, recieved_time, danmaku_type,
                 is_admin=False, is_vip=False):
        self.publisher = publisher
        self.content = content
        self.recieved_time = recieved_time
        self.is_admin = is_admin
        self.is_vip = is_vip
        self.danmaku_type = danmaku_type

    @property
    def title(self):
        """Get the title of danmaku user."""
        title = []
        if self.is_vip:
            title.append(self.VIP)
        if self.is_admin:
            title.append(self.ADMIN)
        else:
            title.append(self.USER)
        return ''.join(title)

    def __str__(self):
        if self.danmaku_type == DANMU_MSG:
            return STRING_DICT.get(self.danmaku_type).format(
                self.recieved_time, self.title,
                self.publisher, self.content)
        elif self.danmaku_type == SEND_GIFT:
            return STRING_DICT.get(self.danmaku_type).format(
                self.recieved_time, self.title,
                self.publisher, self.content)
        elif self.danmaku_type == WELCOME:
            return STRING_DICT.get(self.danmaku_type).format(
                self.recieved_time, self.title,
                self.publisher)
        elif self.danmaku_type == SEND_TOP:
            return STRING_DICT.get(self.danmaku_type).format(
                self.recieved_time,
                self.publisher,
                self.content)
        return None

    def to_string(self):
        """Get the content of danmaku."""
        return self.__str__()


class DanmakuQueue(object):

    """The Danmaku Queue

    Enqueue the danmaku when recieving.
    """

    def __init__(self, room_id):
        self._queue = []
        self.room_id = room_id
        self.__count = 0

    @property
    def count(self):
        """Get the current counts."""
        return self.__count

    @count.setter
    def count(self, count):
        """Set the number of current people in Live room.

        :param count: the number of current people.
        """
        if self.__count != count:
            self.__count = count

    def enqueue(self, danmaku):
        """Enqueue a danmaku.

        :param danmaku: a danamku.
        :return: the bool value.
        """
        if isinstance(danmaku, DanmakuModel):
            self._queue.append(danmaku)
            return True
        return False

    def dequeue(self):
        """Dequeue a danmaku.

        :return: the danmaku when success.
        """
        if self._queue:
            return self._queue.pop(0)
        return None
