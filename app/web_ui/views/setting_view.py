#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging
from flask import render_template,request,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired,IPAddress,URL

from app.lib import msg_bus,common_msg
from app.cli_ui import CliApp
from app.web_ui.server_config import ServerConfig
from app.web_ui.scan_session import ScanSetting, ScanResult
from app.server import AgentStateMonitor
from app.web_ui.views import result_view as result_view

logger = logging.getLogger("Server")
agent_state_list = list(AgentStateMonitor().agent_state_dict.values())


class CCServerSettingForm(FlaskForm):
    CCServerIP = StringField("控制中心IP", validators=[IPAddress], default=ServerConfig.CC_SERVER_IP)
    CCServerPort = IntegerField("控制中心监听端口", validators=[DataRequired],default=ServerConfig.CC_SERVER_PORT)
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    CCProtocol = SelectField('通信协议', choices=[
        ('UDP', 'UDP'),
        ('TCP', 'TCP')
    ], default=ServerConfig.CC_PROTOCOL)

    submit_start = SubmitField('启动控制服务器')
    submit_stop = SubmitField('停止控制服务器')


class ScanSettingForm(FlaskForm):
    StartURL = StringField("起始URL", validators=[DataRequired, URL])
    # ScanPolicy = SelectField("扫描策略", validators=[DataRequired])
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    ScanPolicy = SelectField('扫描策略', choices=[
        ('Normal', 'Normal'),
        ('Quick', 'Quick'),
        ('Full', 'Full'),
    ], validators=[DataRequired])
    submit = SubmitField('确定')


def server_setting():
    server_setting_form = CCServerSettingForm()
    if server_setting_form.is_submitted():
        ccserver_ip = server_setting_form.CCServerIP.data
        ccserver_port = server_setting_form.CCServerPort.data
        ccserver_protocol = server_setting_form.CCProtocol.data

        logger.info("控制服务器参数：(IP:{}, Port：{}, Protocol：{})".format(
            ccserver_ip,
            ccserver_port,
            ccserver_protocol
        ))
        cli_app = CliApp(ip=ccserver_ip, port=ccserver_port, protocol=ccserver_protocol)
        if request.form.get("submit_start") == u"启动控制服务器":
            cli_app.run()

            ScanResult().wvs_result_list.clear()
            msg_bus.add_msg_listener(common_msg.MSG_SCAN_RESULT_RECEIVE, result_view.scan_result_handler)

            logger.info("控制服务器已启动：(IP:{}, Port：{}, Protocol：{})".format(
                ccserver_ip,
                ccserver_port,
                ccserver_protocol
                ))
        elif request.form.get("submit_stop") == u"停止控制服务器":
            cli_app.stop()

            logger.info("控制服务器已停止：(IP:{}, Port：{}, Protocol：{})".format(
                ccserver_ip,
                ccserver_port,
                ccserver_protocol
                ))

        return redirect(url_for("setting",title="配置中心",CCServerSettingForm=server_setting_form))
    else:
        return (url_for("setting"))


def scan_setting():
    scan_config = ScanSetting()
    scan_setting_form = ScanSettingForm()
    if scan_setting_form.is_submitted():
        scan_config.start_url = scan_setting_form.StartURL.data
        scan_config.scan_policy = scan_setting_form.ScanPolicy.data
        logger.info("扫描起始URL: {}, 扫描策略: {}".format(
            scan_config.start_url,
            scan_config.scan_policy
        ))
        # return redirect(url_for("setting",title="配置中心",ScanSettingForm=scan_setting_form))
        # return render_template("monitor.html", title="监控中心", scan_config=scan_config, server_config=ServerConfig())
        return render_template(
            "monitor.html",
            title="监控中心",
            scan_config=scan_config,
            server_config=ServerConfig(),
            agent_state_list=agent_state_list
        )
        # return redirect(url_for("monitor", title="监控中心", scan_config=scan_config, server_config=ServerConfig()))
    else:
        return (url_for("setting"))


def setting():
    server_setting_form = CCServerSettingForm()
    server_setting_form.CCServerIP.data = ServerConfig.CC_SERVER_IP
    server_setting_form.CCServerPort.data = ServerConfig.CC_SERVER_PORT
    server_setting_form.CCProtocol.data = ServerConfig.CC_PROTOCOL

    scan_config = ScanSetting()
    scan_setting_form = ScanSettingForm()
    scan_setting_form.StartURL.data = scan_config.start_url
    scan_setting_form.ScanPolicy.data = scan_config.scan_policy

    return render_template("setting.html", title="配置中心", CCServerSettingForm=server_setting_form, ScanSettingForm=scan_setting_form)