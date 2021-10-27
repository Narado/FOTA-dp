# -*- coding: utf-8 -*-
# @Time    :2021/9/26 17:04
# @Author  :Gao Lei
# @FileName:__init__.py.py
# @Software:PyCharm
#coding=utf-8

import sys
sys.path.append("C:\\08_Robot\\FOTA_NEW")

from core import ManageFota
from core import LoginFota
from core import TaskFota
from core import StatusFota
from conf import readconfig

__version__ = '1.0'
class FOTA_NEW(ManageFota):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

class FOTA_NEW(LoginFota):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

class FOTA_NEW(TaskFota):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

class FOTA_NEW(StatusFota):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

class FOTA_NEW(readconfig):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'