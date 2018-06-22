#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import render_template


def result():
    return render_template("result.html", title="扫描结果")