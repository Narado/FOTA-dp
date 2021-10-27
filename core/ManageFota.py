# coding= utf-8
import os
import time
import numpy as np

from interface.InterceptPic import *
from core.LoginFota import *

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import *
from datetime import datetime
from lib import SoundAlert


from tkinter import filedialog
from lib import SwithCase
from lib import WatchProcess
from lib import MouseOperate
from lib import ChangeName
from lib import GetTime
from conf import readconfig
from interface import AddModuleContent


Bottom = 0
Top    = 1



manageIds_dic={
    'chargePileInfo'   : 1,
    'updatePackManage' : 2,
    'updateTask'       :3,
    'updateStatistic'  : 4,
    'system'           :5
}


operatorID_dic={
    'dupu_suzhou' : 1,
    'dupu_jiangsu': 2,
    'ics_suzhou'  :3
}



chargingPileID_dic={
    'air_colling'  : 1,
    'liqiud_colling': 2

}


# updatemodule_dic={
#     'UM_POSTER' : 1,
#     'UM_CONFFILE' : 2,
#     'UM_BMS1' : 3,
#     'UM_CCU1' : 4,
#     'UM_CCU2' : 5,
#     'UM_EMS' : 6,
#     'UM_HCU' : 7,
#     'UM_TBOX1MPU' : 8,
#     'UM_TBOX1MCU' : 9,
#     'UM_TBOX2MCU' : 10,
#     'UM_TBOX2MPU' : 11,
#     'UM_DCDC1' : 12,
#     'UM_DCDC2' : 13,
#     'UM_DCDC3' : 14,
#     'UM_DCDC4' : 15,
#     'UM_ACDC1' : 16,
#     'UM_ACDC2' : 17,
#     'UM_CMU1' : 18,
#     'UM_CMU2' : 19,
#     'UM_CMU3' : 20,
#     'UM_CMU4' : 21,
#     'UM_CMU5' : 22,
#     'UM_CMU6' : 23,
#     'UM_CMU7' : 24,
#     'UM_CMU8' : 25
# }

addcontentfun_dic={
    1   : "addAdVideo",
    2   : "addConfiguration",
    3   : "addBMS1",
    4   : "addCCU1",
    5   : "addCCU2",
    6   : "addEMS",
    7   : "addHCU",
    8   : "addTBOX1MPU",
    9   : "addTBOX1MCU",
    10  : "addTBOX2MCU",
    11  : "addTBOX2MPU",
    12  : "addDCDC1",
    13  : "addDCDC2",
    14  : "addDCDC3",
    15  : "addDCDC4",
    16  : "addACDC1",
    17  : "addACDC2",
    18  : "addCMU1",
    19  : "addCMU2",
    20  : "addCMU3",
    21  : "addCMU4",
    22  : "addCMU5",
    23  : "addCMU6",
    24  : "addCMU7",
    25  : "addCMU8"
}





