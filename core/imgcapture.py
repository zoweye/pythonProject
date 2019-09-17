#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : 窗口截图方法封装
# @Author  : zwy
# @File    : imgcapture.py
# @Time    : 2019/9/9 10:02
# @Software: PyCharm
import os
import random
import sys
import time

import win32con
import win32gui
import win32ui
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication

from core import logtrace


def genRandomFileName(prefix: str, extention="jpg"):
    """
    生成随机文件名.

    :param prefix: 前缀字符串
    :param extention: 文件扩展名
    :return: 文件名
    """
    return "%s_%s_%s.%s" % (prefix, time.strftime("%Y%m%d%H%M%S"), random.randint(0, 10), extention)


def getFileAbsPath(path: str):
    """
    相对路径转绝对路径.

    :param path: 相对路径字符串
    :return: 返回绝对路径字符串
    """
    return os.path.abspath(path)


def win32CaptureImgSave(hwnd: int, imagePath: str = None, imageName: str = None):
    """
    win32API窗口截图保存方法，支持后台截图，窗口不可最小化.

    :param hwnd: 窗口句柄
    :param imgePath: bmp图片路径
    :param imageName: bmp图片文件名
    :return: 图片路径字符串
    """
    # 窗口句柄校验
    if not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")

    # 图片路径校验，不存在则新建
    if imagePath is None:
        imagePath = "./"
    else:
        if not os.path.exists(imagePath): os.mkdir(imagePath)

    # 图片文件名校验，不存在则生成随机名
    if imageName is None:
        imageName = genRandomFileName("win32", "bmp")
    else:
        if not imageName.lower().endswith(".bmp"):
            raise Exception("文件扩展名无效，只支持bmp格式扩展名")

    # 图片完整路径拼接
    imageURI = getFileAbsPath(imagePath + imageName)
    logtrace.logOut(imageURI)

    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 如果窗口处于最小化则激活窗口
    # if left < 0 and right < 0 and top < 0 and bot < 0:
    #     win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    #     win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SW_INVALIDATE, 0)
    #     time.sleep(3)

    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    ###保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC, imageURI)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)
    return imageURI


def pilCaptureImge(hwnd: int = 0):
    """
    PIL库截图方法，前台截图方式.

    :param hwnd: 窗口句柄，0代表整个屏幕
    :return: Image类型图片
    """
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")
    elif hwnd == 0:
        rect = None
    else:
        rect = win32gui.GetWindowRect(hwnd)
    return ImageGrab.grab(bbox=rect)


def pilCaptureImgeSave(hwnd: int = 0, imagePath: str = None, imageName: str = None):
    """
    PIL库截图保存方法，前台截图方式.

    :param hwnd: 窗口句柄，0代表整个屏幕
    :param imgePath: bmp图片路径
    :param imageName: bmp图片文件名
    :return: 图片路径字符串
    """
    # 窗口句柄校验
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")

    # 图片路径校验，不存在则新建
    if imagePath is None:
        imagePath = "./"
    else:
        if not os.path.exists(imagePath): os.mkdir(imagePath)

    # 图片文件名校验，不存在则生成随机名
    if imageName is None:
        imageName = genRandomFileName("pil", "bmp")
    else:
        if not imageName.lower().endswith(".bmp"):
            raise Exception("文件扩展名无效，只支持bmp格式扩展名")

    # 图片完整路径拼接
    imageURI = getFileAbsPath(imagePath + imageName)
    logtrace.logOut(imageURI)

    pilCaptureImge(hwnd).save(imageURI)
    return imageURI


def pyqtCaptureImge(hwnd: int = 0):
    """
    pyqt5窗口截图方法，支持后台截图方式，窗口不能最小化.

    :param hwnd: 窗口句柄，0代表整个屏幕
    :return: QImage图片
    """
    # 窗口句柄校验
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")
    return QApplication.primaryScreen().grabWindow(hwnd).toImage()


def pyqtCaptureImgeSave(hwnd: int = 0, imagePath: str = None, imageName: str = None):
    """
    pyqt5窗口截图保存方法，支持后台截图方式，窗口不能最小化.

    :param hwnd: 窗口句柄，0代表整个屏幕
    :param imgePath: bmp图片路径
    :param imageName: bmp图片文件名
    :return: 图片路径字符串
    """
    # 窗口句柄校验
    if hwnd != 0 and not win32gui.IsWindow(hwnd):
        raise Exception(str(hwnd) + "无效的窗口句柄。")

    # 图片路径校验，不存在则新建
    if imagePath is None:
        imagePath = "./"
    else:
        if not os.path.exists(imagePath): os.mkdir(imagePath)

    # 图片文件名校验，不存在则生成随机名
    if imageName is None:
        imageName = genRandomFileName("pyqt", "bmp")
    else:
        if not imageName.lower().endswith(".bmp"):
            raise Exception("文件扩展名无效，只支持bmp格式扩展名")

    # 图片完整路径拼接
    imageURI = getFileAbsPath(imagePath + imageName)
    logtrace.logOut(imageURI)

    pyqtCaptureImge(hwnd).save(imageURI)
    return imageURI
