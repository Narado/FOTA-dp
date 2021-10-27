# -*- coding: utf-8 -*-
# @Time    :2021/9/30 8:40
# @Author  :Gao Lei
# @FileName:AFC_CN100_Controller.py
# @Software:PyCharm

import os
import time
import datetime
from lib import ChangeName
from lib import MouseOperate
from conf import readconfig

class afcCN100Controller:
    changename = ChangeName.changeName()
    mo = MouseOperate.mouse_operate()  # 创建鼠标操作对象
    def __init__(self):
        pass

    def AFC_CN100(self, driver, module_classname):
        low_classname = self.changename.changeNametoLow(module_classname)  # 将所有的模块类名小写并去除其中的"-"

        # 将“选择文件”按钮的名称分隔开
        selectfile_xpath_name_list = \
            [
             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//button[contains(text(),"选择文件")]'
            ]

        # 将“选择文件”弹出的文件框后续的操作封装的脚本的路径 分隔开
        uploadprocess_xpath_list = \
            [
             '..\\lib\\upload_',
             low_classname,
             '_pro_cont.au3'
             ]

        uploadapp_xpath_list = \
            [
             '..\\lib\\upload_',
             low_classname,
             '_app.au3'
             ]


        software_xpath_list =\
            [

             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//input[@name="software_version"]'

            ]

        hardware_xpath_list = \
            [

             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//input[@name="hardware_version"]'

             ]

        releasetime_xpath_list =\
            [
             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//input[@name="release_time"]'

             ]
        section_name_list = [low_classname, "conf"]
        swoption_name_list = [low_classname, "_swversion"]
        hwoption_name_list = [low_classname, "_hwversion"]
        rtoption_name_list = [low_classname, "_releasetime"]

        #获取路径
        select_xpath = self.changename.changeNametoCombination(selectfile_xpath_name_list)  # 获取“选择文件”按钮路径
        uploadprocess_sript_path = self.changename.changeNametoCombination(uploadprocess_xpath_list) #上传流程控制的操作的au3文件的路径
        uploadapp_sript_path = self.changename.changeNametoCombination(uploadapp_xpath_list) #上传app的操作的au3文件的路径
        software_xpath = self.changename.changeNametoCombination(software_xpath_list)  # 获取“软件版本”输入框的路径
        hardware_xpath = self.changename.changeNametoCombination(hardware_xpath_list)  # 获取“硬件版本”输入框的路径
        releasetime_xpath = self.changename.changeNametoCombination(releasetime_xpath_list)  # 获取“释放时间”输入框的路径

        #获取配置文件中的section  和 option

        section_name = self.changename.changeNametoCombination(section_name_list)  # 根据classname获取sectionname
        swoption_name = self.changename.changeNametoCombination(swoption_name_list)  # 根据classname获取软件的optionname
        hwoption_name = self.changename.changeNametoCombination(hwoption_name_list)  # 根据classname回去硬件的optionname
        rtoption_name = self.changename.changeNametoCombination(rtoption_name_list)  # 根据classname回去版本释放时间的optionname

        # AFC-CN100所支持的控制器，其添加模块的模板
        # 1.流程控制文件
        control_element = driver.find_elements_by_xpath(select_xpath)[0]  # 定位控制器的流程控制文件
        self.mo.slideroller(driver, control_element)  # 将滚轮移动到“选择文件'位置
        time.sleep(1)
        self.mo.mouseHover(driver, control_element)  # 利用鼠标悬停来点击”选择文件“
        print("点击选择文件后，请耐心等待1s...")
        time.sleep(1.5)
        os.system(uploadprocess_sript_path)  # 通过AUtoIt v3封装的对窗口的操作脚本来完成上传文件操作
        time.sleep(2)

        # 2.应用文件
        app_element = driver.find_elements_by_xpath(select_xpath)[2]  # 定位应用文件
        self.mo.slideroller(driver, app_element)  # 将滚轮移动到“选择文件'位置
        time.sleep(1.5)
        self.mo.mouseHover(driver, app_element)  # 利用鼠标悬停来点击”选择文件“
        print("点击选择文件后，请耐心等待1s...")
        time.sleep(1)
        os.system(uploadapp_sript_path)  # 通过AUtoIt v3封装的对窗口的操作脚本来完成上传文件操作
        time.sleep(1)

        # 3.填写软件版本
        swversion_element = driver.find_element_by_xpath(software_xpath)  # 定位软件版本位置
        self.mo.slideroller(driver, swversion_element)  # 将滚轮移动到“配置文件版本'位置
        time.sleep(0.5)
        swversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, swoption_name)
        print(swversiontxt)
        swversion_element.send_keys(swversiontxt)
        time.sleep(0.5)

        # 4.填写硬件版本
        hwversion_element = driver.find_element_by_xpath(hardware_xpath)  # 定位硬件版本位置
        self.mo.slideroller(driver, hwversion_element)  # 将滚轮移动到“配置文件版本'位置
        time.sleep(0.5)
        hwversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, hwoption_name)
        print(hwversiontxt)
        hwversion_element.send_keys(hwversiontxt)
        time.sleep(0.5)

        # 5.发布时间
        releaseTime = readconfig.readconfig("..\\conf\\Fota.ini", section_name, rtoption_name)
        if (releaseTime == None) or (releaseTime == ""):  # 默认输入为空
            timen = datetime.now()
            nowtime = timen.strftime("%Y-%m-%d %H:%M")
        else:
            nowtime = releaseTime
        print("nowtime:", nowtime)
        release_element = driver.find_element_by_xpath(releasetime_xpath)  # 定位发布时间
        release_element.send_keys(nowtime)  # 发布时间输入当前时间
        return driver

    def TBOX_MPU(self,driver , module_classname):
        low_classname = self.changename.changeNametoLow(module_classname)  # 将所有的模块类名小写并去除其中的"-"

        # 将“选择文件”按钮的名称分隔开
        selectfile_xpath_name_list = \
            [
                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//button[contains(text(),"选择文件")]'
            ]

        # 将“选择文件”弹出的文件框后续的操作封装的脚本的路径 分隔开

        uploadupdate_xpath_list = \
            [
                '..\\lib\\upload_',
                low_classname,
                '_updatefile.au3'
            ]

        software_xpath_list = \
            [

                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//input[@name="software_version"]'

            ]

        hardware_xpath_list = \
            [

                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//input[@name="hardware_version"]'

            ]

        releasetime_xpath_list = \
            [
                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//input[@name="release_time"]'

            ]
        section_name_list = [low_classname, "conf"]
        swoption_name_list = [low_classname, "_swversion"]
        hwoption_name_list = [low_classname, "_hwversion"]
        rtoption_name_list = [low_classname, "_releasetime"]

        # 获取路径
        select_xpath = self.changename.changeNametoCombination(selectfile_xpath_name_list)  # 获取“选择文件”按钮路径
        uploadapp_sript_path = self.changename.changeNametoCombination(uploadupdate_xpath_list)  # 上传升级文件的操作的au3文件的路径
        software_xpath = self.changename.changeNametoCombination(software_xpath_list)  # 获取“软件版本”输入框的路径
        hardware_xpath = self.changename.changeNametoCombination(hardware_xpath_list)  # 获取“硬件版本”输入框的路径
        releasetime_xpath = self.changename.changeNametoCombination(releasetime_xpath_list)  # 获取“释放时间”输入框的路径

        # 获取配置文件中的section  和 option

        section_name = self.changename.changeNametoCombination(section_name_list)  # 根据classname获取sectionname
        swoption_name = self.changename.changeNametoCombination(swoption_name_list)  # 根据classname获取软件的optionname
        hwoption_name = self.changename.changeNametoCombination(hwoption_name_list)  # 根据classname回去硬件的optionname
        rtoption_name = self.changename.changeNametoCombination(rtoption_name_list)  # 根据classname回去版本释放时间的optionname

        # AFC-CN100所支持的控制器，其添加模块的模板


        # 1.升级文件
        app_element = driver.find_element_by_xpath(select_xpath) # 定位应用文件
        self.mo.slideroller(driver, app_element)  # 将滚轮移动到“选择文件'位置
        time.sleep(1)
        self.mo.mouseHover(driver, app_element)  # 利用鼠标悬停来点击”选择文件“
        print("点击选择文件后，请耐心等待1s...")
        time.sleep(1)
        os.system(uploadapp_sript_path)  # 通过AUtoIt v3封装的对窗口的操作脚本来完成上传文件操作
        time.sleep(1)

        # 2.填写软件版本
        swversion_element = driver.find_element_by_xpath(software_xpath)  # 定位软件版本位置
        self.mo.slideroller(driver, swversion_element)  # 将滚轮移动到“配置文件版本'位置
        time.sleep(0.5)
        swversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, swoption_name)
        print(swversiontxt)
        swversion_element.send_keys(swversiontxt)
        time.sleep(0.5)

        # 3.填写硬件版本
        hwversion_element = driver.find_element_by_xpath(hardware_xpath)  # 定位硬件版本位置
        self.mo.slideroller(driver, hwversion_element)  # 将滚轮移动到“配置文件版本'位置
        time.sleep(0.5)
        hwversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, hwoption_name)
        print(hwversiontxt)
        hwversion_element.send_keys(hwversiontxt)
        time.sleep(0.5)

        # 4.发布时间
        releaseTime = readconfig.readconfig("..\\conf\\Fota.ini", section_name, rtoption_name)
        if (releaseTime == None) or (releaseTime == ""):  # 默认输入为空
            timen = datetime.now()
            nowtime = timen.strftime("%Y-%m-%d %H:%M")
        else:
            nowtime = releaseTime
        print("nowtime:", nowtime)
        release_element = driver.find_element_by_xpath(releasetime_xpath)  # 定位发布时间
        release_element.send_keys(nowtime)  # 发布时间输入当前时间
        return driver

    def posterAndConfig(self, driver, module_classname):
        low_classname = self.changename.changeNametoLow(module_classname)  # 将所有的模块类名小写并去除其中的"-"
        #所有的xpath
        # “选择文件”xpath
        selectfile_xpath_name_list = \
            [
             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//button[contains(text(),"选择文件")]'
            ]

        # 将“选择文件”弹出的文件框后续的操作封装的脚本的路径 分隔开
        uploadfile_script_xpath_list = \
            [
             '..\\lib\\upload_',
             low_classname,
             '.au3'
             ]
        #版本文件输入框xpath
        version_xpath_list =\
            [

             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//input[@name="version"]'

            ]

        #发布时间xpath
        releasetime_xpath_list =\
            [
             "//div[@class=",
             '"',
             module_classname,
             '"',
             ']//input[@name="release_time"]'

             ]

        #name
        section_name_list = [low_classname, "conf"]
        option_name_list = [low_classname, "_version"]
        rtoption_name_list = [low_classname, "_releasetime"]

        select_xpath = self.changename.changeNametoCombination(selectfile_xpath_name_list)  # 获取“选择文件”按钮路径
        uploadfile_sript_path = self.changename.changeNametoCombination(uploadfile_script_xpath_list)  # 获取“上传文件”窗口AutoIt V3操作的脚本 的路径
        version_xpath = self.changename.changeNametoCombination(version_xpath_list)  # 获取“版本”输入框的路径
        releasetime_xpath = self.changename.changeNametoCombination(releasetime_xpath_list)  # 获取“释放时间”输入框的路径

        section_name = self.changename.changeNametoCombination(section_name_list)  # 根据classname获取sectionname
        versionoption_name = self.changename.changeNametoCombination(option_name_list)  # 根据classname获取version的optionname
        rtoption_name = self.changename.changeNametoCombination(rtoption_name_list)  # 根据classname回去版本释放时间的optionname

