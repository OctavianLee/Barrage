# -*- coding: utf-8 -*-

from services.sender import SenderService
from services.reciever import RecieverService


class DanmakuHime(object):

    """弹幕姬，可以进行弹幕的接收和发送。
    """

    def __init__(self):
        print (
            """欢迎使用直播弹幕小助手，选择当前服务：\n
            本助手由Octavian开发，邮箱：Octavianlee1@gmail.com\n
        \t 1: 选择 1 接收直播间弹幕信息；  \n
        \t 2: 选择 2 在直播间发送弹幕信息（需要登录）。\n
        """)
        self.run()

    def run(self):
        """运行弹幕姬服务。"""
        option = None
        room_id = None
        while True:
            option = raw_input("请输入你的选择(Exit 退出)：")
            if option in ["1", "2", "Exit"]:
                break
        if option != "Exit":
            while True:
                try:
                    room_id_str = raw_input('您所在直播间(Exit 退出助手)：')
                    if room_id_str == "Exit":
                        break
                    room_id = int(room_id_str)
                except:
                    print "您输入的直播间有误，请重新输入！"
                    continue
                self.create_service(option, room_id)
                break
        print "感谢使用本助手！"

    def create_service(self, option, room_id):
        """创建弹幕姬服务。

        :params: option: 选择选项，1 为接收弹幕服务；2 为发送弹幕服务。
        :params: room_id: 直播间的号码。
        :returns: 对应的弹幕服务。
        """
        danmaku_services = {
            '1': RecieverService,
            '2': SenderService
        }
        try:
            service = danmaku_services[option](room_id)
            if option == "1":
                service.cmd_run()
            else:
                return service
        except KeyError:
            print "选项发生错误!"
