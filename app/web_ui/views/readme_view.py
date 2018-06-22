#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import render_template


def readme():
    return render_template("readme.html", title="使用说明")