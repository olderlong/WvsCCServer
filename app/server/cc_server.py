#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import json
from app.lib import UDPEndPoint, msg_bus, common_msg
from app.server.agent_state_manager import AgentStateMonitor


class CCServer(UDPEndPoint):
    def __init__(self, port=6666):
        self.agent_list = []
        self.agent_state_monitor = AgentStateMonitor()

        msg_bus.add_msg_listener(common_msg.MSG_SERVER_COMMAND, self.send_command)
        super(CCServer, self).__init__(port=port, handler=self.receive_data_handler)

    def receive_data_handler(self, data, address):
        if address not in self.agent_list:
            self.agent_list.append(address)

        pkg_obj = dict(json.loads(str(data, encoding='utf-8')))
        try:
            if pkg_obj["Type"] == "Heartbeat":  #心跳包
                common_msg.msg_heartbeat.data = pkg_obj["Data"]
                msg_bus.send_msg(common_msg.msg_heartbeat)

                # self.heartbeat_handle(data)
            elif pkg_obj["Type"] == "WVSState":
                common_msg.msg_wvs_state.data = pkg_obj["Data"]
                msg_bus.send_event(common_msg.msg_wvs_state)
                # print("收到代理{}的漏扫状态数据".format(address))

            elif pkg_obj["Type"] == "ScanResult":
                common_msg.msg_scan_result_receive.data = pkg_obj["Data"]
                msg_bus.send_event(common_msg.msg_scan_result_receive)
                self.__print_scan_result(pkg_obj["Data"])
            else:
                print("收到来自{}的未知类型数据".format(address))
        except KeyError as e:
            print("收到来自{}的未知类型数据——{}".format(address, data))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __print_scan_result(self, vul_result):
        result_str = "漏洞类型:\t{}\n漏洞URL:\t{}\n漏洞等级:\t{}\n漏洞信息:\t".format(
            vul_result["VulType"],
            vul_result["VulUrl"],
            vul_result["VulSeverity"]
        )
        print(result_str)
        for info in vul_result["VulDetails"]:
            result_str = "\tURL参数变异:\t{}\n\t漏洞原因:\t{}\n\tCWE:\t{}\n\tCVE:\t{}".format(
                info["url_param_variant"],
                info["vul_reasoning"],
                info["CWE"],
                info["CVE"]
            )
            print(result_str)
        print("\r\n")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def send_command(self, msg):
        command_json = msg.data
        for address in self.agent_list:
            print(command_json, address)
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(self.agent_state_monitor.agent_state_dict.keys()):
                # print("in CCServer " + str(command_json))
                self.send_json_to(command_json, address)

    def send_config(self, msg):
        config_json = msg.data
        for address in self.agent_list:
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(self.agent_state_monitor.agent_state_dict.keys()):
                self.send_json_to(config_json, address)


if __name__ == '__main__':
    server = CCServer()
    server.start()
    server.stop()