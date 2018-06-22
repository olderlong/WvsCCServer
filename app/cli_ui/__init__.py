import threading
from app.server import *


def __start_ccserver():
    server = CCServer()
    server.start()
    agent_state_monitor = AgentStateMonitor()
    agent_state_monitor.start_monitor()
    server.join()

def run():
    threading.Thread(target=__start_ccserver).start()