class ManageFota(object):
    mo = MouseOperate.mouse_operate()
    amc = AddModuleContent.addModuleContent()
    sc = SwithCase.switch_case()
    wp = WatchProcess.WatchPro()
    cn =   ChangeName.changeName()

    time_string = ""


    def __init__(self):


        pass


    #打开升级包管理页面
    def openManage(self, driver, manageID=2):
        """
        @Author：GaoLei
        :param driver: 整个网页运行的驱动
        :param manageID: 1：充电桩信息； 2:升级包管理； 3：升级任务； 4：升级统计； 5：升级状态； 6：系统；
        :return:
        """
        # driver = webdriver.Chrome()
        collapse = driver.find_elements_by_xpath("//div[@class='sidebar-collapse']//li")[0]
        classvalue = collapse.get_attribute("class")
        print("classvalue:",classvalue)
        if classvalue == "active":
            time.sleep(0.5)
            pass
        else:
            Manage = driver.find_element_by_xpath("//span[@class='nav-label' and text()='管理']")  # 找到”管理“标签的位置
            Manage.click()  # 打开管理列表
            time.sleep(0.5)

        if manageID == 1:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[1]  # 找到”充电桩信息“标签的位置
        elif manageID == 2:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[2]  # 找到”升级包管理“标签的位置
        elif manageID == 3:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[3]  # 找到”升级任务“标签的位置
        elif manageID == 4:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[4]  # 找到”升级统计“标签的位置
        elif manageID == 5:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[5]  # 找到”升级状态“标签的位置
        elif manageID == 6:
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[6]  # 找到”升级状态“标签的位置

        


        packManage_element.click()  # 打开升级包管理界面

    #打开添加页面
    def openAddPage(self, driver):

        # Iframe中的元素定位出错问题：
        # 现象：如果有iframe存在，可是我们没有做特殊处理，而是通过通用的定位方法，name,id,xpath或者CSS来定位。用Selenium IDE验证能查找到元素，
        # 但是运行测试用例的时候，总是找不到。
        # 原因：在我们运行测试脚本的时候，代码获取的页面的句柄，而iframe在句柄中是当成一个元素来处理的。脚本是没有办法自己去iframe中定位元素的，
        # 所以当搜索完页面时，发现找不到要定位给的元素，就当错误处理。
        # 解决办法：当需要定位iframe中的元素时，先将句柄切换到iframe中 ： driver.switch_to.frame("framename"),具体的iframe_name可以在网页的开发者工具中找到
        driver.switch_to.frame("iframe412")  # 将driver切换到浮动的框架
        plusbutton = driver.find_element_by_xpath("//*[@id='upgradePack']/div[1]/form/div/div/div[6]/button[3]")  # 找到”添加“标签的位置
        plusbutton.click()  # 点击添加标签，打开添加页面
        return driver

    #添加顶部4个框的内容
    def addTopfour(self, driver, pakgName, operatorId, chargingPileIds, releaseTime=""):
        """
        @Author：GaoLei
        :param driver: 网页所用驱动
        :param pakgName: 升级包名称
        :param operatorId: 1：度普（苏州）新能源科技有限公司； 2：江苏度普新能源科技有限公司； 3：埃诺威（苏州）新能源有限公司
        :param chargingPileIds: 1：(AFC-100-AH-CN)100度风冷国内版； 2：(AFC-200-LH-CN)200度液冷国内版
        :param releaseTime:默认填充当前时间
        :return:
        """

        # .操作元素对象clear() 清空；send_keys() 键盘操作；click()
        # 点击；submit() 提交；text 获取对象文本；get_attribute 获取对象属性值
        # 升级包
        updPagNm = driver.find_elements_by_xpath("//input[@class='form-control' and @type='text']")[1]  # 获取”升级包名称“文本框这个元素
        updPagNm.clear()  # 清空”升级包名称“文本框内容
        updPagNm.send_keys(pakgName)  # 往”升级包名称“文本框写入内容

        # 运营商
        optorId = driver.find_element_by_xpath('//div[@class="selecttree operator"]')  # 获取”运营商“文本框元素
        optorId.click()
        time.sleep(0.5)
        if operatorId == 1:
            opclickNm = driver.find_elements_by_xpath('//*[@id="582020040800000001"]/a')[1]  # 输入1，选择供应商“度普（苏州）新能源科技有限公司”
        elif operatorId == 2:
            opclickNm = driver.find_elements_by_xpath('//*[@id="582021030900000002"]/a')[1]  # 输入2，选额供应商“江苏度普新能源科技有限公司”
        else:
            opclickNm = driver.find_elements_by_xpath('//*[@id="582021031900000003"]/a')[1]  # 输入3，选择供应商“埃诺威（苏州）新能源有限公司”
        opclickNm.click()
        time.sleep(0.5)

        # 桩型号
        chargPile = driver.find_element_by_xpath('//div[@class="select charging_piles"]')  # 在添加页面点击运营商的div
        chargPile.click()
        time.sleep(0.5)
        if chargingPileIds == 1:
            charg_ch = driver.find_elements_by_xpath('//li[@class="select-dropdown-menu-item"]')[28]  # 输入1，选择(AFC-100-AH-CN)100度风冷国内版
        else:
            charg_ch = driver.find_elements_by_xpath('//li[@class="select-dropdown-menu-item"]')[29]  # 输入2，选择(AFC-200-LH-CN)200度液冷国内版
        charg_ch.click()

        # 发布时间
        if (releaseTime == None) or (releaseTime == ""):  # 默认输入为空
            timen = datetime.now()
            nowtime = timen.strftime("%Y-%m-%d %H:%M")
            print(nowtime)
        else:
            nowtime = releaseTime
        release_element = driver.find_element_by_xpath('//input[@class="form-control " and @name="add_time"]')
        release_element.send_keys(nowtime)  # 发布时间输入当前时间
        return driver

    #添加备注
    def addRemark(self, driver, remarks=""):
        remark = driver.find_element_by_xpath('//textarea[@class="form-control" and @name="remark"]')
        remark.click()
        remark.send_keys(remarks)
        return driver

    #是否强制升级
    def isUpgradeForced(self, driver, upgrade_value="YES"):
        """
        @Author；GaoLei
        :param driver: 网页所用驱动
        :param upgrade_value: yes或者YES: 选择”是 “； no或者No：选择”否“
        :return:
        """

        if (upgrade_value == "yes") or (upgrade_value == "YES"):
            upgrade_element = driver.find_element_by_xpath("//div[@class='iradio_square-green']")
        elif (upgrade_value == "no") or (upgrade_value == "NO"):
            upgrade_element = driver.find_element_by_xpath("//div[@class='iradio_square-green checked']")
        upgrade_element.click()
        return driver

    #选择升级模块，并添加对应模块的文件
    def addUpgradeMoudle(self,driver,MoudleId):
        """
        @Author:GaoLei
        :param driver:
        :param MoudleId: 1:广告视频； 2：配置文件； 3：BMS1; 4:CCU1; 5:CCU2; 6:EMS; 7:HCU; 8：TBOX1-MPU; 9:TBOX1-MCU; \
                        10:TBOX2-MCU; 11:TBOX2-MPU; 12:DCDC1; 13:DCDC2; 14:DCDC3; 15:DCDC4; 16:ACDC1; 17:ACDC2;\
                        18:CMU1; 19:CMU2; 20:CMU3; 21:CMU4; 22:CMU5; 23:CMU6; 24:CMU7; 25:CMU8
        :return:
        """
        # array_Moudle=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        array_Moudle= np.arange(0,25,1) #生成一个0~24的数组
        need_systemsetting_array = np.arange(3,26,1) #生成一个3~25的数组
        counter = 0  #计数器

        if 0  in MoudleId:
            print("输入的模块id不正确")
            return False
        else:
            for id in MoudleId:
                id_n = id-1 #获得该模块的Index
                real_index = id_n -counter   #获得该模块在每次删减后的真实Index
                print("id:",id)
                print("real_index:",real_index)
                moudle_element = driver.find_elements_by_xpath("//div[@class='icheckbox_square-green']")[real_index]
                moudle_element.click()
                array_Moudle = np.delete(array_Moudle,real_index) #将已经点击的模块id从总的数组里面删除
                counter = 1 + counter  # 计数器记录循环次数
                time.sleep(2)

                method = self.sc.caseToFunction(AddModuleContent.addModuleContent,addcontentfun_dic,id) #在列表中搜索 数值对应的方法
                method(self.amc,driver)
                if id in need_systemsetting_array:  #判断如果该模块是除了“广告视频”和“配置文件”外的其它模块，则需要另外添加系统设置
                    self.amc.addSystemSetting(driver)

        return driver

    #点击确定或取消
    def confirmOrCancle(self, driver):
        confirm = driver.find_element_by_xpath('//div[@class="modal-footer"]//button[contains(text(),"确定")]')
        cancle = driver.find_element_by_xpath('//div[@class="modal-footer"]//button[contains(text(),"取消")]')
        confirm.click()

    #检查升级包是否准备完成
    def waitUpPackComp(self,driver,pakgName):
        driver.switch_to.frame("iframe412")  # 将driver切换到浮动的框架
        uppack = driver.find_element_by_xpath("//input[@name='name' and @placeholder='升级包名称']")
        uppack.send_keys(pakgName)
        time.sleep(0.25)
        findpack = driver.find_element_by_xpath("//button[contains(text(),'查询') and @type='button']")
        findpack.click()
        time.sleep(0.5)
        # forceUp = driver.find_elements_by_xpath("//div[@col-id='force']")[1]
        self.mo.sliderollerRow(driver,'mauna-body-viewport',250 ) #整个查询内容的div向右移动250px，能看到“升级包准备状态”位置
        time.sleep(1)
        result = "未开始"
        while result != "已完成":
            state = driver.find_elements_by_xpath("//div[@col-id='state']")[1]
            time.sleep(0.25)
            result = state.get_attribute("title")
            print(result)
            SoundAlert.sound_alert().speak("打包"+result)
            refresh_element = driver.find_element_by_xpath("//button[contains(text(),'刷新') and @type='button']")
            refresh_element.click()
            time.sleep(5)
        SoundAlert.sound_alert().speak("恭喜您，打包已经完成了")
        print("打包已经完成了")
        return driver


    #整体流程
    def fota_manage_page(self,driver):
        print("进入fota_manage函数")

        self.time_string = GetTime.getTime().nowtimeToString()
        print("在制作升级包时的初始时间：",self.time_string)
        #从配置文件获取信息
        account = readconfig.readconfig("..\\conf\\Fota.ini","baseconf","account")
        password = readconfig.readconfig("..\\conf\\Fota.ini","baseconf","password")
        package_name = readconfig.readconfig("..\\conf\\Fota.ini","moduleconf","package_name")+self.time_string
        operator_id =  readconfig.readconfig("..\\conf\\Fota.ini","moduleconf","operator_id")
        charging_pileids = readconfig.readconfig("..\\conf\\Fota.ini", "moduleconf", "charging_pileids")
        release_time = readconfig.readconfig("..\\conf\\Fota.ini", "moduleconf", "release_time")
        remark_content = readconfig.readconfig("..\\conf\\Fota.ini", "remarkconf", "remark_content")
        upresult = readconfig.readconfig("..\\conf\\Fota.ini", "upgradeforcedconf", "upresult")
        module_list = readconfig.readconfig("..\\conf\\Fota.ini", "upgrademoduleconf", "module_list")
        module_list_int = self.cn.stringL_to_intL(module_list)

        # driver = LoginFota().fota_login_page()  # 首页登录
        # time.sleep(1)
        self.openManage(driver, 2)  # 打开管理界面的升级包管理
        time.sleep(1)
        self.openAddPage(driver)  # 打开“添加页面”
        time.sleep(1)
        self.addTopfour(driver, package_name, operator_id, charging_pileids, release_time)  # 往”添加“页面的顶部4个元素”升级包名称“，”运营商“，”桩型号“，”发布时间“填指定内容
        time.sleep(0.5)
        self.addRemark(driver, remark_content)  # 添加备注
        time.sleep(0.5)
        self.isUpgradeForced(driver, upresult)  # 是否强制立即升级
        time.sleep(0.5)
        print("=======================================================================================\n"
              "1:广告视频； 2：配置文件； 3：BMS1; 4:CCU1; 5:CCU2; 6:EMS; 7:HCU; 8：TBOX1-MPU; 9:TBOX1-MCU;\n"
              "10:TBOX2-MCU; 11:TBOX2-MPU; 12:DCDC1; 13:DCDC2; 14:DCDC3; 15:DCDC4; 16:ACDC1; 17:ACDC2\n"
              "18:CMU1; 19:CMU2; 20:CMU3; 21:CMU4; 22:CMU5; 23:CMU6; 24:CMU7; 25:CMU8\n"
              "=======================================================================================\n")
        self.addUpgradeMoudle(driver, module_list_int)  # 选择需要添加什么模块，并添加对应模块的内容
        self.confirmOrCancle(driver)    #最后点击确定按钮
        time.sleep(8)
        driver.refresh()
        time.sleep(1)
        self.openManage(driver, 2)  # 打开管理界面的升级包管理
        time.sleep(0.5)
        print("package_name:",package_name)
        self.waitUpPackComp(driver,package_name) #等到添加的升级包打包完成
        return True


    def get_managefota_time(self):
        return self.time_string





