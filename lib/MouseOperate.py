# -*- coding: utf-8 -*-
# @Time    :2021/9/28 16:38
# @Author  :Gao Lei
# @FileName:MouseOperate.py
# @Software:PyCharm

from selenium.webdriver.common.action_chains import ActionChains
from core import LoginFota
import time
from interface import InterceptPic
from lib import  SoupCrawler
class mouse_operate:

    sc = SoupCrawler.soup_crawler()
    def __init__(self):
        pass


    def mouseOnlyHover(self, driver, element):  # 鼠标悬停并单机
        ac = ActionChains(driver)
        ac.move_to_element(element)
        ac.perform()

    def mouseHover(self, driver, element):  # 鼠标悬停并单机
        ac = ActionChains(driver)
        ac.move_to_element(element)
        ac.click()
        ac.perform()

    def mouseClickAndHold(self, driver,element):
        ac = ActionChains(driver)
        ac.click_and_hold(element)
        ac.perform()

    def mouseDrop(self,driver,element,x_offset,y_offset):
        ac = ActionChains(driver)
        ac.click_and_hold(element)
        ac.drag_and_drop_by_offset(element, x_offset, y_offset)
        ac.perform()

    def slideroller(self, driver, target_element):  #纵向滚轮

        driver.execute_script("arguments[0].scrollIntoView();", target_element)

    def sliderollerRow(self,driver,classname,leftInstance):    #横向滚轮
        js = "document.getElementsByClassName('{}')[0].scrollTo({},{});".format(classname,leftInstance,0)
        print("js:", js)
        driver.execute_script(js)

    def sliderollerCol(self,driver,classname,topInstance):    #纵向滚轮,一定要移动可以移动的元素
        js = "document.getElementsByClassName('{}')[0].scrollTo({},{});".format(classname,0,topInstance)
        print("js:", js)
        driver.execute_script(js)

    def modifycssText(self,driver,classname,stylecontent):
        js  =  "document.getElementsByClassName('{}')[0].style.cssText='{}';".format(classname, stylecontent)
        print("js:",js)
        driver.execute_script(js)


if __name__ == '__main__':
    driver =InterceptPic.InterceptPic().login("xuliyao","xuliyao")
    time.sleep(13)
    driver.switch_to.frame("iframe412")  # 将driver切换到浮动的框架
    time.sleep(2)

    # driver.execute_script("document.getElementsByClassName('mauna-body-viewport')[0].scrollTo({},{})".format(200,0))
    mouse_operate().sliderollerRow(driver,'mauna-body-viewport',250 )


