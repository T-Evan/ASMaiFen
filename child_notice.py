# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关


# 实例方法
def main():
    while True:
        sleep(8)  # 等待 5 秒
        if 功能开关["fighting"] == 0:
            noticeCancel()

        # 如果 commonVar["fighting"] 为 1 ，则不做任何操作


def noticeCancel():
    if 功能开关["fighting"] == 0:
        # for i in range(1, 2):
        #     res = TomatoOcrFindRangeClick('空白处')

        # res = TomatoOcrTap(292, 1191, 429, 1238, "点击空白处关闭")
        # # 领取离线奖励
        # res = TomatoOcrTap(268, 869, 359, 888, "点击空白处", 30, 100)
        # # 领取离线奖励 - 确认
        # res = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 100)
        # res = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 100)
        # res1 = TomatoOcrTap(289, 1067, 430, 1094, "点击空白处关闭")
        # res2 = TomatoOcrTap(279, 1079, 440, 1099, "点击空白处可领取奖励", 30, 20)
        # res3 = TomatoOcrTap(266, 863, 453, 890, "点击空白处可领取奖励", 30, 100)
        # res5 = TomatoOcrTap(268, 869, 359, 888, "点击空白处", 30, 100)
        # res6 = TomatoOcrTap(261, 861, 457, 893, "点击空白区域继续游戏", 30, 100)

        res = TomatoOcrFindRange('点击空白处', 0.9, 113, 831, 720, 1280, whiteList='点击空白处', timeLock=3,
                                 match_mode='fuzzy')
        if res:
            tapSleep(45, 1245)
            Toast('关闭弹窗')

        # res = TomatoOcrFindRange('本轮时长', 0.9, 113, 831, 720, 1280, whiteList='本轮时长', timeLock=3)
        # if res:
        re = TomatoOcrFindRangeClick('确定', whiteList='确定', timeLock=3)
        if re:
            Toast('战斗结算弹窗确认')

        # 退出待机状态
        reWait, _ = TomatoOcrText(335, 978, 396, 1007, "旅行中")
        if reWait:
            swipe(213, 1104, 568, 1104)
            swipe(213, 1104, 568, 1104)
            Toast('退出待机状态')

        # if not re:
        #     tapSleep(45, 1245)
        #     Toast('关闭战斗结算弹窗')

        # res, _ = TomatoOcrText(257, 464, 459, 530, "离线奖励")
        # if res:
        #     tapSleep(45, 1245)
        #     Toast('关闭弹窗')

    return
