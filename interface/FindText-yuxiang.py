# -*- coding: utf-8-*-
from selenium import webdriver
from PIL import Image
from PIL import ImageFilter
import pytesseract
import time
import requests
import matplotlib.pyplot as plt
import cv2
import numpy as np


def image_to_string():
    img = Image.open('C:/Users/yuxiang.li/Desktop/no1.png')
    #img = img.convert("L")
    #threshold = 155
    #table = []
    #for i in range(256):
        #if i > threshold:
            #table.append(1)
        #else:
            #table.append(0)
    #img = img.point(table, "1")
    #img = img.convert("RGB")
    #width = img.size[0]
    #height = img.size[1]
    #print(width,height)
    #for x in range(width):
        #for y in range(height):
            #color = img.getpixel((x, y))
            #if color[0]<80 and color[1]<70 and color[2]<70:
            #if color <4.5:
                #img.putpixel((x,y),(255,255,255))


    #img.show()
    #img.save('C:/Users/yuxiang.li/Desktop/pic1.png')

    print(img.load())
    aa = pytesseract.image_to_string(img,config='isdigit')
    print ('EDLEE掐指一算,FOTA验证码:')
    return aa

def openbrowser(browser,url):
   #新建浏览器并打开fota界面
    browser.get(url)
    browser.maximize_window()
    time.sleep(1)
    return browser

def get_picture(x,y,w,h):
    # picture = (int(x), int(y), int(x+80), int(y+35))
    w1 = x+w
    h1 = y+h
    picture = (x, y, w1, h1)
    i = Image.open('C:/Users/yuxiang.li/Desktop/aa.png')
    #i.show()
    # 打开截图
    pic1 = i.crop(picture)
    # 使用crpo函数从一个图片中截取需要的部分
    path = 'C:/Users/yuxiang.li/Desktop/pic1.png'
    pic1.save(path)
    pic1.show()
    return pic1

def pic():
    img = cv2.imread('C:/Users/yuxiang.li/Desktop/pic1.png', 1)
    #print(img)
    pixel = int(np.mean(img[img > 222]))
    #print(pixel)
    img[img > 132] = pixel
    path1 = 'C:/Users/yuxiang.li/Desktop/pic3.png'
    image = cv2.imwrite(path1, img)
    return image
def pic_filter():
    path1 = 'C:/Users/yuxiang.li/Desktop/pic3.png'
    img1 = Image.open(path1)
    pic1 = img1.filter(ImageFilter.SMOOTH_MORE)#平滑滤镜加强
    pic1.show()
    pic1.save('C:/Users/yuxiang.li/Desktop/no1.png')
    return pic1

if __name__ == "__main__":
    a = webdriver.Chrome()  # 新建浏览器
    b = "http://admin.fota.du-power.com"
    aa = openbrowser(a,b)
    #输入账号密码
    zhanghu = aa.find_element_by_xpath('//*[@id="focus_first"]')
    time.sleep(1)
    zhanghu.send_keys('xuliyao')#输入账号
    time.sleep(1)
    mima = aa.find_element_by_xpath('//*[@name="password"]')
    time.sleep(1)
    mima.send_keys('xuliyao')  # 输入密码
    #browser.find_element_by_xpath('//*[@name='password']').send_keys('xuliyao')#输入账号
    time.sleep(1)
    # 获取验证码块区域位置
    imagelement = aa.find_element_by_xpath('//*[@id="verifyCanvas"]')
    # 获取图片坐标
    locations = imagelement.location
    print(locations)
    x = locations['x']
    y = locations['y']
    # 获取图片大小
    sizes = imagelement.size
    print(sizes)
    w = sizes['width']
    print("w:{}".format(w))
    h = sizes['height']
    print("h:{}".format(h))
    # 循环如果验证成功则退出循环
    while (True):
        # 截取保存图片
        savepath = 'C:/Users/yuxiang.li/Desktop/aa.png'
        aa.save_screenshot(savepath)
        img = Image.open(savepath)
        # img.show()
        time.sleep(1)
        get_picture(x, y, w, h)
        time.sleep(1)
        #图片降噪
        pic()
        #图片过滤
        pic_filter()
        # 识别图片
        a = image_to_string()
        a = a.replace(' ', '')  # 去除空格
        print(a)
        # 仅仅输入数字
        fil = filter(str.isdigit, a)
        new_text = ''
        for i in fil:
            new_text += i
        print(new_text)
        # time.sleep(1)
        # yanzhengma = aa.find_element_by_xpath('//*[@id="code"]')
        # time.sleep(1)
        # yanzhengma.clear()
        # print("清空输入框")
        # time.sleep(1)
        # yanzhengma.send_keys(new_text)  # 输入验证码
        # time.sleep(3)
        # aa.find_element_by_id("btn_login").click()
        # #time.sleep(5)
        # try:
        #     print("进入try界面")
        #     elements = aa.find_element_by_xpath('//*[@id="side-menu"]/li[1]/a')
        #
        # except :
        #     print("重新输入密码\n")
        #
        # else:
        #     print('successful')
        #     break




    
