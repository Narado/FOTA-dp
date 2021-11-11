# -*- coding: utf-8 -*-
# @Time    :2021/10/12 14:43
# @Author  :Gao Lei
# @FileName:SaveLog.py
# @Software:PyCharm

import logging
import os
import sys
import io
from datetime import datetime
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


    def create_detail_day(self):
        nowtime = datetime.now()
        daytime = nowtime.strftime('log_'+'%Y%m%d'+'_'+'%H%M%S')
        return daytime

    def make_print_to_file(self,path='./'):
        class Logger(object):
            # print(filename)
            def __init__(self,filename="Default.log",path="./"):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
                self.terminal = sys.stdout
                print("path:", path)
                print("filename:",filename)
                self.log = open(os.path.join(path,filename),"a",encoding='utf-8')

            def write(self,message):
                self.terminal.write(message)
                self.log.write(message)

            def flush(self):
                pass

        sys.stdout = Logger(self.create_detail_day() + '.txt', path=path)
        print(self.create_detail_day().center(60,'*'))

if __name__ == '__main__':
    # detail_time = save_log().create_detail_day()
    # print("detail_time:",detail_time)
    save_log().make_print_to_file(path = "C:\\08_Robot\\FOTA_NEW\\log")

    print('explanation'.center(80,'*'))
    info1 = "从小到大排序"
    info2 = "sort the form large to samll"
    print(info1)
    print(info2)
    print('END: explation'.center(80,'*'))