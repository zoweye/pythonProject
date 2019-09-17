#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : 日志跟踪
# @Author  : zwy
# @File    : logTrace.py
# @Time    : 2019/9/17 10:07
# @Software: PyCharm
import os
from datetime import datetime
from enum import unique, Enum

logFile = None

# LOG_OUT: 0表示print  1表示写日志文件
LOG_OUT_MODEL = 0
# log文件路径
LOG_OUT_FILE = None


@unique
class LogLevel(Enum):
    info = 0
    error = 1
    warn = 2


def logOut(logText: str, category: str = "", logLevel=LogLevel.info):
    """
    日志输出接口.

    :param logText: 日志内容
    :param category: 日志种类
    :param logLevel: 日志类型
    :return:
    """
    if LOG_OUT_MODEL == 0:  # 控制台输出
        print("[%s %s]: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], category, logText))
    else:  # 日志文件输出
        if os.path.exists(LOG_OUT_FILE):
            if logLevel == LogLevel.info:
                print("%s %s" % (logLevel, logText))
            elif logLevel == LogLevel.error:
                print(logText)
            elif logLevel == LogLevel.warn:
                print(logText)
            else:
                print(logText)
        else:
            pass
