# 导包
from .baseUtils import *
from .res.ui.ui import 功能开关


# 实例方法
def main():
    while True:
        if 功能开关["fighting"] == 0:
            # print('空白弹窗处理线程 - 运行中')
            sleep(3)  # 等待 5 秒
            noticeCancel()
        if 功能开关["fighting"] == 1 and 功能开关["needHome"] == 0:
            # print('空白弹窗处理线程 - 运行中')
            sleep(10)  # 等待 5 秒
            noticeCancel()

        # 如果 commonVar["fighting"] 为 1 ，则不做任何操作


def noticeCancel():
    if 功能开关["fighting"] == 0 or 功能开关["fighting"] == 1:
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

        bitmap = screen.capture(107,759,603,1257)
        res = TomatoOcrFindRangeClick('', 0.9, 0.9, 107,759,603,1257, whiteList='点击空白处', timeLock=5,
                                      offsetX=10, offsetY=10, bitmap=bitmap,
                                      keywords=[{'keyword': '空白', 'match_mode': 'fuzzy'}])
        if res:
            tapSleep(45, 1245)
            Toast('关闭弹窗')

        res = TomatoOcrTap(214, 1071, 274, 1098, "确定", 10, 10)
        if res:
            Toast('战斗结算弹窗确认')

        res = TomatoOcrTap(587,66,631,89, "跳过", 10, 10)
        if res:
            res = TomatoOcrTap(432,598,475,632, "是", 10, 10)
            Toast('跳过教程')

        # res = TomatoOcrFindRange('本轮时长', 0.9, 113, 831, 720, 1280, whiteList='本轮时长', timeLock=3)
        # if res:
        # re = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=130, y1=294, x2=632, y2=1191, timeLock=5,
        #                              bitmap=bitmap, offsetX=10, offsetY=10)
        # if re:
        #     Toast('战斗结算弹窗确认')

        # 退出待机状态
        # reWait, _ = TomatoOcrText(335, 978, 396, 1007, "旅行中")
        # reWait = CompareColors.compare(
        #     "63,1199,#EBEFA5|105,1197,#EBEFA5|180,1186,#EAEFA5|285,1193,#ECF0A6|331,1193,#ECF0A6|393,1182,#EBEEA4")
        # if reWait:
        #     swipe(213, 1104, 568, 1104)
        #     swipe(213, 1104, 568, 1104)
        #     Toast('退出待机状态')

        # if not re:
        #     tapSleep(45, 1245)
        #     Toast('关闭战斗结算弹窗')

        # res, _ = TomatoOcrText(257, 464, 459, 530, "离线奖励")
        # if res:
        #     tapSleep(45, 1245)
        #     Toast('关闭弹窗')

    return
