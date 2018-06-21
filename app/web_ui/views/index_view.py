#! /usr/bin/env python
# _*_coding:utf-8 -*_

from app.lib import *
from flask import render_template


def start_scan():
    command = {
        "Type": "WVSCommand",
        "Data": {
            "Action": "StartNewScan",
            "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                # "StartURL": "http://192.168.1.28",
                "StartURL": "http://demo.testfire.net",
                "ScanPolicy": "Full"
            }
        }
    }
    common_msg.msg_server_command.data = command
    print("in run_server " + str(common_msg.msg_server_command.data))
    msg_bus.send_msg(common_msg.msg_server_command)

def index():
    return render_template("index.html",title="")