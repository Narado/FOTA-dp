# -*- coding: utf-8 -*-
# @Time    :2021/9/27 9:31
# @Author  :Gao Lei
# @FileName:SwithCase.py
# @Software:PyCharm

class switch_case(object):

    def caseToFunction(self,classElement,funcDic,funcId):
        funcname = funcDic.get(funcId)
        print("函数名称:{}".format(funcname))
        method = getattr(classElement,funcname)
        return method