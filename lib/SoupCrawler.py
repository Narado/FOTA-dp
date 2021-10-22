# -*- coding: utf-8 -*-
# @Time    :2021/10/9 10:09
# @Author  :Gao Lei
# @FileName:SoupCrawler.py
# @Software:PyCharm
import os
import time
import urllib.request
from bs4 import BeautifulSoup
from FOTA.lib import GetTime

class soup_crawler:
    def __init__(self):
        pass

    def find_element_by_className(self,driver,className):
        element = driver.find_element_by_xpath("//body[@class='page-md']")  # which is created by js
        wbHTML = driver.execute_script("return arguments[0].innerHTML;", element)
        self.save_pagesource_to_html(wbHTML)
        print("wbHTML:",wbHTML)
        buff = driver.page_source #获取当前网页内容
        self.save_pagesource_to_html(buff)
        print("buff:", buff)
        self.save_pagesource_to_html(buff)
        #编码方式
        html_doc = buff.encode("utf-8")

        soup  = BeautifulSoup(wbHTML, 'html.parser')
        element = soup.find(attrs={'class':className})
        print("element:",element)
        return element

    def save_pagesource_to_html(self,pagesource):
        time.sleep(1)
        now_time = GetTime.getTime().nowtimeToString()
        try:
            os.mkdir("..\\dp\\HTML")    #在FOTA/dp/目录下面创建目录HTML
        except(FileExistsError):
            print("文件夹已经存在")
        # os.mknod("..\\dp\\HTML\\{}.html".format(now_time))  #在HTML中创建当前时间的.html文件
        fp = open("..\\dp\\HTML\\{}.html".format(now_time),'w')    #直接打开一个文件，如果文件不存在则创建文件
        fp.write(pagesource)