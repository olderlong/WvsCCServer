#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging
from flask import render_template
from app.web_ui import socketio
from app.web_ui.scan_session import ScanResult


logger = logging.getLogger("Server")
scan_result = ScanResult()

def scan_result_handler(msg):
    scan_res = msg.data

    # result = {
    #     'VulType': 'ApplicationTestScriptDetected',
    #     'VulUrl': 'http://192.168.3.10/zentao/theme/',
    #     'VulSeverity': 'Informational',
    #     'VulDetails': [
    #         {
    #             'url_param_variant': 'Method:  HEAD -> GET,Path:  /zentao/theme/default/zh-cn.default.css -> /zentao/theme/test.jsp',
    #             'vul_reasoning': 'AppScan 请求的文件可能不是应用程序的合法部分。响应状态为“200 OK”。这表示测试成功检索了所请求的文件的内容。',
    #             'CWE': None,
    #             'CVE': None
    #         }
    #     ]
    # }
    scan_result.add_scan_result(scan_res)
    existed = scan_result.has(scan_res)
    if not existed:
        logger.info("Recive result data:\t{}".format(scan_res))
    socketio.emit(
            "wvs_result_update",
            scan_res,
            namespace="/wvs_result"
        )


@socketio.on("connect", namespace="/wvs_result")
def wvs_result_connect():
    logger.info("Wvs result websocket is connected")


def result():
    return render_template("result.html", title="扫描结果", scan_result_list=scan_result.wvs_result_list)