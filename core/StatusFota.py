# -*- coding: utf-8 -*-
# @Time    :2021/10/13 10:12
# @Author  :Gao Lei
# @FileName:Statuspy
# @Software:PyCharm
import time
from conf import readconfig
from lib import MouseOperate
from core import LoginFota
from lib import ChangeName
from lib import SoundAlert
from interface import InterceptPic
from lib import MultiThread

DOWN_DIC={
"DOWN_FAIL" : 0,
"DOWN_SUCCESS" : 1,
"DOWN_ING" : 2
}

UPGRADE_DIC={
"UPGRADE_FAIL" : 0,
"UPGRADE_SUCCESS" : 1,
"UPGRADE_NORESPONSE" :2,
"UPGRADE_ING" : 3
}


class StatusFota(object):
    mo = MouseOperate.mouse_operate()
    lf = LoginFota.LoginFota()
    cn = ChangeName.changeName()
    sa = SoundAlert.sound_alert()
    ip= InterceptPic.InterceptPic()
    mt = MultiThread.multi_thread()

    down_result = DOWN_DIC["DOWN_ING"]
    upgrade_result = UPGRADE_DIC["UPGRADE_ING"]
    def __init__(self):
        pass

    # 打开升级包管理页面
    def openStatus(self, driver, manageID=5):
        """
        @Author：GaoLei
        :param driver: 整个网页运行的驱动
        :param manageID: 1：充电桩信息； 2:升级包管理； 3：升级任务； 4：升级统计； 5：升级状态； 6：系统；
        :return:
        """
        # driver = webdriver.Chrome()
        collapse = driver.find_elements_by_xpath("//div[@class='sidebar-collapse']//li")[0]
        classvalue = collapse.get_attribute("class")
        print("classvalue:", classvalue)
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
            packManage_element = driver.find_elements_by_xpath("//span[@class='nav-label']")[6]  # 找到”系统“标签的位置

        packManage_element.click()  # 打开升级状态界面

    def reSend(self,driver):
        resend_button = driver.find_elements_by_xpath("//div[@col-id='manage']//span//button[contains(text(),'重新下发')]")[
            0]  # 重新下发按钮
        resend_button.click()  # 点击"重新下发"按钮
        time.sleep(1)
        popup_form = driver.find_element_by_xpath("//div[@class='modal fade in']//div[@class='popup-form']")
        self.mo.mouseOnlyHover(driver, popup_form)  # 鼠标悬停在弹窗上
        resend_button2 = driver.find_elements_by_xpath("//div[@class='modal-footer']//button[contains(text(),'重新下发')]")[
            0]
        resend_button2.click()
        print("已经点击重新下发按钮，请耐心等待5s后，页面自动刷新")
        self.sa.speak("已经点击重新下发按钮，请耐心等待5秒后，页面自动刷新!")
        return driver


    # 等待指令下发状态-下发成功
    def waitSendStatusOK(self, driver, taskName):
        """
        :param driver: 网页驱动
        :param taskName: 升级任务名称
        :return:
        """
        driver.switch_to.frame("iframe411")  # 将driver切换到浮动的框架
        uppack = driver.find_element_by_xpath("//input[@name='taskName' and @placeholder='升级任务名称']")
        uppack.send_keys(taskName)
        time.sleep(0.25)
        findpack = driver.find_element_by_xpath("//button[contains(text(),'查询') and @type='button']")
        findpack.click()
        time.sleep(0.5)
        # forceUp = driver.find_elements_by_xpath("//div[@col-id='force']")[1]
        self.mo.sliderollerRow(driver, 'mauna-body-viewport', 300)  # #整个查询内容的div向右移动380px，能看到“指令下发状态”位置
        time.sleep(2)
        #查看指令下发状态，1.如果下发失败，需要重新下发(3次)(一般下发失败的原因是升级桩不在线); 2.如果下发成功，直接打开管理中的日志，查看日志内容
        sendstatus = driver.find_elements_by_xpath("//div[@col-id='sendStatus']")[1]
        time.sleep(0.25)
        result = sendstatus.get_attribute("title")  #指令下发状态的值
        fail_counter = 0
        while result == "下发失败":
            if(fail_counter>2):
                print("重试3次,结束任务")
                break
            else:
                fail_counter = fail_counter+1
                print("************************************************************"
                      "下发失败，请检查升级桩，保证升级桩在线，等待1min后，系统将会自动重新下发。"
                      "************************************************************")
                self.sa.beep()
                self.sa.speak("下发失败，请检查升级桩，保证升级桩在线，等待两分钟后，系统将会自动重新下发!")
                time.sleep(10)
                self.reSend(driver) #重新下发
                time.sleep(5)
                refresh_element = driver.find_element_by_xpath("//button[contains(text(),'刷新') and @type='button']")
                refresh_element.click() #点击"刷新"按钮
                time.sleep(1)
                sendstatus = driver.find_elements_by_xpath("//div[@col-id='sendStatus']")[1]
                time.sleep(0.25)
                result = sendstatus.get_attribute("title")  #查看指令下发状态
                print("此时指令下发状态:", result)

        return result

    #查看日志内容
    def seeDailyLog(self,driver):
        """
        :param driver: 网页驱动
        :return:
        """
        dr_button = driver.find_elements_by_xpath("//div[@col-id='manage']//span//button[contains(text(),'日志')]")[
            0]
        dr_button.click()  # 点击"日志"按钮
        # driver.switch_to.frame("iframe411")  # 将driver切换到浮动的框架
        time.sleep(1)
        modal = driver.find_element_by_xpath("//div[@class='modal fade in']")
        print("modal:", modal)
        self.mo.mouseOnlyHover(driver, modal)   #将鼠标悬浮到日志的弹窗上
        time.sleep(1)
        dr_content = driver.find_element_by_xpath("//div[@class='popup-form']")
        drtext = dr_content.text  # 获取日志文本
        print("drtext:\n", drtext)
        chinese_list = self.cn.findChinese(drtext)  # 获取中文字符
        return chinese_list

    #从日志界面返回并刷新
    def backAndFresh(self,driver):
        closebt = driver.find_elements_by_xpath("//div[@class='modal-footer']//button[contains(text(),'关闭')]")[
            0]  # 点击关闭
        closebt.click()
        # time.sleep(1.5)
        # driver.switch_to.frame("iframe411")  # 回到升级状态界面
        time.sleep(2)
        refreshbt = driver.find_element_by_xpath("//button[contains(text(),'刷新') and @type='button']")  # 点击刷新
        refreshbt.click()
        return driver

    #监控升级状态
    def monitorUpStatus(self,driver):
        """
        :param driver: 网页驱动
        :return:
        """
        print("*********************************\n"
              "下发成功，将会打开日志，查看升级进度。。。\n"
              "*********************************\n")
        self.sa.speak("下发成功，将会打开日志，查看升级进度!")
        chinese_list = self.seeDailyLog(driver)
        print("chinese_list:",chinese_list)
        downloading_index = 0 #升级包下载中的index
        for i in range(len(chinese_list)):
            print("member:{}".format(chinese_list[i]))
            if chinese_list[i] == "升级包下载中":
                downloading_index = i
                print("downloading_index:",downloading_index)
                break   #如果找到了升级包下载中的行数，选择跳出循环
        #等待升级包下载完成或下载失败的提示
        while(1):
            print("升级包下载中，请耐心等待。。。")
            self.sa.speak("升级包下载中，请耐心等待")
            self.backAndFresh(driver)   #点击返回按钮并刷新
            time.sleep(2)
            chinese_list = self.seeDailyLog(driver) #重新查看日志
            try:
                print("chinese_list[downloading_index+1]:",chinese_list[downloading_index+1])
                if chinese_list[downloading_index+1] == "升级包下载完成":
                    print("升级包下载完成，请等待安装")
                    self.sa.speak("升级包下载完成，请等待安装")
                    time.sleep(2)
                    self.down_result = DOWN_DIC["DOWN_SUCCESS"]
                    break
                elif chinese_list[downloading_index+1] == "升级包下载失败":
                    print("升级包下载失败")
                    self.sa.beep()
                    self.sa.speak("升级包下载失败,请检查充电桩是否在线！")
                    time.sleep(2)
                    self.down_result = DOWN_DIC["DOWN_FAIL"]
                    break
            except:
                print("没有找到下载结果,继续查找")
                pass

        # 下载完成后，等到升级包安装完成，或者终端无响应，或者升级包安装失败
        if self.down_result == DOWN_DIC["DOWN_SUCCESS"] :
            while(1):
                print("升级包安装中，请耐心等待。。。")
                self.sa.speak("升级包安装中，请耐心等待")
                self.backAndFresh(driver)  # 点击返回按钮并刷新
                time.sleep(1)
                chinese_list = self.seeDailyLog(driver)  # 重新查看日志
                try:
                    if chinese_list[downloading_index + 3] == "升级包安装完成":
                        print("恭喜您，升级包安装完成！")
                        speakstr = "恭喜您，升级包安装完成"
                        abspath = ("..\\dp\\images\\升级包安装完成3.PNG")  # 相对于SoundAlert.py的相对路径
                        tasks = {self.sa.speak : (speakstr,),self.sa.playCatton:(abspath,)}
                        self.mt.runthreads_meanwhile(tasks)
                        time.sleep(5)
                        self.upgrade_result = UPGRADE_DIC["UPGRADE_SUCCESS"]
                        break

                    elif chinese_list[downloading_index + 3] == "升级包安装失败":
                        print("升级包下载失败")
                        self.sa.beep()
                        self.sa.electronicAlert()
                        self.sa.speak("升级包安装失败,请检查充电桩!")
                        time.sleep(2)
                        self.upgrade_result = UPGRADE_DIC["UPGRADE_FAIL"]
                        break
                    elif chinese_list[downloading_index + 3] == "终端无响应":
                        print("终端无响应")
                        self.sa.beep()
                        self.sa.speak("终端无响应,请检查充电桩!")
                        time.sleep(2)
                        self.upgrade_result = UPGRADE_DIC["UPGRADE_NORESPONSE"]
                        break
                except:
                    print("没有找到安装结果，继续查找")
        return driver


    def fota_status_page(self,driver,status_time_string):
        print("进入fota_status函数")
        now_time = status_time_string  # 获取创建升级包时的时间
        print("获取创建升级包时的时间:", now_time)
        task_name = readconfig.readconfig("..\\conf\\ini", "taskconf", "task_name") + now_time # 从配置文件获取信息
        driver.refresh()
        time.sleep(1)
        self.openStatus(driver,5)    # 打开升级状态页面
        result = self.waitSendStatusOK(driver,task_name) #等待下发指令成功
        if(result == "下发成功"):
            self.monitorUpStatus(driver) #通过查看日志，监控升级结果
        else:
            print("下发失败3次，结束升级任务")
            self.sa.speak("下发失败三次，将结束升级任务")
        return


if __name__ == '__main__':
    sf = StatusFota()
    driver = sf.lf.fota_login_page()

    time.sleep(15)
    sf.fota_status_page(driver,'20211027101646')