if __name__ == '__main__':
    print("main函数")

    it = InterceptPic()
    mf = ManageFota()
    wp = WatchProcess.WatchPro()


    mf.fota_manage_page()

    # driver = it.login("xuliyao", "xuliyao")
    # time.sleep(25)
    # driver.switch_to.frame("iframe412")
    # time.sleep(2)
    # mf.amc.addAdVideo(driver)

    # location = midbody.location
    # size = midbody.size
    #
    # print("location:",location)
    # print("size:",size)
    # w= size['width']
    # h= size['height']
    # x= location['x']
    # y =location['y']
    # print("w:{},h:{},x:{},y:{}".format(w,h,x,y))
    #
    # print("******************************稍等10s**************************")
    # time.sleep(10)
    # midbody = driver.find_element_by_xpath("//div[@class='modal-body']")
    # location = midbody.location
    # size = midbody.size
    # print("location:", location)
    # print("size:", size)
    # w = size['width']
    # h = size['height']
    # x = location['x']
    # y = location['y']
    # print("w:{},h:{},x:{},y:{}".format(w, h, x, y))

###############################完整测试内容##################################
    # driver = ReuseBrowser().fota_login_page()  # 首页登录
    # time.sleep(1)
    # mf.openUpgrade(driver, 2)  # 打开管理界面的升级包管理
    # time.sleep(0.5)
    # mf.openAddPage(driver)  # 打开“添加页面”
    # time.sleep(1)
    # mf.addTopfour(driver, "AFC100-CN-风机", 2, 2)  # 往”添加“页面的顶部4个元素”升级包名称“，”运营商“，”桩型号“，”发布时间“填指定内容
    # time.sleep(0.5)
    # mf.addRemark(driver, "注意此版修复项：\n 1.软件版本V4.1.0 2nd \n 2.去除急停滤波 \n 3.调整热管理策略")    #添加备注
    # time.sleep(0.5)
    # mf.isUpgradeForced(driver,"yes") #是否强制立即升级
    # time.sleep(0.5)
    # print("=======================================================================================\n"
    #       "1:广告视频； 2：配置文件； 3：BMS1; 4:CCU1; 5:CCU2; 6:EMS; 7:HCU; 8：TBOX1-MPU; 9:TBOX1-MCU;\n"
    #       "10:TBOX2-MCU; 11:TBOX2-MPU; 12:DCDC1; 13:DCDC2; 14:DCDC3; 15:DCDC4; 16:ACDC1; 17:ACDC2\n"
    #       "18:CMU1; 19:CMU2; 20:CMU3; 21:CMU4; 22:CMU5; 23:CMU6; 24:CMU7; 25:CMU8\n"
    #       "=======================================================================================\n")
    # mf.addUpgradeMoudle(driver,[1,2,3]) #选择需要添加什么模块，并添加对应模块的内容

