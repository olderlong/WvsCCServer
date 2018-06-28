#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import Flask
from flask_socketio import SocketIO


def create_web_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SECRET_KEY"] = "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    return app


app = create_web_app()
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


from app.web_ui.views import *
app.add_url_rule(rule="/", endpoint="index", view_func=index)
# app.add_url_rule(rule="/task<action>", endpoint="task", view_func=task, methods=('GET', 'POST'))
app.add_url_rule(rule="/setting", endpoint="setting", view_func=setting, methods=('GET', 'POST'))
app.add_url_rule(rule="/server_setting", endpoint="server_setting", view_func=server_setting,methods=('GET', 'POST'))
app.add_url_rule(rule="/scan_setting", endpoint="scan_setting", view_func=scan_setting, methods=('GET', 'POST'))
app.add_url_rule(rule="/monitor", endpoint="monitor", view_func=monitor)
app.add_url_rule(rule="/result", endpoint="result", view_func=result)
app.add_url_rule(rule="/readme", endpoint="readme", view_func=readme)


__all__ = ["app", "socketio"]