# 导包
from time import sleep

from ascript.android import system
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import switch_lock
from .baseUtils import *
from threading import Lock

# 实例方法
def main():
    while True:
        if 功能开关["needHome"] == 1:
            returnHome()
            ldE.sleep(1)  # 等待 1 秒
        else:
            ldE.sleep(3)  # 等待 5 秒


def returnHome():
    return1 = False
    return2 = False
    return3 = False
    return4 = False
    return1 = ldE.element_exist('返回-1')
    if return1 and 功能开关["needHome"] == 1:
        return1.click(rx=5, ry=5).execute(sleep=1)
        Toast('返回首页')
    return3 = ldE.element_exist('返回-3')
    if return3 and 功能开关["needHome"] == 1:
        return3.click(rx=5, ry=5).execute(sleep=1)
        Toast('返回首页')

    if not return1 and not return3:
        return2 = ldE.element_exist('返回-2')
        if return2 and 功能开关["needHome"] == 1:
            return2.click(rx=5, ry=5).execute(sleep=1)
            Toast('返回首页')

        return4 = ldE.element_exist('返回-4')
        if return4 and 功能开关["needHome"] == 1:
            return4.click(rx=5, ry=5).execute(sleep=1)
            Toast('返回首页')

    if not return1 and not return2 and not return3 and not return4:
        # 点击冒险
        ldE.element('首页-冒险').click().execute(sleep=1)

        # 识别是否进入首页
        shou_ye1 = ldE.element_exist('首页-冒险手册')
        shou_ye2 = False
        if not shou_ye1:
            shou_ye2 = ldE.element_exist('首页-新手试炼')
        if shou_ye1 or shou_ye2:
            with switch_lock:
                功能开关["needHome"] = 0
            Toast('已返回首页')
            return True

    return
