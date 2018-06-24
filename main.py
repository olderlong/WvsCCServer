# import time
# from app.lib import *
# from app.cli_ui import CliApp
import app.web_ui

command = {
    "Type": "WVSCommand",
    "Data": {
        "Action": "StartNewScan",
        "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
            "StartURL":  "http://demo.testfire.net",
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
    # CliApp.run() # 类的静态方法在导入时已经调用

    # time.sleep(10)
    # common_msg.msg_server_command.data = command
    # # print("in run_server " + str(agent_event.event_wvs_command.dict))
    # msg_bus.send_msg(common_msg.msg_server_command)
    app.web_ui.socketio.run(app.web_ui.app, host="", port=80)
    # app.web_ui.app.run(port=80)

