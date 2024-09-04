# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关


# 实例方法
def main():
    while True:
        sleep(10)  # 等待 5 秒
        if 功能开关["fighting"] == 0:
            noticeCancel()

        # 如果 commonVar["fighting"] 为 1 ，则不做任何操作


def noticeCancel():
    if 功能开关["fighting"] == 0:
        # for i in range(1, 2):
        #     res = ocrFindRangeClick('空白处')

        res = TomatoOcrTap(292, 1191, 429, 1238, "点击空白处关闭")
        # 领取离线奖励
        res = TomatoOcrTap(268, 869, 359, 888, "点击空白处", 30, 100)
        # 领取离线奖励 - 确认
        res = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 100)
        res = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 100)
        res1 = TomatoOcrTap(289, 1067, 430, 1094, "点击空白处关闭")
        res2 = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 20)
        res3 = TomatoOcrTap(266, 863, 453, 890, "点击空白处可领取奖励", 30, 100)
        res5 = TomatoOcrTap(268, 869, 359, 888, "点击空白处", 30, 100)
        res6 = TomatoOcrTap(261, 861, 457, 893, "点击空白区域继续游戏", 30, 100)

        # res = ocrFindRange('点击空白处', 0.9, 113, 831, 720, 1280, whiteList='点击空白处')
        # if res:
        #     tapSleep(45, 1245)
        #     Toast('关闭弹窗')

        res = ocrFindRange('本轮时长', 0.9, 97, 462, 625, 959, whiteList='本轮时长')
        if res:
            re = ocrFindRangeClick('确定')
            if not re:
                tapSleep(45, 1245)
                Toast('关闭战斗结算弹窗')
            Toast('战斗结算弹窗确认')

        # res, _ = TomatoOcrText(257, 464, 459, 530, "离线奖励")
        # if res:
        #     tapSleep(45, 1245)
        #     Toast('关闭弹窗')

    return
