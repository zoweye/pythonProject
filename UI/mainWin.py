#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : 主窗口程序 - 逻辑层
# @Author  : zwy
# @File    : mainWin.py
# @Time    : 2019/9/9 22:25
# @Software: PyCharm
import os
import random
import sys
import time
import traceback
from xml.etree.ElementTree import ElementTree, Element

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QRegExp, QPoint
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QRegExpValidator, QColor, QCursor, QContextMenuEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QCompleter, QMessageBox, QItemDelegate, QHeaderView, \
    QTableView, QMenu

from const import const
from UI.mainUI import Ui_MainWindow
from core import xml, logtrace
from widget.combobox import ExtendedComboBox


class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWin, self).__init__()
        self.setupUi(self)

        # 控件初始化及设置
        self.widgetInit()

        # 添加事件
        self.tab2_nodeRefleshpushButton.clicked.connect(self.tab2_nodetableViewRefleshMenu)
        self.tab2_nodeDelpushButton.clicked.connect(self.tab2_nodetableViewDelMenu)
        self.tab2_nodetableView.doubleClicked.connect(self.tab2_nodetableViewDoubleClick)

        self.tab2_funRefleshpushButton.clicked.connect(self.tab2_mainFunctableViewRefleshMenu)
        self.tab2_funAddpushButton.clicked.connect(self.tab2_mainFunctableViewAddMenu)
        self.tab2_funSavepushButton.clicked.connect(self.tab2_mainFunctableViewSaveMenu)
        self.tab2_funDelpushButton.clicked.connect(self.tab2_mainFunctableViewDelMenu)

        self.tab3_picOpenpushButton.clicked.connect(self.tab3_picOpenpushButtonClick)
        self.tab3_keyAddpushButton.clicked.connect(self.tab3_keyAddpushButtonClick)
        self.tab3_keySavepushButton.clicked.connect(self.tab3_keySavepushButtonClick)
        self.tab3_mouseAddpushButton.clicked.connect(self.tab3_mouseAddpushButtonClick)
        self.tab3_mouseSavepushButton.clicked.connect(self.tab3_mouseSavepushButtonClick)

        # tableView右键菜单信号与槽
        self.tab2_nodetableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab2_nodetableView.customContextMenuRequested.connect(self.tab2_nodetableViewMenuRequested)
        self.tab2_mainFuntableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab2_mainFuntableView.customContextMenuRequested.connect(self.tab2_mainFuntableViewMenuRequested)
        self.tab2_detailFuntableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab2_detailFuntableView.customContextMenuRequested.connect(self.tab2_detailFuntableViewMenuRequested)

        # 初始化功能
        self.load()

    def widgetInit(self):
        # ===========================
        #   tab2 控件设置
        # ===========================

        # 初始化UI - tab2_nodetableView ###
        self.nodeShowLabel = {"rowId": "节点ID", "name": "节点名称", "desc": "节点描述", "nodeType": "类型"}
        self.initTableUI(self.tab2_nodetableView, self.nodeShowLabel)

        # 初始化UI - tab2_mainFuntableView
        self.funcMainShowLabel = {"rowId": "功能ID", "name": "功能名称", "desc": "功能描述"}
        self.initTableUI(self.tab2_mainFuntableView, self.funcMainShowLabel)

        # 初始化UI - tab2_detailFuntableView
        self.funcDetailShowLabel = {"rowId": "节点ID", "name": "节点名称", "desc": "节点描述"}
        self.initTableUI(self.tab2_detailFuntableView, self.funcDetailShowLabel)

        # 初始化UI - tab1_funtableView ###
        self.funcShowLabel = {"rowId": "功能ID", "name": "功能名称", "desc": "功能描述"}
        self.initTableUI(self.tab1_funtableView, self.funcShowLabel)

        # 初始化UI - tab1_mainMissiontableView
        self.taskMainShowLabel = {"rowId": "任务ID", "name": "任务名称", "desc": "任务描述"}
        self.initTableUI(self.tab1_mainMissiontableView, self.taskMainShowLabel)

        # 初始化UI - tab1_detailMissiontableView
        self.taskDetailShowLabel = {"rowId": "功能ID", "name": "功能名称", "desc": "功能描述"}
        self.initTableUI(self.tab1_detailMissiontableView, self.taskDetailShowLabel)

        # 初始化UI - tab0_missiontableView ###
        self.taskShowLabel = {"rowId": "任务ID", "name": "任务名称", "desc": "任务描述"}
        self.initTableUI(self.tab0_missiontableView, self.taskShowLabel)

        # 初始化UI - tab0_mainThreadtableView
        self.threadMainShowLabel = {"rowId": "线程ID", "name": "线程名称", "desc": "线程描述"}
        self.initTableUI(self.tab0_mainThreadtableView, self.threadMainShowLabel)

        # 初始化UI - tab0_detailThreadtableView
        self.threadDetailShowLabel = {"rowId": "任务ID", "name": "任务名称", "desc": "任务描述"}
        self.initTableUI(self.tab0_detailThreadtableView, self.threadDetailShowLabel)

        # ===========================
        #   tab3 控件设置
        # ===========================
        # ExtendedComboBox控件添加 - tab3_keySelectcomboBox
        self.tab3_keySelectcomboBox = ExtendedComboBox(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab3_keySelectcomboBox.sizePolicy().hasHeightForWidth())
        self.tab3_keySelectcomboBox.setSizePolicy(sizePolicy)
        self.tab3_keySelectcomboBox.setEditable(True)
        self.tab3_keySelectcomboBox.setObjectName("tab3_keySelectcomboBox")
        self.tab3_keySelectcomboBox.addItems(const.KEYMAP)
        self.horizontalLayout_5.addWidget(self.tab3_keySelectcomboBox)

        # tab3_mouseXlineEdit:限制只输入数字
        self.tab3_mouseXlineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))
        # tab3_mouseXlineEdit:限制只输入数字
        self.tab3_mouseYlineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))
        # tab3_mouseDelaylineEdit:限制只输入数字
        self.tab3_mouseDelaylineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))

        # tab3_keyDelaylineEdit:限制只输入数字
        self.tab3_keyDelaylineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]+$")))

    def initTableUI(self, tableView: QTableView, showLabel: dict, isSortable=True):
        """
        初始化tableview显示.

        :param tableView: tableview对象
        :param showLabel: 列标题dict
        :param isSortable: 列是否可以排序
        :return:
        """
        if len(showLabel) > 0:
            # 设置模型及标题
            model = QStandardItemModel()
            model.setColumnCount(len(showLabel))
            for cindex, value in enumerate(showLabel.values()):
                model.setHeaderData(cindex, Qt.Horizontal, value)
            tableView.setModel(model)

            # 设置自适应列宽
            tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tableView.horizontalHeader().setMinimumSectionSize(100)
            tableView.setSortingEnabled(isSortable)

    def load(self):
        """
        窗口初始化后功能.

        :return:
        """
        # xml配置文件加载(不存在新增)
        self.xmlConf = xmlConfig("./conf.xml")

        # tableView模型初始化
        self.reloadModelFromXmlConf()

        # 日志文件加载

    def rebuildTableRowNum(self, tableView: QTableView):
        """
        重建tableview行号
        :return:
        """
        model = tableView.model()
        # 设置行数据
        for rindex in range(model.rowCount()):
            model.setHeaderData(rindex, Qt.Vertical, rindex)

    def tab2_nodetableViewMenuRequested(self, point: QPoint):
        """
        右键菜单事件.

        :param point: 右键鼠标坐标
        :return:
        """
        self.statusbar.showMessage("右键菜单 [%s,%s]" % (point.x(), point.y()))

        try:
            menu = QMenu()
            menu.addAction("刷新").triggered.connect(self.tab2_nodetableViewRefleshMenu)
            menu.addSeparator()
            menu.addAction("删除").triggered.connect(self.tab2_nodetableViewDelMenu)
            menu.addAction("添加至功能").triggered.connect(self.tab2_nodetableViewAddFuncMenu)
            menu.exec(QCursor.pos())
        except Exception as e:
            traceback.print_exc()

    def tab2_mainFuntableViewMenuRequested(self, point: QPoint):
        """
        右键菜单事件.

        :param point: 右键鼠标坐标
        :return:
        """
        self.statusbar.showMessage("右键菜单 [%s,%s]" % (point.x(), point.y()))

        try:
            menu = QMenu()
            menu.addAction("刷新").triggered.connect(self.tab2_mainFunctableViewRefleshMenu)
            menu.addSeparator()
            menu.addAction("新增").triggered.connect(self.tab2_mainFunctableViewAddMenu)
            menu.addAction("保存").triggered.connect(self.tab2_mainFunctableViewSaveMenu)
            menu.addAction("删除").triggered.connect(self.tab2_mainFunctableViewDelMenu)
            menu.exec(QCursor.pos())
        except Exception as e:
            traceback.print_exc()

    def tab2_detailFuntableViewMenuRequested(self, point: QPoint):
        """
        右键菜单事件.

        :param point: 右键鼠标坐标
        :return:
        """
        self.statusbar.showMessage("右键菜单 [%s,%s]" % (point.x(), point.y()))

        try:
            pass
        except Exception as e:
            traceback.print_exc()

    def tab2_nodetableViewDoubleClick(self):
        """
        节点tableview-双击.

        :return:
        """
        modelIndex = self.tab2_nodetableView.currentIndex()
        self.statusbar.showMessage("双击行 [%s]" % modelIndex.row())

        try:
            pass
        except Exception as e:
            traceback.print_exc()

    def tab2_nodetableViewRefleshMenu(self, checked=False):
        """
        单击菜单 - 刷新.

        :return:
        """
        self.statusbar.showMessage("单击 [刷新]")

        try:
            self.xmlConf.reloadXml()
            self.refleshNodeModel()
        except Exception as e:
            traceback.print_exc()

    def tab2_nodetableViewDelMenu(self, checked=False):
        """
        单击菜单 - 删除.

        :return:
        """
        self.statusbar.showMessage("单击 [删除]")

        try:
            modelIndexList = self.tab2_nodetableView.selectionModel().selectedRows()
            if len(modelIndexList) > 0:
                # 考虑到移除行行索引会变，从后往前移行
                for modexIndex in modelIndexList[::-1]:
                    cindex = self.getIndexFromCaption(modexIndex.model(), self.nodeShowLabel["rowId"])
                    idText = modexIndex.model().index(modexIndex.row(), cindex).data()
                    self.tab2_nodetableView.model().removeRow(modexIndex.row())
                    self.xmlConf.delNodeNode(idText)
                    logtrace.logOut("%s %s" % (modexIndex.row(), idText), "delRow")

                # 重建行号
                self.rebuildTableRowNum(self.tab2_nodetableView)
            else:
                QMessageBox.information(self, "提示信息", "未选中行数据！", QMessageBox.Ok)
        except Exception as e:
            traceback.print_exc()

        self.statusbar.showMessage("删除节点成功")

    def tab2_nodetableViewAddFuncMenu(self, checked=False):
        """
        单击菜单 - 添加至功能.

        :return:
        """
        self.statusbar.showMessage("单击 [添加至功能]")

        try:
            modelIndexList = self.tab2_nodetableView.selectionModel().selectedRows()
            if len(modelIndexList) > 0:
                pass
            else:
                QMessageBox.information(self, "提示信息", "未选中行数据！", QMessageBox.Ok)
        except Exception as e:
            traceback.print_exc()

    def tab2_mainFunctableViewRefleshMenu(self, checked=False):
        """
        单击菜单 - 刷新.

        :return:
        """
        self.statusbar.showMessage("单击 [刷新]")

        try:
            self.xmlConf.reloadXml()
            self.refleshFunctionModel()
        except Exception as e:
            traceback.print_exc()

    def tab2_mainFunctableViewAddMenu(self, checked=False):
        """
        单击菜单 - 新增.

        :return:
        """
        self.statusbar.showMessage("单击 [新增]")

        try:
            # 新增功能
            self.xmlConf.addFunctionNode({"name": "功能名", "desc": "功能描述"})
            # 刷新功能模型
            self.refleshFunctionModel()
        except Exception as e:
            traceback.print_exc()

    def tab2_mainFunctableViewSaveMenu(self, checked=False):
        """
        单击菜单 - 保存.

        :return:
        """
        self.statusbar.showMessage("单击 [保存]")

        try:
            modelIndexList = self.tab2_mainFuntableView.selectionModel().selectedRows()
            if len(modelIndexList) > 0:
                for modelIndex in modelIndexList:
                    # 获取单元格值 - rowId
                    rowIdIndex = self.getIndexFromCaption(modelIndex.model(), self.funcShowLabel["rowId"])
                    rowIdText = modelIndex.model().index(modelIndex.row(), rowIdIndex).data()
                    # 获取单元格值 - name
                    nameIndex = self.getIndexFromCaption(modelIndex.model(), self.funcShowLabel["name"])
                    nameText = modelIndex.model().index(modelIndex.row(), nameIndex).data()
                    # 获取单元格值 - desc
                    descIndex = self.getIndexFromCaption(modelIndex.model(), self.funcShowLabel["desc"])
                    descText = modelIndex.model().index(modelIndex.row(), descIndex).data()

                    # 修改节点值
                    attrs = {"rowId": rowIdText, "name": nameText, "desc": descText}
                    logtrace.logOut(attrs, "saveFunc")
                    self.xmlConf.changeFunctionNode(rowIdText, attrs)
                    self.refleshFunctionModel()
            else:
                QMessageBox.information(self, "提示信息", "未选中行数据！", QMessageBox.Ok)
        except Exception as e:
            traceback.print_exc()

    def tab2_mainFunctableViewDelMenu(self, checked=False):
        """
        单击菜单 - 删除.

        :return:
        """
        self.statusbar.showMessage("单击 [删除]")

        try:
            modelIndexList = self.tab2_mainFuntableView.selectionModel().selectedRows()
            if len(modelIndexList) > 0:
                # 考虑到移除行行索引会变，从后往前移行
                for modexIndex in modelIndexList[::-1]:
                    cindex = self.getIndexFromCaption(modexIndex.model(), self.funcShowLabel["rowId"])
                    idText = modexIndex.model().index(modexIndex.row(), cindex).data()
                    self.tab2_mainFuntableView.model().removeRow(modexIndex.row())
                    self.xmlConf.delFunctionNode(idText)
                    logtrace.logOut("%s %s" % (modexIndex.row(), idText), "delRow")

                # 重建行号
                self.rebuildTableRowNum(self.tab2_mainFuntableView)
            else:
                QMessageBox.information(self, "提示信息", "未选中行数据！", QMessageBox.Ok)
        except Exception as e:
            traceback.print_exc()

    def tab3_picOpenpushButtonClick(self):
        """
        图片按钮-单击.

        :return:
        """
        self.statusbar.showMessage("单击 [%s]" % self.tab3_picOpenpushButton.text())

        try:
            filePath, fileType = QFileDialog.getOpenFileName(self, "选择图片", "./", "图片(*.jpg;*.png;*.bmp)")
            if os.path.exists(filePath):
                self.statusbar.showMessage("打开图片 [%s]" % filePath)
                self.tab3_picPathlineEdit.setText(filePath)
                self.tab3_picShowlabel.setPixmap(QPixmap(filePath))
        except Exception as e:
            traceback.print_exc()

    def tab3_keyAddpushButtonClick(self):
        """
        按键新增节点-单击.

        :return:
        """
        self.statusbar.showMessage("单击 [%s]" % self.tab3_keyAddpushButton.text())

        try:
            nodeType = "key"
            keyName = self.tab3_keyNamelineEdit.text()
            keySelect = self.tab3_keySelectcomboBox.currentText()
            keyDelay = self.tab3_keyDelaylineEdit.text()
            keyDesc = "按键[%s] 延迟[%s]" % (keySelect, keyDelay)
            # 校验值
            if keyName.strip() == "":
                QMessageBox.critical(self, "错误消息", "节点名称值无效！请重新输入！", QMessageBox.Ok)
                return
            elif keySelect.strip() == "":
                QMessageBox.critical(self, "错误消息", "按键值无效！请重新输入！", QMessageBox.Ok)
                return
            elif keyDelay.strip() == "":
                QMessageBox.critical(self, "错误消息", "延迟值无效！请重新输入！", QMessageBox.Ok)
                return

            # 新增节点
            self.currKeyNode = {"nodeType": nodeType, "name": keyName, "desc": keyDesc, "key": keySelect,
                                "delay": keyDelay}
            self.xmlConf.addNodeNode(self.currKeyNode)
            # 刷新节点模型
            self.refleshNodeModel()

            # 切换tab2显示
            # self.tabWidget.setCurrentIndex(2)
        except Exception as e:
            traceback.print_exc()

        self.statusbar.showMessage("新增节点成功")

    def tab3_keySavepushButtonClick(self):
        """
        按键保存节点-单击.

        :return:
        """
        self.statusbar.showMessage("单击 [%s]" % self.tab3_keySavepushButton.text())

        try:
            # 存在成员属性且存在内容
            if not hasattr(self, "currKeyNode"): return
            if len(self.currKeyNode) == 0: return

            keyName = self.tab3_keyNamelineEdit.text()
            keySelect = self.tab3_keySelectcomboBox.currentText()
            keyDelay = self.tab3_keyDelaylineEdit.text()
            keyDesc = "按键[%s] 延迟[%s]" % (keySelect, keyDelay)
            # 校验值
            if keyName.strip() == "":
                QMessageBox.critical(self, "错误消息", "节点名称值无效！请重新输入！", QMessageBox.Ok)
                return
            elif keySelect.strip() == "":
                QMessageBox.critical(self, "错误消息", "按键值无效！请重新输入！", QMessageBox.Ok)
                return
            elif keyDelay.strip() == "":
                QMessageBox.critical(self, "错误消息", "延迟值无效！请重新输入！", QMessageBox.Ok)
                return

            self.currKeyNode["name"] = keyName
            self.currKeyNode["key"] = keySelect
            self.currKeyNode["delay"] = keyDelay
            self.currKeyNode["desc"] = keyDesc
            logtrace.logOut(self.currKeyNode)
            self.xmlConf.changeNodeNode(self.currKeyNode["rowId"], self.currKeyNode)
            self.refleshNodeModel()

            # 切换tab2显示
            # self.tabWidget.setCurrentIndex(2)
        except Exception as e:
            traceback.print_exc()

        self.statusbar.showMessage("保存按键节点[%s]成功" % self.currKeyNode["rowId"])

    def tab3_mouseAddpushButtonClick(self):
        """
        鼠标新建节点-单击.

        :return:
        """
        self.statusbar.showMessage("单击 [%s]" % self.tab3_mouseAddpushButton.text())

        try:
            pass
        except Exception as e:
            traceback.print_exc()

    def tab3_mouseSavepushButtonClick(self):
        """
        鼠标保存节点-单击.

        :return:
        """
        self.statusbar.showMessage("单击 [%s]" % self.tab3_mouseSavepushButton.text())

        try:
            pass
        except Exception as e:
            traceback.print_exc()

    def reloadModelFromXmlConf(self):
        self.refleshNodeModel()
        self.refleshFunctionModel()
        self.refleshTaskModel()
        self.refleshThreadModel()

    def refleshFunctionModel(self):
        nodeList = self.xmlConf.convertFunctionToModel()
        logtrace.logOut("%s" % nodeList, "refleshFuncModel")
        # 显示列标题
        if len(nodeList) > 0:
            model = self.tab2_mainFuntableView.model()

            # 设置行数据
            model.setRowCount(len(nodeList))
            for rindex, rowdata in enumerate(nodeList):
                model.setHeaderData(rindex, Qt.Vertical, rindex)
                for cindex, key in enumerate(self.funcShowLabel.keys()):
                    if key in rowdata:
                        item = QStandardItem(rowdata[key])
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    else:
                        item = QStandardItem("")
                    model.setItem(rindex, cindex, item)
        else:
            # 清空tableview数据
            model = self.tab2_mainFuntableView.model()
            model.removeRows(0, model.rowCount())

    def refleshNodeModel(self):
        nodeList = self.xmlConf.convertNodeToModel()
        logtrace.logOut("%s" % nodeList, "refleshNodeModel")
        # 显示列标题
        if len(nodeList) > 0:
            model = self.tab2_nodetableView.model()

            # 设置行数据
            model.setRowCount(len(nodeList))
            for rindex, rowdata in enumerate(nodeList):
                model.setHeaderData(rindex, Qt.Vertical, rindex)
                for cindex, key in enumerate(self.nodeShowLabel.keys()):
                    if key in rowdata:
                        item = QStandardItem(rowdata[key])
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    else:
                        item = QStandardItem("")
                    model.setItem(rindex, cindex, item)
        else:
            # 清空tableview数据
            model = self.tab2_nodetableView.model()
            model.removeRows(0, model.rowCount())

    def refleshTaskModel(self):
        pass

    def refleshThreadModel(self):
        pass

    def getIndexFromCaption(self, model: QStandardItemModel, caption: str):
        """
        获取指定列标题的索引.

        :param model: tableView模型
        :param caption: 列标题
        :return: 返回找到索引值，未找到返回-1
        """
        for index in range(model.columnCount()):
            text = model.headerData(index, Qt.Horizontal)
            if text == caption:
                return index

        return -1


