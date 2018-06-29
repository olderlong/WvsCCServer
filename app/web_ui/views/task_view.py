#! /usr/bin/env python3
# _*_coding:utf-8 -*_

from flask import render_template,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired,IPAddress,URL

from app.web_ui.scan_task_manager import *
from app.web_ui import app
from app.lib import msg_bus, common_msg


task_info = {
    "TaskName":"",
    "ScanSetting": {
        "StartURL": "http://127.0.0.1",
        "ScanPolicy": "Normal"
    },
    "ScanResultFile": "scan_result.json",
    "Timestamp": 1529455672.7734838
}
task_manager = ScanTaskManager()

def get_task_info_list():
    task_manager = ScanTaskManager()
    task_list = task_manager.scan_task_list
    task_info_list = []
    if len(task_list):
        for task in task_list:
            task_info, _, _ = task_manager.get_task_info(task[0])
            task_info_dict = task_info.get_task_info_dict()
            task_info_dict["TaskName"]=task[0]
            task_info_dict["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(float(task_info_dict["Timestamp"])))
            task_info_list.append(task_info_dict)

    return task_info_list

class NewTaskForm(FlaskForm):
    Name = StringField("任务名称", validators=[DataRequired], default="Task_Name")
    StartURL = StringField("起始URL", validators=[DataRequired, URL], default="http://www.demo.net")
    # ScanPolicy = SelectField("扫描策略", validators=[DataRequired])
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    ScanPolicy = SelectField('扫描策略', choices=[
        ('Normal', 'Normal'),
        ('Quick', 'Quick'),
        ('Full', 'Full'),
    ], validators=[DataRequired],default=ScanSetting().scan_policy)
    submit = SubmitField('新建任务')

@app.route("/task/new", endpoint="task_new", methods=('GET', 'POST'))
def new_task():
    new_task_form = NewTaskForm()
    if new_task_form.is_submitted():
        task_name = new_task_form.Name.data
        task_manager.add_new_task(task_name)
        ScanSetting().set_scan_setting(new_task_form.StartURL.data, new_task_form.ScanPolicy.data)
        logger.info(ScanSetting().get_scan_setting())
        logger.info("新任务信息>>  任务名称:{},URL:{}, 策略:{}".format(task_name, new_task_form.StartURL.data,
                                                            new_task_form.ScanPolicy.data))
        ScanResult().clear_result_list()
        task_manager.save_task(task_name)
        return redirect(url_for("task"))

@app.route("/task/restart/<task_name>",endpoint="task_start", methods=('GET', 'POST'))
def start_task(task_name):
    if task_name:
        task_manager.get_task_info(task_name)
        ScanResult().wvs_result_list.clear()
        task_manager.save_task(task_name)
        start_scan_cmd = {
            "Type": "WVSCommand",
            "Data": {
                "Action": "StartNewScan",
                "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                    "StartURL": ScanSetting().start_url,
                    "ScanPolicy": ScanSetting().scan_policy
                }
            }
        }
    common_msg.msg_server_command.data = start_scan_cmd
    msg_bus.send_msg(common_msg.msg_server_command)
    logger.info("Start scan with config: {}".format(start_scan_cmd))
    return redirect(url_for("monitor"))


@app.route("/task/del/<task_name>", endpoint="task_delete", methods=('GET', 'POST'))
def delete_task(task_name):
    if task_name:
        task_manager.del_task(task_name)
        return redirect(url_for("task"))
        # return render_template("task.html", title="任务管理", task_info_list=get_task_info_list())

@app.route("/task/<task_name>", endpoint="task_result", methods=('GET', 'POST'))
def show_result(task_name):
    if task_name:
        _,_, result_list = task_manager.get_task_info(task_name)
        logger.info(result_list)
        return render_template("result.html", title="扫描结果", scan_result_list=result_list)

@app.route("/task", endpoint="task", methods=('GET', 'POST'))
def task():
    new_task_form = NewTaskForm()
    task_info_list = get_task_info_list()
    logger.info("任务列表：{}".format(task_info_list))
    return render_template("task.html", title="任务管理",task_info_list=task_info_list, new_task_form=new_task_form)