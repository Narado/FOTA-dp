# -*- coding: utf-8 -*-
# @Time    :2021/10/17 8:49
# @Author  :Gao Lei
# @FileName:MuiltiProcess.py
# @Software:PyCharm

import os
import time
import multiprocessing
from multiprocessing import Process

class multi_process:
    def __init__(self):
        pass

    def fun(self,name):
        print("2子进程信息：pid=%s, ppid=%s" %(os.getpid(), os.getppid()))
        print("hello"+name)

    def test(self):
        print('aaaaaa')

    def func(self,msg):
        return multiprocessing.current_process().name + '-' + msg

    def oneProces(self):
        print("1 主进程信息：pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
        ps = Process(target=self.fun(name='java'))
        print("111 #### ps pid:" + str(ps.pid) + ",ident:" + str(ps.ident))
        print("3 进程信息：pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
        print(ps.is_alive())  # 启动之前 is_alive为False(系统未创建)
        ps.start()
        print(ps.is_alive())  # 启动之后，is_alive为True(系统未创建)

        print("222 #### ps pid:" + str(ps.pid) + ",ident:" + str(ps.ident))
        print("4 进程信息：pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
        ps.join()  # 等待子进程完成任务 类似于os.wait()
        print("5 进程信息：pid=%s, ppid=%s" % (os.getpid(), os.getppid()))
        ps.terminate()  # 终端进程
        print("6 进程信息：pid=%s, ppid=%s" % (os.getpid(), os.getppid()))

    def multiProces(self):
        pool  =multiprocessing.Pool(processes=4)    #创建4个进程
        results = []
        for i in range(20):
            msga = "process %d" %(i)
            results.append(pool.apply_async(self.func(msg=msga)))
        pool.close()    #关闭进程池，表示不在往进程池中添加进程，需要哎join之前调用
        pool.join()     #等待进程池中所有的进程执行完
        print("Sub-process(es) done")


        for res in results:
            print(res)




if __name__== "__main__":
   mp = multi_process()
   # mp.oneProces()
   mp.multiProces()