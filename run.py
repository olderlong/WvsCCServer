import time
from app.lib import *

command = {
    "Type": "WVSCommand",
    "Data": {
        "Action": "StartNewScan",
        "Config": {
            "StartURL": "http://www.cnblog.com",
            "ScanPolicy": "Normal"
        }
    }
}

def listener(msg):
    print(time.time())
    json_obj = msg.data
    print(json_obj)


if __name__ == '__main__':
    msg_bus.add_msg_listener(common_msg.MSG_SERVER_COMMAND, listener)

    time.sleep(1)

    common_msg.msg_server_command.data = command
    for _ in range(10):
        msg_bus.send_msg(common_msg.msg_server_command)

    time.sleep(5)