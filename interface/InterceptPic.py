#导入驱动的包和控制时间的库
import psutil
from selenium import webdriver
import time
import datetime
from PIL import Image
from FOTA.conf import  readconfig
from FOTA.lib import GetTime

# from FindText import *


class InterceptPic:
    def login(self,account,password):
        """
        param
        """

        #设置网页路径
        # url = "http://admin.fota.du-power.com/"
        url = readconfig.readconfig("..\\conf\\Fota.ini","baseconf","host")
        #初始化驱动
        driver = webdriver.Chrome()
        #打开度普FOTA
        driver.get(url)
        #等待页面加载完成
        time.sleep(3)
        #最大化浏览器窗口
        driver.maximize_window()
        #先找到指定的文本框对应的元素
        account_name = driver.find_element_by_id("focus_first")
        pswrd = driver.find_element_by_name("password")
        #往元素对应的文本框输入值
        account_name.send_keys(account)
        pswrd.send_keys(password)

        # 保存当前的网页
        self.driver = driver
        return driver

    def cropVeryCode(self,driver):
        url = driver.current_url
        #抓取页面
        print("正在抓取->%s" %url)
        #把当前的网页地址按照“//”和“.”来划分，取第2个和第3个‘.’前面的字段
        urlcontent = url.split('//')[1]
        uid = urlcontent.split('.')[1]
        cid = urlcontent.split('.')[2]
        print("uid:%s"%uid)
        print("cid:%s"%cid)

        now_time = GetTime.getTime().nowtimeToString()    #获取当前时间的字符串形式
        scresult = driver.get_screenshot_as_file("C:\\09_photo\\screenshot\\{}-{}-{}.png".format(uid,cid,now_time))
        if scresult==1:
            img_name= "{}-{}-{}".format(uid,cid,now_time)
            img_path = "C:\\09_photo\\screenshot\\{}-{}-{}.png".format(uid,cid,now_time)
            print("当前网页已保存{}".format(img_name))
        else:
            print("保存网页为图片失败！")
        #截取指定位置的图片
        print("{}.png正在裁剪中。。。".format(img_name))
        im = Image.open(img_path)
        # location = im.location
        # x0= location['x']
        # y0= location['y']

        w0= im.width
        h0= im.height
        print("w0:{},h0:{}".format(w0, h0))
        # print("x0:{},y0:{},w0:{},h0:{}".format(x0,y0,w0,h0))
        #分辨率不一样，按照两次图片的大小求个比例
        x_rate = 1920/1213
        y_rate = 908/573
        x = 683*x_rate
        y = 429*y_rate
        w = 82*x_rate
        h = 38*y_rate
        region = im.crop((x,y,x+w,y+h))  #把图片对象按照横纵坐标来画一个区域变成另外一个图像对象

        cropimg_path = 'C:\\09_photo\\screenshot_final\\{}-final.png'.format(img_name)
        region.save(cropimg_path) #向指定文件夹中的文件名 来保存该截好的区域图像
        print("裁剪完成，图片展示：")
        im2 = Image.open(cropimg_path)
        # im2.show()
        return im2


    def get_sessid(self):
        return self.session_id


    def get_commandurl(self):
        return self.comurl

    def get_driver(self):
        return self.driver







if __name__ == '__main__':
    ic = InterceptPic()
    ic.interceptPic("xuliyao","xuliyao")

# print("account:",account_name,'\n')
# print("password:",pswrd,'\n')