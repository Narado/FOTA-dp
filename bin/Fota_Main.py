# -*- coding: utf-8 -*-
# @Time    :2021/9/30 12:27
# @Author  :Gao Lei
# @FileName:Fota_Main.py
# @Software:PyCharm

from FOTA.core import ManageFota
from FOTA.core import LoginFota
from FOTA.core import TaskFota
from FOTA.core import StatusFota
from FOTA.conf import readconfig
from FOTA.lib import SaveLog

if __name__ == '__main__':
        lf = LoginFota.LoginFota()
        mf = ManageFota.ManageFota()
        tf = TaskFota.TaskFota()
        sf = StatusFota.StatusFota()

        sl = SaveLog.save_log()

        driver = lf.fota_login_page()           #登录Fota
        mf.fota_manage_page(driver)             #升级包管理界面 添加升级包、查询升级包状态
        time = mf.get_managefota_time()         #获得制作升级包时的时间
        tf.fota_task_page(driver,time)          #升级任务界面：添加升级任务
        sf.fota_status_page(driver,time)        #升级状态界面
