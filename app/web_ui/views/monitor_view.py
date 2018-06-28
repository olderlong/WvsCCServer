#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging
from flask import render_template

from app.web_ui import socketio
from app.lib import msg_bus, common_msg
from app.web_ui.server_config import ServerConfig
from app.web_ui.scan_session import ScanSetting, WVSState, AgentState
from app.server import AgentStateMonitor

logger = logging.getLogger("Server")
# agent_state_list = list(AgentStateMonitor().agent_state_dict.values())
all_agent_state = AgentState()
all_wvs_state = WVSState()



def monitor():
    # server_config = ServerConfig()
    # scan_config = ScanSetting()
    logger.info(all_agent_state.get_agent_list())
    return render_template(
        "monitor.html",
        title="监控中心",
        server_config=ServerConfig(),
        scan_config=ScanSetting(),
        agent_state_list=all_agent_state.get_agent_list(),
        wvs_state_list=all_wvs_state.get_wvs_state_list()
    )


def ws_agent_state_send(msg):
    agent_state = msg.data
    all_agent_state.add_agent_state(agent_state)
    socketio.emit(
        "agent_state_update",
        agent_state,
        namespace="/agent_state_ns"
    )

    logger.info("Send agent state: {}".format(agent_state))
    # socketio.emit(
    #     "agent_state_update",
    #     {
    #         "Name": "AppscanAgent",
    #         "Address": ["127.0.0.1", 6000],
    #         "Timestamp": 1529455672.7734838,
    #         "State": "Online"
    #     },
    #     namespace="/agent_state_ns"
    # )


def ws_wvs_state_send(msg):
    wvs_state = msg.data
    all_wvs_state.add_wvs_state(wvs_state)
    socketio.emit(
        "wvs_state_update",
        wvs_state,
        namespace="/wvs_state_ns"
    )
    logger.info("Send wvs state: {}".format(wvs_state))


@socketio.on("connect", namespace="/agent_state_ns")
def ws_agent_state_connect():
    msg_bus.add_msg_listener(common_msg.MSG_AGENT_STATE_UPDATE, ws_agent_state_send)
    logger.info("Agent state websocket is connected")
    # socketio.emit(
    #     "agent_state_update",
    #     {
    #         "Name": "AppscanAgent",
    #         "Address": ["127.0.0.1", 6000],
    #         "Timestamp": 1529455672.7734838,
    #         "State": "Online"
    #     },
    #     namespace="/agent_state_ns"
    # )


@socketio.on("connect", namespace="/wvs_state_ns")
def ws_wvs_state_connect():
    msg_bus.add_msg_listener(common_msg.MSG_WVS_STATE, ws_wvs_state_send)
    logger.info("Wvs state websocket is connected")

    # socketio.emit("wvs_state_update",
    #               {
    #                   "Name": "Appscan",
    #                   "AgentIP": "127.0.0.1",
    #                   "AgentPort": 5000,
    #                   "Time": 1271231231.100,
    #                   "State": "等待初始化"
    #               },
    #               namespace="/wvs_state_ns"
    #               )


@socketio.on("connect", namespace="/wvs_scan")
def wvs_scan_connect():
    logger.info("Wvs scan websocket is connected")


@socketio.on("wvs_scan_control", namespace="/wvs_scan")
def wvs_scan_control(data):
    command = data.get("Command")
    logger.info("Start scan with config: {}".format(command))
    if command == "start":
        setting = ScanSetting()
        start_scan_cmd = {
            "Type": "WVSCommand",
            "Data": {
                "Action": "StartNewScan",
                "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                    "StartURL": setting.start_url,
                    "ScanPolicy": setting.scan_policy
                }
            }
        }
        common_msg.msg_server_command.data = start_scan_cmd
        msg_bus.send_msg(common_msg.msg_server_command)
        logger.info("Start scan with config: {}".format(start_scan_cmd))
    elif command is "stop":
        stop_scan_cmd = {
            "Type": "WVSCommand",
            "Data": {
                "Action": "StopScan",
            }
        }
        common_msg.msg_server_command.data = stop_scan_cmd
        msg_bus.send_msg(common_msg.msg_server_command)
        logger.info("Start scan")
