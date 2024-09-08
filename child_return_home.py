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
        if 功能开关["needHome"] == 1 and 功能开关["fighting"] == 0:
            returnHome()
            sleep(1)  # 等待 1 秒
        else:
            sleep(3)  # 等待 5 秒


def returnHome():
    return1 = False
    return2 = False
    return3 = False
    return4 = False
    return1 = TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
    if return1 and 功能开关["needHome"] == 1:
        # 返回上级页面时二次确认入口通用处理
        re = TomatoOcrFindRangeClick('确定', whiteList='确定')
        Toast('返回首页')
    return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
    if return3 and 功能开关["needHome"] == 1:
        re = TomatoOcrFindRangeClick('确定', whiteList='确定')
        Toast('返回首页')

    if not return1 and not return3:
        return2 = imageFindClick('返回_1')
        if return2 and 功能开关["needHome"] == 1:
            Toast('返回首页')

        return4 = imageFindClick('返回_2')
        if return4 and 功能开关["needHome"] == 1:
            Toast('返回首页')

    if not return1 and not return2 and not return3 and not return4:
        # 识别是否进入首页
        res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
        shou_ye1 = False
        shou_ye2 = False
        if not res2:
            shou_ye1, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
            # 暂不处理，提高执行效率
            # if not shou_ye1:
            #     shou_ye2 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
            # shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
        if res2 or shou_ye1 or shou_ye2:
            功能开关["needHome"] = 0
            Toast('已返回首页')
            return True

    return
