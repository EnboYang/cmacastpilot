#!/usr/bin/ python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/06/14 21:22:08
@Author  :   Enbo Yang
@Version :   0.1
@Contact :   enboyang@outlook.com
@License :   GPL v3
@Desc    :   Copyright (c) 2021 Enbo Yang
'''

# here put the import lib
from datetime import datetime  # , timedelta
import paramiko
import requests
import os

# self-defined module
from config import readcfg

cfg = readcfg(filename='config.ini')

ip = cfg.get('cmacast', 'ip')
port = cfg.get('cmacast', 'port')

username = '***'
passwd = '***'

log_path = cfg.get('cmacast', 'log_path')

wx_key = cfg.get('wxwork', 'key')
wx_mobile = cfg.get('wxwork', 'mobile')


def file_down(log_file,
              ip=ip,
              port=int(port),
              username=username,
              passwd=passwd,
              log_path=log_path):
    '''
    下载日志文件
    '''
    trans = paramiko.Transport(sock=(ip, int(port)))
    trans.connect(username=username, password=passwd)

    try:
        sftp = paramiko.SFTPClient.from_transport(trans)
        sftp.get(log_file, log_path + log_file)
        sftp.close()
        return 0
    except Exception as e:
        print(e)
        return e


def line_count(log_file):
    '''
    错误文件行数统计
    '''
    count = 0
    for index, line in enumerate(open(log_file, 'r')):
        count += 1
    os.remove(log_file)
    return count


def msg_send(wx_url, count, wx_mobile=wx_mobile):
    '''
    发送企业微信消息
    '''
    data = {
        "msgtype": "text",
        "text": {
            "content": "任务：CMACAST卫星接收监控；告警信息：未完整接收文件个数--%i个；" % count,
            "mentioned_mobile_list": ["%s" % wx_mobile]
        },
    }
    header = {'Content-Type': 'application/json'}
    session = requests.session()
    session.post(wx_url, headers=header, json=data)


if __name__ == '__main__':
    log_name = datetime.now().strftime('recv%Y%m%d.err')
    down_result = file_down(log_file=log_name)
    if down_result == 0:
        file_count = line_count(log_name)
        if file_count > 10:
            wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s' % wx_key
            msg_send(wx_url=wx_url, count=file_count)
    else:
        print(down_result)
