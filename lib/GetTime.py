# -*- coding: utf-8 -*-
# @Time    :2021/10/8 14:47
# @Author  :Gao Lei
# @FileName:GetTime.py
# @Software:PyCharm

import datetime

class getTime:
    def __init__(self):
        pass

    def nowtimeToString(self):
        # 获取当前时间对象
        nowtime = datetime.datetime.now()
        # 把时间对象转换为字符串
        now_time = datetime.datetime.strftime(nowtime, '%Y%m%d%H%M%S')
        print("当前时间:{}".format(now_time))
        return now_time