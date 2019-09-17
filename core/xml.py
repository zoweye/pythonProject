#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : xml文件操作
# @Author  : zwy
# @File    : xml.py
# @Time    : 2019/9/10 10:51
# @Software: PyCharm
import os
from xml.etree.ElementTree import ElementTree, Element, SubElement


def loadXml(filePath) -> ElementTree:
    """
    加载xml文件.

    :param filePath: xml文件路径
    :return: xml文件ElementTree对象
    """
    if not os.path.exists(filePath):
        raise FileExistsError("[%s]文件不存在" % filePath)
    return ElementTree(file=filePath)


def createBlankXml(rootEl="root") -> ElementTree:
    """
    创建空白xml文件，只有根节点.

    :param rootEl: root根节点名
    :return: xml文件ElementTree对象
    """
    return ElementTree(Element(rootEl))


def saveXml(eTree: ElementTree, filePath):
    """
    保存内容至xml文件.

    :param eTree: ElementTree对象
    :param filePath: xml文件保存路径
    :return:
    """
    prettyXml(eTree.getroot())
    eTree.write(filePath, encoding="utf-8", xml_declaration=True)


def prettyXml(element: Element, indent="\t", newline="\n", level=0):
    """
    xml美化器，格式化xml内容.

    :param element: Element对象
    :param indent: 缩进字符串
    :param newline: 换行字符串
    :param level: 标签层级，用于设置第几层缩进
    :return:
    """
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level

    # 将elemnt转成list
    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


def getRootNode(eTree: ElementTree) -> Element:
    """
    获取根节点对象.

    :param eTree: ElementTree对象
    :return: Element对象
    """
    return eTree.getroot()


def findAllNode(eTree: ElementTree, xPath: str) -> list:
    """
    查找所有满足条件节点list.

    :param eTree: ElementTree对象
    :param xPath: xpath语法
    :return: list(Element对象)
    """
    return eTree.findall(xPath)


def findFirstNode(eTree: ElementTree, xPath: str) -> Element:
    """
    查找满足条件第一个节点Element对象.

    :param eTree: ElementTree对象
    :param xPath: xpath语法
    :return: Element对象
    """
    return findAllNode(eTree, xPath)[0]


def containAttrs(node: Element, keyMap: dict):
    """
    判断节点是否全包括keyMap中属性及属性值.

    :param node: 节点
    :param keyMap: 属性map
    :return: 布尔值
    """
    for key in keyMap:
        if node.get(key) != keyMap.get(key):
            return False
    return True


def getNodesWithAttrs(node: Element, keyMap: dict):
    """
    根据属性及属性值定位当前结点及子节点，返回节点list.

    :param node: Element对象节点
    :param keyMap: 属性map
    :return: 节点list(Element对象)
    """
    result_nodes = []
    for node in list(node.iter()):
        if containAttrs(node, keyMap):
            result_nodes.append(node)
    return result_nodes


def changeNodesAttrs(nodes, keyMap: dict, isDelete=False):
    """
    修改/新增/删除节点属性.

    :param node: 节点list/节点
    :param keyMap: 属性map
    :param isDelete: 是否删除节点属性
    :return:
    """
    if isinstance(nodes, list):
        for node in nodes:
            for key in keyMap:
                if isDelete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, keyMap.get(key))
    elif isinstance(nodes, Element):
        for key in keyMap:
            if isDelete:
                if key in nodes.attrib:
                    del nodes.attrib[key]
            else:
                nodes.set(key, keyMap.get(key))
    else:
        raise TypeError("nodes 参数类型错误")


def changeNodesText(nodes, text, isDelete=False):
    """
    改变/增加/删除一个节点的文本.

    :param nodes: 节点list/节点
    :param text: 文本字符串
    :param keyMap: keymap
    :param isDelete: 是否删除文件
    :return:
    """
    if isinstance(nodes, list):
        for node in nodes:
            if isDelete:
                node.text = ""
            else:
                node.text = text
    elif isinstance(nodes, Element):
        if isDelete:
            nodes.text = ""
        else:
            nodes.text = text
    else:
        raise TypeError("nodes 参数类型错误")


def deleteNodesByKey(nodes, keyMap: dict):
    """
    根据属性删除当前节点所有满足条件子节点

    :param nodes: 节点list/节点
    :param keyMap: 属性dict
    :return:
    """
    if isinstance(nodes, list):
        for node in nodes:
            childNodes = node.getchildren()
            for child in childNodes:
                if containAttrs(child, keyMap):
                    node.remove(child)

    elif isinstance(nodes, Element):
        childNodes = nodes.getchildren()
        for child in childNodes:
            if containAttrs(child, keyMap):
                nodes.remove(child)
    else:
        raise TypeError("nodes 参数类型错误")


def createNode(nodeTag: str, attrMap: dict = {}, text: str = ""):
    """
    新建一个节点.

    :param nodeTag: 节点标签
    :param attrMap: 属性map
    :param text: 节点文本text
    :return:
    """
    element = Element(nodeTag, attrMap)
    if text.strip() != "":
        element.text = text
    return element


def addChildNode(nodes, element: Element):
    """
    给一个节点添加子节点.

    :param nodes: 节点list/节点
    :param element: 子节点
    :return:
    """
    if isinstance(nodes, list):
        for node in nodes:
            node.append(element)
    elif isinstance(nodes, Element):
        nodes.append(element)
    else:
        raise TypeError("nodes 参数类型错误")