###############################完整测试内容##################################












    # # try:
    # time.sleep(25)
    # element0 = driver.switch_to.active_element
    # print("elment0:{}".format(element0.text))
    # driver.switch_to.frame("iframe412")
    # plusbutton = driver.find_element_by_xpath("//*[@id='upgradePack']/div[1]/form/div/div/div[6]/button[3]")
    # print("plusbutton:{}".format(plusbutton.text))
    # plusbutton.click()  #点击“添加”按钮，打开添加页面
    # time.sleep(2)
    # # element1 = driver.switch_to.active_element
    # # print("element1:{}".format(element1.text))
    # # time.sleep(3)
    #
    # #print("开始选择“升级包名称”")
    # updPagNm = driver.find_elements_by_xpath("//input[@class='form-control' and @type='text']")[1]  # 获取”升级包名称“文本框这个元素
    # updPagNm.clear()  # 清空”升级包名称“文本框内容
    # updPagNm.send_keys("AFC-100 国冷")  # 往”升级包名称“文本框写入内容
    # time.sleep(0.5)
    #
    # #print("在添加页面点击运营商的框")
    # operat = driver.find_element_by_xpath('//div[@class="selecttree operator"]') #在添加页面点击运营商的div
    # print("operat.text:{},operat.tag:{},operat.size:{},operat.location:{}".format(operat.text, operat.tag_name, operat.size, operat.location))
    # operat.click()
    # time.sleep(0.5)
    #
    # #print("开始选择“度普（苏州）新能源科技有限公司”")
    # dupu = driver.find_elements_by_xpath('//*[@id="582020040800000001"]/a')[1]
    # print("dupu.text:{},dupu.tag:{},dupu.size:{},dupu.location:{}".format(dupu.text,dupu.tag_name,dupu.size,dupu.location))
    # dupu.click()
    #
    # #print("打开充电桩型号")
    # chargPile = driver.find_element_by_xpath('//div[@class="select charging_piles"]')  # 在添加页面点击运营商的div
    # print("chargPile.text:{},chargPile.tag:{},chargPile.size:{},chargPile.location:{}".format(chargPile.text, chargPile.tag_name, chargPile.size, chargPile.location))
    # chargPile.click()
    # time.sleep(0.5)
    #
    # #print("开始选择“(AFC-100-AH-CN)100度风冷国内版”")
    # charg_ch = driver.find_elements_by_xpath('//li[@class="select-dropdown-menu-item"]')[28]
    # print("charg_ch.text:{},charg_ch.tag:{},charg_ch.size:{},charg_ch.location:{}".format(charg_ch.text, charg_ch.tag_name, charg_ch.size, charg_ch.location))
    # charg_ch.click()
    #
    # #print("打开“发布时间”")
    # release_time= driver.find_element_by_xpath('//input[@class="form-control " and @name="add_time"]')
    # print("release_time.text:{},release_time.tag:{},release_time.size:{},release_time.location:{}".format(release_time.text, release_time.tag_name, release_time.size,release_time.location))
    #
    # time = datetime.now()
    # nowtime = time.strftime("%Y-%m-%d %H:%M")
    # print(nowtime)
    # release_time.click()
    # release_time.send_keys(nowtime)
    #
    # #print("打开'备注'")
    # remark = driver.find_element_by_xpath('//textarea[@class="form-control" and @name="remark"]')
    # remark.send_keys("这个版本大概升级5min，请耐心等待！！！")
