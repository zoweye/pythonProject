#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Desc    : 描述
# @Author  : zwy
# @File    : test.py
# @Time    : 2019/9/10 11:22
# @Software: PyCharm
import os
from xml.etree.ElementTree import *

import core.xml as xml

filePath = "./test.xml"
# if os.path.exists(filePath):
#     os.remove(filePath)

root = Element("root")
root.text = "aaa"
tree = ElementTree(root)
xml.saveXml(tree, filePath)
