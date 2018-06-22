#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging
from flask import render_template

from flask_socketio import SocketIO, emit
from app.web_ui import socketio
from app.lib import msg_bus, common_msg


logger = logging.getLogger("Server")


def monitor():
    return render_template("monitor.html", title="监控中心")


def ws_agent_state_send(msg):
    agent_state = msg.data
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
