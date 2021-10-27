# -*- coding: utf-8 -*-
# @Time    :2021/10/14 14:50
# @Author  :Gao Lei
# @FileName:SoundAlert.py
# @Software:PyCharm
import os
import time
import winsound
import pygame , sys
import pygame.mouse
import pythoncom
import win32com.client
from pygame import mixer
from win32com.client import Dispatch
from lib import MultiThread
from selenium.common.exceptions import WebDriverException






class sound_alert:

    speak_out = win32com.client.Dispatch("SAPI.SPVOICE")

    mt = MultiThread.multi_thread()

    def __init__(self):
        pass

    #在多线程里面使用win32com调用com组件的时候，需要用pythoncom.CoInitialize初始化一下。
    #最后还需要用pythoncom.CoUninitialize释放资源。
    def speak(self,str):
        pythoncom.CoInitialize()
        print(str)
        # self.speak_out.Speak(str)
        try:
            for i in range(3):
                self.speak_out.Speak(str)
                time.sleep(1)
        except Exception as e:
            print(e.message)
        finally:
            # if self.speak_out:
            #     self.speak_out.Quit()

            #释放资源,
            pythoncom.CoUninitialize()
            return 0


        # winsound.PlaySound(str,winsound.SND_ASYNC)

    def beep(self):
        for i in range(3):
            winsound.Beep(200 + 100 * i, 2000)
            time.sleep(1)

    def webAlertPop(self, driver):
        try:
            driver.execute_script("alert('升级包下载失败,请检查充电桩！');")
        except WebDriverException:
            pass
        time.sleep(2)
        driver.switch_to_alert.accept()

    def electronicAlert(self):
        # path1 = os.path
        # print("path1:",path1)
        # path2 = os.path.abspath('.')
        # print("path2:",path2)
        # path3 = os.path.abspath('..')
        # print("path3:",path3)
        # newpath =os.path.join(path3,"dp\\electronic_alert.wav")
        # print("newpath:",newpath)
        pygame.init()   #初始化pygame类
        mixer.init()
        fcclock = pygame.time.Clock()
        fps = 3
        pygame.mouse.set_visible(1)
        # ship = pygame.image.load("")
        pygame.time.delay(1000) #等待1秒让mixer初始化完成
        mixer.music.load('..\\dp\\musics\\electronic_alert2.mp3')
        n= 0
        while n<10:
            fcclock.tick(fps)
            mixer.music.play(1)
            n +=1

    def playCatton(self,catton_path="..\\dp\\images\\升级包安装完成3.PNG"):
        pygame.init()  # 初始化pygame类
        screen = pygame.display.set_mode([500, 600])  # 设置窗口大小
        pygame.display.set_caption("动画测试")  # 设置窗口标题
        image = pygame.image.load(catton_path)  # 加载背景图片
        # tick = pygame.time.Clock()
        frameNumber = 6
        frameRect = image.get_rect()    #获取全图的框体数据，以此计算单帧框体
        print("全图宽度：",frameRect.width)
        frameRect.width //=frameNumber    #整除
        print("每一幅图片宽度：", frameRect.width)
        fps = 10 #设置刷新率，数字越大刷新频率约高，但是因为图片只有6帧所以建议设置低点，否则闪的太快
        fcclock = pygame.time.Clock()
        n = 0
        # for i in range(100):
        while True:
            for event in pygame.event.get():    #事件检测，如果点击右上角的x，则程序退出，如果没有此循环。窗口可能会在打开时闪退
                if event.type == pygame.QUIT:
                    sys.exit()
            if n <frameNumber:
                frameRect.x = frameRect.width * n #这里通过移动单帧框体的x轴坐标实现单帧框体的位移
                # print("start x:", frameRect.x)
                n += 1
            else:
                n = 0
            # self.speak_out.Speak("恭喜您，升级包安装完成！")
            screen.fill([255,255,255])#设置背景为白色
            screen.blit(image,(0,0),frameRect)  #3个实参，分别是图像，绘制的位置，绘制的截面框
            fcclock.tick(fps)
            pygame.display.flip() #刷新窗口









if __name__ == '__main__':
    # sound_alert().speak("Our tower is under attack！")
    # sound_alert().beep()
    # sound_alert().electronicAlert()
    # sound_alert().playCatton()
    speak_content = "Our tower is under attack！"
    pic_path   = "..\\dp\\images\\升级包安装完成3.PNG"

    tasks = { sound_alert().speak: (speak_content,), sound_alert().playCatton:(pic_path,)}
    sound_alert().mt.runthreads_meanwhile(tasks)
    pass