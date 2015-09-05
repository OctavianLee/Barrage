# -*- coding: utf-8 -*-
from danmaku.cores.socket_process import run_recieve


class RecieverService(object):

    """提供弹幕接收服务。
    """

    def __init__(self, room_id):
        """初始化服务。
        :param room_id: 直播间号。
        """
        self.room_id = room_id

    def cmd_run(self):
        """启动服务(只针对命令行使用)"""
        run_recieve(self.room_id)
