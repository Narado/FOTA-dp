#coding=utf-8


from interface.InterceptPic import *
from interface.FindText import *
from conf import readconfig
from lib import SoundAlert

class LoginFota:

    def __init__(self):
        pass

    def reconnect(self,driver,verycode):
        driver.maximize_window()
        codetext = driver.find_element_by_id("code")
        codetext.clear()
        codetext.send_keys(verycode)
        loginbutton = driver.find_element_by_id("btn_login")
        print("value2", loginbutton.get_property('value'))  # 可以获取元素的属性值
        loginbutton.click()

    def fota_login_page(self):
        account = readconfig.readconfig("..\\conf\\Fota.ini", "baseconf", "account")
        password = readconfig.readconfig("..\\conf\\Fota.ini", "baseconf", "password")
        it = InterceptPic()
        ft = FindText()
        driver = it.login(account, password)  # 打开Fota网页并输入账号密码，截取验证码的图
        while (True):
            cropimg = it.cropVeryCode(driver)  # 裁剪当前网页中的验证码图片
            procimg = ft.processing_image(cropimg)  # 灰度处理验证码图片
            delspimg = ft.delete_spot(procimg)  # 把灰度处理的图片降噪
            verycode = ft.findtext(delspimg)  # 从验证码图片获取验证码
            time.sleep(1)  # 延迟1s
            self.reconnect(driver, verycode)  # 向网页重新输入验证码，并且点击连接
            try:
                time.sleep(1)
                print("进入try界面")
                element = driver.find_element_by_id("side-menu")
            except:
                print("重新截取并填入验证码\n")
            else:
                print("元素内容:{}".format(element.text))
                SoundAlert.sound_alert().speak("验证码识别成功，登录完成！")
                break
        return driver

if __name__== "__main__":
    lf = LoginFota()
    lf.fota_login_page()