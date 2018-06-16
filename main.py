import time
from app.lib import *
import app.cli_ui as cli_app
import app.web_ui

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
stop_scan_cmd = {
    "Type": "WVSCommand",
    "Data": {
        "Action": "StopScan",
    }
}


if __name__ == '__main__':
    cli_app.run()

    app.web_ui.app.run()
    time.sleep(10)
    common_msg.msg_server_command.data = command
    # print("in run_server " + str(agent_event.event_wvs_command.dict))
    msg_bus.send_msg(common_msg.msg_server_command)

    time.sleep(60)

    # common_msg.msg_server_command.data = stop_scan_cmd
    # msg_bus.send_msg(common_msg.msg_server_command)