class xmlConfig(object):
    def __init__(self, filePath):
        """
        配置文件构造方法.

        :param filePath: 配置文件路径
        """
        self.filePath = filePath
        if os.path.exists(filePath):
            self.loadXml(filePath)
        else:
            self.createConfXml(filePath)

    def loadXml(self, filePath):
        """
        加载xml配置文件.

        :param filePath: 配置文件路径
        :return:
        """
        self.filePath = filePath
        self.xmlTree = xml.loadXml(filePath)

    def reloadXml(self):
        """
        重新加载xml配置文件
        :return:
        """
        self.xmlTree = xml.loadXml(self.filePath)

    def createConfXml(self, filePath):
        """
        新建配置文件

        :param filePath: 配置文件路径
        :return:
        """
        root = xml.createNode("root")

        # 添加线程节点
        threadsNode = xml.createNode("threads")
        xml.addChildNode(root, threadsNode)

        # 添加任务节点
        tasksNode = xml.createNode("tasks")
        xml.addChildNode(root, tasksNode)

        # 添加功能节点
        funcsNode = xml.createNode("functions")
        xml.addChildNode(root, funcsNode)

        # 添加节点节点
        nodesNode = xml.createNode("nodes")
        xml.addChildNode(root, nodesNode)

        # 保存配置文件
        self.xmlTree = ElementTree(root)
        xml.saveXml(self.xmlTree, filePath)

    def generatorID(self, prefix: str):
        """
        生成带指定前缀唯一ID值.

        :param prefix: 前缀
        :return:
        """
        # return "%s-%s" % (prefix, str(uuid.uuid1()))
        return "%s-%s%s" % (prefix, time.strftime("%y%m%d%H%M%S"), random.randint(0, 9))

    def addTreadNode(self, attrsMap: dict = {}):
        """
        添加线程节点.

        :param attrsMap: 属性map
        :return:
        """
        attrsMap["rowId"] = self.generatorID("T")
        self.__addNode("threads", "thread", attrsMap)

    def changeThreadNode(self, id: str, attrsMap: dict = {}, text: str = "", isDelete=False):
        """
        查找指定id值线程节点 并修改/新增/删除节点属性或文本.

        :param id: 节点id属性值
        :param attrsMap:节点属性map
        :param text: 节点文本
        :param isDelete: 删除标记
        :return:
        """
        xpath = r".//thread[@rowId='%s']" % (id)
        self.__changeNode(xpath, attrsMap, text, isDelete)

    def addTaskNode(self, attrsMap: dict = {}):
        """
        添加任务节点.

        :param attrsMap: 属性map
        :return:
        """
        attrsMap["rowId"] = self.generatorID("M")
        self.__addNode("tasks", "task", attrsMap)

    def changeTaskNode(self, id: str, attrsMap: dict = {}, text: str = "", isDelete=False):
        """
        查找指定id值任务节点 并修改/新增/删除节点属性或文本.

        :param id: 节点id属性值
        :param attrsMap:节点属性map
        :param text: 节点文本
        :param isDelete: 删除标记
        :return:
        """
        xpath = r".//task[@rowId='%s']" % (id)
        self.__changeNode(xpath, attrsMap, text, isDelete)

    def addFunctionNode(self, attrsMap: dict = {}):
        """
        添加功能节点.

        :param attrsMap: 属性map
        :return:
        """
        attrsMap["rowId"] = self.generatorID("F")
        self.__addNode("functions", "function", attrsMap)

    def changeFunctionNode(self, id: str, attrsMap: dict = {}, text: str = "", isDelete=False):
        """
        查找指定id值功能节点 并修改/新增/删除节点属性或文本.

        :param id: 节点id属性值
        :param attrsMap:节点属性map
        :param text: 节点文本
        :param isDelete: 删除标记
        :return:
        """
        xpath = r".//function[@rowId='%s']" % (id)
        self.__changeNode(xpath, attrsMap, text, isDelete)

    def addNodeNode(self, attrsMap: dict = {}):
        """
        添加节点节点.

        :param attrsMap: 属性map
        :return:
        """
        attrsMap["rowId"] = self.generatorID("N")
        self.__addNode("nodes", "node", attrsMap)

    def changeNodeNode(self, id: str, attrsMap: dict = {}, text: str = "", isDelete=False):
        """
        查找指定id值功能节点 并修改/新增/删除节点属性或文本.

        :param id: 节点id属性值
        :param attrsMap:节点属性map
        :param text: 节点文本
        :param isDelete: 删除标记
        :return:
        """
        xpath = r".//node[@rowId='%s']" % (id)
        self.__changeNode(xpath, attrsMap, text, isDelete)

    def delThreadNode(self, id: str):
        """
        删除线程节点.

        :param id: 要删除的节点id
        :return:
        """
        node = xml.findFirstNode(self.xmlTree, r".//threads")
        self.__delNode(node, {"rowId": id})

    def delFunctionNode(self, id: str):
        """
        删除功能节点.

        :param id: 要删除的节点id
        :return:
        """
        node = xml.findFirstNode(self.xmlTree, r".//functions")
        self.__delNode(node, {"rowId": id})

    def delTaskNode(self, id: str):
        """
        删除任务节点.

        :param id: 要删除的节点id
        :return:
        """
        node = xml.findFirstNode(self.xmlTree, r".//tasks")
        self.__delNode(node, {"rowId": id})

    def delNodeNode(self, id: str):
        """
        删除节点节点.

        :param id: 要删除的节点id
        :return:
        """
        node = xml.findFirstNode(self.xmlTree, r".//nodes")
        self.__delNode(node, {"rowId": id})

    def __addNode(self, nodeTag: str, chidNodeTag: str, attrsMap: dict = {}):
        """
        添加子节点.

        :param nodeTag: 当前节点标签
        :param chidNodeTag: 子节点标签
        :param attrsMap: 子节点属性
        :return:
        """
        # 查找节点
        node = xml.findFirstNode(self.xmlTree, r".//%s" % nodeTag)

        # 新建子节点
        childNode = xml.createNode(chidNodeTag, attrsMap)

        # 添加thread节点
        xml.addChildNode(node, childNode)

        # 保存xml文件
        self.saveXml()

    def __delNode(self, parentNode: Element, attrsMap: dict = {}):
        # 删除节点
        xml.deleteNodesByKey(parentNode, attrsMap)

        # 保存xml文件
        self.saveXml()

    def __changeNode(self, xPath: str, attrsMap: dict = {}, text: str = "", isDelete=False):
        """
        查找满足xpath节点 并修改/新增/删除节点属性或文本.

        :param xPath: 查找节点xpath
        :param attrsMap:节点属性map
        :param text: 节点文本
        :param isDelete: 删除标记
        :return:
        """
        nodes = xml.findAllNode(self.xmlTree, xPath)
        if len(nodes) > 0:
            xml.changeNodesAttrs(nodes, attrsMap, isDelete)
            xml.changeNodesText(nodes, text, isDelete)

            # 保存xml文件
            self.saveXml()
        else:
            raise Exception("未找到节点[xpath=%s]" % xPath)

    def saveXml(self):
        """
        保存xml文件.

        :return:
        """
        xml.saveXml(self.xmlTree, self.filePath)

    def convertNodeToModel(self) -> list:
        """
        node节点转tableview model.

        :return: list数组，元素为dict类型
        """
        # 定位nodes节点
        node = xml.findFirstNode(self.xmlTree, ".//nodes")
        return [subNode.attrib for subNode in list(node)]

    def convertFunctionToModel(self) -> list:
        """
        function节点转tableview model.

        :return: list数组，元素为dict类型
        """
        # 定位functions节点
        node = xml.findFirstNode(self.xmlTree, ".//functions")
        return [subNode.attrib for subNode in list(node)]

    def convertTaskToModel(self) -> list:
        """
        task节点转tableview model.

        :return: list数组，元素为dict类型
        """
        # 定位tasks节点
        node = xml.findFirstNode(self.xmlTree, ".//tasks")
        return [subNode.attrib for subNode in list(node)]

    def convertThreadToModel(self) -> list:
        """
        thread节点转tableview model.

        :return: list数组，元素为dict类型
        """
        # 定位threads节点
        node = xml.findFirstNode(self.xmlTree, ".//threads")
        return [subNode.attrib for subNode in list(node)]


class EmptyDelegate(QItemDelegate):
    """
    tableview列不可编辑代理类
    """

    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


def startApp():
    app = QApplication(sys.argv)
    mainwin = mainWin()
    mainwin.show()
    app.exec_()
