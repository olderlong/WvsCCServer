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



if __name__ == '__main__':


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
                "ScanPolicy": "Full"
            }
        }
    }
    time.sleep(10)
    common_msg.msg_server_command.data = command
    # print("in run_server " + str(agent_event.event_wvs_command.dict))
    msg_bus.send_msg(common_msg.msg_server_command)

    time.sleep(60)
    stop_scan_cmd = {
        "Type": "WVSCommand",
        "Data": {
            "Action": "StopScan",
        }
    }
    common_msg.msg_server_command.data = stop_scan_cmd
    # print("in run_server " + str(agent_event.event_wvs_command.dict))
    msg_bus.send_msg(common_msg.msg_server_command)

    server.join()
    # server.stop()