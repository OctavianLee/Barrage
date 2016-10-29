# -*- coding: utf-8 -*-
import struct
import urllib

def get_server(room_id):
    url = ("http://live.bilibili.com/api/player?id=cid:"+ str(room_id))
    info = urllib.urlopen(url).read()
    start = info.find("<server>") + len("<server>")
    end = info.find("</server>", start)
    if 0 < start < end:
        server_url = info[start:end]
        return server_url
    else:
        return "livecmt-1.bilibili.com"

def send_socket_data(sock, total_len, head_len, version, action, param5=1,
   data=b''):
    send_data = struct.pack("!ihhii" + str(len(data)) + "s", total_len,
    head_len, version, action, param5, data)
    try:
        sock.send(send_data)
        return True
    except socket.error:
        return False
