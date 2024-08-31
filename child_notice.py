# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关


# 实例方法
def main():
    while True:
        sleep(15)  # 等待 5 秒
        if 功能开关["fighting"] == 0:
            noticeCancel()

        # 如果 commonVar["fighting"] 为 1 ，则不做任何操作


def noticeCancel():
    for i in range(1, 2):
        res = ocrFindRangeClick('空白处')
        if res:
            tapSleep(45, 1245)
            Toast('关闭弹窗')

        res, _ = TomatoOcrText(257, 464, 459, 530, "离线奖励")
        if res:
            tapSleep(45, 1245)
            Toast('关闭弹窗')

    return
