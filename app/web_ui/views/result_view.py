#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging, os
from flask import render_template, send_from_directory, send_file
from app.web_ui import socketio
from app.web_ui.scan_task_manager import ScanResult,ScanSetting, ScanTaskManager
from app.web_ui.gen_report_file import GenReport
from app.web_ui import app


logger = logging.getLogger("Server")
scan_result = ScanResult()


@app.route("/report/<timestramp>", endpoint="report", methods=['GET'])
def report(timestramp):
    gen_report = GenReport()
    gen_report.gen_report()
    return send_file(os.path.join(gen_report.report_path, gen_report.report_file_name), as_attachment=True)
    # return send_from_directory(gen_report.report_path, gen_report.report_file_name, as_attachment=True)


@app.route("/result/save")
def save_result():
    stm = ScanTaskManager()
    logger.info("保存任务{}".format(ScanSetting().scan_name))
    # stm.add_new_task(ScanSetting().scan_name)
    stm.save_task(ScanSetting().scan_name)

    logger.info("任务列表：{}".format(stm.scan_task_list))

    return render_template("result.html", title="扫描结果", scan_result_list=scan_result.wvs_result_list)


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