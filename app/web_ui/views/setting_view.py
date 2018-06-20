#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import render_template,request,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired,IPAddress,URL

def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

class CCServerSetting(FlaskForm):
    CCServerIP = StringField("控制中心IP", validators=[IPAddress],default="192.168.1.31")
    CCServerPort = IntegerField("控制中心监听端口", validators=[DataRequired],default=6000)
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    CCProtocol = SelectField('通信协议', choices=[
        ('UDP', 'UDP'),
        ('TCP', 'TCP')
    ],default="UDP")
    submit = SubmitField('启动控制服务器')


class ScanSetting(FlaskForm):
    StartURL = StringField("起始URL", validators=[DataRequired,URL])
    # ScanPolicy = SelectField("扫描策略", validators=[DataRequired])
    # Select类型，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    ScanPolicy = SelectField('扫描策略', choices=[
        ('Normal', 'Normal'),
        ('Quick', 'Quick'),
        ('Full', 'Full'),
    ], validators=[DataRequired])
    submit = SubmitField('确定')



@singleton
class ServerSetting:
    def __init__(self, ip = "192.168.1.31", port=6000 , protocol="UDP"):
        self.ccserver_ip = ip
        self.ccserver_port = port
        self.ccserver_protocol = protocol


@singleton
class ScanPolicy:
    def __init__(self, url="", policy="Normal"):
        self.start_url = url
        self.scan_policy = policy

server_set = ServerSetting()
scan_setting = ScanPolicy()

def server_setting():
    server_setting_form = CCServerSetting()
    if server_setting_form.is_submitted():
        server_set.ccserver_ip = server_setting_form.CCServerIP.data
        server_set.ccserver_port = server_setting_form.CCServerPort.data
        server_set.ccserver_protocol = server_setting_form.CCProtocol.data
        print(server_set.ccserver_ip)

        # return render_template("setting.html", title="配置中心", CCServerSettingForm=server_setting_form,
        #                        ScanSettingForm=scan_setting_form)
        return redirect(url_for("setting",title="配置中心",CCServerSettingForm=server_setting_form))
    else:
        return (url_for("setting"))

def scan_setting():
    server_setting_form = CCServerSetting()
    if server_setting_form.is_submitted():
        server_set.ccserver_ip = server_setting_form.CCServerIP.data
        server_set.ccserver_port = server_setting_form.CCServerPort.data
        server_set.ccserver_protocol = server_setting_form.CCProtocol.data
        print(server_set.ccserver_ip)

        # return render_template("setting.html", title="配置中心", CCServerSettingForm=server_setting_form,
        #                        ScanSettingForm=scan_setting_form)
        return redirect(url_for("setting",title="配置中心",CCServerSettingForm=server_setting_form))
    else:
        return (url_for("setting"))

def setting():
    server_setting_form = CCServerSetting()
    server_setting_form.CCServerIP.data = server_set.ccserver_ip
    server_setting_form.CCServerPort.data = server_set.ccserver_port
    server_setting_form.CCProtocol.data = server_set.ccserver_protocol

    scan_setting_form = ScanSetting()
    #
    # if server_setting_form.is_submitted():
    #     print(server_setting_form.CCServerIP.data)
    #     print(server_setting_form.CCServerPort.data)
    #     print(server_setting_form.CCProtocol.data)
    #
    # if scan_setting_form.is_submitted():
    #     print(scan_setting_form.StartURL.data)
    #     print(scan_setting_form.ScanPolicy.data)

    return render_template("setting.html", title="配置中心", CCServerSettingForm=server_setting_form, ScanSettingForm=scan_setting_form)