# import time
# from app.lib import *
from app.server import *



class CliApp:
    server = None
    agent_state_monitor = None

    @staticmethod
    def run():
        # 类的静态方法在导入时已经调用
        CliApp.server = CCServer()
        CliApp.agent_state_monitor = AgentStateMonitor()

        CliApp.server.start()
        CliApp.agent_state_monitor.start_monitor()


__all__ = ["CliApp"]