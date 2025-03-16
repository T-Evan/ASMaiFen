# 导包
import time

from .baseUtils import *
from .res.ui.ui import 功能开关
from ascript.android.screen import FindColors
from ascript.android import screen
from .child_another_login import anotherLogin

checkSkipTime = 0
checkLoginTime = 0


# 实例方法
def main():
    global checkSkipTime
    checkSkipTime = time.time()
    checkLoginTime = time.time()
    while True:
        if 功能开关["fighting"] == 0:
            # print('空白弹窗处理线程 - 运行中')
            sleep(4)  # 等待 5 秒
            noticeCancel()
        if 功能开关["fighting"] == 1 and 功能开关["needHome"] == 0:
            # print('空白弹窗处理线程 - 运行中')
            sleep(5)  # 等待 5 秒
            noticeCancel()
        if 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
            currTime = time.time() - checkLoginTime
            if currTime > 30:
                anotherLogin()
                checkLoginTime = time.time()
        # 如果 commonVar["fighting"] 为 1 ，则不做任何操作


def noticeCancel():
    if 功能开关["fighting"] == 0 or 功能开关["fighting"] == 1:
        # for i in range(1, 2):
        #     res = TomatoOcrFindRangeClick('空白处')

        # screen.cache(True)
        # 自动拒绝，避免影响日常任务进行
        if 功能开关["秘境自动接收邀请"] == 0 and 功能开关['梦魇自动接收邀请'] == 0 and 功能开关[
            '恶龙自动接收邀请'] == 0 and 功能开关['暴走自动接收邀请'] == 0 and 功能开关['终末战自动接收邀请'] == 0 and \
                功能开关['绝境自动接收邀请'] == 0 and 功能开关['调查队自动接收邀请'] == 0:
            # 匹配拒绝提示
            res2 = CompareColors.compare(
                "514,667,#F4E0AC|468,659,#F4E0AC|521,659,#F4E0AC|478,664,#846D4F|480,667,#D4C193|480,670,#DCC899|487,661,#D8C596|487,661,#D8C596|500,669,#DCC899")
            if res2:
                tapSleep(489, 664)  # 点击拒绝
                Toast('日常任务执行中 - 拒绝邀请')

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
        # bitmap = screen.capture(107, 759, 603, 1257)
        res = TomatoOcrFindRangeClick('', 0.9, 0.9, 107, 759, 603, 1257, whiteList='点击空白处', timeLock=5,
                                      offsetX=20, offsetY=40,
                                      keywords=[{'keyword': '空白', 'match_mode': 'fuzzy'}])
        # res = PaddleOcrFindRangeClick('空白', 0.9, 0.9, 107, 759, 603, 1257, timeLock=5,
        #                               offsetX=20, offsetY=40, match_mode='fuzzy')
        # res = CompareColors.compare(
        #     "341,872,#A09BA7|345,872,#A09BA7|339,884,#9E9AA5|344,884,#9E9AA5|359,872,#A49FAB|362,884,#A09BA7")
        # if not res:
        #     res = CompareColors.compare(
        #         "317,1232,#87838F|321,1232,#888490|320,1242,#A19CA8|335,1232,#9D98A4|336,1237,#A09BA7|336,1243,#615D69")
        # if not res:
        #     res = CompareColors.compare(
        #         "342,1122,#97939E|342,1129,#96929D|338,1134,#97929D|345,1134,#97929D|359,1123,#8B8791|361,1135,#6B6770")
        # if not res:
        #     res = CompareColors.compare(
        #         "343,1208,#A09CA7|359,1209,#948F9A|363,1209,#94909A|344,1216,#A6A1AD|360,1214,#96929D|345,1219,#9994A0")
        # if not res:
        #     res = CompareColors.compare(
        #         "314,873,#7C767F|331,873,#9A95A1|314,879,#A49FAC|332,879,#807A84|315,885,#6F6971|331,885,#7C767F")
        if res:
            # tapSleep(35, 1260)
            Toast('关闭弹窗')
        # res = PaddleOcrFindRangeClick('空白', x1=107, y1=759, x2=603, y2=1257, offsetX=20, offsetY=40)
        # if res:
        #     Toast('关闭弹窗')
        # screen.cache(False)

        if 功能开关["优先推图到最新关卡"] == 1:
            res = TomatoOcrTap(428, 1073, 521, 1100, "下一关卡", 10, 10)
            if res:
                Toast('前往下一关')

        res = TomatoOcrTap(214, 1071, 274, 1098, "确定", 10, 10)
        if res:
            Toast('战斗结算弹窗确认')

        global checkSkipTime
        currTime = time.time() - checkSkipTime
        if currTime > 20:
            res = TomatoOcrTap(587, 66, 631, 89, "跳过", 10, 10)
            if res:
                res = TomatoOcrTap(432, 598, 475, 632, "是", 10, 10)
                Toast('跳过教程')
            checkSkipTime = time.time()

        # 跳过对话
        re = CompareColors.compare(
            "671,1253,#F4EEDE|666,1235,#F4EEDE|664,1201,#F4EEDE|685,1197,#F4EEDE|685,1216,#F4EEDE")
        if re:
            for k in range(10):
                tapSleep(652, 1243)
                tmp = CompareColors.compare(
                    "671,1253,#F4EEDE|666,1235,#F4EEDE|664,1201,#F4EEDE|685,1197,#F4EEDE|685,1216,#F4EEDE")
                if not tmp:
                    break
        # res = TomatoOcrFindRange('本轮时长', 0.9, 113, 831, 720, 1280, whiteList='本轮时长', timeLock=10)
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
