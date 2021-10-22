# -*- coding: utf-8 -*-
# @Time    :2021/10/17 10:31
# @Author  :Gao Lei
# @FileName:MultiThread.py
# @Software:PyCharm

import threading
from time import ctime,sleep




class multi_thread:

    def __init__(self):
        pass

    def music(self,func):
        for i in range(3):
            print("I was listening to %s. %s" % (func, ctime()))
            sleep(1)

    def move(self,func):
        for i in range(3):
            print("I was at the %s! %s" % (func, ctime()))
            sleep(5)



    def createthread(self, tasks):
        """
        :param tasks:   以字典形式存储任务的名字和参数，即{taskname1:args1,taskname2:args2}
        :return:
        """
        # threads = []
        # t1 = threading.Thread(target=self.music, args=(u'爱情买卖',))
        # threads.append(t1)
        # t2 = threading.Thread(target=self.move, args=(u'阿凡达',))
        # threads.append(t2)
        threads = []
        for key  in tasks:
            print("keys:{},values:{}".format(key, tasks[key]))
            th =threading.Thread(target=key,args=tasks[key])
            threads.append(th)
        return threads

    def runthreads_meanwhile(self,tasks):
        print("进入runthreads_meanwhile函数")
        threads = self.createthread(tasks)
        for t in threads:
            t.setDaemon(True)   #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
            t.start()

        for t in threads:  # 等待子线程完成，在子线程完成之前，该子线程的父线程一致被阻塞
            t.join()

        print("\nall over %s" % ctime())



if __name__ == '__main__':
    threads = multi_thread().createthread()
    for t in threads:
        t.setDaemon(True)   #守护线程，如果不设置守护线程，程序会被无限挂起。子线程启动后，父线程也继续执行下去
        t.start()

    for t in threads:   #等待子线程完成，在子线程完成之前，该子线程的父线程一致被阻塞
        t.join()



    print("\nall over %s" %ctime())
