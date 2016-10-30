# -*- coding: utf-8 -*-
"""
    常用工具
"""
import struct

def generate_send_data(total_len, head_len, version, action, param=1,
                data=b''):
    """生产socket信息

    Args:
        total_len (i16): 总长度
        head_len (i16): 头长度
        version (i16): 弹幕协议版本
        action (i16): 弹幕执行动作
        param (i16): 参数
        data (str): 数据包
    """
    send_data = struct.pack(
        "!ihhii" + str(len(data)) + "s",
        total_len, head_len,
        version, action, param, data)
    return send_data
