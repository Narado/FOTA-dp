# -*- coding: utf-8 -*-
# @Time    :2021/9/29 16:00
# @Author  :Gao Lei
# @FileName:ChangeName.py
# @Software:PyCharm

import string
import os
import re
from selenium import webdriver
from FOTA.interface import InterceptPic
from selenium.common.exceptions import WebDriverException
import time
import winsound


class changeName:
    def __init__(self):
        pass

    def changeNametoLow(self, name):
        lowname = name.lower()
        name_list = lowname.split('-')
        newlowname = ""
        for namepart in name_list:
            newlowname = newlowname + namepart
        return newlowname


    def changeNametoCombination(self,name_list):
        newlowname = ""
        for namepart in name_list:
            newlowname = newlowname + namepart
        return newlowname

    def stringL_to_intL(self,string_list):
        int_list=[]
        list1 = string_list.split('[')
        list2 = list1[1].split(']')
        list3 = list2[0].split(',')
        print(list3)
        for s in list3:
            i = int(s)
            int_list.append(i)
        return int_list

    def stringL_removeFrame(self,string_list):
        rf_list=[]
        list1 = string_list.split('[')
        list2 = list1[1].split(']')
        list3 = list2[0].split(',')
        print(list3)
        for s in list3:
            rf_list.append(s)
        print("rf_list:",rf_list)
        return rf_list

    def get_styleattrs(self, string_list):
        style_dic = {}
        attrs_list = string_list.split(";")
        print("attrs_list：",attrs_list)
        for attrs in attrs_list:

            print("attrs：", attrs)
            if (attrs != None) and (attrs != ""):
                attr_list = attrs.split(":")
                print("attr_list：", attr_list)
                style_dic.update({attr_list[0]: attr_list[1]})
            else:
                print("attrs为空")
        return style_dic


    def removeSpacebyJS(self,driver,strtext):
        js = "document.write('{}'.replace(/\s*/gm,''))".format(strtext)
        # js = 'document.write('+strtext+'.replace(/\s*/gm,""))'
        # str = driver.execute_script('document.write("2021-10-13 15:35:33    升级包下载中".replace(/\s*/gm,""))')
        str = driver.execute_script(js)
        return str



    def removeSpacebyPY(self,strtext):
        new_str =strtext.replace(" ","")
        return new_str

    def removeSpacebyRE(self,strtext):
        new_str = re.sub(r'\s*','',strtext)
        return new_str

    def findChinese(self,strtext):
        new_str = re.findall(r"[\u4e00-\u9fa5]*",strtext)
        final_str =[]
        for i in new_str:
            if i !="":
                final_str.append(i)
        return final_str


if __name__ == '__main__':


    # string_list='[A1111AHC0212101800,A1111AHC0212108002]'
    # rf_list = changeName().stringL_removeFrame(string_list)

    str = "2021-10-13 15:35:33    升级包下载中\n\n2021-10-13 15:35:41    升级包下载完成\n\n2021-10-13 15:35:41    升级包安装中\n\n2021-10-13 15:45:04    升级包安装完成"
    str2 = "2021-10-13 15:35:33    升级包下载中"
    print(str)
    # newstr =  changeName().removeSpacebyPY(str)
    driver = webdriver.Chrome()
    changeName().removeSpacebyJS(driver, str2)
    newstr = changeName().removeSpacebyPY(str)
    newstr2 = changeName().removeSpacebyRE(str)
    print(newstr)
    print(newstr2)
    newstr3 = re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s*",str)
    newstr5 = re.findall(r"[\u4e00-\u9fa5]+",str2)
    print(newstr3.group())
    print(len(newstr5))

    try:
        driver.execute_script("alert('升级包下载失败,请检查充电桩！');")
    except WebDriverException:
        pass

    winsound.Beep(440,2000)
    winsound.PlaySound("升级包下载失败,请检查充电桩！", winsound.SND_ASYNC)
    time.sleep(2)
    print(driver.switch_to.alert.text)
    driver.switch_to.alert.accept() #确认
