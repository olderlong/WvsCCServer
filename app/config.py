#! /usr/bin/env python3
# _*_coding:utf-8 -*_
import psutil


def get_host_ip():
    info = psutil.net_if_addrs()
    # print(info)
    for k, v in info.items():
        if str(k).startswith("以太网") or str(k).startswith("eth") or str(k).startswith("本地连接"):
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    return item[1]
        else:
            return "127.0.0.1"


class Configure(object):
    Address = (get_host_ip(), 6000)


