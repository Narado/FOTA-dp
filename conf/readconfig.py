# -*- coding: utf-8 -*-
# @Time    :2021/9/26 17:32
# @Author  :Gao Lei
# @FileName:readconfig.py.py
# @Software:PyCharm
import configparser

def readconfig(filepath,section_name,option_name):
    cf = configparser.ConfigParser()
    cf.read(filepath, encoding="utf-8-sig")     #读取配置文件内容,读取的文件含有中文的话，此处是utf-8-sig，而不是utf-8
    value = ""
    secs = cf.sections()    #获取文件中所有的section（章节名）
    print("查找section:{} 和 option:{}".format(section_name,option_name))
    # print('sections:',secs)
    if section_name in secs:
        print("配置中有该section")
        opts = cf.options(section_name)
        # print('options:',opts)
        if option_name in opts:
            print("配置中有该option")
            value = cf.get(section_name,option_name)
            # value = cf.getint(section_name,option_name)
        else:
            print("配置中没有该option！！！")
    else:
        print("配置中没有该section！！！")

    return value

if __name__ == '__main__':
    value = readconfig("..\\conf\\Fota.ini","Poster","poster_version")
    print("value:{}".format(value))