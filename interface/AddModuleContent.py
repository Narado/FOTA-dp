# -*- coding: utf-8 -*-
# @Time    :2021/9/28 20:20
# @Author  :Gao Lei
# @FileName:AddModuleContent.py
# @Software:PyCharm
import sys
import time
import os

from conf import readconfig
from lib import MouseOperate
from interface  import AFC_CN100_Controller

class addModuleContent:
    mo = MouseOperate.mouse_operate() #创建鼠标操作对象
    afcCN100 = AFC_CN100_Controller.afcCN100Controller()






    def __init__(self):
        pass

    def addSystemSetting(self, driver):
        print("进入函数addSystemSetting")
        self.afcCN100.systemSetting(driver, "system-setting")


    def addAdVideo(self,driver):
        print("进入函数addAdVideo")
        self.afcCN100.posterAndConfig(driver,"ad-video")


    def addConfiguration(self,driver):
        print("进入函数addConfiguration")
        self.afcCN100.posterAndConfig(driver, "configuration")


    def addBMS1(self,driver):
        print("进入函数addBMS1")
        self.afcCN100.AFC_CN100(driver,"BMS1")

    def addCCU1(self,driver):
        print("进入函数addCCU1")
        self.afcCN100.AFC_CN100(driver, "CCU1")

    def addCCU2(self,driver):
        print("进入函数addCCU2")
        self.afcCN100.AFC_CN100(driver, "CCU2")

    def addEMS(self,driver):
        print("进入函数addEMS")
        self.afcCN100.AFC_CN100(driver, "EMS")

    def addHCU(self,driver):
        print("进入函数addHCU")
        self.afcCN100.AFC_CN100(driver, "HCU")

    def addTBOX1MPU(self,driver):
        print("进入函数addTBOX1MPU")
        self.afcCN100.TBOX_MPU(driver, "TBOX1-MPU")

    def addTBOX1MCU(self, driver):
        print("进入函数addTBOX1MCU")
        self.afcCN100.AFC_CN100(driver, "TBOX1-MCU")

    def addTBOX2MCU(self, driver):
        print("进入函数addTBOX2MCU")
        self.afcCN100.AFC_CN100(driver, "TBOX2-MCU")

    def addTBOX2MPU(self, driver):
        print("进入函数addTBOX2MPU")
        self.afcCN100.TBOX_MPU(driver, "TBOX2-MPU")

    def addDCDC1(self, driver):
        print("进入函数addDCDC1")


    def addDCDC2(self, driver):
        print("进入函数addDCDC2")

    def addDCDC3(self, driver):
        print("进入函数addDCDC3")

    def addDCDC4(self, driver):
        print("进入函数addDCDC4")



    def addACDC1(self,driver):
        print("进入函数addACDC1")

    def addACDC2(self, driver):
        print("进入函数addACDC2")

    def addCMU1(self, driver):
        print("进入函数addCMU1")

    def addCMU2(self, driver):
        print("进入函数addCMU2")

    def addCMU3(self, driver):
        print("进入函数addCMU3")

    def addCMU4(self, driver):
        print("进入函数addCMU4")

    def addCMU5(self, driver):
        print("进入函数addCMU5")

    def addCMU6(self, driver):
        print("进入函数addCMU6")

    def addCMU7(self, driver):
        print("进入函数addCMU7")

    def addCMU8(self, driver):
        print("进入函数addCMU8")

