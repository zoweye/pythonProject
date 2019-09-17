#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : 描述
# @Author  : zwy
# @File    : win.py
# @Time    : 2019/9/9 10:29
# @Software: PyCharm
import win32gui


def getWindowRect(hwnd: int):
    """
    获取窗口矩形区域.

    :param hwnd: 窗口句柄
    :return: 元组(左上X坐标,左上Y坐标,宽度,高度)
    """
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    return (left, top, width, height)


def getClientRect(hwnd: int):
    """
    获取客户矩形区.

    :param hwnd: 窗口句柄
    :return: 元组(左上X坐标,左上Y坐标,宽度,高度)
    """
    # 获取句柄客户区的大小信息
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bot - top
    return (left, top, width, height)


def clientToScreen(hwnd: int, cx, cy):
    """
    客户区坐标转屏幕坐标

    :param hwnd: 窗口句柄
    :param cx: 客户区坐标x
    :param cy: 客户区坐标y
    :return: 元组(屏幕坐标x，屏幕坐标y)
    """
    # 窗口句柄校验
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")
    sx, sy = win32gui.ClientToScreen(hwnd, (cx, cy))
    return (sx, sy)


def screenToClient(hwnd: int, sx, sy):
    """
    客户区坐标转屏幕坐标

    :param hwnd: 窗口句柄
    :param sx: 屏幕坐标x
    :param sy: 屏幕坐标y
    :return: 元组(客户区坐标x，客户区坐标y)
    """
    # 窗口句柄校验
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")
    cx, cy = win32gui.ScreenToClient(hwnd, (sx, sy))
    return (cx, cy)


def WindowFromMouse():
    """
    获取鼠标点窗口句柄.

    :return: 窗口句柄hwnd
    """
    (mx, my) = win32gui.GetCursorPos()
    return win32gui.WindowFromPoint((mx, my))