# 广告和配置文件添加模块的模板
        # 1.文件
        app_element = driver.find_element_by_xpath(select_xpath)  # 定位文件
        self.mo.slideroller(driver, app_element)  # 将滚轮移动到“选择文件'位置
        time.sleep(1)
        self.mo.mouseHover(driver, app_element)  # 利用鼠标悬停来点击”选择文件“
        print("点击选择文件后，请耐心等待1s...")
        time.sleep(1)
        os.system(uploadfile_sript_path)  # 通过AUtoIt v3封装的对窗口的操作脚本来完成上传文件操作
        time.sleep(1)

        # 3.填写软件版本
        version_element = driver.find_element_by_xpath(version_xpath)  # 定位软件版本位置
        self.mo.slideroller(driver, version_element)  # 将滚轮移动到“配置文件版本'位置
        time.sleep(0.5)
        swversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, versionoption_name)
        print(swversiontxt)
        version_element.send_keys(swversiontxt)
        time.sleep(0.5)


        # 5.发布时间
        releaseTime = readconfig.readconfig("..\\conf\\Fota.ini", section_name, rtoption_name)
        if (releaseTime == None) or (releaseTime == ""):  # 默认输入为空
            timen = datetime.now()
            nowtime = timen.strftime("%Y-%m-%d %H:%M")
        else:
            nowtime = releaseTime
        print("nowtime:", nowtime)
        release_element = driver.find_element_by_xpath(releasetime_xpath)  # 定位发布时间
        release_element.send_keys(nowtime)  # 发布时间输入当前时间
        return driver

    def systemSetting(self, driver, module_classname):
        low_classname = self.changename.changeNametoLow(module_classname)  # 将所有的模块类名小写并去除其中的"-"
        # 所有的xpath

        # 版本文件输入框xpath
        version_xpath_list = \
            [

                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//input[@name="system_software_version"]'

            ]

        # 发布时间xpath
        releasetime_xpath_list = \
            [
                "//div[@class=",
                '"',
                module_classname,
                '"',
                ']//input[@name="release_time"]'

            ]

        # name
        section_name_list = [low_classname, "conf"]
        option_name_list = [low_classname, "_swversion"]
        rtoption_name_list = [low_classname, "_releasetime"]


        version_xpath = self.changename.changeNametoCombination(version_xpath_list)  # 获取“版本”输入框的路径
        releasetime_xpath = self.changename.changeNametoCombination(releasetime_xpath_list)  # 获取“释放时间”输入框的路径

        section_name = self.changename.changeNametoCombination(section_name_list)  # 根据classname获取sectionname
        versionoption_name = self.changename.changeNametoCombination(
            option_name_list)  # 根据classname获取version的optionname
        rtoption_name = self.changename.changeNametoCombination(rtoption_name_list)  # 根据classname回去版本释放时间的optionname

        # 系统设置的模板
        # 1.填写软件版本

        version_element = driver.find_element_by_xpath(version_xpath)  # 定位软件版本位置
        version_value = version_element.get_attribute("value")
        print("version_value:",version_value)
        if version_value == None or version_value =="":
            self.mo.slideroller(driver, version_element)  # 将滚轮移动到“配置文件版本'位置
            time.sleep(0.5)
            swversiontxt = readconfig.readconfig("..\\conf\\Fota.ini", section_name, versionoption_name)
            print(swversiontxt)
            version_element.send_keys(swversiontxt)
            time.sleep(0.5)

            #2.发布时间
            releaseTime = readconfig.readconfig("..\\conf\\Fota.ini", section_name, rtoption_name)
            if (releaseTime == None) or (releaseTime == ""):  # 默认输入为空
                timen = datetime.now()
                nowtime = timen.strftime("%Y-%m-%d %H:%M")
            else:
                nowtime = releaseTime
            print("nowtime:", nowtime)
            release_element = driver.find_element_by_xpath(releasetime_xpath)  # 定位发布时间
            release_element.send_keys(nowtime)  # 发布时间输入当前时间

        else:
            pass
        return driver