from AutoItLibrary import AutoItLibrary
from FOTA.lib import MouseOperate
from FOTA.lib import ChangeName
from FOTA.conf import readconfig
from FOTA.core import LoginFota
from FOTA.core import ManageFota
from FOTA.lib import SoundAlert
import time

class TaskFota:
    mo = MouseOperate.mouse_operate()
    cn = ChangeName.changeName()
    mf = ManageFota.ManageFota()


    # def __init__(self,task_time_string):
    #     self.task_time_string = task_time_string
    #     pass

    def __init__(self):
        pass

    #在左侧的"管理"列表中选择"升级任务"
    def openTask(self, driver, manageID=3):
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
        packManage_element.click()  # 打开升级任务界面

    # 在升级任务界面添加升级任务
    def openAddPage(self, driver):

        # Iframe中的元素定位出错问题：
        # 现象：如果有iframe存在，可是我们没有做特殊处理，而是通过通用的定位方法，name,id,xpath或者CSS来定位。用Selenium IDE验证能查找到元素，
        # 但是运行测试用例的时候，总是找不到。
        # 原因：在我们运行测试脚本的时候，代码获取的页面的句柄，而iframe在句柄中是当成一个元素来处理的。脚本是没有办法自己去iframe中定位元素的，
        # 所以当搜索完页面时，发现找不到要定位给的元素，就当错误处理。
        # 解决办法：当需要定位iframe中的元素时，先将句柄切换到iframe中 ： driver.switch_to.frame("framename"),具体的iframe_name可以在网页的开发者工具中找到
        driver.switch_to.frame("iframe409")  # 将driver切换到浮动的框架
        plusbutton = driver.find_element_by_xpath(
            '//div[@class="page-container"]//button[contains(text(),"添加")]')  # 找到”添加“标签的位置
        plusbutton.click()  # 点击添加标签，打开添加页面
        return driver



    def addTopfour(self, driver, taskName,pakgName, hwVersion):
        """
        :param driver: 网页驱动
        :param taskName: 任务名称
        :param pakgName: 升级包名称
        :param hwVersion: 硬件版本号
        :return: 返回driver
        """

        # .操作元素对象clear() 清空；send_keys() 键盘操作；click() 点击；
        # submit() 提交；text 获取对象文本；get_attribute 获取对象属性值
        # 任务名称
        taskNm = driver.find_elements_by_xpath("//input[@class='form-control' and @type='text']")[3]  # 获取”任务名称“文本框这个元素
        taskNm.clear()  # 清空”任务名称“文本框内容
        taskNm.send_keys(taskName)  # 往”任务名称“文本框写入内容

        #升级包
        try:
            print("查看升级包是否被点开")
            packId = driver.find_element_by_xpath("//div[@class='select packageId']")
            packId.click() #点击升级包文本框

        except:
            print("已经点开升级包，不需要再点开")
            packId = driver.find_element_by_xpath("//div[@class='select packageId opened']")

        finally:    #遍历所有的升级包标题，看是否有所需要的升级包名称
            pack_elements = driver.find_elements_by_xpath("//div[@class='select packageId opened']//ul//li")
            for pack in pack_elements:
                gettitle = pack.get_attribute('title')
                if pakgName == gettitle:
                    print("已经找到{}".format(pakgName))
                    pack.click()
                    break
                else:
                    print("元素的标题为{}，和要找的{}不同".format(gettitle, pakgName))

        # 硬件版本
        hwversion_element = driver.find_element_by_xpath('//input[@class="form-control" and @name="hardwareVersion"]')  # 获取”硬件版本“文本框元素
        hwversion_element.send_keys(hwVersion)
        time.sleep(0.5)

        # # 软件版本
        # swversion_element = driver.find_element_by_xpath(
        #     '//input[@class="form-control" and @name="softwareVersion"]')  # 获取”软件版本“文本框元素
        # swversion_element.send_keys(swVersion)
        # time.sleep(0.5)
        return driver

    #选择升级类型
    def taskType(self,driver,type,planTime=""):
        """
        :param driver: 网页驱动
        :param type: 升级类型：立即升级，按计划时间升级
        :param planTime: 选择“按计划时间升级”后，需要选择升级时间
        :return:
        """
        if(type == "now"):
            print("选择立即升级")
            type_element = driver.find_elements_by_xpath("//label[@class='radio-parent']")[0]
            type_element.click()
        elif(type == "delay"):
            print("选择按计划时间升级")
            type_element = driver.find_elements_by_xpath("//label[@class='radio-parent']")[1] #选择“按计划时间升级”
            type_element.click()
            plantime_element = driver.find_element_by_xpath("//input[@name='planTime']")
            plantime_element.send_keys(planTime)
        else:
            print("Tasktype error, please input 'now' or 'delay'.")

    #添加备注
    def addRemark(self, driver, taskremarks=""):
        """
        :param driver: 网页驱动
        :param taskremarks:  任务备注内容
        :return:
        """
        remark = driver.find_element_by_xpath('//textarea[@class="form-control" and @name="remarks"]')
        remark.click()
        remark.send_keys(taskremarks)
        return driver

    #选择要升级的充电桩
    def selectUpPile(self, driver, station,piletype, pileidlist):
        """
        :param driver: 网页驱动
        :param station: 站点名称
        :param piletype: 桩型号
        :param pileidlist: 桩编号列表
        :return:
        """
        #源站点
        #1.先搜索需要的站点
        station_element = driver.find_element_by_xpath("//input[@placeholder='所属站点']")
        station_element.click()
        station_list = driver.find_elements_by_xpath("//div[@class='select opened']/ul/li")
        for st in station_list:
            sttitle = st.get_attribute("title")
            if station == sttitle:
                print("找到站点{}".format(station))
                st.click()
                break
            print("在所有站点中未找到{}".format(station))
        time.sleep(0.5)

        #2.搜索需要的桩型号
        piletype_element = driver.find_element_by_xpath("//input[@placeholder='桩型号']")
        piletype_element.click()
        piletype_list = driver.find_elements_by_xpath("//div[@class='select opened']/ul/li")
        for pt in piletype_list:
            pttitle = pt.get_attribute("title")
            if piletype == pttitle:
                print("找到桩型号{}".format(piletype))
                pt.click()
                break
            print("在所有桩型号中未找到{}".format(piletype))
        time.sleep(0.5)

        #3.填写桩编号，并查询
        for pileid in pileidlist:

            pilecode_element = driver.find_element_by_xpath("//input[@name='pileCode' and @placeholder='充电桩编号']")
            pilecode_element.clear()
            pilecode_element.send_keys(pileid)
            time.sleep(0.5)

            #点击查询
            find_element = driver.find_element_by_xpath("//div[@class='modal fade in']//button[contains(text(),'查询')]")
            find_element.click()
            #找到查询的桩内容
            find_content = driver.find_elements_by_xpath("//div[@class='table-parent']//div[@class='mauna-body-container']")[0]
            styleString = find_content.get_attribute("style")
            styledic = self.cn.get_styleattrs(styleString)
            print("styledic:",styledic)
            # if styledic.has_key("height"):
            if "height" in styledic:
                print("style存在属性height")
                value = styledic.get("height")
                print("height value:", value)
                if value != '1px' :
                    print("已经找到可升级充电桩")
                    pilename_list = driver.find_elements_by_xpath("//div[@class='popup-form']//div[@class='mauna-body-viewport-wrapper']//div[@col-id='name']")
                    for pilename in pilename_list:
                        print("桩名称为:",pilename.get_attribute("title"))
                else:
                    print("没有找到可升级充电桩")
            else:
                print("style不存在属性height")
            #全选
            selectall_element = driver.find_elements_by_xpath("//span[@class='mauna-header-select-all']")[0]
            selectall_element.click()

            #添加到升级侧
            upgrade_element = driver.find_element_by_xpath("//button[@class='btn btn-sm btn-primary up-to-right']")
            upgrade_element.click()

        # 在升级列表全选2
        selectall_element2 = driver.find_elements_by_xpath("//span[@class='mauna-header-select-all']")[0]
        self.mo.slideroller(driver, selectall_element2)
        time.sleep(0.25)
        selectall_element2.click()

    # 点击确定或取消
    def confirmOrCancle(self, driver):
        confirm = driver.find_element_by_xpath('//div[@class="modal-footer"]//button[contains(text(),"确定")]')
        cancle = driver.find_element_by_xpath('//div[@class="modal-footer"]//button[contains(text(),"取消")]')
        confirm.click()



    def fota_task_page(self, driver, task_time_string):
        print("fota_manage函数")
        now_time = task_time_string  #获取创建升级包时的时间
        print("获取创建升级包时的时间:",now_time)
        # 从配置文件获取信息

        task_name = readconfig.readconfig("..\\conf\\Fota.ini","taskconf","task_name")+now_time
        package_name = readconfig.readconfig("..\\conf\\Fota.ini", "moduleconf", "package_name")+now_time
        hwversion = readconfig.readconfig("..\\conf\\Fota.ini", "taskconf", "hwversion")
        task_type = readconfig.readconfig("..\\conf\\Fota.ini", "taskconf", "task_type")
        plan_time = readconfig.readconfig("..\\conf\\Fota.ini", "taskconf", "plan_time")
        taskremark_content = readconfig.readconfig("..\\conf\\Fota.ini", "taskconf", "taskremark_content")
        source_station = readconfig.readconfig("..\\conf\\Fota.ini", "sourcelistconf", "source_station")
        source_piletype = readconfig.readconfig("..\\conf\\Fota.ini","sourcelistconf","source_piletype")
        source_pileid_list = readconfig.readconfig("..\\conf\\Fota.ini","sourcelistconf","source_pileid")
        # source_pileid_list_int = self.cn.stringL_to_intL(source_pileid_list)
        source_pileid_list_new = self.cn.stringL_removeFrame(source_pileid_list)

        driver.refresh()
        time.sleep(1)
        self.openTask(driver, 3)  # 打开管理界面的升级任务
        time.sleep(0.5)
        self.openAddPage(driver)  # 打开“添加页面”
        time.sleep(1)
        self.addTopfour(driver,task_name,package_name,hwversion)  # 往”添加“页面的顶部4个元素"任务名称"，”升级包“，”硬件版本“，”软件版本“添加指定内容
        time.sleep(0.25)
        self.taskType(driver,'now')   #选择是否立即升级
        time.sleep(0.25)
        self.addRemark(driver, taskremark_content)  # 添加备注
        time.sleep(0.25)
        self.selectUpPile(driver, source_station,source_piletype, source_pileid_list_new) #按照站点，桩型号，桩名称查询，然后添加到升级列表
        time.sleep(0.25)
        self.confirmOrCancle(driver)  #确定或取消
        time.sleep(1)
        SoundAlert.sound_alert().speak("任务创建完成！")
        return True







if __name__ == '__main__':
    lf = LoginFota.LoginFota()
    tf = TaskFota()
    driver = lf.fota_login_page()
    tf.openTask(driver,3)
    time.sleep(0.5)
    tf.openAddPage(driver)
