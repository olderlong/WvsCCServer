#! /usr/bin/env python3
# _*_coding:utf-8 -*_
import time


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class WVSState:
    def __init__(self):
        self.wvs_state_list = []

    def has(self, state):
        identifier = "{}_{}".format(state["Name"], state["Address"][0])
        for i in range(len(self.wvs_state_list)):
            wvs_identifier = "{}_{}".format(self.wvs_state_list[i]["Name"], self.wvs_state_list[i]["Address"][0])
            if wvs_identifier == identifier:
                return True, i

        return False, -1

    def add_wvs_state(self, state):
        existed, index = self.has(state)
        if not existed:
            state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
            self.wvs_state_list.append(state)
        else:
            state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
            self.wvs_state_list[index] = state


    def get_wvs_state_list(self):
        return self.wvs_state_list

    def remove_agent(self, state):
        existed, index = self.has(state)
        if existed:
            self.wvs_state_list.remove(state)


@singleton
class AgentState(object):
    def __init__(self):
        self.agent_list = []

    def has(self, state):
        identifier = "{}_{}".format(state["Name"], state["Address"][0])
        for i in range(len(self.agent_list)):
            wvs_identifier = "{}_{}".format(self.agent_list[i]["Name"], self.agent_list[i]["Address"][0])
            if wvs_identifier == identifier:
                return True, i

        return False, -1

    def add_agent_state(self, state):
        existed, index = self.has(state)
        state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
        if not existed:
            self.agent_list.append(state)
        else:
            self.agent_list[index] = state

    def get_agent_list(self):
        return self.agent_list

    def remove_agent(self, state):
        existed, index = self.has(state)
        if existed:
            self.agent_list.remove(state)


if __name__ == '__main__':
        state = {
            "Name": "AppscanAgent",
            "Address": ["127.0.0.1", 6000],
            "Timestamp": 1529455672.7734838,
            "State": "Online"
        }
        print(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"])))

        agent_list = WVSState()
        agent_list.add_wvs_state(state)
        agent_list.add_wvs_state(state)
        agent_list.add_wvs_state(state)

        for state in agent_list.get_wvs_state_list():
            print(state)

