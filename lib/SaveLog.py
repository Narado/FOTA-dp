# -*- coding: utf-8 -*-
# @Time    :2021/10/12 14:43
# @Author  :Gao Lei
# @FileName:SaveLog.py
# @Software:PyCharm

import logging
import os
from FOTA.lib import GetTime

class save_log:
    def __init__(self):
        pass

    def log_to_console(self):

        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.DEBUG)
        logging.debug('debug信息')
        logging.info('info 信息')
        logging.warning('warning 信息')
        logging.error("error 信息")
        logging.critical('critical信息')

    def log_to_file(self):
        now_time = GetTime.getTime().nowtimeToString()
        filenamepath = "..\\log\\log_{}.txt".format(now_time)
        logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                            filename= filenamepath,
                            filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                            # a是追加模式，默认如果不写的话，就是追加模式
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            # 日志格式
                            )

if __name__ == '__main__':
    save_log().log_to_file()