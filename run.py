import time
from app.lib import *
from app.server import *

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
    # for _ in range(10):
    #     msg_bus.send_msg(common_msg.msg_server_command)
    #
    # time.sleep(5)

    server = CCServer()
    server.start()
    agent_state_monitor = AgentStateMonitor()
    agent_state_monitor.start_monitor()

    command = {
        "Type": "WVSCommand",
        "Data": {
            "Action": "StartNewScan",
            "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                "StartURL": "http://192.168.3.10",
                "ScanPolicy": "Normal"
            }
        }
    }
    time.sleep(15)
    common_msg.msg_server_command.data = command
    # print("in run_server " + str(agent_event.event_wvs_command.dict))
    msg_bus.send_msg(common_msg.msg_server_command)

    time.sleep(50)
    server.stop()