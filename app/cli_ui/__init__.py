#! /usr/bin/env python3
# _*_coding:utf-8 -*_
# import time
# from app.lib import *
from app.server import *

def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@singleton
class CliApp(object):
    def __init__(self,ip="127.0.0.1", port=6000, protocol="UDP"):
        self.__is_running = False
        self.server_ip = ip
        self.server_port = port

    def run(self):
        if self.__is_running:
            pass
        else:
            self.__is_running = True
            self.server = CCServer(ip=self.server_ip, port=self.server_port)
            self.agent_state_monitor = AgentStateMonitor()

            self.server.start()
            self.agent_state_monitor.start_monitor()

    def stop(self):
        self.__is_running = False
        self.server.stop()
        self.agent_state_monitor.stop_monitor()

    def is_running(self):
        return self.__is_running




# class CliApp:
#     server = None
#     agent_state_monitor = None
#
#     @staticmethod
#     def run():
#         # 类的静态方法在导入时已经调用
#         CliApp.server = CCServer()
#         CliApp.agent_state_monitor = AgentStateMonitor()
#
#         CliApp.server.start()
#         CliApp.agent_state_monitor.start_monitor()


__all__ = ["CliApp"]

