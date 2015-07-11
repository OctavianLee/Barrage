# -*- coding: utf-8 -*-

import time
import json
import gevent
import requests
from datetime import datetime


class DanmuProcessor(object):

    """关于弹幕处理的类"""

    def __init__(self, room_id):
        self.__room_id = room_id
        self.__last_time = "000000000000"
        self._danmus = self.__get_all_danmus()

        self.admin_danmus = self.get_all_administrators_danmus()
        print self.admin_danmus[0]
        self.user_danmus = self.get_all_users_danmus()

    def run(self):
        event = gevent.spawn(self.update_danmus, 10)
        gevent.joinall([event])

    def __get_all_danmus(self):
        """获取一个房间的所有的弹幕信息。

        :returns: 房间中所有的弹幕信息。
        """
        data = {
            "roomid": self.__room_id
        }
        json_data = json.dumps(data)
        response = requests.request(
            'post',
            'http://live.bilibili.com/ajax/msg',
            data=data
        )
        response.raise_for_status()
        self._danmus = response.json().get('data')
        return self._danmus

    def filter_danmu_by_time(self, danmus):
        """根据时间过滤弹幕。

        显示在上次弹幕时间之后获取的新弹幕。

        :params: danmus: 新获取的所有弹幕。
        :returns: 上次弹幕获取时间之后的弹幕。

        """
        now = datetime.now()
        now_time = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        new_time = filter(str.isdigit, now_time[4:])
        self.admin_danmus = [
            danmu
            for danmu in danmus['admin']
            if self.__last_time < filter(str.isdigit, danmu['timeline'].encode('utf-8')[4:])
        ]
        self.user_danmus = [
            danmu
            for danmu in danmus['room']
            if self.__last_time < filter(str.isdigit, danmu['timeline'].encode('utf-8')[4:])
        ]
        self.__last_time = new_time

    def update_danmus(self, per_time):
        """定时更新弹幕信息。"""
        while True:
            self.__get_all_danmus()
            self.filter_danmu_by_time(self._danmus)
            for danmu in self.user_danmus:
                print self.format_danmus(danmu)
            for danmu in self.admin_danmus:
                print self.format_danmus(danmu)
            time.sleep(per_time)

    def get_all_administrators_danmus(self):
        """获取所有的房间管理员的弹幕。

        :returns: 房间中所有房间管理员的弹幕信息。
        """
        admin_danmus = self._danmus['admin']
        return admin_danmus

    def get_all_users_danmus(self):
        """获取所有的房间用户的弹幕。

        :returns: 房间中所有房间管理员的弹幕信息。
        """
        user_danmus = self._danmus['room']
        return user_danmus

    @classmethod
    def format_danmus(cls, danmu):
        """格式化输出一条弹幕信息。

        :params: danmu: 一条弹幕信息。
        :returns: 格式化的弹幕。
        """

        string = u"[{0}] 用户 {1} 说：{2}".format(
            danmu['timeline'],
            danmu['nickname'],
            danmu['text'])
        return string
