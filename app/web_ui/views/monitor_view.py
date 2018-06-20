#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import render_template


def monitor():
    return render_template("monitor.html", title="监控中心")