# -*- coding: utf-8 -*-
# @Time    :2021/9/27 11:25
# @Author  :Gao Lei
# @FileName:WatchProcess.py
# @Software:PyCharm

import psutil
import os
import signal
import time

import win32con
import win32gui
import win32api

from selenium import webdriver
from win32 import win32process
from AutoItLibrary import AutoItLibrary

class WatchPro():

    process_list = []
    handles_list = []

    def __init__(self):
        pass

    def get_AllPro(self):
        for proc in psutil.process_iter():
            self.process_list.append(proc)
        return self.process_list

    def get_newProId(self):
        procpid = 0
        for proc in psutil.process_iter():
            if proc not in self.process_list:
                procpid = proc.pid
                return procpid

    def showAllHandles(self,driver):
        i = 0
        all_handles = driver.window_handles #获取所有打开的句柄
        for handle in all_handles:
            i = i + 1
            print("handle.name:{}".format(handle))
            self.handles_list.append(handle)
        print("总共有{}个句柄".format(i))

    def newHandle(self,driver):
        i = 0
        all_handles = driver.window_handles  # 获取所有打开的句柄
        for handle in all_handles:
            i = i + 1
            print("handle.name:{}".format(handle))
            if handle not in self.handles_list:
                print("新的handle：{}".format(handle))

        print("总共有{}个句柄".format(i))

    def get_hwnds_forpid(self,pid):
        def callback(hwnd,hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):   #如果窗口可见并且是激活的，则获取它的pid
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)  #判断当前存在的窗口的pid是否与要找的pid相符合
                if found_pid == pid:
                    hwnds.append(hwnd)
                return True
            return True
        hwnds = []
        win32gui.EnumWindows(callback,hwnds)
        return hwnds


    def get_window_forhwnd(self,pid):
        hwnd = 0
        for hwnd in self.get_hwnds_forpid(pid):
            title = win32gui.GetWindowText(hwnd)
            classname = win32gui.GetClassName(hwnd)
            print("title:{},classname:{}".format(title, classname))
            return hwnd,classname



if __name__ == '__main__':
    wp = WatchPro()
    at = AutoItLibrary()
    wp.get_AllPro()
    print("******************************** 睡眠 **********************************\n")
    time.sleep(15)
    print("******************************** 获取新的进程*****************************\n")
    pid = wp.get_newProId()


    hwnds = wp.get_hwnds_forpid(pid)
    print("hwnds:{}",hwnds)
    windowhwnd,windowname = wp.get_window_forhwnd(pid)
    #函数原型：HWND FindWindowEx（HWND hwndParent，HWND hwndChildAfter，LPCTSTR lpszClass，LPCTSTR lpszWindow）
    #参数1. hwndParent:查找子窗口的父窗口句柄； 如果该值为NULL ，则函数以桌面窗口为父窗口，查找桌面窗口的所有子窗口。如果hwndParent是HWND_MESSAGE，函数仅查找所有消息窗口
    #参数2. hwndChildAfter：子窗口句柄。查找从在Z序中的下一个子窗口开始。子窗口必须为hwndParent窗口的直接子窗口为非后代窗口。如果HwndChildAfer为NUL，查找从hwndParent的第一个子窗口开始。
    # 如果hwndParent和hwndChildAfter同时为NULL，则函数查找所有的顶层窗口及消息窗口
    #参数3. ipszClass:指向一个指定了类名的空结束字符串，或一个标识类名字符串的成员的指针。如果该参数为一个成员，则它必须为前次调用theGloabalAddAtom函数产生的全局成员。该成员为16为，必须
    #位于IpClassName的低16位，高位bicultural为0.
    #参数4 ipsWindow：指向一个指定了窗口名（窗口标题）的空结束字符串。如果该参数为NULL，则为所有窗口全匹配。返回值：如果函数成功，返回值为具有指定类名和窗口名的窗口句柄。如果函数失败，返回值为NULL.

    print("hwnd:",windowhwnd)
    print("windowname:",windowname)
    time.sleep(2)
    dlg = win32gui.FindWindowEx(windowhwnd , None,windowname,None) #获取hld下第一个为edit控件的句柄
    print("Edit句柄:{}".format(dlg))
    buffer = '0'*50
    len = win32gui.SendMessage(dlg, win32con.WM_GETTEXTLENGTH)+1    #获取edit控件文本长度
    print("len:",len)



