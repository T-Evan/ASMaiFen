# 导包
import time
import sys
import traceback
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 任务记录
from .child_return_home import *
from .baseUtils import *
from .startUp import StartUp
from ascript.android import action
from ascript.android.screen import CompareColors
from .thread import *
from ascript.android.screen import FindColors
import pymysql
import random
import re


class ShiLianTask:
    def __init__(self):
        # 定义环境和关卡名称的配对
        self.stagePoi = {
            "古遗迹上的幽影": [302, 373, 468, 402],
            "旧国之王的野心": [302, 373, 468, 402],
            "三宝齐聚黄金船": [302, 373, 468, 402],
            "海洋征服计划": [302, 373, 468, 402],
            "噩兆降临之谷": [302, 373, 468, 402],
            "永冻禁区矿场": [303, 373, 447, 401],
            "尤弥尔深渊": [303, 567, 423, 596],
            "蒸汽炎池浴场": [303, 373, 447, 401],
            "艾特拉之心": [303, 567, 423, 596],
            "雷电焦土深处": [303, 373, 447, 401],
            "九王角斗场": [303, 567, 423, 596],
            "溪谷大暴走": [302, 373, 469, 401],
            "躁动绿洲之丘": [301, 568, 447, 596],
            "白沙渊下的鼓动": [304, 759, 469, 792],
            "浴火燃墟伐木场": [302, 373, 469, 401],
            "激战构造体工厂": [301, 568, 447, 596],
            "无始无终燃烧塔": [304, 759, 469, 792],
            "魔偶师赌局": [302, 373, 469, 401],
            "下城危险警报": [301, 568, 447, 596],
            "无夜大王驾到": [304, 759, 469, 792],
            "金色歌剧院": [303, 373, 447, 401],
            "决战黄金穹顶": [303, 567, 423, 596],
            "巨像思维首脑": [303, 373, 447, 401],
            "世间万象其中": [303, 567, 423, 596],
            "薄纱笑靥舞": [303, 373, 447, 401],
            "傲慢者赫朗格尼": [303, 567, 423, 596],
            "悲恸骑士游猎场": [303, 373, 447, 401],
            "云涌风雷王座": [303, 567, 423, 596],
            "无法无天章鱼帮": [303, 373, 447, 401],
            "长夜明灯之孤塔": [303, 567, 423, 596],
            "三头盘踞拦路关": [303, 373, 447, 401],
            "上游泥沼的尽头": [303, 567, 423, 596],
            "白网与织女": [303, 373, 447, 401],
            "香腐的行刑台": [303, 567, 423, 596],
            "魇舞聚会厅": [303, 373, 447, 401],
            "黯淡冠冕的宝珠": [303, 567, 423, 596],
        }
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")

    def shilian(self):
        if 功能开关['大暴走开关'] == 1 and 功能开关['暴走自动接收邀请'] == 0:
            for i in range(3):
                self.daBaoZou()
            # 兜个底
            self.homePage()
            self.quitTeam()

        if 功能开关['三魔头开关'] == 1 and 功能开关['三魔头自动接收邀请'] == 0:
            for i in range(3):
                self.sanMoTou()
            # 兜个底
            self.homePage()
            self.quitTeam()

        if 功能开关['桎梏之形开关'] == 1 and 功能开关['桎梏之形自动接收邀请'] == 0:
            self.zhiGuZhiXing()
            # 兜个底
            self.homePage()
            self.quitTeam()

        if 功能开关['冒险总开关'] == 0:
            return

        # 开始试炼
        if 功能开关['秘境开关'] == 1 and 功能开关['秘境自动接收邀请'] == 0:
            # if 功能开关['秘境开关'] == 1:
            if 功能开关['秘境地图'] == "" or 功能开关['秘境关卡'] == "":
                return
            fightTimes = 0
            while 1:
                fightTimes = fightTimes + 1
                self.mijing()
                # 不开宝箱时无需循环
                # 开启宝箱时循环至体力用尽
                if 功能开关["秘境不开宝箱"] == 1 or 任务记录['试炼-秘境-体力消耗完成'] == 1:
                    break
                if fightTimes > 3:
                    break

        if 功能开关['恶龙开关'] == 1 and 功能开关['恶龙自动接收邀请'] == 0:
            for i in range(3):
                self.elong()
            # 兜个底
            self.homePage()
            self.quitTeam()

        if 功能开关['梦魇开关'] == 1 and 功能开关['梦魇自动接收邀请'] == 0:
            for i in range(3):
                self.mengYan()
            # 兜个底
            self.homePage()
            self.quitTeam()

    # 三打三守三魔头
    def sanMoTou(self):
        if 任务记录["三魔头-完成"] == 1:
            return
        Toast('三打三守三魔头 - 开始')
        self.homePage()
        self.quitTeam()
        # res = TomatoOcrFindRangeClick('西行记', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                               sleep1=1.5, match_mode='fuzzy')
        #
        # if not res:
        #     Toast('三打三守三魔头 - 未找到活动入口')
        #     return

        # 开始暴走
        res = False
        for k in range(3):
            res = FindColors.find(
                "585,356,#927A6D|579,362,#E9CD78|578,365,#947D64|582,369,#FBEECE|587,366,#927969|592,370,#917761",
                diff=0.95)
            if res:
                tapSleep(res.x, res.y, 1)
                break
        if not res:
            Toast('三打三守三魔头 - 未找到入口')
            return

        # res = TomatoOcrTap(521, 604, 585, 632, '三魔头', sleep1=1.5)
        # if not res:
        #     Toast('三打三守三魔头 - 未找到活动入口')
        #     return

        Toast('三打三守三魔头 - 任务开始')
        # 领取全服榜奖励
        re = CompareColors.compare("169,241,#EE5C40|171,243,#ED5B3E|172,241,#EF5D3F")
        if re:
            Toast('领取共享战利品')
            tapSleep(145, 215, 0.8)
            for j in range(6):
                re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            swipe(345, 935, 339, 337)
            sleep(2)
            for k in range(6):
                re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            swipe(345, 935, 339, 337)
            sleep(2)
            for k in range(6):
                re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            tapSleep(93, 1213)  # 返回

        # 领取全服心火奖励
        re = FindColors.find("610,517,#F46042|610,513,#F86244|615,516,#F45F42|614,521,#F2503E",
                             rect=[551, 400, 637, 757], diff=0.85)
        if re:
            tapSleep(re.x - 5, re.y + 10)
            tapSleep(353, 1245)  # 点击空白处返回
            tapSleep(353, 1245)

        # 装备法宝
        re = CompareColors.compare(
            "124,656,#F4EDDC|126,683,#EFE2BE|138,684,#EFE2BD|145,683,#B98A55|153,678,#F1E7CB|153,670,#B98A55")
        if re:
            Toast('三魔头任务 - 装备法宝')
            tapSleep(124, 656, 0.8)
            re = TomatoOcrTap(328, 1008, 393, 1038, '装备')
            if re:
                tapSleep(90, 1204)  # 点击空白处返回

        # 升级法宝
        re = CompareColors.compare("180,639,#F15D41|180,637,#F55F42|181,639,#EF5C40")
        if re:
            tapSleep(137, 666)  # 点击法宝
            for k in range(3):
                TomatoOcrTap(330, 1009, 355, 1035, '升')  # 点击升级
                TomatoOcrTap(330, 1009, 355, 1035, '突')  # 点击升级
            tapSleep(353, 1245)  # 点击空白处返回
            tapSleep(353, 1245)

        # 识别目标阶段
        toLevel = safe_int_v2(功能开关['三魔头目标阶段'])
        if toLevel == 0:
            toLevel = 15
        if toLevel > 0:
            re, level = TomatoOcrText(124, 1011, 205, 1041, "阶段")
            level = level.replace("阶", "")
            level = safe_int_v2(level)
            if level >= toLevel:
                Toast("三魔头 - 已达到目标等阶")
                sleep(1.5)
                任务记录["三魔头-完成"] = 1
                return

        self.startFightMoTou()

    # 桎梏之形
    def zhiGuZhiXing(self):
        if 任务记录["桎梏之形-完成"] == 1:
            return
        Toast('桎梏之形 - 开始')
        sleep(2)

        isFind = False
        for p in range(3):
            self.homePage()
            self.quitTeam()
            # 开始桎梏之形
            res = TomatoOcrTap(544, 460, 631, 487, "之形", 30, -10, match_mode='fuzzy')  # 适配新手试炼 - 下方入口
            if not res:
                res = TomatoOcrTap(556, 380, 618, 404, "之形", 30, -10, match_mode='fuzzy')
            if not res:
                res = TomatoOcrFindRangeClick('之形', x1=543, y1=336, x2=634, y2=626, offsetX=30, offsetY=-10)
            if not res:
                res = TomatoOcrFindRangeClick('形', x1=543, y1=336, x2=634, y2=626, offsetX=30, offsetY=-10)
            if res:
                isFind = True
                break
        if not isFind:
            Toast('桎梏之形 - 未找到入口')
            return
        sleep(2)

        # 关闭提示
        return4 = imageFindClick('返回_2', x1=9, y1=1092, x2=172, y2=1261)

        # 结算前一次的宝箱（兜底）
        res = TomatoOcrTap(334, 771, 386, 801, "开启")  # 领取宝箱
        if not res:
            res = TomatoOcrTap(334, 771, 386, 801, "开户")  # 领取宝箱
        if not res:
            res = TomatoOcrFindRangeClick(keywords=[{'keyword': '开启', 'match_mode': 'fuzzy'},
                                                    {'keyword': '开户', 'match_mode': 'fuzzy'}], x1=75,
                                          y1=419, x2=610, y2=887,
                                          match_mode='fuzzy')
        if res:
            Toast("桎梏之形 - 开启前一次宝箱")
            sleep(2)
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白

        # 领取累积奖励
        for k in range(8):
            re = FindColors.find("548,729,#F2A949|553,727,#F2A949|562,727,#F2A949",
                                 rect=[101, 260, 611, 1089])  # 匹配已领取奖励
            if re:
                swipe(543, 724, 430, 726)
                sleep(0.5)

            re = FindColors.find("284,693,#F56042|281,694,#F45F42|287,696,#EF5C40", rect=[97, 669, 628, 784],
                                 diff=0.95)  # 匹配红点
            if re:
                Toast("桎梏之形 - 领取累积奖励")
                tapSleepV2(re.x - 30, re.y + 30)
                tapSleep(125, 1050)  # 领取后，点击空白
                tapSleep(125, 1050)  # 领取后，点击空白

        # 识别目标阶段
        toLevel = safe_int_v2(功能开关['桎梏之形目标阶段'])
        if toLevel == 0:
            toLevel = 80
        if toLevel > 0:
            re, level = TomatoOcrText(132, 972, 191, 995, "阶段")
            import re as rep
            level = int(rep.findall(r'\d+', level)[0]) if rep.findall(r'\d+', level) else None
            level = safe_int_v2(level)
            print(level)
            if level >= toLevel:
                Toast("桎梏之形 - 已达到目标等阶")
                任务记录["桎梏之形-完成"] = 1
                return

        self.startFightZhiGu()

    # 史莱姆大暴走
    def daBaoZou(self):
        if 任务记录["大暴走-完成"] == 1:
            return
        Toast('大暴走 - 开始（建议游戏画质调整为高）')
        sleep(2)
        if 功能开关["暴走进入战斗后启动"] == 1:
            Toast('暴走史莱姆 - 等待进入战斗')
            totalWait = 150 * 1000
            elapsed = 0
            # 等待进入战斗
            while elapsed <= totalWait:
                if elapsed >= totalWait:
                    Toast("进入战斗失败 - 队友未准备")
                    return False

                Toast("请操作进入战斗")
                功能开关["needHome"] = 0
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                fightStatus, x, y = imageFind('战斗-喊话', 0.9, 360, 0, 720, 1280)
                fightStatu2, _ = TomatoOcrText(642, 461, 702, 483, "克风", match_mode='fuzzy')
                if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2 or fightStatus or fightStatu2:
                    Toast("进入战斗成功 - 开始战斗")
                    self.fightingBaoZou()
                    return True
                sleep(5)
                elapsed = elapsed + 5 * 1000
            return False

        self.homePage()
        self.quitTeam()
        # 开始暴走
        res = TomatoOcrTap(556, 380, 618, 404, "大暴走", 30, -10)
        if not res:
            res = TomatoOcrTap(554, 464, 622, 487, "大暴走", 30, -10)  # 适配新手试炼 - 下方大暴走入口
            if not res:
                res = TomatoOcrFindRangeClick('大暴走', x1=543, y1=336, x2=634, y2=626, offsetX=30, offsetY=-10)
                if not res:
                    Toast('大暴走 - 未找到入口')
                    return
        sleep(2)

        # 关闭提示
        return4 = imageFindClick('返回_2', x1=9, y1=1092, x2=172, y2=1261)

        # 结算前一次的宝箱（兜底）
        res = TomatoOcrTap(333, 715, 384, 745, "开启")  # 领取宝箱
        res2 = TomatoOcrTap(333, 715, 384, 745, "开户")  # 领取宝箱
        if not res:
            res = TomatoOcrTap(330, 752, 388, 782, "开启")  # 领取宝箱
            res2 = TomatoOcrTap(330, 752, 388, 782, "开户")  # 领取宝箱
        if res:
            Toast("大暴走 - 开启前一次宝箱")
            sleep(2)
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白

        # 领取全服榜奖励
        re = CompareColors.compare("168,204,#FFFFFF|170,205,#FFFFFF|171,205,#FFFFFF|172,205,#FFFFFF")
        if re:
            Toast('大暴走 - 领取共享战利品')
            tapSleep(145, 215, 0.8)
            for j in range(6):
                re = FindColors.find("584,321,#F25E41|581,323,#F05D40|585,325,#FF5438", rect=[480, 295, 614, 1030],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            swipe(345, 935, 339, 337)
            sleep(2)
            for k in range(6):
                re = FindColors.find("584,321,#F25E41|581,323,#F05D40|585,325,#FF5438", rect=[480, 295, 614, 1030],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            swipe(339, 337, 345, 935)
            sleep(2)
            for k in range(6):
                re = FindColors.find("584,321,#F25E41|581,323,#F05D40|585,325,#FF5438", rect=[480, 295, 614, 1030],
                                     diff=0.9)
                if re:
                    tapSleep(re.x, re.y)
                    tapSleep(427, 217)
                    tapSleep(427, 217)
            tapSleep(93, 1213)  # 返回
        hdPage, 功能开关['史莱姆选择'] = TomatoOcrText(279, 574, 440, 606, "暴走名称")

        # 领取累计奖励
        res = CompareColors.compare("611,732,#F46042|612,737,#F05F42")  # 好运礼盒红点
        if res:
            Toast("大暴走 - 领取好运礼盒")
            tapSleep(611, 732)
            for i in range(4):
                res = TomatoOcrFindRangeClick("领取", sleep1=0.5, whiteList='领取', x1=108, y1=342, x2=603, y2=983)
                if res:
                    tapSleep(350, 1010)  # 点击空白处
                else:
                    break
            res = TomatoOcrTap(71, 1202, 124, 1231, "返回")

        # 识别目标阶段
        toLevel = safe_int_v2(功能开关['暴走目标阶段'])
        if toLevel > 0:
            re, level = TomatoOcrText(121, 1011, 198, 1032, "阶段")
            import re as rep
            level = int(rep.findall(r'\d+', level)[0]) if rep.findall(r'\d+', level) else None
            level = safe_int_v2(level)
            print(level)
            if level >= toLevel:
                Toast("大暴走 - 已达到目标等阶")
                任务记录["大暴走-完成"] = 1
                return

        self.startFightBaoZou()

    def startFightMoTou(self):
        # 直接开始匹配
        res = TomatoOcrTap(304, 1153, 412, 1185, "开始匹配", 40, -40)
        Toast("三魔头 - 开始匹配")

        # 判断职业选择
        if res:
            for i in range(3):
                res, _ = TomatoOcrText(315, 484, 405, 522, "选择职业")
                if res:
                    Toast("三魔头 - 选择职业")
                    if 功能开关["三魔头职能优先输出"] != "" or 功能开关['三魔头职能优先坦克'] != "" or 功能开关[
                        '三魔头职能优先治疗'] != "":
                        if 功能开关["三魔头职能优先输出"] == 1:
                            tapSleep(280, 665, 1)  # 职能输出
                        elif 功能开关['三魔头职能优先坦克'] == 1 or 功能开关['三魔头职能优先治疗'] == 1:
                            tapSleep(435, 665, 1)  # 坦克
                        else:
                            tapSleep(280, 665, 1)  # 职能输出
                    else:
                        if 功能开关["职能优先输出"] == 1:
                            tapSleep(280, 665, 1)  # 职能输出
                        elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                            tapSleep(435, 665, 1)  # 坦克
                        else:
                            tapSleep(280, 665, 1)  # 职能输出
                    res = TomatoOcrTap(332, 754, 387, 789, "确定")
                else:
                    break

        # 判断正在匹配中 - 循环等待300s
        totalWait = 240  # 30000 毫秒 = 30 秒
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(320, 1166, 393, 1190, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            Toast(f"三魔头任务 - 匹配中 - 等待{elapsed}/150s")

            waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
            if 20 < elapsed and not waitStatus3:
                Toast("三魔头任务 - 尝试寻找房间")
                re = TomatoOcrFindRangeClick('更多队伍', x1=453, y1=464, x2=623, y2=1171)
                if re:
                    findTeam = False
                    for k in range(1):
                        re = TomatoOcrFindRangeClick(keywords=[{'keyword': '加入', 'match_mode': 'fuzzy'}], x1=470,
                                                     y1=249,
                                                     x2=601, y2=988, sleep1=1)
                        if not re:
                            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '申请', 'match_mode': 'fuzzy'}], x1=470,
                                                         y1=249,
                                                         x2=601, y2=988, sleep1=5)
                        re1, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                        if re1:
                            findTeam = True
                            # elapsed = 0
                            break
                    if not findTeam:
                        Toast("三魔头任务 - 无可进入房间")
            re2, _ = TomatoOcrText(307, 1019, 407, 1046, '创建队伍')
            if re2:
                TomatoOcrTap(210, 727, 262, 758, "取消")
                TomatoOcrTap(74, 1202, 129, 1229, '返回', sleep1=0.8)  # 点击返回匹配页

            # 判断无合适队伍，重新开始匹配
            res = TomatoOcrTap(304, 1153, 412, 1185, "开始匹配", 40, -40)
            res, _ = TomatoOcrText(230, 625, 306, 648, "匹配超时")
            if res:
                Toast("三魔头 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(455, 729, 512, 758, "确定")

            re = CompareColors.compare(
                "214,285,#FDF6B4|222,284,#FEF6B5|219,277,#FFFEB6|225,285,#FEF5B4|230,280,#FFEEBB")
            if re:
                Toast("三魔头 - 队友全部离队 - 重新匹配")
                break

            waitStatus, _ = TomatoOcrText(320, 1166, 393, 1190, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(325, 1156, 390, 1182, "匹配中")
                if not waitStatus:
                    res, waitTime = TomatoOcrText(334, 1184, 383, 1201, "等待时间")
                    if waitTime != "":
                        waitStatus = True

            res1 = self.WaitFight("三魔头")

            shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
            if shou_ye1:
                Toast("三魔头 - 已取消匹配")
                break

            if res1 == True or (waitStatus == False):  # 成功准备战斗 或 未匹配到
                # 超时取消匹配
                res = TomatoOcrTap(320, 1166, 393, 1190, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

    # 桎梏之形
    def startFightZhiGu(self):
        # 直接开始匹配
        res = TomatoOcrTap(311, 1134, 407, 1160, "开始匹配", 40, -40)
        Toast("桎梏之形 - 开始匹配")

        # 判断职业选择
        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
        if res:
            Toast("桎梏之形 - 选择职业")
            if 功能开关["桎梏之形职能优先输出"] != "" or 功能开关['桎梏之形职能优先坦克'] != "" or 功能开关[
                '桎梏之形职能优先治疗'] != "":
                if 功能开关["桎梏之形职能优先输出"] == 1:
                    tapSleep(280, 665)  # 职能输出
                elif 功能开关['桎梏之形职能优先坦克'] == 1 or 功能开关['桎梏之形职能优先治疗'] == 1:
                    tapSleep(435, 665)  # 坦克
                else:
                    tapSleep(280, 665)  # 职能输出
            else:
                if 功能开关["职能优先输出"] == 1:
                    tapSleep(280, 665, 1)  # 职能输出
                elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                    tapSleep(435, 665, 1)  # 坦克
                else:
                    tapSleep(280, 665, 1)  # 职能输出
            res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(326, 1144, 393, 1169, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            Toast(f"桎梏之形任务 - 匹配中 - 等待{elapsed}/150s")
            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(230, 625, 306, 648, "匹配超时")
            if res:
                Toast("桎梏之形 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(455, 729, 512, 758, "确定")
                # if res:
                # elapsed = 0

            waitStatus, _ = TomatoOcrText(326, 1144, 393, 1169, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(325, 1156, 390, 1182, "匹配中")
                if not res:
                    waitStatus, _ = TomatoOcrText(321, 1151, 393, 1185, "匹配中")
                # if waitStatus == False:
                #     res, waitTime = TomatoOcrText(334, 1184, 383, 1201, "等待时间")
                #     if waitTime != "":
                #         waitStatus = True

            res1 = self.WaitFight("桎梏之形")
            if res1 == True or (waitStatus == False):  # 成功准备战斗 或 未匹配到
                # 超时取消匹配
                res = TomatoOcrTap(326, 1144, 393, 1169, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            sleep(5)
            elapsed = elapsed + 5

    def startFightBaoZou(self):
        # 直接开始匹配
        res = TomatoOcrTap(311, 1156, 407, 1182, "开始匹配", 40, -40)
        Toast("大暴走 - 开始匹配")

        # 判断职业选择
        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
        if res:
            Toast("大暴走 - 选择职业")
            if 功能开关["暴走职能优先输出"] != "" or 功能开关['暴走职能优先坦克'] != "" or 功能开关[
                '暴走职能优先治疗'] != "":
                if 功能开关["暴走职能优先输出"] == 1:
                    tapSleep(280, 665)  # 职能输出
                elif 功能开关['暴走职能优先坦克'] == 1 or 功能开关['暴走职能优先治疗'] == 1:
                    tapSleep(435, 665)  # 坦克
                else:
                    tapSleep(280, 665)  # 职能输出
            else:
                if 功能开关["职能优先输出"] == 1:
                    tapSleep(280, 665, 1)  # 职能输出
                elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                    tapSleep(435, 665, 1)  # 坦克
                else:
                    tapSleep(280, 665, 1)  # 职能输出
            res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(311, 1156, 407, 1182, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            Toast(f"大暴走任务 - 匹配中 - 等待{elapsed}/150s")
            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(230, 625, 306, 648, "匹配超时")
            if res:
                Toast("大暴走 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(455, 729, 512, 758, "确定")
                # if res:
                # elapsed = 0

            waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
            if 20 < elapsed and not waitStatus3:
                Toast("大暴走 - 尝试寻找房间")
                re = TomatoOcrFindRangeClick('更多队伍', x1=453, y1=464, x2=623, y2=1171)
                if re:
                    findTeam = False
                    for k in range(1):
                        re = TomatoOcrFindRangeClick(keywords=[{'keyword': '加入', 'match_mode': 'fuzzy'}], x1=470,
                                                     y1=249,
                                                     x2=601, y2=988, sleep1=1)
                        if not re:
                            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '申请', 'match_mode': 'fuzzy'}], x1=470,
                                                         y1=249,
                                                         x2=601, y2=988, sleep1=5)
                        re1, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                        if re1:
                            findTeam = True
                            # elapsed = 0
                            break
                    if not findTeam:
                        Toast("大暴走 - 无可进入房间")
            re2, _ = TomatoOcrText(307, 1019, 407, 1046, '创建队伍')
            if re2:
                TomatoOcrTap(210, 727, 262, 758, "取消")
                TomatoOcrTap(74, 1202, 129, 1229, '返回', sleep1=0.8)  # 点击返回匹配页

            re = CompareColors.compare(
                "214,285,#FDF6B4|222,284,#FEF6B5|219,277,#FFFEB6|225,285,#FEF5B4|230,280,#FFEEBB")
            if re:
                Toast("大暴走 - 队友全部离队 - 重新匹配")
                break

            waitStatus, _ = TomatoOcrText(311, 1156, 407, 1182, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(325, 1156, 390, 1182, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(321, 1151, 393, 1185, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')

            # if waitStatus == False:
            #     res, waitTime = TomatoOcrText(334, 1184, 383, 1201, "等待时间")
            #     if waitTime != "":
            #         waitStatus = True

            res1 = self.WaitFight("暴走")
            if res1 == True or (waitStatus == False):  # 成功准备战斗 或 未匹配到
                # 超时取消匹配
                res = TomatoOcrTap(311, 1156, 407, 1182, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

    # 梦魇狂潮
    def mengYan(self):
        Toast('梦魇任务 - 开始')
        self.homePage()
        self.quitTeam()
        res = TomatoOcrTap(645, 505, 691, 527, "试炼", sleep1=0.8)
        if not res:
            res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
        if res:
            re = imageFindClick('梦魇狂潮', sleep1=2.5, x1=101, y1=140, x2=618, y2=1087)
            if not re:
                Toast("梦魇任务 - 未找到梦魇入口 - 重新尝试")
                return
        else:
            Toast("梦魇任务 - 未找到试炼入口 - 重新尝试")
            return

        # 领取狂潮补给

        # 判断是否添加佣兵
        if 功能开关["梦魇添加佣兵"] == 1:
            Toast("梦魇任务 - 添加佣兵")
            re = imageFindClick('秘境-创建队伍', confidence1=0.85)
            if re:
                tapSleep(554, 827)  # 点击 创建队伍 - 添加佣兵
                TomatoOcrFindRangeClick("创建队伍", 0.9, 0.9, 60, 511, 652, 1153)
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                return self.fighting()

        # 开始匹配
        re4, level = TomatoOcrText(311, 591, 355, 612, "无尽层数")
        if level == "":
            re4, level = TomatoOcrText(312, 879, 368, 899, "无尽层数")
        wujinLevel = safe_int_v2(level)
        if wujinLevel > 60:
            Toast("梦魇任务 - 无尽模式>72层 - 完成挑战")
            sleep(1)
            return

        # re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
        re1 = FindColors.find(
            "306,1089,#6584B9|327,1090,#6E8ABC|341,1102,#FBFBFC|356,1094,#9FAECE|372,1092,#6785B9|402,1094,#DCE0EB|411,1093,#6584B9",
            rect=[80, 157, 644, 1155], diff=0.9)  # 开始匹配按钮
        if re1:
            tapSleep(re1.x, re1.y)
            for i in range(3):
                res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
                if res:
                    Toast("梦魇任务 - 选择职业")
                    if 功能开关["职能优先输出"] == 1:
                        tapSleep(280, 665)  # 职能输出
                    elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                        tapSleep(435, 665)  # 坦克
                    else:
                        tapSleep(280, 665)  # 职能输出
                    res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=1)
                else:
                    break

        # 判断正在匹配中 - 循环等待300s
        totalWait = 240  # 30000 毫秒 = 30 秒
        elapsed = 0
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                Toast("梦魇任务 - 匹配超时")
                teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中', x1=85, y1=288, x2=647, y2=1120)
                if not teamStatus1:
                    teamStatus1 = imageFindClick('队伍-匹配中', x1=85, y1=288, x2=647, y2=1120)
                if teamStatus1:
                    Toast('梦魇任务 - 匹配超时 - 取消匹配')
                break

            # allQuit, _ = TomatoOcrText(325, 558, 393, 585, "等待加入")
            # if allQuit:
            #     Toast("梦魇任务 - 队友全部离队")
            #     teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中', x1=85, y1=288, x2=647, y2=1120)
            #     if not teamStatus1:
            #         teamStatus1 = imageFindClick('队伍-匹配中', x1=85, y1=288, x2=647, y2=1120)
            #     if teamStatus1:
            #         Toast('梦魇任务 - 队友全部离队 - 取消匹配')
            #     break

            # 判断无合适队伍，重新开始匹配
            # res, _ = TomatoOcrText(229, 621, 305, 646, "匹配超时")
            # if res:
            res = TomatoOcrTap(210, 727, 262, 758, "取消")
            if res:
                Toast("梦魇任务 - 匹配超时")

            waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
            if 20 < elapsed and not waitStatus3:
                Toast("梦魇任务 - 尝试寻找房间")
                re = TomatoOcrFindRangeClick('更多队伍', x1=453, y1=464, x2=623, y2=1171)
                if re:
                    findTeam = False
                    for k in range(1):
                        re = TomatoOcrFindRangeClick(keywords=[{'keyword': '加入', 'match_mode': 'fuzzy'}], x1=470,
                                                     y1=249,
                                                     x2=601, y2=988, sleep1=1)
                        if not re:
                            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '申请', 'match_mode': 'fuzzy'}], x1=470,
                                                         y1=249,
                                                         x2=601, y2=988, sleep1=5)
                        re1, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                        if re1:
                            findTeam = True
                            # elapsed = 0
                            break
                    if not findTeam:
                        Toast("梦魇任务 - 无可进入房间")
            re2, _ = TomatoOcrText(307, 1019, 407, 1046, '创建队伍')
            if re2:
                TomatoOcrTap(210, 727, 262, 758, "取消")
                TomatoOcrTap(74, 1202, 129, 1229, '返回', sleep1=0.8)  # 点击返回匹配页

            re = CompareColors.compare(
                "214,285,#FDF6B4|222,284,#FEF6B5|219,277,#FFFEB6|225,285,#FEF5B4|230,280,#FFEEBB")
            if re:
                Toast("梦魇 - 队友全部离队 - 重新匹配")
                break

            # re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
            re1 = FindColors.find(
                "306,1089,#6584B9|327,1090,#6E8ABC|341,1102,#FBFBFC|356,1094,#9FAECE|372,1092,#6785B9|402,1094,#DCE0EB|411,1093,#6584B9",
                rect=[80, 157, 644, 1155], diff=0.9)  # 开始匹配按钮
            if re1:
                tapSleep(re1.x, re1.y)
                for i in range(3):
                    res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
                    if res:
                        Toast("梦魇任务 - 选择职业")
                        if 功能开关["职能优先输出"] == 1:
                            tapSleep(280, 665)  # 职能输出
                        elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                            tapSleep(435, 665)  # 坦克
                        else:
                            tapSleep(280, 665)  # 职能输出
                        res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=1)
                    else:
                        break

            waitStatus1 = False
            waitStatus2 = False
            waitStatus3 = False
            for p in range(3):
                waitStatus1 = FindColors.find(
                    "314,809,#F3A84B|312,819,#F3A84B|415,812,#F3A84A|402,822,#F3A84B|412,817,#F3A84B|416,817,#F3AD53",
                    rect=[85, 288, 647, 1120], diff=0.95)
                if not waitStatus1:
                    waitStatus1, _, _ = TomatoOcrFindRange('匹配中', x1=91, y1=113, x2=641, y2=1112)
                    waitStatus2, x, y = imageFind('队伍-匹配中', x1=91, y1=113, x2=641, y2=1112)
                    waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                if waitStatus1 or waitStatus2 or waitStatus3:
                    break
                sleep(0.5)
            res1 = self.WaitFight('梦魇挑战')
            if res1 == True or (not waitStatus1 and not waitStatus2 and not waitStatus3):  # 成功准备战斗 或 未匹配到 或 未进入房间
                break
            Toast(f"匹配中,已等待{round(elapsed / 60, 2)}/{totalWait / 60}分")
            sleep(0.5)

    # 恶龙大通缉
    def elong(self):
        if 任务记录['恶龙任务'] == 1:
            return

        Toast('恶龙任务 - 开始')
        self.homePage()
        self.quitTeam()
        res = TomatoOcrTap(645, 505, 691, 527, "试炼", sleep1=0.8)
        if not res:
            res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
        if res:
            re = imageFindClick('恶龙大通缉', x1=101, y1=140, x2=618, y2=1087, confidence1=0.7)
            if not re:
                Toast("恶龙任务 - 未找到恶龙入口 - 重新尝试")
                return self.elong()

        # 关闭提示
        return4 = imageFindClick('返回_2', x1=9, y1=1092, x2=172, y2=1261)

        # 判断是否重复挑战（已开启过宝箱）
        re = FindColors.find(
            "200,667,#256ADE|197,678,#D6B573|187,670,#FEE5A8|203,673,#FEF6BE|203,694,#FBE4A0|211,694,#C28434",
            rect=[121, 621, 270, 714], diff=0.95)
        if re:
            Toast("恶龙任务 - 领取宝箱")
            tapSleep(re.x, re.y)
            tapSleep(600, 929, 1)
            tapSleep(600, 929, 1)
            tapSleep(600, 929, 1)

        re1 = FindColors.find("173,871,#5F4319|168,882,#F0CE8B|162,892,#E3AB42|171,889,#77C3FF|178,887,#B7823C",
                              rect=[122, 821, 247, 911], diff=0.95)
        if not re1:
            re1 = CompareColors.compare(
                "165,875,#5F4319|168,882,#F0CE8B|162,891,#C78830|168,888,#FFE5A5|178,890,#DE9736|172,861,#FCEABB|172,893,#74DAFE")
        if not re1:
            re1 = FindColors.find(
                "210,667,#EAD098|191,672,#5F4319|199,675,#5F4319|189,692,#D59938|192,696,#E0A93E|199,696,#2E8CF4|202,695,#1155DD",
                rect=[126, 647, 252, 713], diff=0.95)
        if not re1:
            re1 = CompareColors.compare(
                "164,858,#EB9D50|167,860,#E9AB7B|178,860,#E36B3B|161,887,#DB6839|183,890,#D87C3D|172,893,#6CDCFC")
            # re1, x, y = imageFind('恶龙-宝箱金币', x1=129, y1=841, x2=213, y2=912)
        # re1 = TomatoOcrFindRange('最高', match_mode='fuzzy')
        if re1:
            if 功能开关["恶龙重复挑战"] == 0:
                Toast("恶龙任务 - 已领取宝箱 - 退出挑战")
                任务记录['恶龙任务'] = 1
                tapSleep(326, 1216)  # 点击返回，返回首页
                tapSleep(326, 1216)
                sleep(1)
                return

        # 判断是否添加佣兵
        if 功能开关["恶龙添加佣兵"] == 1:
            Toast("恶龙任务 - 添加佣兵")
            re = imageFindClick('秘境-创建队伍', confidence1=0.8)
            if re:
                tapSleep(558, 830)  # 点击 创建队伍 - 添加佣兵
                res = TomatoOcrTap(311, 915, 407, 950, "创建队伍", 10, 10, sleep1=1.5)  # 创建队伍 - 创建队伍
                res = TomatoOcrTap(326, 969, 390, 1000, "开始", 10, 10, sleep1=1.5)
                if not res:
                    res = TomatoOcrFindRangeClick("开始", x1=232, y1=885, x2=484, y2=1123, offsetX=10, offsetY=10,
                                                  sleep1=1.5)
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
                return self.fighting()

        # 开始匹配
        # re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
        re1 = FindColors.find(
            "306,1089,#6584B9|327,1090,#6E8ABC|341,1102,#FBFBFC|356,1094,#9FAECE|372,1092,#6785B9|402,1094,#DCE0EB|411,1093,#6584B9",
            rect=[80, 157, 644, 1155], diff=0.9)  # 开始匹配按钮
        if re1:
            tapSleep(re1.x, re1.y)
            for i in range(3):
                res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
                if res:
                    Toast("恶龙任务 - 选择职业")
                    if 功能开关["恶龙职能优先输出"] == 1:
                        tapSleep(280, 665)  # 职能输出
                    elif 功能开关["恶龙职能优先坦克"] == 1 or 功能开关["恶龙职能优先治疗"] == 1:
                        tapSleep(435, 665)  # 坦克
                    elif 功能开关["职能优先输出"] == 1:
                        tapSleep(280, 665)  # 职能输出
                    elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                        tapSleep(435, 665)  # 坦克
                    else:
                        tapSleep(280, 665)  # 职能输出
                    res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=1)
                    break
                else:
                    sleep(0.2)

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                Toast("恶龙任务 - 匹配超时")
                res = TomatoOcrTap(210, 727, 262, 758, "取消")
                teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中', x1=85, y1=288, x2=647, y2=1120)
                if not teamStatus1:
                    teamStatus1 = imageFindClick('队伍-匹配中', x1=85, y1=288, x2=647, y2=1120)
                if teamStatus1:
                    Toast('恶龙任务 - 匹配超时 - 取消匹配')
                break

            allQuit, _ = TomatoOcrText(325, 558, 393, 585, "等待加入")
            if not allQuit:
                allQuit = CompareColors.compare(
                    "186,405,#F2C173|189,405,#F2C173|192,405,#FFF5B4|194,405,#F4C376|192,399,#FCF1B3")  # 判断是否成为房主
                if not allQuit:
                    allQuit = CompareColors.compare("192,406,#FFF6B5|192,403,#FFF4B3|192,400,#FFFFB6")
            if allQuit:
                Toast("恶龙任务 - 队友全部离队")
                teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中', x1=85, y1=288, x2=647, y2=1120)
                if not teamStatus1:
                    teamStatus1 = imageFindClick('队伍-匹配中', x1=85, y1=288, x2=647, y2=1120)
                if teamStatus1:
                    Toast('恶龙任务 - 队友全部离队 - 取消匹配')
                break

            if 功能开关["恶龙匹配中寻找房间"] == 1:
                waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                if 20 < elapsed and not waitStatus3:
                    Toast("恶龙任务 - 尝试寻找房间")
                    re = TomatoOcrFindRangeClick('更多队伍', x1=453, y1=464, x2=623, y2=1171)
                    if re:
                        findTeam = False
                        for k in range(1):
                            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '加入', 'match_mode': 'fuzzy'}], x1=300,
                                                         y1=366,
                                                         x2=421, y2=797, sleep1=1)
                            if not re:
                                re = TomatoOcrFindRangeClick(keywords=[{'keyword': '申请', 'match_mode': 'fuzzy'}],
                                                             x1=300,
                                                             y1=366,
                                                             x2=421, y2=797, sleep1=5)
                            re1, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                            if re1:
                                findTeam = True
                                break
                        if not findTeam:
                            Toast("恶龙任务 - 无可进入房间")
                re2, _ = TomatoOcrText(307, 1019, 407, 1046, '创建队伍')
                if re2:
                    TomatoOcrTap(210, 727, 262, 758, "取消")
                    TomatoOcrTap(74, 1202, 129, 1229, '返回', sleep1=0.8)  # 点击返回匹配页

            # 判断无合适队伍，重新开始匹配
            # res, _ = TomatoOcrText(229, 621, 305, 646, "匹配超时")
            # if res:
            res = TomatoOcrTap(210, 727, 262, 758, "取消")
            if res:
                Toast("恶龙任务 - 匹配超时 - 无队伍")
                # elapsed = 0

            # 开始匹配
            # re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
            re1 = FindColors.find(
                "306,1089,#6584B9|327,1090,#6E8ABC|341,1102,#FBFBFC|356,1094,#9FAECE|372,1092,#6785B9|402,1094,#DCE0EB|411,1093,#6584B9",
                rect=[80, 157, 644, 1155], diff=0.9)  # 开始匹配按钮
            if re1:
                tapSleep(re1.x, re1.y)
                for i in range(3):
                    res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
                    if res:
                        Toast("恶龙任务 - 选择职业")
                        if 功能开关["恶龙职能优先输出"] == 1:
                            tapSleep(280, 665)  # 职能输出
                        elif 功能开关["恶龙职能优先坦克"] == 1 or 功能开关["恶龙职能优先治疗"] == 1:
                            tapSleep(435, 665)  # 坦克
                        elif 功能开关["职能优先输出"] == 1:
                            tapSleep(280, 665)  # 职能输出
                        elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                            tapSleep(435, 665)  # 坦克
                        else:
                            tapSleep(280, 665)  # 职能输出
                        res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=1)
                        break
                    else:
                        sleep(0.2)

            waitStatus1 = False
            waitStatus2 = False
            waitStatus3 = False
            for p in range(3):
                waitStatus1 = FindColors.find(
                    "314,809,#F3A84B|312,819,#F3A84B|415,812,#F3A84A|402,822,#F3A84B|412,817,#F3A84B|416,817,#F3AD53",
                    rect=[85, 288, 647, 1120], diff=0.95)
                if not waitStatus1:
                    waitStatus1, _, _ = TomatoOcrFindRange('匹配中', x1=91, y1=113, x2=641, y2=1112)
                    waitStatus2, x, y = imageFind('队伍-匹配中', x1=91, y1=113, x2=641, y2=1112)
                    waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                if waitStatus1 or waitStatus2 or waitStatus3:
                    break
                sleep(0.5)
            res1 = self.WaitFight()
            if res1:
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
            if res1 == True or (not waitStatus1 and not waitStatus2 and not waitStatus3):  # 成功准备战斗 或 未匹配到
                break
            Toast(f"匹配中,已等待{round(elapsed / 60, 2)}/{totalWait / 60}分")
            sleep(0.5)

    def mijing(self):
        if 任务记录['试炼-秘境-体力消耗完成'] == 1 and 功能开关["秘境无体力继续"] == 0:
            return

        Toast('秘境任务 - 开始')

        selectMap = 功能开关['秘境地图']
        selectStage = 功能开关['秘境关卡']

        isFind = False
        for k in range(3):
            self.homePage()
            self.quitTeam()
            res = TomatoOcrTap(645, 505, 691, 527, "试炼", sleep1=0.8)
            if not res:
                res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
            if res:
                # 限时活动，寻找周年小妖
                re = CompareColors.compare("415,536,#FBF4EA|432,539,#FBF4EA|418,566,#FAF5EB")  # 判断小兵对话框
                if re:
                    tapSleep(366, 615)
                    for k in range(10):
                        tapSleep(309, 1261)
                        res = TomatoOcrTap(131, 1204, 156, 1230, '回')
                        if res:
                            break

                re = imageFindClick('秘境之间', x1=85, y1=53, x2=636, y2=700)
                if re:
                    isFind = True
                    break
                if not re:
                    re = TomatoOcrFindRangeClick('秘境之间', x1=374, y1=101, x2=562, y2=156)
                if not re:
                    Toast("秘境任务 - 未找到秘境入口 - 重新尝试")
                    res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）
                    res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            else:
                Toast("秘境任务 - 未找到试炼入口 - 重新尝试")
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）
                res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")

        if not isFind:
            return

        self.openTreasure(noNeedOpen=1)

        # # 限时活动，寻找西行小妖
        # re = CompareColors.compare("296,1186,#B7AC9F|301,1194,#F6F2E9|306,1196,#F6F2E9|318,1182,#CBC3B7")  # 判断小兵对话框
        # if re:
        #     for k in range(10):
        #         tapSleep(214, 1201)
        #         res = TomatoOcrTap(131, 1204, 156, 1230, '回')
        #         if res:
        #             break

        # 判断是否已在当前地图
        if selectMap != '最新地图':
            res, mapText = TomatoOcrText(329, 223, 388, 253, selectMap)
            if not res:
                res, _, _ = TomatoOcrFindRange(selectMap, x1=80, y1=214, x2=637, y2=599)
            if not res:
                res = self.changeMap(selectMap, selectStage)
                if not res:
                    return
        else:
            Toast('默认挑战最新关卡')

        # 识别当前关卡
        tiliPoint = FindColors.find(
            "577,363,#F4DB77|577,358,#F3D76B|585,364,#888A93|585,356,#888992|592,356,#D9DADC|601,364,#F3F3F4",
            rect=[72, 205, 655, 1120], diff=0.9)
        if tiliPoint:
            x1 = tiliPoint.x - 280
            y1 = tiliPoint.y - 25
            x2 = x1 + 175
            y2 = y1 + 30
            res, 任务记录['玩家-当前关卡'] = TomatoOcrText(x1, y1, x2, y2, "当前关卡")

        if selectMap != '最新地图' and 任务记录['玩家-当前关卡'] != selectStage:
            # res = TomatoOcrFindRangeClick(selectStage, x1=93, y1=99, x2=626, y2=1133)
            res = TomatoOcrFindRangeClick(keywords=[{'keyword': selectStage, 'match_mode': 'fuzzy'},
                                                    {'keyword': selectStage[:2], 'match_mode': 'fuzzy'},
                                                    {'keyword': selectStage[-2:], 'match_mode': 'fuzzy'}], x1=93, y1=99,
                                          x2=626, y2=1133)

        self.startFight()

    # 开始匹配
    def startFight(self):
        # 识别剩余体力不足40时，尝试补充
        res2, availableTiLi = TomatoOcrText(599, 81, 632, 101, "剩余体力")  # 20/60
        availableTiLi = safe_int(availableTiLi)
        if 功能开关["秘境不开宝箱"] == 0 and (availableTiLi == "" or availableTiLi < 40):  # 识别剩余体力不足40时，尝试补充
            self.tili()

        # 判断体力不足，退出挑战
        res2, availableTiLi = TomatoOcrText(599, 81, 632, 101, "剩余体力")  # 20/60
        availableTiLi = safe_int(availableTiLi)
        if availableTiLi == "" or availableTiLi < 20:  # 识别剩余体力不足20时
            # 体力消耗完成
            任务记录["试炼-秘境-体力消耗完成"] = 1
            if 功能开关["秘境无体力继续"] == 0:
                Toast("秘境任务 - 体力不足 - 退出挑战")
                sleep(1)
                tapSleep(75, 1210)  # 点击返回，返回首页
                tapSleep(75, 1210)
                return

        # 判断是否添加佣兵
        if 功能开关["秘境添加佣兵"] == 1:
            Toast("秘境任务 - 添加佣兵")
            re = imageFindClick('秘境-创建队伍', confidence1=0.85)
            if re:
                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                        self.tili()

                tapSleep(554, 827)  # 点击 创建队伍 - 添加佣兵
                res = TomatoOcrTap(311, 915, 410, 948, "创建队伍", 5, 5)  # 创建队伍 - 创建队伍
                sleep(1)
                res = TomatoOcrTap(333, 974, 383, 1006, "开始", 5, 5)
                if not res:
                    Toast("秘境任务 - 添加佣兵 - 创建房间失败")
                    return
                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                        self.tili()
                self.fighting()
                Toast("秘境任务 - 添加佣兵 - 战斗结束")
                return

        # 判断是否创建房间
        if 功能开关["秘境创建房间"] == 1:
            Toast("秘境任务 - 创建房间")
            re1 = imageFindClick('秘境-创建队伍', confidence1=0.85)
            re2 = False
            if not re1:
                re2 = TomatoOcrFindRangeClick('创建队伍', whiteList='创建队伍', offsetX=10, offsetY=10, sleep1=0.8)
            if re1 or re2:
                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                        self.tili()

                res = TomatoOcrTap(309, 915, 408, 948, "创建队伍")  # 创建队伍 - 创建队伍
                # 等待队员（120s超时）
                totalWait = 120  # 30000 毫秒 = 30 秒
                elapsed = 0
                aleadyFightCt = 0
                needFightCt = safe_int(功能开关["秘境建房重复挑战次数"])
                if needFightCt == '':
                    needFightCt = 1  # 默认挑战1次

                failTeamStatus = 0
                start_time = int(time.time())
                while 1:
                    功能开关["fighting"] = 0
                    self.openTreasure(noNeedOpen=1)
                    # 返回房间
                    res1 = TomatoOcrTap(611, 610, 688, 636, "组队", match_mode='fuzzy')
                    if not res1:
                        res2 = TomatoOcrTap(551, 595, 597, 617, "秘境")
                        if not res2:
                            res3 = TomatoOcrTap(620, 625, 682, 650, "匹配中")
                    # 返回房间 - 队伍满员，开始挑战提醒
                    # wait1, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
                    # wait2, _ = TomatoOcrText(240, 610, 344, 653, "队伍已满员")  # 队伍已满员，准备开启挑战
                    # if wait1 or wait2:
                    #     Toast("秘境任务 - 队伍已满员，返回队伍")
                    #     res = TomatoOcrTap(453, 727, 511, 760, "确定", 10, 10)  # 队伍已满员，准备开启挑战 - 确定
                    res = TomatoOcrTap(453, 727, 506, 759, "确定", 10, 10)  # 队伍已满员，准备开启挑战 - 确定

                    # 判断是否在队伍页面
                    res, _ = TomatoOcrText(502, 192, 581, 215, "离开队伍")
                    if not res:
                        res, _, _ = TomatoOcrFindRange('点击空白处', 0.9, 113, 831, 720, 1280, whiteList='点击空白处')
                        if res:
                            tapSleep(45, 1245)
                            Toast('关闭弹窗')
                        res1 = TomatoOcrTap(651, 559, 682, 577, "组队", sleep1=1)
                        res, _ = TomatoOcrText(502, 192, 581, 215, "离开队伍")
                        if not res:
                            sleep(2)
                            failTeamStatus = failTeamStatus + 1
                            if failTeamStatus > 3:
                                Toast("秘境任务 - 已离开队伍 - 结束")
                                break
                    else:
                        failTeamStatus = 0

                    current_time = int(time.time())
                    elapsed = current_time - start_time
                    if aleadyFightCt >= needFightCt or elapsed > totalWait:
                        if aleadyFightCt >= needFightCt:
                            Toast(f"秘境任务 - 挑战次数{aleadyFightCt}/{needFightCt}达成 - 结束")
                        if elapsed > totalWait:
                            Toast("秘境任务 - 等待队友2min超时 - 结束")
                        res = TomatoOcrTap(502, 192, 581, 215, "离开队伍")  # 点击离开队伍
                        res = TomatoOcrTap(330, 728, 385, 759, "确定")  # 确定离开队伍
                        self.quitTeamFighting()
                        break
                    Toast(f"秘境任务 - 创建房间 - 等待队友{elapsed}/{totalWait}s")
                    # 识别队友及关卡名称
                    if 任务记录['战斗-房主名称'] == '':
                        res, 任务记录['战斗-房主名称'] = TomatoOcrText(153, 827, 260, 850, "队友名称")
                        res, 任务记录['战斗-关卡名称'] = TomatoOcrText(352, 284, 601, 318, "关卡名称")
                        任务记录['带队次数'], last_time = self.daiDuiCount()
                    # 检查是否队友全为佣兵
                    if elapsed < 20:
                        # 等待队友结算完成
                        self.quitAi()

                    res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                    TomatoOcrTap(322, 970, 393, 995, "匹配中")  # 避免错误点击匹配，取消匹配中状态
                    if not res and elapsed >= 20:
                        # 判断是否已存在队友
                        re = CompareColors.compare("191,756,#B7D8F9|203,756,#B6D5F6|211,759,#B5D5F6|198,770,#8CA8D4")
                        if not re:
                            # 添加佣兵，避免等不到4个人
                            Toast('等待超过20s，添加佣兵')
                            tapSleep(511, 754)
                            re = TomatoOcrTap(450, 326, 487, 345, '佣兵')
                            if re:
                                tapSleep(528, 424)
                                tapSleep(521, 546)
                                tapSleep(522, 664)
                                tapSleep(524, 781)
                                tapSleep(200, 1070)
                        res = TomatoOcrTap(333, 974, 383, 1006, "开始")

                    if res:
                        Toast(f"秘境任务 - 重复挑战第{aleadyFightCt + 1}/{needFightCt}次")
                        # 满员开始，退出循环
                        # 判断体力用尽提示
                        res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                        if res1:
                            if 功能开关["秘境无体力继续"]:
                                Toast("秘境任务 - 体力不足继续挑战")
                                res = TomatoOcrTap(334, 743, 385, 771, "确定")
                            else:
                                Toast("秘境任务 - 体力不足")
                                res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                                self.tili()

                        # 等待进入战斗
                        for i in range(15):
                            wait1, _ = TomatoOcrText(309, 976, 408, 1006, '开始匹配')
                            wait2 = TomatoOcrTap(322, 970, 393, 995, "匹配中")  # 避免错误点击匹配，取消匹配中状态
                            if wait1 or wait2:
                                Toast('队友离开，重新等待')
                                break
                            waitTime = 3 * i
                            Toast(f"秘境任务 - 匹配成功 - 等待进入战斗 - {waitTime}/45s")
                            sleep(3)

                            if i == 14:
                                Toast(f"秘境任务 - 匹配成功 - 等待进入战斗失败 - 重新等待队友")
                                sleep(1)

                            # 返回房间
                            res1 = TomatoOcrTap(611, 610, 688, 636, "组队", match_mode='fuzzy')
                            if not res1:
                                res2 = TomatoOcrTap(551, 595, 597, 617, "秘境")
                                if not res2:
                                    res3 = TomatoOcrTap(620, 625, 682, 650, "匹配中")

                            # 返回房间 - 队伍满员，开始挑战提醒
                            wait1, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
                            wait2, _ = TomatoOcrText(240, 610, 344, 653, "队伍已满员")  # 队伍已满员，准备开启挑战
                            if wait1 or wait2:
                                Toast("秘境任务 - 队伍已满员，返回队伍")
                                res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
                                res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

                            # 上面点击开始后队友退出，再次点击开始时增加超时等待；避免实际进入战斗前判断为不在战斗状态
                            res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                            if res:
                                sleep(10)
                            TomatoOcrFindRangeClick('跳过', sleep1=1, confidence1=0.9, x1=522, y1=17, x2=685, y2=110,
                                                    offsetX=10, offsetY=10)
                            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                            # fightStatus, x, y = imageFind('战斗-喊话', 0.9, 360, 0, 720, 1280)
                            # fightStatu2, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
                            # if "等级" in teamName1 or  "等级" in teamName2 or fightStatus or fightStatu2:
                            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                                Toast("秘境任务 - 匹配成功 - 进入战斗")
                                self.fighting()
                                sleep(2)
                                self.quitAi()
                                aleadyFightCt = aleadyFightCt + 1
                                功能开关["fighting"] = 0
                                start_time = int(time.time())  # 初始化等待队员时间
                                fightDone = 1
                                任务记录['AI发言-上一次发言'] = []
                                任务记录['AI发言-检测队友关注'] = 0
                                任务记录['战斗-房主名称'] = ""
                                break
                    # 等待队员
                    sleep(2)
            return

        # resStart1 = TomatoOcrTap(311, 697, 405, 725, "开始匹配", sleep1=0.8)  # 图1
        # resStart2 = False
        # resStart3 = False
        # resStart4 = False
        # if not resStart1:
        #     resStart2 = TomatoOcrTap(309, 892, 407, 918, "开始匹配", sleep1=0.8)  # 图2
        #     if not resStart2:
        #         resStart3 = TomatoOcrTap(311, 1084, 405, 1116, "开始匹配", sleep1=0.8)  # 图3
        #         if not resStart3:
        #             resStart4 = TomatoOcrFindRangeClick("开始匹配", x1=83, y1=260, x2=650, y2=1137)
        # if not resStart1 and not resStart2 and not resStart3 and not resStart4:
        #     return
        re1 = FindColors.find("309,898,#6584B9|311,912,#6584B9|350,902,#F7F8FA|371,907,#6584B9|413,915,#6584B9",
                              rect=[64, 198, 674, 1177], diff=0.9)  # 开始匹配按钮
        if not re1:
            Toast("秘境任务 - 开始匹配失败")
            return

        tapSleep(re1.x, re1.y, 1)
        Toast("秘境任务 - 开始匹配", 500)
        # 判断体力用尽提示
        res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
        if res1:
            if 功能开关["秘境无体力继续"]:
                Toast("秘境任务 - 体力不足继续挑战")
                res = TomatoOcrTap(334, 743, 385, 771, "确定")
            else:
                Toast("秘境任务 - 体力不足")
                res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                self.tili()

        # 判断职业选择
        for i in range(3):
            res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
            if res:
                Toast("秘境任务 - 选择职业")
                if 功能开关["职能优先输出"] == 1:
                    tapSleep(280, 665)  # 职能输出
                elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                    tapSleep(435, 665)  # 坦克
                else:
                    tapSleep(280, 665)  # 职能输出
                res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=0.8)
                break
            else:
                sleep(0.2)

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        start_time = int(time.time())
        waitFailTimes = 0
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrFindRangeClick("匹配中", x1=83, y1=260, x2=650, y2=1137, offsetX=10, offsetY=10)
                if not res:
                    res = TomatoOcrTap(320, 692, 392, 716, "匹配中", offsetX=10, offsetY=10)  # 图1
                    if not res:
                        res = TomatoOcrTap(323, 886, 394, 910, "匹配中", offsetX=10, offsetY=10)  # 图2
                        if not res:
                            res4 = TomatoOcrTap(324, 1080, 392, 1103, "匹配中", offsetX=10, offsetY=10)  # 图3
                            if not res4:
                                TomatoOcrFindRangeClick("匹配中", x1=83, y1=260, x2=650, y2=1137, offsetX=10,
                                                        offsetY=10)
                break
            Toast(f"秘境任务 - 匹配中 - {elapsed}/150s")

            if 功能开关["秘境匹配中寻找房间"] == 1:
                waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                if 20 < elapsed and not waitStatus3:
                    Toast("秘境任务 - 尝试寻找房间")
                    re = TomatoOcrFindRangeClick('更多队伍', x1=453, y1=464, x2=623, y2=1171)
                    if re:
                        findTeam = False
                        for k in range(1):
                            re1 = TomatoOcrFindRangeClick(keywords=[{'keyword': '加入', 'match_mode': 'fuzzy'}], x1=470,
                                                          y1=249,
                                                          x2=601, y2=988, sleep1=1)
                            re2 = False
                            if not re1:
                                re2 = TomatoOcrFindRangeClick(keywords=[{'keyword': '申请', 'match_mode': 'fuzzy'}],
                                                              x1=470,
                                                              y1=249,
                                                              x2=601, y2=988, sleep1=1)
                            # 判断体力用尽提示
                            res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                            if res1:
                                if 功能开关["秘境无体力继续"]:
                                    Toast("秘境任务 - 体力不足继续挑战")
                                    res = TomatoOcrTap(334, 743, 385, 771, "确定")
                                else:
                                    Toast("秘境任务 - 体力不足")
                                    res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                                    self.tili()
                            if re2:
                                sleep(4)  # 申请后等待4秒
                            re1, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
                            if re1:
                                findTeam = True
                                elapsed = 0
                                break
                        if not findTeam:
                            Toast("秘境任务 - 无可进入房间")
                for k in range(2):
                    re2, _ = TomatoOcrText(307, 1019, 407, 1046, '创建队伍')
                    if re2:
                        TomatoOcrTap(210, 727, 262, 758, "取消")
                        TomatoOcrTap(74, 1202, 129, 1229, '返回', sleep1=0.8)  # 点击返回匹配页

            # 判断无合适队伍，重新开始匹配
            # res, _ = TomatoOcrText(303, 607, 418, 632, "暂无合适队伍")
            # if res:
            res = TomatoOcrTap(210, 727, 262, 758, "取消")
            if res:
                Toast("秘境任务 - 匹配超时 - 无合适队伍")

            re = CompareColors.compare(
                "214,285,#FDF6B4|222,284,#FEF6B5|219,277,#FFFEB6|225,285,#FEF5B4|230,280,#FFEEBB")
            if re:
                Toast("秘境 - 队友全部离队 - 重新匹配")
                break

            # 重新开始匹配
            re1 = FindColors.find("309,898,#6584B9|311,912,#6584B9|350,902,#F7F8FA|371,907,#6584B9|413,915,#6584B9",
                                  rect=[64, 198, 674, 1177], diff=0.9)  # 开始匹配按钮
            if re1:
                tapSleep(re1.x, re1.y, 1)
                Toast("秘境任务 - 开始匹配", 500)
                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
                        self.tili()

                    # 判断职业选择
                    for i in range(3):
                        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
                        if res:
                            Toast("秘境任务 - 选择职业")
                            if 功能开关["职能优先输出"] == 1:
                                tapSleep(280, 665)  # 职能输出
                            elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                                tapSleep(435, 665)  # 坦克
                            else:
                                tapSleep(280, 665)  # 职能输出
                            res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=0.8)
                            break
                        else:
                            sleep(0.2)

            res2 = FindColors.find(
                "314,809,#F3A84B|312,819,#F3A84B|415,812,#F3A84A|402,822,#F3A84B|412,817,#F3A84B|416,817,#F3AD53",
                rect=[85, 288, 647, 1120], diff=0.95)  # 匹配中
            waitStatus3 = False
            if not res2:
                res2, _ = TomatoOcrText(320, 692, 392, 716, "匹配中")  # 图1
            res3 = False
            if not res2:
                res3, _ = TomatoOcrText(323, 886, 394, 910, "匹配中")  # 图2
            if not res3:
                res3, _ = TomatoOcrText(324, 1080, 392, 1103, "匹配中")  # 图3
            if not res3:
                waitStatus3, _ = TomatoOcrText(502, 190, 581, 211, '离开队伍')
            if not res3:
                res3, _, _ = TomatoOcrFindRange("匹配中", x1=83, y1=260, x2=650, y2=1137)

            res1 = self.WaitFight()
            # if res1 == True or (res2 == False and res3 == False and not waitStatus3):  # 成功准备战斗 或 未匹配到
            if res2 == False and res3 == False and not waitStatus3:  # 成功准备战斗 或 未匹配到
                waitFailTimes = waitFailTimes + 1
                tapSleep(571, 86)  # 点击体力图标，点击空白处避免结算弹窗影响
                Toast(f'秘境 - 匹配失败{waitFailTimes}/3')
                if waitFailTimes > 3:
                    break
            if res1:
                Toast('战斗结束')
                start_time = int(time.time())
            sleep(1)

    # 踢出佣兵
    def quitAi(self):
        for i in range(5):
            wait1, _ = TomatoOcrText(179, 809, 224, 826, '结算中')
            wait2, _ = TomatoOcrText(336, 810, 382, 825, '结算中')
            wait3, _ = TomatoOcrText(495, 809, 539, 825, '结算中')
            if not wait1 and not wait2 and not wait3:
                break
            Toast('等待队友结算完成')
            sleep(2)

        resJ, _ = TomatoOcrText(189, 811, 216, 827, '镜像')  # 第一位队友为镜像
        if resJ:
            Toast('等待不足20s，踢出佣兵')
            tapSleep(194, 803)
            tapSleep(194, 803)
            tapSleep(200, 1070)

        resJ, _ = TomatoOcrText(346, 811, 376, 825, '镜像')  # 第二位队友为镜像
        if resJ:
            Toast('等待不足20s，踢出佣兵')
            tapSleep(353, 800)
            tapSleep(353, 800)
            tapSleep(200, 1070)

        resJ, _ = TomatoOcrText(503, 810, 532, 825, '镜像')  # 第三位队友为镜像
        if resJ:
            Toast('等待不足20s，踢出佣兵')
            tapSleep(513, 806)
            tapSleep(513, 806)
            tapSleep(200, 1070)

    def tili(self):
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0
        功能开关["noHomeMust"] = 1
        if 功能开关["补充体力次数"] == "" or 功能开关["补充体力次数"] == 0:
            return
        Toast("体力购买 - 开始")
        for k in range(3):
            tapSleep(690 + k, 90 + k, 0.8)  # 点击补充体力加号
            re, _ = TomatoOcrText(317, 344, 401, 370, '补充体力')
            if re:
                break
        for i in range(1, 3):
            res, count = TomatoOcrText(500, 817, 515, 834, "0")
            buyCount = count.replace("/", "")
            buyCount = safe_int(buyCount)
            needCount = safe_int(功能开关["补充体力次数"])
            if buyCount != "" and buyCount < needCount:
                res = TomatoOcrTap(456, 873, 499, 898, "购买")
                Toast("体力购买 - 成功")
            else:
                break

        if 功能开关["秘境使用体力果实"] == 1:
            re = TomatoOcrTap(220, 874, 263, 895, '使用', offsetX=20, offsetY=20)
            re = TomatoOcrTap(220, 874, 263, 895, '使用', offsetX=20, offsetY=20)
            if re:
                Toast("体力购买 - 使用体力果实")

        Toast("体力购买 - 结束")
        tapSleep(61, 1187)  # 返回
        功能开关["fighting"] = 0
        功能开关["noHomeMust"] = 0

    # 切换地图
    def changeMap(self, selectMap, selectStage):
        Toast("秘境任务 - 切换地图")
        tapSleep(74, 160, 1.5)  # 点击地图列表
        res = CompareColors.compare("254,650,#BBBBBB|251,643,#BDBDBD|246,637,#BDBDBC|254,632,#BFBFBE|255,628,#BDBDBD")
        if not res:
            tapSleep(74, 160, 2)  # 点击地图列表
        # mapPoi = self.mapPoi[selectMap]
        maps_to_check = ('原野', '森林', '沙漠', '海湾', '深林', '冰原', '火山', '高原', '绿洲')
        for k in range(4):
            if selectMap not in maps_to_check:
                swipe(150, 1000, 150, 600)
                sleep(2)
            else:
                # 判断是否已在第一屏
                res, _ = TomatoOcrText(110, 235, 175, 267, "原野")
                if res:
                    sleep(0.1)
                else:
                    # 向上滚动第一屏
                    swipe(150, 300, 150, 700)
                    sleep(2)
            res = TomatoOcrFindRangeClick(selectMap, 1, 0.8, 12, 160, 282, 1171)
            if not res:
                res = TomatoOcrFindRangeClick(selectMap, 1, 0.8, 118, 230, 178, 1133)

            # stagePoi = self.stagePoi[selectStage]
            # res = TomatoOcrTap(stagePoi[0], stagePoi[1], stagePoi[2], stagePoi[3], selectStage)
            res = TomatoOcrFindRangeClick(keywords=[{'keyword': selectStage, 'match_mode': 'fuzzy'},
                                                    {'keyword': selectStage[:2], 'match_mode': 'fuzzy'},
                                                    {'keyword': selectStage[-2:], 'match_mode': 'fuzzy'}], x1=80,
                                          y1=209,
                                          x2=634, y2=871, match_mode='fuzzy')
            if not res:
                res = TomatoOcrTap(303, 342, 468, 371, selectStage)  # 兼容默认识别第一图
            if not res:
                res = TomatoOcrTap(304, 375, 468, 403, selectStage)  # 兼容默认识别第一图
            if not res:
                res = TomatoOcrTap(302, 535, 470, 568, selectStage)  # 兼容默认识别第二图
            if not res:
                res = TomatoOcrTap(287, 559, 501, 600, selectStage)  # 兼容默认识别第二图
            if not res:
                res = TomatoOcrTap(303, 731, 469, 759, selectStage)  # 兼容默认识别第三图

            # 判断是否切换成功
            res, _, _ = TomatoOcrFindRange(keywords=[{'keyword': selectStage, 'match_mode': 'fuzzy'},
                                                     {'keyword': selectStage[:2], 'match_mode': 'fuzzy'},
                                                     {'keyword': selectStage[-2:], 'match_mode': 'fuzzy'}], x1=80,
                                           y1=209,
                                           x2=634, y2=871, match_mode='fuzzy')
            if res:
                return True
        Toast(f'切换地图失败')
        return False

    # 开启宝箱
    def openTreasure(self, noNeedOpen=0):
        isTreasure = 0  # 是否在宝箱页
        if noNeedOpen == 0:
            noNeedOpen = 功能开关['秘境不开宝箱']

        res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱", match_mode='fuzzy')  # 避免前置错误点击弹出宝箱尚未开启
        if res:
            res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

        res1 = False
        res2 = False
        res3 = False
        tmp2 = False
        tmp3 = False
        tmp4 = False
        bitmap = screen.capture(x=108, y=462, x1=618, y1=1120)
        # 房间页 - 宝箱UI
        res1 = FindColors.find(
            "174,1019,#F3A84B|207,1039,#F4D96F|225,1037,#C27717|281,1020,#F3A84B|301,1035,#F3A84B|298,1012,#F3A84B",
            rect=[77, 83, 641, 1160], diff=0.95)
        if not res1:
            res1 = FindColors.find(
                "297,1031,#A6A1AD|294,1060,#A6A1AD|339,1058,#F2D569|409,1037,#A6A1AD|433,1036,#A6A1AD|425,1057,#A6A1AD",
                rect=[77, 83, 641, 1160], diff=0.96)
            # res1, tmp1 = TomatoOcrText(514, 607, 592, 634, "战斗", match_mode='fuzzy')  # 战斗结束页。宝箱提示
            # if not res1:
            #     res1, tmp2 = TomatoOcrText(510, 547, 592, 572, "一键", match_mode='fuzzy')  # 战斗结束页。宝箱提示
            #     if not res1:
            #         res1, tmp2 = TomatoOcrText(511, 458, 595, 484, "一键", match_mode='fuzzy')  # 战斗结束页。宝箱提示
            #     if not res1:
            #         res1, tmp3 = TomatoOcrText(311, 449, 356, 486, "宝箱")  # 房间页。宝箱提示
        # if not res1:
        #     # 先快速图色匹配一次宝箱图标
        #     res1 = TomatoOcrFindRange("", x1=108, y1=462, x2=618, y2=1120,
        #                               bitmap=bitmap, keywords=[{'keyword': '通关奖励', 'match_mode': 'fuzzy'},
        #                                                        {'keyword': '开启', 'match_mode': 'exact'},
        #                                                        {'keyword': '体力不足', 'match_mode': 'fuzzy'},
        #                                                        {'keyword': '战斗统计',
        #                                                         'match_mode': 'fuzzy'}])  # 战斗结束页。宝箱提示
        # if not res1:
        # res2, _ = TomatoOcrText(267, 755, 313, 783, "开启")  # 战斗结束页。宝箱提示
        # res2 = TomatoOcrFindRange("开启", x1=108, y1=462, x2=618, y2=1120, match_mode='fuzzy',
        #                           bitmap=bitmap)  # 战斗结束页。宝箱提示
        # if not res2:
        # res3, _ = TomatoOcrText(273, 397, 360, 425, "是否开启")  # 结算页，宝箱提示
        # res3 = TomatoOcrFindRange("是否开启", x1=108, y1=462, x2=618, y2=1120)  # 结算页，宝箱提示
        if res1 or res2 or res3:
            isTreasure = 1
            # 加锁兜底
            功能开关["fighting"] = 1
            功能开关["needHome"] = 0
            # 功能开关["noHomeMust"] = 1

        if noNeedOpen == 1:
            # res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
            # res7, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
            # if res6 or res7:
            #     Toast('已返回房间')
            #     return 1

            openStatus = 0
            if isTreasure == 1:
                if 功能开关['秘境点赞队友'] == 1:
                    Toast('点赞队友')
                    res = TomatoOcrTap(516, 549, 592, 572, "一", 5, 5, match_mode='fuzzy')  # 一键点赞
                    if not res:
                        res = TomatoOcrTap(511, 458, 595, 484, "一", 5, 5, match_mode='fuzzy')  # 一键点赞
                        if not res:
                            res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                          match_mode='fuzzy')  # 一键点赞
                    # if not res:
                    #     for i in range(2):
                    #         imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                    #         imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                Toast('不开宝箱-返回房间')
                # 加锁兜底
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                # 功能开关["noHomeMust"] = 1
                tapSleep(645, 1235, 0.8)  # 战斗结束页确认不领取
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                    if not res:
                        tapSleep(645, 1235, 1)  # 战斗结束页确认不领取
                        res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    Toast('返回房间-2')
                    res = TomatoOcrTap(96, 1199, 130, 1232, "回", 10, 10, 0.8)  # 返回
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                    if not res:
                        Toast('返回房间-3')
                        res = TomatoOcrFindRangeClick("确定", whiteList='确定', x1=88, y1=277, x2=644,
                                                      y2=986)  # 战斗结束页确认退出
                        # res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                    if res:
                        openStatus = 1
                else:
                    openStatus = 1
                功能开关["fighting"] = 0
                # 功能开关["noHomeMust"] = 0
            return openStatus

        # 点赞队友
        if 功能开关['秘境点赞队友'] == 1:
            if isTreasure == 1:
                Toast('点赞队友')
                res = TomatoOcrTap(516, 549, 592, 572, "一键", 5, 5, match_mode='fuzzy')  # 一键点赞
                if not res:
                    res = TomatoOcrTap(511, 458, 595, 484, "一键", 5, 5, match_mode='fuzzy')  # 一键点赞
                    if not res:
                        res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                      match_mode='fuzzy')  # 一键点赞
                # if not res:
                #     for i in range(1, 4):
                #         imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                #         imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)

        attempts = 0  # 初始化尝试次数
        maxAttempts = 4  # 设置最大尝试次数

        openStatus = 0
        if isTreasure == 1:
            re = FindColors.find(
                "292,1065,#A6A1AD|306,1068,#A6A1AD|314,1065,#A6A1AD|306,1079,#A6A1AD|314,1077,#A6A1AD|290,1093,#A6A1AD",
                rect=[101, 623, 618, 1087], diff=0.93)
            if not re:
                re, _ = TomatoOcrText(453, 1006, 528, 1029, '体力不足')
            if re:
                Toast('体力不足 - 跳过宝箱')
                tapSleep(645, 1235, 0.8)  # 战斗结束页确认不领取
                res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                    if not res:
                        tapSleep(645, 1235, 1)  # 战斗结束页确认不领取
                        res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                if not res:
                    Toast('返回房间-2')
                    res = TomatoOcrTap(96, 1199, 130, 1232, "回", 10, 10, 0.8)  # 返回
                    res = TomatoOcrTap(333, 732, 386, 757, "确定", 10, 0)  # 确定
                    if not res:
                        Toast('返回房间-3')
                        res = TomatoOcrFindRangeClick("确定", whiteList='确定', x1=88, y1=277, x2=644,
                                                      y2=986)  # 战斗结束页确认退出
                        # res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                if res:
                    openStatus = 1
            else:
                Toast('准备开启宝箱')
                while attempts < maxAttempts:
                    res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱尚未开启")  # 避免前置错误点击弹出宝箱尚未开启
                    if res:
                        res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

                    attempts = attempts + 1
                    # 先快速图色匹配一次宝箱图标
                    # res1 = FindColors.find(
                    #     "314,809,#F3A84B|312,819,#F3A84B|415,812,#F3A84A|402,822,#F3A84B|412,817,#F3A84B|416,817,#F3AD53",
                    #     rect=[85, 288, 647, 1120], diff=0.95)
                    # if res1:
                    # 图色识别兜底
                    res = imageFindClick('宝箱-开启')
                    if res:
                        Toast('开启宝箱')
                        sleep(2.5)
                        tapSleep(340, 930)
                        openStatus = 1
                        continue
                    tmp = FindColors.find(
                        "292,1065,#A6A1AD|306,1068,#A6A1AD|314,1065,#A6A1AD|306,1079,#A6A1AD|314,1077,#A6A1AD|290,1093,#A6A1AD",
                        rect=[101, 623, 618, 1087], diff=0.93)
                    if tmp:
                        Toast('体力不足 - 跳过宝箱')
                        break
                    res = imageFindClick('宝箱-开启2')
                    if res:
                        Toast('开启宝箱')
                        sleep(2.5)
                        tapSleep(340, 930)
                        openStatus = 1

        if openStatus == 1:
            Toast('开启宝箱 - 成功')

        # 开启宝箱后，返回
        if openStatus == 1 or isTreasure == 1:
            Toast("已开启宝箱 - 返回房间")
            res = TomatoOcrTap(96, 1199, 130, 1232, "回", sleep1=0.8)  # 返回
            if not res:
                tapSleep(320, 1220, 1.5)  # 点击空白处返回
            res = TomatoOcrTap(330, 726, 387, 759, "确定")  # 确定返回
            if not res:
                res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
            if not res:
                # 识别战斗结束页提前返回
                res1 = False
                res1, _, _ = TomatoOcrFindRange("通关奖励", x1=112, y1=456, x2=620, y2=1032)  # 战斗结束页。宝箱提示
                if res1:
                    tapSleep(645, 1235, 3)  # 战斗结束页确认不领取
                    # res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 战斗结束页确认退出
                    res = TomatoOcrFindRangeClick("确定", whiteList='确定')  # 战斗结束页确认退出
                    if not res:
                        res = TomatoOcrTap(96, 1199, 130, 1232, "回")  # 返回
                        res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 确定
                        if not res:
                            res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                            openStatus = 1
        功能开关["fighting"] = 0
        # 功能开关["noHomeMust"] = 0
        return openStatus

    # 等待匹配
    def WaitFight(self, fightType='秘境'):
        res1 = TomatoOcrTap(457, 607, 502, 631, "准备")  # 秘境准备
        res2 = False
        res3 = False
        res4 = False
        if not res1:
            res2 = TomatoOcrTap(453, 650, 505, 684, "准备")  # 恶龙准备
        # if not res1 and not res2:
        #     res4 = TomatoOcrFindRangeClick('准备', x1=94, y1=276, x2=633, y2=1089)  # 全屏识别准备按钮

        # 队伍满员，开始挑战
        res, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        if res:
            res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
            res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

        if res1 or res2 or res3 or res4:
            Toast("匹配成功-等待进入战斗")
            totalWait = 15
            elapsed = 0
            # 等待进入战斗
            while elapsed <= totalWait:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if elapsed >= totalWait:
                    功能开关["fighting"] = 0
                    Toast("进入战斗失败-队友未准备")
                    return False

                TomatoOcrFindRangeClick('跳过', sleep1=1, confidence1=0.9, x1=522, y1=17, x2=685, y2=110, offsetX=10,
                                        offsetY=10)
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                # res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                Toast(f"等待进入战斗 {elapsed}/{totalWait}")
                if "等级" in teamName1 or "Lv" in teamName1:
                    Toast("进入战斗成功 - 开始战斗")
                    if fightType == "秘境" or fightType == "秘境带队":
                        self.fighting(fightType)
                    elif fightType == "暴走":
                        self.fightingBaoZou()
                    elif fightType == "三魔头":
                        self.fightingSanMoTou()
                    elif fightType == "斗歌会":
                        self.fightingDouGeHui()
                    elif fightType == "使徒来袭":
                        self.fightingShiTuLaiXi()
                    elif fightType == "使徒来袭带队":
                        self.fightingShiTuLaiXiTeam()
                    elif fightType == "斗歌会带队":
                        self.fightingDouGeHuiTeam()
                    elif fightType == "三魔头带队":
                        self.fightingSanMoTouTeam()
                    elif fightType == "梦魇带队" or fightType == "梦魇挑战":
                        self.fightingMengYanTeam(fightType)
                    elif fightType == "恶龙带队" or fightType == "恶龙挑战":
                        self.fightingELongTeam(fightType)
                    elif fightType == "桎梏之形" or fightType == "桎梏之形带队" or fightType == "桎梏之形挑战":
                        self.fightingZhiGuTeam(fightType)
                    elif fightType == "绝境带队":
                        self.fightingJueJingTeam()
                    elif fightType == "终末战带队":
                        self.fightingZhongMoTeam()
                    elif fightType == "调查队带队":
                        self.fightingDiaoChaTeam()
                    elif fightType == "暴走带队":
                        self.fightingBaoZouTeam()
                    else:
                        self.fighting()
                    return True
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                res4 = TomatoOcrFindRangeClick('准备', x1=94, y1=276, x2=633, y2=1089)  # 避免点击开始瞬间队友离队，错误点击了开始匹配，兜底准备按钮
                res = TomatoOcrTap(332, 754, 387, 789, "确定")
                # 判断当前在行李页，跳转为冒险页
                tmp = CompareColors.compare(
                    "230,1202,#FCF8EE|240,1205,#FCF8EE|258,1207,#F8ECCD|271,1205,#FDF5E6|257,1223,#FAEFD5|273,1231,#FCF8EE")
                if tmp:
                    tapSleep(355, 1202)
                # shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                # if shou_ye1:
                #     break
                sleep(1)
                elapsed = elapsed + 1
        return False

    #  切换宠物
    def changeChongWu(self, fight_type):
        if 功能开关["自动切换主战宠物"] == 0:
            return
        宠物名称 = ''
        if fight_type == '恶龙挑战' or fight_type == '恶龙带队':
            if 功能开关["恶龙宠物切换"] == 0:
                return
            宠物名称 = 功能开关["恶龙宠物名称"]
        if fight_type == '梦魇挑战' or fight_type == '梦魇带队':
            if 功能开关["梦魇宠物切换"] == 0:
                return
            宠物名称 = 功能开关["梦魇宠物名称"]

        Toast('自动切换主战宠物 - 开始')
        tapSleep(563, 1205, 0.5)  # 点击麦乐兽
        tapSleep(355, 350, 0.5)  # 点击主战宠物
        tapSleep(547, 486, 0.5)  # 点击更换主战
        res = TomatoOcrFindRangeClick(宠物名称, 0.5, 0.9, 100, 648, 617, 947, offsetY=-60)
        if not res:
            re, _ = TomatoOcrText(140, 376, 239, 402, 宠物名称)
            if re:
                Toast('当前已设置主战宠物 - ' + 宠物名称)
                tapSleep(356, 1204, 0.3)  # 点击返回
                tapSleep(356, 1204, 0.3)  # 点击冒险
                return
            else:
                Toast('未找到主战宠物 - ' + 宠物名称)
                tapSleep(356, 1204, 0.3)  # 点击返回
                tapSleep(356, 1204, 0.3)  # 点击冒险
                return
        tapSleep(361, 1018, 0.5)  # 点击上阵
        tapSleep(356, 1204, 0.3)  # 点击返回
        tapSleep(356, 1204, 0.3)  # 点击冒险

    def zhiYeZhanLi(self):
        res, name = TomatoOcrText(94, 78, 210, 102, '玩家名称')
        任务记录["玩家名称"] = name
        res, fightNum = TomatoOcrText(107, 101, 198, 118, '玩家战力')
        if fightNum != "":
            if "万" in fightNum:
                任务记录["玩家战力"] = float(fightNum.replace("万", "")) * 10000
            else:
                任务记录["玩家战力"] = float(fightNum.replace("万", ""))
        # 识别当前职业
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "34,75,#384458|37,78,#FEFEE3|34,77,#384458|37,78,#FEFEE3|37,83,#384458|31,85,#FEFEDD|30,78,#384458|41,78,#FEFEDC|39,85,#384458")
            if re:
                Toast('识别当前职业-战士')
                任务记录['玩家-当前职业'] = '战士'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "39,83,#384458|36,86,#FFFEE1|39,80,#585F68|33,83,#384458|33,80,#4A5260|34,77,#404A5B|34,75,#464F5E|34,77,#404A5B|36,78,#FFFEE1")
            if re:
                Toast('识别当前职业-服事')
                任务记录['玩家-当前职业'] = '服事'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "30,77,#B2B4A4|33,75,#CBCDBA|33,80,#374558|34,83,#374558|37,83,#FEFEE1|39,83,#FEFEE1|39,86,#374558")
            if re:
                Toast('识别当前职业-法师')
                任务记录['玩家-当前职业'] = '法师'
        if 任务记录['玩家-当前职业'] == '':
            re = CompareColors.compare(
                "34,75,#374558|39,78,#FDFDDD|31,78,#374558|34,75,#374558|36,80,#FFFEE1|37,77,#FEFEE3|39,83,#374558|34,83,#374558")
            if re:
                Toast('识别当前职业-游侠')
                任务记录['玩家-当前职业'] = '游侠'
        # if 任务记录['玩家-当前职业'] == '':
        #     Toast('识别当前职业-刺客')
        #     任务记录['玩家-当前职业'] = '刺客'

    # 使徒来袭带队
    def fightingShiTuLaiXiTeam(self):
        totalWait = 250
        elapsed = 0
        teamShoutDone = 0
        if 功能开关["使徒来袭自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["使徒来袭自动离队时间"].replace('s', '').replace('S', ''))
            if totalWait == 0:
                totalWait = 220
        Toast("战斗开始 - 使徒来袭组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 使徒来袭超时退出组队")
                self.teamShoutAI(f'使徒来袭-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'使徒来袭战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'使徒来袭-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
            else:
                # 战斗结束
                res1 = TomatoOcrTap(331, 1092, 390, 1119, "开启", offsetX=10, offsetY=10)  # 领取宝箱
                res2 = TomatoOcrTap(331, 1092, 390, 1119, "开户", offsetX=10, offsetY=10)  # 领取宝箱
                res5 = TomatoOcrText(506, 833, 584, 857, '战斗统计')
                if res5:
                    tapSleep(358, 1098)  # 点击开启
                if res1 or res2 or res5:
                    Toast("使徒来袭 - 战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("使徒来袭 - 战斗结束")
                    功能开关["fighting"] = 0
                    break
                else:
                    tapSleep(365, 1135, 3)
                Toast("使徒来袭 - 战斗胜利 - 结算页返回房间")
                break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            if elapsed > 180 or (
                    "等级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2):
                Toast(f"使徒来袭战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"使徒来袭战斗中状态 - 识别失败 - 退出战斗")
                    break
                if failNum > 7:
                    failStatus = self.fight_fail()
                    break
            self.fight_fail_alert()
            sleep(3)
            elapsed = elapsed + 4

    # 斗歌会带队
    def fightingDouGeHuiTeam(self):
        totalWait = 220
        elapsed = 0
        teamShoutDone = 0
        if 功能开关["斗歌会自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["斗歌会自动离队时间"].replace('s', '').replace('S', ''))
            if totalWait == 0:
                totalWait = 220
        Toast("战斗开始 - 莱茵幻境组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 莱茵幻境超时退出组队")
                self.teamShoutAI(f'莱茵幻境-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'莱茵幻境战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'莱茵幻境-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
            else:
                # 战斗结束
                res1 = TomatoOcrTap(329, 1083, 391, 1110, "开启", offsetX=10, offsetY=10)  # 领取宝箱
                res2 = TomatoOcrTap(329, 1083, 391, 1110, "开户", offsetX=10, offsetY=10)  # 领取宝箱
                res5 = TomatoOcrText(516, 836, 596, 863, '战斗统计')
                if res5:
                    tapSleep(358, 1098)  # 点击开启
                if res1 or res2 or res5:
                    Toast("莱茵幻境 - 战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("莱茵幻境 - 战斗结束")
                    功能开关["fighting"] = 0
                    break
                else:
                    tapSleep(365, 1135, 3)
                Toast("莱茵幻境 - 战斗胜利 - 结算页返回房间")
                break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            if elapsed > 180 or (
                    "等级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2):
                Toast(f"莱茵幻境战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"莱茵幻境战斗中状态 - 识别失败 - 退出战斗")
                    break
                if failNum > 7:
                    failStatus = self.fight_fail()
                    break
            self.fight_fail_alert()
            sleep(3)
            elapsed = elapsed + 4

    def fightingSanMoTouTeam(self):
        totalWait = 360
        elapsed = 0
        teamShoutDone = 0
        if 功能开关["三魔头自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["三魔头自动离队时间"].replace('s', '').replace('S', ''))
            if totalWait == 0:
                totalWait = 360
        Toast("战斗开始 - 三魔头组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 三魔头超时退出组队")
                self.teamShoutAI(f'三魔头-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'三魔头战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'三魔头-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
            else:
                # 战斗结束
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(323, 1106, 391, 1137, "开启")  # 领取宝箱
                res4 = CompareColors.compare(
                    "448,803,#FFE298|445,782,#F8D37E|448,770,#FBD682|426,770,#D0714C|483,763,#9C3B43")  # 匹配宝箱颜色
                res5 = TomatoOcrText(513, 885, 592, 905, '战斗统计')
                if res1 or res2 or res3 or res4 or res5:
                    Toast("三打三守三魔头 - 战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    sleep(1)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("三打三守三魔头 - 战斗结束")
                    功能开关["fighting"] = 0
                    break
                else:
                    tapSleep(365, 1135, 3)
                Toast("三魔头 - 战斗胜利 - 结算页返回房间")
                break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            if elapsed > 180 or (
                    "等级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2):
                Toast(f"三魔头战斗中状态 - 识别失败 - 次数 {failNum}/4")
                sleep(1)
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"三魔头战斗中状态 - 识别失败 - 退出战斗")
                    break
                if failNum > 7:
                    failStatus = self.fight_fail()
                    break
            self.fight_fail_alert()

    def fightingBaoZouTeam(self):
        try:
            totalWait = 30
            elapsed = 0
            teamShoutDone = 0
            if 功能开关["暴走自动离队时间"] != "":
                totalWait = safe_int_v2(功能开关["暴走自动离队时间"].replace('s', '').replace('S', ''))
                if totalWait == 0:
                    totalWait = 30
            Toast("战斗开始 - 暴走组队邀请")
            failNum = 0  # 战斗中状态识别失败次数
            start_time = int(time.time())
            while 1:
                current_time = int(time.time())
                elapsed = current_time - start_time
                if elapsed >= totalWait:
                    Toast("战斗结束 - 暴走超时退出组队")
                    res1 = TomatoOcrTap(325, 1059, 391, 1089, "开", match_mode='fuzzy')
                    if not res1:
                        res1 = TomatoOcrTap(333, 716, 384, 744, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(334, 1090, 385, 1117, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(333, 1052, 385, 1081, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(331, 749, 386, 778, '开', match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(323, 1106, 391, 1137, "开", match_mode='fuzzy')  # 领取宝箱
                    # self.teamShoutAI(f'大暴走-即将离队-期待下次相遇', shoutType="fight")
                    self.quitTeamFighting()  # 退出队伍
                    break

                # 识别战斗中状态
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
                if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                    功能开关["fighting"] = 1
                    功能开关["needHome"] = 0
                    Toast(f'暴走战斗中,战斗时长{elapsed}/{totalWait}秒')
                    if teamShoutDone == 0:
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'大暴走-{任务记录["战斗-关卡名称"]}-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                            shoutType="fight")
                        teamShoutDone = self.teamShout()

                    # 战斗逻辑
                    for i in range(7):
                        if 任务记录["战斗-关卡名称"] or 功能开关["史莱姆选择"] == '暴走雷电大王':
                            self.daBaoZouLeidian()
                        if 任务记录["战斗-关卡名称"] or 功能开关["史莱姆选择"] == '暴走烈焰大王':
                            self.daBaoZouLieYan()
                        if 任务记录["战斗-关卡名称"] or 功能开关["史莱姆选择"] == '暴走深林大王':
                            self.daBaoZouShenLin()
                        if 任务记录["战斗-关卡名称"] or 功能开关["史莱姆选择"] == '暴走水波大王':
                            self.daBaoZouShuiBo()
                        else:
                            Toast(f'错误 - 未识别的史莱姆类型 - {功能开关["史莱姆选择"]}')
                            sleep(1)
                    self.fight_fail_alert()
                    sleep(0.5)
                else:
                    # 战斗结束
                    res1 = TomatoOcrTap(325, 1059, 391, 1089, "开", match_mode='fuzzy')
                    if not res1:
                        res1 = TomatoOcrTap(333, 716, 384, 744, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(334, 1090, 385, 1117, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(333, 1052, 385, 1081, "开", match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(331, 749, 386, 778, '开', match_mode='fuzzy')  # 领取宝箱
                    if not res1:
                        res1 = TomatoOcrTap(323, 1106, 391, 1137, "开", match_mode='fuzzy')  # 领取宝箱
                    if res1:
                        Toast("暴走战斗结束 - 战斗胜利")
                        功能开关["fighting"] = 0
                        self.quitTeam()
                        break
                    else:
                        self.quitTeam()

                    Toast("暴走任务 - 战斗胜利 - 结算页返回房间")
                    break

                # 判断是否战斗失败（战斗4分钟后）
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                if "级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2:
                    Toast(f"暴走战斗中状态 - 识别失败 - 次数 {failNum}/7")
                    sleep(1)
                    shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                    failNum = failNum + 1
                    if shou_ye1 or failNum > 4:
                        Toast(f"暴走战斗中状态 - 识别失败 - 退出战斗")
                        break
                    if failNum > 7:
                        failStatus = self.fight_fail()
                        break
                self.fight_fail_alert()
        except Exception as e:
            # 处理异常
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 输出异常信息和行号
            file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
            error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
            # 显示对话框
            print(error_message)

    def fightingDiaoChaTeam(self):
        totalWait = 30
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 调查队组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 调查队超时退出组队")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'调查队战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
            else:
                # 战斗结束
                openStatus = self.openTreasure()
                if openStatus == 1:
                    功能开关["fighting"] = 0
                    Toast("调查队战斗结束 - 战斗胜利")
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2:
                Toast(f"调查队战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"调查队战斗中状态 - 识别失败 - 退出战斗")
                    功能开关["fighting"] = 0
                    break
                failStatus = self.fight_fail()
                if failStatus:
                    功能开关["fighting"] = 0
                    break
            sleep(3)
            elapsed = elapsed + 5

    def fightingJueJingTeam(self):
        totalWait = 90
        if 功能开关["绝境自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["绝境自动离队时间"].replace('s', '').replace('S', '').replace('秒', ''))
            if totalWait == 0:
                totalWait = 90
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 绝境组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 绝境超时退出组队")
                self.teamShoutAI(f'绝境-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break
            if elapsed >= 25:
                colors = generate_random_color()
                tmpContent = f"<color={colors}>绝境-战斗即将结束-辛苦了~期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'绝境战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'绝境-{任务记录["战斗-关卡名称"]}-开始战斗~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
                # 自动锁敌走位
                # self.autoMove()
            else:
                # 战斗结束
                # 战斗结束
                res1, _ = TomatoOcrText(303, 962, 412, 1002, "通关奖励")
                res2, _ = TomatoOcrText(502, 187, 582, 213, '离开队伍')
                res3, _ = TomatoOcrText(512, 999, 596, 1024, '战斗统计')
                res4, _ = TomatoOcrText(514, 937, 590, 964, '战斗统计')
                if res1 or res2 or res3 or res4:
                    if 功能开关['秘境点赞队友'] == 1:
                        Toast('点赞队友')
                        res = TomatoOcrTap(517, 909, 595, 929, "一键", 5, 5, match_mode='fuzzy')  # 一键点赞
                        if not res:
                            res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                          match_mode='fuzzy')  # 一键点赞

                    tapSleep(364, 1136, 0.3)
                    tapSleep(364, 1136, 0.3)
                    Toast("绝境战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2:
                Toast(f"绝境战斗中状态 - 识别失败 - 次数 {failNum}/5")
                sleep(1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                failNum = failNum + 1
                if failNum > 8:
                    Toast(f"绝境战斗中状态 - 识别失败 - 退出战斗")
                if failNum > 11:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break
                res6, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
                if shou_ye1 or res6:
                    功能开关["fighting"] = 0
                    Toast(f"绝境战斗中状态 - 识别失败 - 退出战斗")
                    break
            # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
            allQuit = self.allQuit()
            if allQuit:
                break
            self.fight_fail_alert()

    def fightingZhongMoTeam(self):
        totalWait = 240
        elapsed = 0
        teamShoutDone = 0
        if 功能开关["终末自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["终末自动离队时间"].replace('s', '').replace('S', ''))
            if totalWait == 0:
                totalWait = 240

        Toast("战斗开始 - 终末战组队邀请")
        start_time = int(time.time())
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 终末战超时退出组队")
                colors = generate_random_color()
                tmpContent = f"<color={colors}>终末战-即将离队-期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            if elapsed >= 25:
                colors = generate_random_color()
                tmpContent = f"<color={colors}>终末战-战斗即将结束-辛苦了~期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")

            # 识别战斗中状态
            res, teamName4 = TomatoOcrText(4, 247, 56, 265, "队友名称")
            # res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "级" in teamName4 or "Lv" in teamName4:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'终末战战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'终末战-{任务记录["战斗-关卡名称"]}-开始战斗-{teamName}-第{teamCount}次相遇~祝你武运昌隆~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
                # 自动锁敌走位
                # self.autoMove()
            else:
                # 战斗结束
                res1, _ = TomatoOcrText(303, 962, 412, 1002, "通关奖励")
                res2, _ = TomatoOcrText(502, 187, 582, 213, '离开队伍')
                res3, _ = TomatoOcrText(512, 999, 596, 1024, '战斗统计')
                if not res3:
                    res3, tmp1 = TomatoOcrText(513, 939, 595, 964, "战斗统计")  # 战斗结束页。宝箱提示
                if res1 or res2 or res3:
                    tapSleep(364, 1136, 0.3)
                    tapSleep(364, 1136, 0.3)
                    Toast("终末战战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2:
                Toast(f"终末战战斗中状态 - 识别失败 - 次数 {failNum}/8")
                sleep(1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                failNum = failNum + 1
                if failNum > 8:
                    Toast(f"终末战战斗中状态 - 识别失败 - 退出战斗")
                if shou_ye1 or failNum > 9:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break

            # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
            allQuit = self.allQuit()
            if allQuit:
                break
            self.fight_fail_alert()

    def fightingZhiGuTeam(self, fightType='桎梏之形'):
        totalWait = 260
        if fightType == '桎梏之形带队':
            totalWait = 30
        if fightType == '桎梏之形挑战':
            totalWait = 260
        if 功能开关["桎梏之形自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["桎梏之形自动离队时间"].replace('s', '').replace('S', ''))

        teamShoutDone = 0

        Toast("战斗开始 - 桎梏之形")
        start_time = int(time.time())
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            self.fight_fail_alert()
            if elapsed >= totalWait:
                Toast("战斗结束 - 桎梏之形超时退出组队")
                colors = generate_random_color()
                tmpContent = f"<color={colors}>桎梏之形-即将离队-期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")
                功能开关["fighting"] = 1
                res, _ = TomatoOcrText(495, 585, 576, 609, "战斗统计")
                if res:
                    if 功能开关['秘境点赞队友'] == 1:
                        Toast('点赞队友')
                        res = TomatoOcrTap(508, 784, 592, 804, "一键", 10, 10, match_mode='fuzzy')  # 一键点赞
                        if not res:
                            res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                          match_mode='fuzzy')  # 一键点赞

                    res = TomatoOcrTap(322, 1064, 395, 1100, "开", match_mode='fuzzy')
                    if not re:
                        res = TomatoOcrFindRangeClick(keywords=[{'keyword': '开启', 'match_mode': 'fuzzy'},
                                                                {'keyword': '开户', 'match_mode': 'fuzzy'}], x1=104,
                                                      y1=801, x2=617, y2=1122,
                                                      match_mode='fuzzy')
                    if res:
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                    else:
                        tapSleep(363, 1191)
                        tapSleep(363, 1191)
                        tapSleep(363, 1191, 2)
                    Toast("桎梏之形 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            if elapsed >= 15:
                colors = generate_random_color()
                tmpContent = f"<color={colors}>桎梏之形-战斗即将结束-辛苦了~期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
                Toast(f'桎梏之形战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    if fightType == '桎梏之形挑战':
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'桎梏之形-{任务记录["战斗-关卡名称"]}-等待战斗结束~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                            shoutType="fight")
                    if fightType == '桎梏之形带队':
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'桎梏之形-{任务记录["战斗-关卡名称"]}-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                            shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
            else:
                # 战斗结束
                res, _ = TomatoOcrText(514, 853, 593, 880, "战斗统计")
                if res:
                    res = TomatoOcrTap(322, 1064, 395, 1100, "开", match_mode='fuzzy')
                    if res:
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                    else:
                        tapSleep(363, 1191)
                        tapSleep(363, 1191)
                        tapSleep(363, 1191, 2)
                    Toast("桎梏之形 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break
                res2, _ = TomatoOcrText(502, 187, 582, 213, '离开队伍')
                if res2:
                    Toast("桎梏之形 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2:
                Toast(f"桎梏之形战斗中状态 - 识别失败 - 次数 {failNum}/12")
                sleep(1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                failNum = failNum + 1
                if failNum > 10:
                    Toast(f"桎梏之形战斗中状态 - 识别失败 - 退出战斗")
                if shou_ye1 or failNum > 12:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break
                res6, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
                if res6:
                    Toast(f"桎梏之形战斗中状态 - 识别失败 - 退出战斗")
                    break

    def fightingELongTeam(self, fightType='恶龙带队'):
        totalWait = 30
        if fightType == '恶龙挑战':
            totalWait = 360
        if 功能开关["恶龙自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["恶龙自动离队时间"].replace('s', '').replace('S', '').replace('秒', ''))
            if totalWait == 0:
                totalWait = 30
                if fightType == '恶龙挑战':
                    totalWait = 360
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 恶龙组队邀请")
        start_time = int(time.time())
        self.changeChongWu(fightType)
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 恶龙超时退出组队")
                colors = generate_random_color()
                tmpContent = f"<color={colors}>恶龙-即将离队-期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")
                功能开关["fighting"] = 1
                res, _ = TomatoOcrText(495, 585, 576, 609, "战斗统计")
                if res:
                    if 功能开关['秘境点赞队友'] == 1:
                        Toast('点赞队友')
                        res = TomatoOcrTap(515, 513, 593, 534, "一键", 5, 5, match_mode='fuzzy')  # 一键点赞
                        if not res:
                            res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                          match_mode='fuzzy')  # 一键点赞

                    res = TomatoOcrTap(334, 1049, 385, 1079, "开启")
                    if not res:
                        res = TomatoOcrTap(334, 1049, 385, 1079, "开户")
                    if res:
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(649, 1248, 0.3)
                        tapSleep(649, 1248, 0.3)
                    else:
                        tapSleep(363, 1191)
                        tapSleep(649, 1248)
                        tapSleep(649, 1248, 2)
                    Toast("恶龙任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            if elapsed >= 15:
                colors = generate_random_color()
                tmpContent = f"<color={colors}>恶龙-战斗即将结束-辛苦了~期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "Lv" in teamName1:
                Toast(f'恶龙战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    if fightType == '恶龙挑战':
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'恶龙-{任务记录["战斗-关卡名称"]}-等待战斗结束~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                            shoutType="fight")
                    else:
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'恶龙-{任务记录["战斗-关卡名称"]}-留镜像后离队~祝你武运昌隆~{teamName}-第{teamCount}次相遇~祝你游戏开心~',
                            shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
                # self.autoMove()
            else:
                # 战斗结束
                # 兼容恶龙战斗结算页
                res, _ = TomatoOcrText(495, 585, 576, 609, "战斗统计")
                if res:
                    res = TomatoOcrTap(334, 1049, 385, 1079, "开启")
                    if not res:
                        res = TomatoOcrTap(334, 1049, 385, 1079, "开户")
                    if res:
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                        tapSleep(363, 1191, 0.3)
                    else:
                        tapSleep(363, 1191)
                        tapSleep(363, 1191)
                        tapSleep(363, 1191, 2)
                    Toast("恶龙任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break
                res2, _ = TomatoOcrText(502, 187, 582, 213, '离开队伍')
                if res2:
                    Toast("恶龙任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "级" not in teamName1 and "Lv" not in teamName1:
                Toast(f"恶龙战斗中状态 - 识别失败 - 次数 {failNum}/12")
                sleep(1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                failNum = failNum + 1
                if failNum > 10:
                    Toast(f"恶龙战斗中状态 - 识别失败 - 退出战斗")
                if failNum > 12:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break
                res6, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
                if shou_ye1 or res6:
                    Toast(f"恶龙战斗中状态 - 识别失败 - 退出战斗")
                    功能开关["fighting"] = 0
                    break
            self.fight_fail_alert()

    def fightingMengYanTeam(self, fightType='梦魇带队'):
        totalWait = 28  # 30000 毫秒 = 30 秒
        if fightType == '梦魇挑战':
            totalWait = 850
        if 功能开关["梦魇自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["梦魇自动离队时间"].replace('s', '').replace('S', ''))
            if totalWait == 0:
                totalWait = 30
                if fightType == '梦魇挑战':
                    totalWait = 850
        elapsed = 0
        teamShoutDone = 0

        if fightType == '梦魇带队':
            Toast("战斗开始 - 梦魇组队邀请")
        if fightType == '梦魇挑战':
            Toast("战斗开始 - 梦魇挑战")
        start_time = int(time.time())
        self.changeChongWu(fightType)
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                colors = generate_random_color()
                tmpContent = f"<color={colors}>梦魇-即将离队-期待下次相遇~</COLOR>"
                self.teamShoutAI(tmpContent, shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "等级" in teamName1 or "Lv" in teamName1:
                # if teamShoutDone == 0:
                #     teamShoutDone = self.teamShout()
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'梦魇战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    if fightType == '梦魇挑战':
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'梦魇-{任务记录["战斗-关卡名称"]}-等待战斗结束~{teamName}-第{teamCount}次相遇~祝你武运昌隆~',
                            shoutType="fight")
                    else:
                        teamName = 任务记录['战斗-房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(
                            f'梦魇-{任务记录["战斗-关卡名称"]}-留镜像后离队~{teamName}-第{teamCount}次相遇~祝你武运昌隆~',
                            shoutType="fight")
                    teamShoutDone = self.teamShout()
                self.AIContent()
            else:
                # 战斗结束
                # openStatus = self.openTreasure()
                # if openStatus == 1:
                #     Toast("梦魇战斗结束 - 战斗胜利")
                #     功能开关["fighting"] = 0
                #     break

                res1, _ = TomatoOcrText(514, 876, 594, 901, "一键", match_mode='fuzzy')
                if not res1:
                    res1, _ = TomatoOcrText(517, 937, 593, 959, "战斗统计")
                if res1:
                    if 功能开关['秘境点赞队友'] == 1:
                        Toast('点赞队友')
                        res = TomatoOcrTap(517, 909, 595, 929, "一键", 5, 5, match_mode='fuzzy')  # 一键点赞
                        if not res:
                            res = TomatoOcrFindRangeClick("一键", x1=480, y1=490, x2=615, y2=768,
                                                          match_mode='fuzzy')  # 一键点赞

                    tapSleep(358, 1137, 3)
                    Toast("梦魇任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            # res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
            # res7, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
            if "级" not in teamName1 and "Lv" not in teamName1:
                Toast(f"梦魇战斗中状态 - 识别失败 - 次数 {failNum}/4")
                sleep(1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                failNum = failNum + 1
                if shou_ye1 or failNum > 3:
                    Toast(f"梦魇战斗中状态 - 识别失败 - 退出战斗")
                    break
                if failNum > 6:
                    failStatus = self.fight_fail()
                    break

    def fighting(self, fightType='秘境'):
        totalWait = 400  # 30000 毫秒 = 30 秒
        elapsed = 0
        teamShoutDone = 0

        failNum = 0  # 战斗中状态识别失败次数

        TomatoOcrFindRangeClick('跳过', sleep1=1, confidence1=0.9, x1=522, y1=17, x2=685, y2=110, offsetX=10,
                                offsetY=10)

        任务记录['战斗-上一次移动'] = time.time()
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            # if "等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2:
            if "等级" in teamName1 or "Lv" in teamName1:
                Toast(f'秘境战斗中 {elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamName = 任务记录['战斗-房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(
                        f'秘境-{任务记录["战斗-关卡名称"]}-开始战斗~{teamName}-第{teamCount}次相遇~祝你武运昌隆~',
                        shoutType="fight")
                    teamShoutDone = self.teamShout(shoutType="fight")
                if elapsed > 25 and fightType == '秘境带队':
                    colors = generate_random_color()
                    tmpContent = f"<color={colors}>秘境-战斗即将结束-辛苦了~期待下次相遇~</COLOR>"
                    self.teamShoutAI(tmpContent, shoutType="fight")
                self.AIContent()
                # 自动锁敌走位
                # self.autoMove()
            else:
                # 战斗结束
                if fightType == '秘境带队' and 功能开关['秘境不开宝箱'] == 1:
                    openStatus = self.openTreasure(noNeedOpen=1)
                else:
                    openStatus = self.openTreasure()
                if openStatus == 1:
                    Toast("战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break
                # 兼容恶龙战斗结算页
                res, _ = TomatoOcrText(309, 569, 411, 607, "战斗详情")
                if res:
                    res, _ = TomatoOcrText(333, 1049, 384, 1077, "开启")
                    if res:
                        tapSleep(365, 1135)
                        tapSleep(365, 1135)
                        tapSleep(365, 1135)
                        tapSleep(365, 1135, 3)
                    else:
                        tapSleep(365, 1135, 3)
                    Toast("恶龙任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break
                # 未开启宝箱，尝试返回冒险页
                res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")

            # 判断是否战斗失败（战斗4分钟后）
            # res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            # if elapsed > 400 or ("等级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2):
            res, teamName4 = TomatoOcrText(4, 247, 56, 265, "队友名称")
            if elapsed > 400 or ("等级" not in teamName4 and "Lv" not in teamName4):
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                if shou_ye1:
                    Toast(f"战斗中状态 - 识别失败 - 退出战斗")
                    break
                # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
                allQuit = self.allQuit()
                if allQuit:
                    break
                failNum = failNum + 1
                if failNum > 8:
                    Toast(f"战斗中状态 - 识别失败 - {failNum}/15")
                if failNum > 13:
                    Toast(f"战斗中状态 - 识别失败 - 退出战斗")
                    failStatus = self.fight_fail()
                    self.quitTeamFighting()  # 退出队伍
                    break
            else:
                # 重置战败计算
                failNum = 0

            if elapsed > 200:
                res, teamName4 = TomatoOcrText(56, 220, 138, 249, "队友名称")
                if teamName4 == "":
                    allQuit = self.allQuit(needCheck=True)
                    if allQuit:
                        break
            self.fight_fail_alert()
            sleep(0.5)
        功能开关["fighting"] = 0

    def fightingShiTuLaiXi(self):
        totalWait = 250  # 30000 毫秒 = 30 秒

        teamShoutDone = 0
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1 or ("等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2):
                Toast(f'使徒来袭战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout(shoutType="fight")
            else:
                功能开关["fighting"] = 0

            # 判断是否战斗失败（战斗5分钟后）
            if not res1 and (teamName1 == "" and teamName2 == ""):
                功能开关["fighting"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(331, 1092, 390, 1119, "开启", offsetX=10, offsetY=10)  # 领取宝箱
                res2 = TomatoOcrTap(331, 1092, 390, 1119, "开户", offsetX=10, offsetY=10)  # 领取宝箱
                res5 = TomatoOcrText(506, 833, 584, 857, '战斗统计')
                if res5:
                    tapSleep(358, 1098)  # 点击开启
                if res1 or res2 or res5:
                    Toast("使徒来袭 - 战斗结束 - 战斗胜利")
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("使徒来袭 - 战斗结束")
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
            self.fight_fail_alert()
            sleep(0.5)
        功能开关["fighting"] = 0

    def fightingDouGeHui(self):
        totalWait = 380  # 30000 毫秒 = 30 秒

        teamShoutDone = 0
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1 or ("等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2):
                Toast(f'莱茵幻境战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout(shoutType="fight")
            else:
                功能开关["fighting"] = 0

            # 判断是否战斗失败（战斗5分钟后）
            if not res1 and (teamName1 == "" and teamName2 == ""):
                功能开关["fighting"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(329, 1083, 391, 1110, "开启", offsetX=10, offsetY=10)  # 领取宝箱
                res2 = TomatoOcrTap(329, 1083, 391, 1110, "开户", offsetX=10, offsetY=10)  # 领取宝箱
                res5 = TomatoOcrText(516, 836, 596, 863, '战斗统计')
                if res5:
                    tapSleep(358, 1098)  # 点击开启
                if res1 or res2 or res5:
                    Toast("莱茵幻境 - 战斗结束 - 战斗胜利")
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("莱茵幻境 - 战斗结束")
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
            self.fight_fail_alert()
            sleep(0.5)
        功能开关["fighting"] = 0

    def fightingSanMoTou(self):
        totalWait = 380  # 30000 毫秒 = 30 秒

        teamShoutDone = 0
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1 or ("等级" in teamName1 or "等级" in teamName2 or "Lv" in teamName1 or "Lv" in teamName2):
                Toast(f'三魔头战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout(shoutType="fight")
            else:
                功能开关["fighting"] = 0

            # 判断是否战斗失败（战斗5分钟后）
            if not res1 and (teamName1 == "" and teamName2 == ""):
                功能开关["fighting"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(323, 1106, 391, 1137, "开启")  # 领取宝箱
                res4 = CompareColors.compare(
                    "448,803,#FFE298|445,782,#F8D37E|448,770,#FBD682|426,770,#D0714C|483,763,#9C3B43")  # 匹配宝箱颜色
                res5 = TomatoOcrText(513, 899, 590, 923, '战斗统计')
                if res1 or res2 or res3 or res4 or res5:
                    Toast("三打三守三魔头 - 战斗结束 - 战斗胜利")
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("三打三守三魔头 - 战斗结束")
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
            sleep(0.5)
        功能开关["fighting"] = 0

    def fightingBaoZou(self):
        totalWait = 380  # 30000 毫秒 = 30 秒

        teamShoutDone = 0
        start_time = int(time.time())
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed >= totalWait:
                Toast("战斗结束 - 暴走超时退出组队")
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(333, 1052, 385, 1081, "开启")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(331, 749, 386, 778, '开启')  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(333, 716, 384, 744, "开户")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(334, 1090, 385, 1117, "开户")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(323, 1106, 391, 1137, "开户")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(333, 1052, 385, 1081, "开户")  # 领取宝箱
                if not res1:
                    res1 = TomatoOcrTap(331, 749, 386, 778, '开户')  # 领取宝箱
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            # res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            # res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1:
                # Toast("战斗中")
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast('暴走史莱姆 - 战斗中')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout(shoutType="fight")
            else:
                功能开关["fighting"] = 0

            # 战斗逻辑
            # 循环10次，优先处理战斗中走位
            if res1:
                for i in range(1, 10):
                    if 功能开关["史莱姆选择"] == '暴走雷电大王':
                        self.daBaoZouLeidian()
                    if 功能开关["史莱姆选择"] == '暴走烈焰大王':
                        self.daBaoZouLieYan()
                    if 功能开关["史莱姆选择"] == '暴走深林大王':
                        self.daBaoZouShenLin()
                    if 功能开关["史莱姆选择"] == '暴走水波大王':
                        self.daBaoZouShuiBo()

                # 战斗结束
                # res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                # res3 = TomatoOcrTap(332, 1067, 387, 1096, "开启")  # 领取宝箱
                # if res2 or res3:
                #     Toast("战斗结束 - 战斗胜利")
                #     tapSleep(55, 1140)  # 领取后，点击空白
                #     tapSleep(55, 1140)  # 领取后，点击空白
                #     break
                self.fight_fail_alert()
                sleep(0.5)

            # 判断是否战斗失败（战斗5分钟后）
            if not res1:
                # 房间 - 关闭邀请玩家
                re1, _ = TomatoOcrText(318, 222, 401, 247, '邀请玩家')
                if re1:
                    tapSleep(590, 1076)
                    tapSleep(590, 1076)
                功能开关["fighting"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(323, 1106, 391, 1137, "开启")  # 领取宝箱
                res4 = TomatoOcrTap(333, 1052, 385, 1081, "开启")  # 领取宝箱
                if not res1 and not res2 and not res3 and not res4:
                    res1 = TomatoOcrTap(333, 716, 384, 744, "开户")  # 领取宝箱
                    res2 = TomatoOcrTap(334, 1090, 385, 1117, "开户")  # 领取宝箱
                    res3 = TomatoOcrTap(323, 1106, 391, 1137, "开户")  # 领取宝箱
                    res4 = TomatoOcrTap(333, 1052, 385, 1081, "开户")  # 领取宝箱
                if res1 or res2 or res3 or res4:
                    Toast("暴走史莱姆 - 战斗结束 - 战斗胜利")
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(60, 1100)  # 领取后，点击空白
                    tapSleep(50, 1234)  # 领取后，点击空白
                    quitStatus = self.quitTeam()
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("暴走史莱姆 - 战斗结束")
                    quitStatus = self.quitTeam()
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
        功能开关["fighting"] = 0

    # 大暴走（雷电大王）
    def daBaoZouLeidian(self):
        def 草():
            point = FindColors.find(
                "145,673,#B9D6AB|153,672,#BFD7AD|159,672,#95B48C|151,680,#A1D8A1|138,681,#98D99D|148,688,#2D4645",
                rect=[9, 637, 202, 803], diff=0.92)
            if point:
                tapSleep(point.x, point.y, 1)

        def 火():
            point = FindColors.find(
                "137,683,#DF8768|138,675,#E1A482|146,677,#CF9677|156,683,#DF8768|157,677,#E29E7C|146,675,#E2A382",
                rect=[9, 637, 202, 803], diff=0.92)
            if point:
                tapSleep(point.x, point.y, 1)

        def 水():
            point = FindColors.find(
                "63,673,#91CFCE|69,667,#A5D4CE|75,672,#95D0CF|69,691,#57BACF|74,686,#5CBACE|77,686,#5AB9CF",
                rect=[9, 637, 202, 803], diff=0.92)
            if point:
                tapSleep(point.x, point.y, 1)

        # 当前职业
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                任务记录['玩家-当前职业'] = '战士'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
            if re:
                # Toast('识别当前职业-服事')
                任务记录['玩家-当前职业'] = '服事'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                任务记录['玩家-当前职业'] = '刺客'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                任务记录['玩家-当前职业'] = '法师'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                任务记录['玩家-当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '' and 功能开关['userColor'] == '':
            Toast('暴走史莱姆 - 战斗中 - 等待走位')
            # if 当前职业 == '战士':
            #     Toast('战士-战斗中-自动走位火')
            #     火()
            if 任务记录['玩家-当前职业'] == '服事' and 功能开关['暴走职能优先治疗'] == 1:
                Toast('服事-战斗中-自动走位草')
                草()
            # if 当前职业 == '刺客':
            #     Toast('刺客-战斗中-自动走位火')
            #     火()
            # if 当前职业 == '游侠':
            #     Toast('游侠-战斗中-自动走位火')
            #     火()
            # if 当前职业 == '法师':
            #     Toast('法师-战斗中-自动走位火')
            #     火()

        if 功能开关['bossColor'] != '' and 功能开关['userColor'] != '':
            if (功能开关['bossLastColor'] != '' and 功能开关['bossLastColor'] == 功能开关['bossColor']) and (
                    功能开关['userLastColor'] != '' and 功能开关['userLastColor'] == 功能开关['userColor']):
                Toast('暴走史莱姆 - 战斗中 - 无需走位')
            else:
                功能开关['bossLastColor'] = 功能开关['bossColor']
                功能开关['userLastColor'] = 功能开关['userColor']
                if 功能开关['userColor'] == '开花':
                    if 功能开关['bossColor'] == '木':
                        Toast('前往-水')
                        水()
                        sleep(1)
                    if 功能开关['bossColor'] == '水':
                        Toast('前往-草')
                        草()
                        sleep(1)
                if 功能开关['userColor'] == '篝火':
                    if 功能开关['bossColor'] == '火':
                        Toast('前往-草')
                        草()
                        sleep(1)
                    if 功能开关['bossColor'] == '木':
                        Toast('前往-火')
                        火()
                        sleep(1)
                if 功能开关['userColor'] == '蒸汽':
                    if 功能开关['bossColor'] == '火':
                        Toast('前往-水')
                        水()
                        sleep(1)
                    if 功能开关['bossColor'] == '水':
                        Toast('前往-火')
                        火()
                        sleep(1)

    # 大暴走（水波大王）
    def daBaoZouShuiBo(self):
        def 草():
            point = FindColors.find(
                "145,673,#B9D6AB|153,672,#BFD7AD|159,672,#95B48C|151,680,#A1D8A1|138,681,#98D99D|148,688,#2D4645",
                rect=[9, 637, 202, 803], diff=0.92)
            if point:
                tapSleep(point.x, point.y, 1)

        def 火():
            point = FindColors.find(
                "137,683,#DF8768|138,675,#E1A482|146,677,#CF9677|156,683,#DF8768|157,677,#E29E7C|146,675,#E2A382",
                rect=[9, 637, 202, 803], diff=0.94)
            if point:
                tapSleep(point.x, point.y, 1)

        def 水():
            point = FindColors.find(
                "63,673,#91CFCE|69,667,#A5D4CE|75,672,#95D0CF|69,691,#57BACF|74,686,#5CBACE|77,686,#5AB9CF",
                rect=[9, 637, 202, 803], diff=0.94)
            if point:
                tapSleep(point.x, point.y, 1)

        # 当前职业
        # if 任务记录['玩家-当前职业'] == '':
        #     re, x, y = imageFind("职业-战士", 0.95, 4, 41, 72, 118)
        #     if re:
        #         Toast('识别当前职业-战士')
        #         任务记录['玩家-当前职业'] = '战士'
        # if 任务记录['玩家-当前职业'] == '':
        #     re, x, y = imageFind("职业-服事", 0.95, 4, 41, 72, 118)
        #     if re:
        #         # Toast('识别当前职业-服事')
        #         任务记录['玩家-当前职业'] = '服事'
        # if 任务记录['玩家-当前职业'] == '':
        #     re, x, y = imageFind("职业-刺客", 0.95, 4, 41, 72, 118)
        #     if re:
        #         Toast('识别当前职业-刺客')
        #         任务记录['玩家-当前职业'] = '刺客'
        # if 任务记录['玩家-当前职业'] == '':
        #     re, x, y = imageFind("职业-法师", 0.95, 4, 41, 72, 118)
        #     if re:
        #         Toast('识别当前职业-法师')
        #         任务记录['玩家-当前职业'] = '法师'
        # if 任务记录['玩家-当前职业'] == '':
        #     re, x, y = imageFind("职业-游侠", 0.95, 4, 41, 72, 118)
        #     if re:
        #         Toast('识别当前职业-游侠')
        #         任务记录['玩家-当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '' and 功能开关['bossColor1'] == '' and 功能开关['bossColor2'] == '':
            # if 当前职业 == '战士':
            #     Toast('战士-战斗中-自动走位火')
            #     火()
            if 任务记录['玩家-当前职业'] == '服事':
                Toast('服事-战斗中-自动走位草')
                草()
                return
            # if 当前职业 == '刺客':
            #     Toast('刺客-战斗中-自动走位火')
            #     火()
            # if 当前职业 == '游侠':
            #     Toast('游侠-战斗中-自动走位火')
            #     火()
            # if 当前职业 == '法师':
            #     Toast('法师-战斗中-自动走位火')
            #     火()

        if 功能开关['bossColor1'] != '' and 功能开关['bossColor2'] != '':
            if 功能开关['bossLastColor1'] != '' and 功能开关['bossLastColor2'] != '' and (
                    功能开关['bossLastColor1'] == 功能开关['bossColor1'] and 功能开关['bossLastColor2'] == 功能开关[
                'bossColor2']):
                Toast('战斗中')
            else:
                功能开关['bossLastColor1'] = 功能开关['bossColor1']
                功能开关['bossLastColor2'] = 功能开关['bossColor2']
                if 功能开关['bossLastColor1'] == '水':
                    if 功能开关['bossLastColor2'] == '水':
                        Toast('前往-水')
                        水()
                        sleep(1)
                    if 功能开关['bossLastColor2'] == '花':
                        Toast('前往-草')
                        草()
                        sleep(1)
                    if 功能开关['bossLastColor2'] == '蒸汽':
                        Toast('前往-火')
                        火()
                        sleep(1)
                if 功能开关['bossLastColor1'] == '木':
                    if 功能开关['bossLastColor2'] == '木':
                        Toast('前往-木')
                        草()
                        sleep(1)
                if 功能开关['bossLastColor1'] == '火':
                    if 功能开关['bossLastColor2'] == '火':
                        Toast('前往-火')
                        火()
                        sleep(1)
                    if 功能开关['bossLastColor2'] == '篝火':
                        Toast('前往-木')
                        草()
                        sleep(1)

        if 功能开关['bossColor'] != "":
            if 功能开关['bossLastColor'] != '' and (功能开关['bossLastColor'] == 功能开关['bossColor']):
                Toast('战斗中')
            else:
                功能开关['bossLastColor'] = 功能开关['bossColor']
                if 功能开关['bossColor'] == "水":
                    Toast('前往-水')
                    水()
                    sleep(1)
                if 功能开关['bossColor'] == "木":
                    Toast('前往-木')
                    草()
                    sleep(1)
                if 功能开关['bossColor'] == "火":
                    Toast('前往-火')
                    火()
                    sleep(1)

    # 大暴走（深林大王）
    def daBaoZouShenLin(self):
        def 草():
            point = FindColors.find(
                "67,675,#B2D3A9|71,669,#C8D7AF|78,673,#BBD6AC|74,686,#2D4744|63,691,#323C4A|61,675,#B4D6A9",
                rect=[25, 631, 187, 803], diff=0.9)
            if point:
                tapSleep(point.x + 5, point.y + 10, 1)

        def 火():
            point = FindColors.find(
                "143,670,#E2B591|148,672,#E2AD89|143,681,#A87061|150,684,#323C4A|153,680,#E19171",
                rect=[25, 631, 187, 803], diff=0.82)
            if point:
                tapSleep(point.x + 5, point.y + 10, 1)

        def 水():
            point = FindColors.find(
                "101,741,#9CD3CF|104,741,#9CD0CF|110,741,#9CD3CF|113,740,#9FD3CF|120,744,#91CECF|116,760,#57B1C7",
                rect=[25, 631, 187, 803], diff=0.85)
            if point:
                tapSleep(point.x + 5, point.y + 10, 1)

        # 当前职业
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                任务记录['玩家-当前职业'] = '战士'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
            if re:
                # Toast('识别当前职业-服事')
                任务记录['玩家-当前职业'] = '服事'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                任务记录['玩家-当前职业'] = '刺客'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                任务记录['玩家-当前职业'] = '法师'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                任务记录['玩家-当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '':
            Toast('暴走史莱姆 - 战斗中 - 等待走位')
            if 任务记录['玩家-当前职业'] == '服事' and 功能开关['暴走职能优先治疗'] == 1:
                Toast('服事-战斗中-自动走位草')
                草()

        if 功能开关['bossColor'] != '':
            if 功能开关['bossLastColor'] != '' and 功能开关['bossLastColor'] == 功能开关['bossColor']:
                Toast('暴走史莱姆 - 战斗中 - 无需走位')
            else:
                功能开关['bossLastColor'] = 功能开关['bossColor']
                if 功能开关['bossColor'] == '木':
                    Toast('前往-草')
                    草()
                    sleep(1)
                if 功能开关['bossColor'] == '蒸汽':
                    Toast('前往-火')
                    火()
                    sleep(1)
                if 功能开关['bossColor'] == '篝火':
                    Toast('前往-草')
                    草()
                    sleep(1)
                if 功能开关['bossColor'] == '水':
                    Toast('前往-水')
                    水()
                    sleep(1)
                if 功能开关['bossColor'] == '火':
                    Toast('前往-火')
                    火()
                    sleep(1)
                if 功能开关['bossColor'] == '开花':
                    Toast('前往-草')
                    草()
                    sleep(1)

    # 大暴走（烈焰大王）
    def daBaoZouLieYan(self):
        for i in range(3):
            def 往左():
                tapSleep(63, 680, 4)

            def 往右():
                tapSleep(148, 675, 4)

            sleep(0.5)
            # print(任务记录['玩家-当前职业'])
            # print(功能开关['暴走职能优先治疗'])
            if 任务记录['玩家-当前职业'] == '服事' and 功能开关['暴走职能优先治疗'] == 1:
                notGreen = 0
                re1 = False
                re2 = False
                for k in range(5):
                    re1 = FindColors.find("141,646,#79DC1A|141,643,#63D110|141,638,#45BF04|145,642,#55C90E",
                                          rect=[61, 520, 341, 729], diff=0.95)
                    if not re1:
                        re1 = FindColors.find("453,805,#4FCDCB|457,801,#45C9CA|461,797,#45C9CC",
                                              rect=[47, 711, 623, 860], diff=0.95)
                    if not re1:
                        re1 = FindColors.find("140,640,#7DC51C|145,626,#639C13|140,631,#8DCC2A",
                                              rect=[30, 511, 309, 667], diff=0.95)
                    if not re1:
                        re1 = FindColors.find("185,689,#85CE2E|188,689,#89D22E|188,686,#7DC52D",
                                              rect=[25, 509, 262, 714], diff=0.92)
                    if not re1:
                        re1 = FindColors.find("192,694,#77D8DD|192,691,#7BD1D9|194,691,#7ED4DA",
                                              rect=[37, 703, 631, 888], diff=0.95)
                    re2 = FindColors.find("132,653,#B0D0D7|132,648,#ACC1CC|134,645,#B7BBC6", rect=[30, 511, 309, 667],
                                          diff=0.95)
                    if not re2:
                        FindColors.find(
                            "510,785,#FD6025|505,778,#FD5926|514,778,#FD5927|519,774,#FE794F|521,773,#FE5C2E",
                            rect=[47, 711, 623, 860], diff=0.95)
                    if not re2:
                        re2 = FindColors.find("558,768,#F65A1E|555,771,#FA6626|558,762,#F95621|553,762,#F56623",
                                              rect=[33, 705, 631, 879])
                    if not re2:
                        re2 = FindColors.find("192,694,#77D8DD|192,691,#7BD1D9|194,691,#7ED4DA",
                                              rect=[35, 565, 273, 732], diff=0.95)
                    if not re2:
                        re2 = FindColors.find(
                            "532,754,#ECDCD1|533,759,#EBD8CD|535,760,#EBD8CD|521,768,#FC5E39|532,767,#F85837",
                            rect=[37, 703, 631, 888], diff=0.95)
                    if re1 or re2:
                        notGreen = notGreen + 1
                    sleep(0.2)
                if notGreen > 3:
                    Toast('服事-战斗中-准备走位草')
                    re = CompareColors.compare("75,673,#384558|77,669,#384558|80,675,#384558")
                    if re:
                        Toast('服事-战斗中-自动走位草')
                        if re1:
                            tapSleep(72, 677)
                        elif re2:
                            tapSleep(143, 672)
                        sleep(2)
                continue

            if 功能开关['bossNumber0'] == '' and 功能开关['bossNumber1'] == '' and 功能开关['bossNumber2'] == '':
                notBlue = 0
                re1 = False
                re2 = False
                for k in range(5):
                    re1 = FindColors.find("195,670,#9ABCC8|199,664,#8BAFBD|199,670,#9AC7D0", rect=[61, 528, 295, 713],
                                          diff=0.97)
                    if not re1:
                        re1 = FindColors.find("189,605,#939FAF|185,605,#939AA8|182,610,#A6B0B9|188,616,#A2C0C7",
                                              rect=[52, 546, 243, 648], diff=0.97)
                    if not re1:
                        re1 = FindColors.find("541,784,#FD5E35|543,774,#F84C31|546,763,#F44C32",
                                              rect=[108, 705, 628, 858], diff=0.97)
                    if not re1:
                        re1 = FindColors.find("196,675,#85C9D2|196,677,#8CCFD6|194,670,#74B6C5",
                                              rect=[20, 501, 306, 705], diff=0.95)
                    if not re1:
                        re1 = FindColors.find("189,684,#39A0B5|189,682,#3499AF|190,686,#3CA7BA",
                                              rect=[90, 574, 240, 760])
                    re2 = FindColors.find("570,645,#7ECCD3|571,639,#61B0C2|573,634,#529EB2",
                                          rect=[390, 552, 641, 711], diff=0.97)
                    if not re2:
                        re2 = FindColors.find("562,630,#4CB8CD|562,634,#68C7D3|565,628,#56BFCE",
                                              rect=[440, 544, 642, 694], diff=0.97)
                    if not re2:
                        re2 = FindColors.find("511,785,#8BDA31|514,778,#70C528|523,778,#7ED02A|528,773,#70C627",
                                              rect=[108, 705, 628, 858], diff=0.97)
                    if not re2:
                        re2 = FindColors.find("533,781,#72C923|534,776,#5EB71F|538,765,#47941E",
                                              rect=[60, 710, 639, 902], diff=0.95)
                    if re1 or re2:
                        notBlue = notBlue + 1
                    sleep(0.2)
                if notBlue > 3:
                    # re = CompareColors.compare("75,673,#384558|77,669,#384558|80,675,#384558")
                    # if re:
                    战斗胜利 = CompareColors.compare("221,464,#F4D58C|322,476,#F6CD7D")
                    if not 战斗胜利:
                        Toast('复位蓝色')
                        if re1:
                            tapSleep(72, 677)
                        elif re2:
                            tapSleep(143, 672)
                        sleep(2)

            if 功能开关['bossNumber1'] != '' and 功能开关['bossNumber2'] != '':
                if 功能开关['bossLastNumber1'] != '' and 功能开关['bossLastNumber2'] != '' and (
                        功能开关['bossLastNumber1'] == 功能开关['bossNumber1'] and 功能开关['bossNumber2'] == 功能开关[
                    'bossLastNumber2']):
                    Toast('战斗中')
                else:
                    功能开关['bossLastNumber1'] = 功能开关['bossNumber1']
                    功能开关['bossLastNumber2'] = 功能开关['bossNumber2']
                    if 功能开关['bossNumber1'] != '' and 功能开关['bossNumber2'] != '' and 功能开关['bossNumber1'] > \
                            功能开关['bossNumber2']:
                        diffNum = 功能开关['bossNumber1'] - 功能开关['bossNumber2']
                        if diffNum in [1, 4, 7]:
                            Toast('往左一格')
                            往左()
                        if diffNum in [2, 5, 8]:
                            Toast('往右一格')
                            往右()
                        if diffNum in [0, 3, 6, 9]:
                            Toast('原地不动')

                    if 功能开关['bossNumber1'] != '' and 功能开关['bossNumber2'] != '' and 功能开关['bossNumber1'] < \
                            功能开关['bossNumber2']:
                        diffNum = 功能开关['bossNumber2'] - 功能开关['bossNumber1']
                        if diffNum in [1, 4, 7]:
                            Toast('往右一格')
                            往右()
                        if diffNum in [2, 5, 8]:
                            Toast('往左一格')
                            往左()
                        if diffNum in [0, 3, 6, 9]:
                            Toast('原地不动')

            if 功能开关['bossColor'] == "橙":
                if 功能开关['bossNumber0'] != 0:
                    if 功能开关['bossLastColor'] != '' and 功能开关['bossLastNumber0'] != '' and (
                            功能开关['bossLastColor'] == 功能开关['bossColor'] and 功能开关['bossLastNumber0'] ==
                            功能开关['bossNumber0']):
                        Toast('战斗中')
                    else:
                        功能开关['bossLastColor'] = 功能开关['bossColor']
                        功能开关['bossLastNumber0'] = 功能开关['bossNumber0']
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [1, 4, 7]:
                            Toast('往左一格')
                            往左()
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [2, 5, 8]:
                            Toast('往右一格')
                            往右()
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [3, 6, 9]:
                            Toast('原地不动')

            if 功能开关['bossColor'] == "紫":
                if 功能开关['bossNumber0'] != 0:
                    if 功能开关['bossLastColor'] != '' and 功能开关['bossLastNumber0'] != '' and 功能开关[
                        'bossLastColor'] == 功能开关['bossColor'] and 功能开关['bossLastNumber0'] == 功能开关[
                        'bossNumber0']:
                        Toast('战斗中')
                    else:
                        功能开关['bossLastColor'] = 功能开关['bossColor']
                        功能开关['bossLastNumber0'] = 功能开关['bossNumber0']
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [1, 4, 7]:
                            Toast('往右一格')
                            往右()
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [2, 5, 8]:
                            Toast('往左一格')
                            往左()
                        if 功能开关['bossNumber0'] != '' and 功能开关['bossNumber0'] in [0, 3, 6]:
                            Toast('原地不动')

    def teamShoutAI(self, content="", shoutType="fight"):
        # sleep(0.3)
        if 功能开关["队伍AI发言"] == 0:
            return

        # 使用正则表达式匹配
        matched_text = content
        match = re.search(r'<color=#[0-9a-fA-F]+>(.*?)</COLOR>', content)
        if match:
            matched_text = match.group(1)
        if matched_text in 任务记录['AI发言-上一次发言']:
            return
        res = self.teamShout(content, shoutType)
        if res:
            任务记录['AI发言-上一次发言'].append(matched_text)
        print(任务记录['AI发言-上一次发言'])
        sleep(0.5)

    def teamShout(self, content="", shoutType=""):
        if 功能开关['队伍喊话'] == "" and content == "":
            return 1

        point = FindColors.find(
            "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
            rect=[11, 26, 364, 489])
        if point:
            Toast('收起喊话窗口')
            tapSleep(point.x, point.y, 1)

        point = CompareColors.compare(
            "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)

        contentTemp = content

        # 指定喊话内容时，不记入倒计时
        if content == "":
            if 功能开关['队伍喊话'] != "":
                contentTemp = 功能开关['队伍喊话']

            need_dur_minute = safe_int(
                功能开关.get("队伍喊话间隔", 0).replace("分钟", "").replace("分", "").replace("秒", "").replace("s",
                                                                                                                ""))  # 分钟
            if need_dur_minute == '':
                need_dur_minute = 0
            if need_dur_minute > 0 and 任务记录["队伍喊话-倒计时"] > 0:
                diffTime = time.time() - 任务记录["队伍喊话-倒计时"]
                if diffTime < need_dur_minute * 60:
                    Toast(f'日常 - 队伍喊话 - 倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                    return

        # 判断已进入待准备页，提前返回
        res, _ = TomatoOcrText(451, 607, 505, 631, '准备')
        if res:
            return

        Toast("队伍发言")
        # print('10-'+contentTemp)

        # 关闭喊话窗口
        for i in range(2):
            point = FindColors.find(
                "104,334,#F6EFDE|104,344,#6383B6|99,331,#6584B9|112,336,#6685BA|107,345,#F2ECDF|112,351,#6584B9|94,355,#6688BA",
                rect=[56, 299, 281, 601])
            if point:
                Toast('收起喊话窗口')
                tapSleep(point.x, point.y)

        res1 = False
        res2 = False
        res3 = False
        res4 = False
        success = 0
        任务记录['喊话-并发锁'] = 1

        # 判断是否战斗中
        if shoutType == "fight":
            res, _ = TomatoOcrText(644, 785, 688, 806, '喊话')  # 战斗内喊话
            if not res:
                res, _ = TomatoOcrText(651, 321, 693, 341, '队伍')  # 战斗内喊话
                if not res:
                    Toast('战斗内喊话 - 不在战斗中')
                    任务记录['喊话-并发锁'] = 0
                    return 1

        if shoutType == "room":
            res4, _ = TomatoOcrText(311, 967, 407, 1002, '开始匹配')  # 房间内喊话
            if not res4:
                res4, _ = TomatoOcrText(290, 972, 431, 1006, '等待队长开始')  # 房间内喊话
            if not res4:
                res4, _ = TomatoOcrText(290, 972, 431, 1006, '等待队长开启')  # 房间内喊话
            if res4:
                tapSleep(219, 986, 0.8)
        else:
            res1 = TomatoOcrTap(19, 1102, 90, 1127, "点击", 10, 10, sleep1=0.6, match_mode='fuzzy')
            # if not res1:
            #     res2 = TomatoOcrTap(19, 1104, 94, 1128, "点击输入", 10, 10, sleep1=0.6, match_mode='fuzzy')
            #     if not res2:
            #         res3 = TomatoOcrTap(25, 1096, 104, 1133, "点击输入", 10, 10, sleep1=0.6, match_mode='fuzzy')

        # if not res1 and not res2 and not res3 and not res4:
        #     tapSleep(74, 1120)
        #     res1 = True
        # sleep(1.5)  # 等待输入法弹窗
        if res1 or res2 or res3 or res4:
            contents = contentTemp.split('|')
            for tmpContent in contents:
                res2 = TomatoOcrTap(19, 1102, 90, 1127, "点击", 10, 10, sleep1=0.6, match_mode='fuzzy')

                # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
                sleep(0.2)
                # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                # if content != "":
                #     AI 喊话发送彩色字符
                # colors = generate_random_color()
                # tmpContent = f"<color={colors}>{tmpContent}</COLOR>"
                action.input(tmpContent)
                tapSleep(360, 104, 0.3)  # 点击空白处确认输入
                for i in range(3):
                    # 检查是否已输入
                    notInput = TomatoOcrTap(78, 1155, 156, 1191, "点击", 5, 5, match_mode='fuzzy')
                    # if not notInput:
                    #     notInput = TomatoOcrTap(79, 1157, 118, 1190, "点击", 5, 5)
                    if notInput:
                        action.input(tmpContent)
                        tapSleep(360, 104, 0.2)  # 点击空白处确认输入
                    else:
                        break

                res = TomatoOcrTap(555, 1156, 603, 1188, "发送", offsetX=52)
                if not res:
                    sleep(0.3)
                    res = TomatoOcrTap(555, 1156, 603, 1188, "发送", offsetX=52)
                if res:
                    res = TomatoOcrTap(555, 1156, 603, 1188, "发送", offsetX=52)
                    if res:
                        sleep(0.5)
                        res = TomatoOcrTap(555, 1156, 603, 1188, "发送", offsetX=52)
                # # 关闭喊话窗口
                # point = FindColors.find(
                #     "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                #     rect=[11, 26, 364, 489])
                # if point:
                #     tapSleep(point.x, point.y, 1)
                #
                # # 关闭喊话窗口
                # point = CompareColors.compare(
                #     "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
                # if point:
                #     Toast('收起喊话窗口')
                #     tapSleep(107, 93)
                # # 关闭喊话窗口
                # point = FindColors.find(
                #     "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                #     rect=[11, 26, 364, 489])
                # if point:
                #     Toast('收起喊话窗口')
                #     tapSleep(point.x, point.y, 1)
                if content == "":
                    任务记录["队伍喊话-倒计时"] = time.time()
                success = 1

                # 关闭喊话窗口
                for i in range(2):
                    point = FindColors.find(
                        "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                        rect=[11, 26, 364, 489])
                    if point:
                        Toast('收起喊话窗口')
                        tapSleep(point.x, point.y)

                    point = CompareColors.compare(
                        "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
                    if point:
                        Toast('收起喊话窗口')
                        tapSleep(107, 93)

        任务记录['喊话-并发锁'] = 0
        return success

    # 战斗中退出组队
    def quitTeamFighting(self):
        功能开关["fighting"] = 1
        任务记录["喊话-并发锁"] = 1  # 中断只能施法
        hasQuit = False
        self.closeLiaoTian()
        for i in range(4):
            # sleep(0.5)
            self.fight_fail_alert()
            # res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            res = TomatoOcrTap(649, 319, 694, 342, "队伍", sleep1=0.8)
            # if res:
            #     res = TomatoOcrTap(501, 191, 581, 217, "离开队伍", sleep1=0.8)
            #     res = TomatoOcrTap(329, 726, 391, 761, "确定", sleep1=0.8)
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍", sleep1=0.8)
            res = TomatoOcrTap(329, 726, 391, 761, "确定", sleep1=0.8)
            if res:
                hasQuit = True
            if i > 2 and hasQuit:
                break
        quitRes = self.quitTeam()
        # sleep(0.5)
        功能开关["fighting"] = 0
        任务记录["喊话-并发锁"] = 0

    def fight_fail_alert(self):
        res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认战败
        res = TomatoOcrTap(588, 637, 630, 661, "同意")  # 点击同意重新开始
        res = TomatoOcrTap(453, 961, 549, 989, "再次挑战")  # 点击同意再次挑战

    def fight_fail(self):
        res1, _ = TomatoOcrText(459, 853, 546, 881, "你被击败了")
        res2, _ = TomatoOcrText(475, 1038, 527, 1065, "放弃")
        res3, _ = TomatoOcrText(459, 853, 546, 881, "发起重开")
        res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
        teamName2 = ""
        if teamName1 == "":
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
        if res1 or res2 or res3 or (
                "等级" not in teamName1 and "等级" not in teamName2 and "Lv" not in teamName1 and "Lv" not in teamName2):  # 战败提示 or 队友全部离队
            # Toast("战斗结束 - 战斗失败")
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            self.quitTeamFighting()  # 退出队伍
            return True
        return False

    def homePage(self):
        tryTimes = 0
        while True:
            tryTimes = tryTimes + 1
            if tryTimes < 10:
                res, _ = TomatoOcrText(649, 321, 694, 343, '队伍')
                if res:
                    Toast(f'返回首页-等待战斗结束{tryTimes * 5}/50')
                    sleep(5)
                    continue

            # resConnErr, _ = TomatoOcrText(292, 691, 427, 722, "尝试重新连接")
            # if resConnErr:
            #     Toast('网络断开，尝试重启游戏')
            #     # 结束应用
            #     r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
            #     # 重启游戏
            #     return self.startupTask.start_app()

            if tryTimes > 5:
                system.open(f"{功能开关['游戏包名']}")
                # 暂不处理战败页启动，提高执行效率
                # 判断战败页面
                if 功能开关["fighting"] == 0:
                    self.allQuit()
                    self.fight_fail()
                    self.quitTeamFighting()
                    self.quitTeam()

            if tryTimes > 18:
                Toast(f'尝试返回游戏,{tryTimes}/20')
                system.open(f"{功能开关['游戏包名']}")

            if tryTimes > 20:
                res1, _ = TomatoOcrText(311, 588, 408, 637, "异地登录")
                if (res1 and 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0"):
                    return

                Toast('尝试重启游戏')
                # 结束应用
                # r = system.shell("am kill com.xd.cfbmf", L())
                r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
                # 重启游戏
                return self.startupTask.start_app()
            if tryTimes > 23:
                return

            # 点击首页-冒险
            re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')

            # 判断是否已在首页
            # 判断底部冒险图标
            res2 = FindColors.find(
                "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
                rect=[301, 1130, 421, 1273])
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                if not shou_ye1:
                    shou_ye2, _ = TomatoOcrText(545, 381, 628, 404, "新手试炼")
                    if not shou_ye2:
                        shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
            if res2 or shou_ye1 or shou_ye2:
                # 关闭喊话窗口
                point = FindColors.find(
                    "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                    rect=[11, 26, 364, 489])
                if point:
                    Toast('关闭喊话窗口')
                    tapSleep(point.x, point.y, 1)
                功能开关["needHome"] = 0
                Toast('已返回首页')
                return True
            # 重启游戏
            # self.startupTask.start_app()
            功能开关["needHome"] = 1
            sleep(0.5)

    def quitTeam(self):
        res5 = False
        功能开关["needHome"] = 0
        功能开关["fighting"] = 1
        功能开关["noHomeMust"] = 1

        # 返回房间 - 队伍满员，开始挑战提醒
        # wait1, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        # wait2 = False
        # if not wait1:
        #     wait2, _ = TomatoOcrText(240, 610, 344, 653, "队伍已满员")  # 队伍已满员，准备开启挑战
        # if wait1 or wait2:
        res5 = TomatoOcrTap(453, 727, 511, 760, "确定", 10, 10)  # 队伍已满员，准备开启挑战 - 确定

        res1 = False
        res2 = False
        res3 = False
        res4 = False

        res6 = TomatoOcrTap(500, 184, 579, 214, "离开队伍", 20, 20)  # 已在队伍页面，直接退出
        if not res6:
            # 匹配组队中灰色底UI
            # tmp = FindColors.find(
            #     "569,561,#354E67|572,560,#777D85|574,560,#767B81|578,561,#2E4964|583,562,#3C5067|597,575,#8C9093|549,580,#818792",
            #     rect=[533, 490, 704, 681], diff=0.8)
            # if not tmp:
            #     功能开关["noHomeMust"] = 0
            #     return False

            res1 = TomatoOcrTap(651, 559, 682, 577, "组队")
            if not res1:
                res2 = TomatoOcrFindRangeClick(
                    keywords=[{'keyword': '正', 'match_mode': 'fuzzy'},
                              {'keyword': '组', 'match_mode': 'fuzzy'}, {'keyword': '队', 'match_mode': 'fuzzy'},
                              {'keyword': '匹', 'match_mode': 'fuzzy'}], whiteList='正在组队', x1=544, y1=528, x2=699,
                    y2=672, sleep1=2,
                    match_mode='fuzzy')
                # if not res2:
                #     res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中", offsetX=10, offsetY=20)
                #     if not res3:
                #         res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中", offsetX=10, offsetY=20)  # 大暴走匹配中
        if res1 or res2 or res3 or res4 or res5 or res6:
            功能开关["needHome"] = 0
            功能开关["fighting"] = 1
            # sleep(0.5)

            teamExitTap = False
            if not res1 and not res2:
                teamExitTap = TomatoOcrTap(337, 730, 382, 759, "确定", offsetX=10, offsetY=20)
                if not teamExitTap:
                    teamExitTap = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=105, y1=304, x2=631, y2=953)
            if not teamExitTap:
                teamExist = TomatoOcrFindRangeClick('离开队伍', whiteList='离开队伍', x1=416, y1=126, x2=628,
                                                    y2=284)
                if teamExist:
                    teamExitTap = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=105, y1=304, x2=631, y2=953)

            if teamExitTap:
                Toast('试炼-退出组队')
                sleep(0.3)
                TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
                return3 = TomatoOcrTap(76, 1161, 126, 1190, '返回', 10, 10)
                功能开关["fighting"] = 0
                功能开关["noHomeMust"] = 0
                return True

            teamStatus = TomatoOcrFindRangeClick(
                keywords=[{'keyword': '匹配中', 'match_mode': 'fuzzy'}, {'keyword': '中', 'match_mode': 'fuzzy'}],
                x1=91, y1=402, x2=573, y2=1207)
            if teamStatus:
                Toast('取消匹配')
            # res = TomatoOcrTap(501, 191, 581, 217, "离开队伍")
            # if not res:
            #     tapSleep(540, 200, 0.8)
            # res = TomatoOcrTap(329, 726, 391, 761, "确定")
            # if not res:
            #     tapSleep(360, 740, 0.8)
            # if res:
            #     Toast("退出组队")
            #     sleep(0.3)
            #     TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
            #     功能开关["fighting"] = 0
            #     return True
        功能开关["fighting"] = 0
        功能开关["noHomeMust"] = 0
        return False

    def closeLiaoTian(self):
        point = FindColors.find(
            "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
            rect=[61, 34, 322, 623], diff=0.95)
        if point:
            Toast('收起喊话窗口')
            tapSleep(point.x, point.y)

        point = CompareColors.compare(
            "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)

    def AIContent(self):
        try:
            if 功能开关["队伍AI发言"] == 0:
                return

            res, _ = TomatoOcrText(644, 785, 688, 806, '喊话')  # 战斗内喊话
            if not res:
                Toast('战斗内喊话 - 不在战斗中')
                任务记录['喊话-并发锁'] = 0
                return

            # 检测队友是否已关注
            if 任务记录['AI发言-检测队友关注'] == 0:
                content = ""
                任务记录['AI发言-检测队友关注'] = 1
                tapSleep(30, 134, 0.8)  # 点击队友1
                re, _ = TomatoOcrText(536, 1060, 595, 1090, '养成')
                if re:
                    re, _ = TomatoOcrText(293, 988, 336, 1011, '回关')
                    if not re:
                        colors = generate_random_color()
                        content += f"<color={colors}>您还没有关注我喔,麻烦给个关注吧~</COLOR>"

                if content == "":
                    re, teamName = TomatoOcrText(125, 822, 313, 856, '队友名称')
                    if teamName != "":
                        tapSleep(448, 1076, 0.2)  # 点击属性页
                        # tapSleep(448, 1076, 0.1)  # 点击属性页
                        re, teamFightText = TomatoOcrText(159, 596, 261, 629, '队友战力')
                        # 检查是否包含“万”
                        # print(teamFightText)
                        teamFightNum = 0
                        teamFightNum = safe_float_v2(
                            teamFightText.replace("万", "").replace("厰", "").replace("廠", "").replace("個",
                                                                                                        "").replace(
                                "麺", "").replace("時", "").replace("闇", "").replace("間", "")) * 10000
                        # print(teamFightNum)
                        print(任务记录['战斗-房主战力'])
                        tapSleep(96, 1235, 0.1)  # 返回
                        tapSleep(96, 1235, 0.1)  # 返回
                        任务记录['战斗-房主战力'] = safe_int_v2(任务记录['战斗-房主战力'])
                        if 任务记录['战斗-房主战力'] != 0 and teamFightNum != 0:
                            teamFightNumDiff = round(abs(teamFightNum - 任务记录['战斗-房主战力']) / 10000, 1)
                            diffHour = round((time.time() - 任务记录['战斗-房主上次相遇']) / 3600, 1)
                            if teamFightNumDiff != 0:
                                content += f"相遇已{diffHour}h,您的战力提升{teamFightNumDiff}w.恭喜!"
                        if teamFightNum != 0:
                            p = threading.Thread(target=self.daiDuiZhanLi, args=(teamName, teamFightNum))
                            p.start()
                if content != "":
                    self.teamShoutAI(content)

            re, teamText1 = TomatoOcrText(62, 1023, 251, 1052, "队友发言")
            re, teamText2 = TomatoOcrText(58, 1049, 244, 1079, "队友发言")
            re, teamText3 = TomatoOcrText(63, 965, 252, 994, "队友发言")
            if 任务记录["AI发言-广告开关"] == 1:
                wenList = ['脚本', '科技', '狠活', '高级', '群', '挂', '智能', 'ai', 'AI', '啥', '什么', '托管', '人机',
                           '机器', '功能']
                contains_zan1 = any(zan in teamText1 for zan in wenList)
                contains_zan2 = any(zan in teamText2 for zan in wenList)
                contains_zan3 = any(zan in teamText3 for zan in wenList)
                if contains_zan1 or contains_zan2 or contains_zan3:
                    # 回复夸赞
                    colors = generate_random_color()
                    tmpContent = f"<color={colors}>自动回复~欢迎加鹅来玩喔~372~270~534</COLOR>"
                    self.teamShoutAI(tmpContent)
                    # self.teamShoutAI("全自动日常、一键刷赞、AI带队、智能走位施法、摸鱼种菜，欢迎来鹅了解~372~270~534")

            zanList = ['棒', '厉害', '谢', '哇', '牛', '6', '已关注', '佬', '专业']
            contains_zan1 = any(zan in teamText1 for zan in zanList)
            contains_zan2 = any(zan in teamText2 for zan in zanList)
            contains_zan3 = any(zan in teamText3 for zan in zanList)
            if contains_zan1 or contains_zan2 or contains_zan3:
                # 回复夸赞
                colors = generate_random_color()
                tmpContent = f"<color={colors}>自动回复~蟹蟹</COLOR>"
                self.teamShoutAI(tmpContent)

            otherList = ['再', '把', '带']
            contains_zan1 = any(zan in teamText1 for zan in otherList)
            contains_zan2 = any(zan in teamText2 for zan in otherList)
            contains_zan3 = any(zan in teamText3 for zan in otherList)
            if contains_zan1 or contains_zan2 or contains_zan3:
                # 回复夸赞
                colors = generate_random_color()
                tmpContent = f"<color={colors}>自动回复~当然可以 我会一直等你~</COLOR>"
                self.teamShoutAI(tmpContent)

            blackList = ['*']
            contains_zan1 = any(zan in teamText1 for zan in blackList)
            contains_zan2 = any(zan in teamText2 for zan in blackList)
            contains_zan3 = any(zan in teamText3 for zan in blackList)
            if contains_zan1 or contains_zan2 or contains_zan3:
                # 回复夸赞
                self.teamShoutAI("自动回复~请文明发言哟")

            moveList = ['动', '左', '右']
            contains_zan1 = any(zan in teamText1 for zan in moveList)
            contains_zan2 = any(zan in teamText2 for zan in moveList)
            contains_zan3 = any(zan in teamText3 for zan in moveList)
            if contains_zan1 or contains_zan2 or contains_zan3:
                # 移动走位
                imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                任务记录['战斗-上一次移动'] = time.time()

            # 判断战力差距，提醒队友

            # 识别当前地图，提醒队友攻略
            # 秘境
            if "无法无" in 任务记录["战斗-关卡名称"]:  # 无法无天章鱼帮
                self.teamShoutAI("提示:boss大招后，集火攻击一只鹦鹉喔！")
            elif "云涌风" in 任务记录["战斗-关卡名称"]:  # 云涌风雷王座
                self.teamShoutAI("提示:一阶段上风加攻、二阶段远离上风！大招时分别站两个区域、大招后正负极在一起！")
            elif "骑士游" in 任务记录["战斗-关卡名称"]:  # 骑士游猎场
                self.teamShoutAI("提示:boss四周护盾会降伤，大招后暂时消散，坦克可往左跑两格引开boss，其他人不动~")
            elif "傲慢者" in 任务记录["战斗-关卡名称"]:  # 傲慢者赫朗格尼
                self.teamShoutAI("提示:boss大招时请前往坦克位置协助击破或屏障~")
            elif "薄纱笑" in 任务记录["战斗-关卡名称"]:  # 薄纱笑靥舞
                self.teamShoutAI("提示:月球掉落时需要至少1人接到伤害~")
            elif "世界万" in 任务记录["战斗-关卡名称"]:  # 世界万象其中
                self.teamShoutAI("提示:光阶段走位暗、暗阶段走位光~大招期间掉落光球需要走位躲避或使用光明屏障")
            elif "巨像思维首脑" in 任务记录["战斗-关卡名称"]:  # 巨像思维首脑
                self.teamShoutAI("提示:boss召唤模块后需集火清理模块~")
            elif "决战黄" in 任务记录["战斗-关卡名称"]:  # 决战黄金穹顶
                self.teamShoutAI("提示:坦克请远离人群避免飞弹波及，可各自站一格~")
            elif "金色歌" in 任务记录["战斗-关卡名称"]:  # 金色歌剧院
                self.teamShoutAI("提示:boss大招后，集火机器人喔~")

            # 绝境
            if "下锚白帆" in 任务记录["战斗-关卡名称"]:  # 绝境26：下锚白帆登陆战
                self.teamShoutAI("提示:boss大招后，集火攻击一只鹦鹉喔！")
            elif "雷神之锤" in 任务记录["战斗-关卡名称"]:  # 绝境25：雷神之锤抢夺战
                self.teamShoutAI("提示:一阶段上风加攻、二阶段远离上风！大招时分别站两个区域、大招后正负极在一起！")
            elif "空心骑士" in 任务记录["战斗-关卡名称"]:  # 绝境24：空心骑士追猎战
                self.teamShoutAI("提示:boss四周护盾会降伤，大招后暂时消散，坦克可往左跑两格引开boss，其他人不动~")
            elif "夜蝶" in 任务记录["战斗-关卡名称"]:  # 绝境23：夜蝶遗迹破关战
                self.teamShoutAI("提示:boss大招时请前往坦克位置协助击破或屏障~")
            elif "控制中" in 任务记录["战斗-关卡名称"]:  # 绝境22：控制中枢搜寻战
                self.teamShoutAI("提示:boss召唤模块后需集火清理模块~")
            elif "黄金穹顶击破战" in 任务记录["战斗-关卡名称"]:  # 绝境21：黄金穹顶击破战
                self.teamShoutAI("提示:坦克请远离人群避免飞弹波及，可各自站一格~")
            elif "血色剧院" in 任务记录["战斗-关卡名称"]:  # 绝境20：血色剧院安可战
                self.teamShoutAI("提示:留存两个喇叭，可在谢幕阶段提供减伤")
            elif "无夜底" in 任务记录["战斗-关卡名称"]:  # 绝境19：无夜底层灭鼠战
                self.teamShoutAI("提示:注意躲避红圈~")
            elif "下城" in 任务记录["战斗-关卡名称"]:  # 绝境18：下城械斗平定战
                self.teamShoutAI("提示:boss和小怪需在12s内同时击杀~")

            # 判断当前时间，回复吉祥话
            from datetime import datetime
            now = datetime.now()
            hour = now.hour
            # 根据时间段选择吉祥话
            # import requests
            colors = generate_random_color()
            if 5 <= hour < 12:
                tmpContent = f"<color={colors}>早安，愿你今天也元气满满！</COLOR>"
                self.teamShoutAI(tmpContent)
            elif 12 <= hour < 18:
                tmpContent = f"<color={colors}>午安，愿你此间战无不胜！</COLOR>"
                self.teamShoutAI(tmpContent)
            elif 18 <= hour < 22:
                tmpContent = f"<color={colors}>晚好，愿你度过愉快的夜晚！</COLOR>"
                self.teamShoutAI(tmpContent)
            else:
                # r = requests.get("https://api.kuleu.com/api/getGreetingMessage?type=json")
                # # 打印状态Code
                # # 进行转码
                # r.encoding = r.apparent_encoding
                # # 转换为json对象
                # obj = r.json()
                # print(obj['code'])
                # if obj != "" and obj['code'] == 200:
                #     greet = obj['data']['greeting']
                #     tip = obj['data']['tip']
                #     self.teamShoutAI(f"{greet}~{tip}")
                tmpContent = f"<color={colors}>夜深了，愿你今晚好梦！</COLOR>"
                self.teamShoutAI(tmpContent)
        except Exception as e:
            # 处理异常
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 输出异常信息和行号
            file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
            error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
            # 显示对话框
            Dialog.confirm(error_message)

    # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)；离队
    def allQuit(self, needCheck=False):
        res1, _ = TomatoOcrText(246, 459, 327, 482, "你被击败了")
        res2, _ = TomatoOcrText(475, 1038, 527, 1065, "放弃")
        res3, _ = TomatoOcrText(451, 959, 551, 989, "再次挑战")
        res4, _ = TomatoOcrText(459, 853, 546, 881, "发起重开")
        if res1 or res2 or res3 or res4 or needCheck:
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            colors = generate_random_color()
            tmpContent = f"<color={colors}>战斗失败QAQ~期待下次相遇~</COLOR>"
            self.teamShoutAI(tmpContent, shoutType="fight")
            # tmpContent = f"<color={colors}>大家加油~~</COLOR>"
            # self.teamShoutAI(tmpContent, shoutType="fight")
            # self.teamShoutAI(f'可以提醒我进行移动哟~', shoutType="fight")
            sleep(0.5)
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            tapSleep(30, 134, 1.3)  # 点击队友1
            re, teamInfo1 = TomatoOcrText(532, 1060, 596, 1089, '养成')
            TomatoOcrTap(72, 1202, 121, 1231, '返回')
            if teamInfo1 == "":
                sleep(0.5)
                tapSleep(25, 186, 1.3)  # 点击队友2
                re, teamInfo1 = TomatoOcrText(532, 1060, 596, 1089, '养成')
                TomatoOcrTap(72, 1202, 121, 1231, '返回')
                if teamInfo1 == "":
                    # 队友为人机，退出
                    Toast("剩余队友全为人机，退出战斗")
                    res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
                    self.quitTeamFighting()  # 退出队伍
                    return True
        return False

    # 自动锁敌、自动走位
    def autoMove(self):
        # 识别当前职业
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                任务记录['玩家-当前职业'] = '战士'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-服事')
                任务记录['玩家-当前职业'] = '服事'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                任务记录['玩家-当前职业'] = '刺客'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                任务记录['玩家-当前职业'] = '法师'
        if 任务记录['玩家-当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                任务记录['玩家-当前职业'] = '游侠'

        if 功能开关['队伍AI锁敌']:
            # 切换攻击目标
            point = FindColors.find("135,252,#7CA2E2|153,238,#7DA1E2|170,255,#85A7E1|164,265,#7DA1E2|150,271,#94B1E5",
                                    rect=[1, 175, 697, 836], diff=0.95)
            if point:
                Toast('切换攻击目标')
                print(point.x, point.y)
                tapSleep(point.x, point.y)

        if 功能开关['队伍AI走位']:
            # 移动走位
            # 部分地图根据机制走位
            if 任务记录['玩家-当前职业'] == '战士':
                if "云涌风雷王座" in 任务记录['玩家-当前关卡'] or "雷神之锤" in 任务记录['玩家-当前关卡']:
                    # 不走位，避免移动引雷
                    Toast('停止移动，避免引雷')
                    return

            # 恶龙红圈
            re = FindColors.find("211,1018,#EA1F1B|214,1025,#EA3020|215,1020,#E71919|210,1020,#EA281D",
                                 rect=[118, 894, 503, 1052], diff=0.9)
            if re:
                re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                if re:
                    Toast('boss技能，自动走位')

            if time.time() - 任务记录['战斗-上一次移动'] > 7:
                re = imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                if re:
                    Toast('自动走位')
                任务记录['战斗-上一次移动'] = time.time()

    # 带队队友战力计算
    def daiDuiZhanLi(self, teamName, teamFightNum):
        if teamFightNum == 0 or teamName == "":
            return
        db = pymysql.connect(
            host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
            port=3307,  # 开发者后台,创建的数据库 “端口”
            user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
            password='233233',  # 开发者后台,创建的数据库 “初始密码”
            database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
            charset='utf8mb4'  ""
        )  # 连接数据库
        cursor = db.cursor()

        # 插入
        # 构造 SQL 语句
        sql = "UPDATE daidui SET team_fight_num = %s WHERE user_name = %s and team_name = %s"
        # 使用参数化查询
        cursor.execute(sql, (teamFightNum, 任务记录["玩家名称"], teamName))
        db.commit()  # 不要忘了提交,不然数据上不去哦

        # 执行完之后要记得关闭游标和数据库连接
        cursor.close()
        # 执行完毕后记得关闭db,不然会并发连接失败哦
        db.close()

    def daiDuiCount(self, teamName='', needUpdate=True):
        db = pymysql.connect(
            host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
            port=3307,  # 开发者后台,创建的数据库 “端口”
            user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
            password='233233',  # 开发者后台,创建的数据库 “初始密码”
            database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
            charset='utf8mb4'  ""
        )  # 连接数据库

        count = 0
        last_time = 0
        team_fight_num = 0
        now_time = int(time.time())

        cursor = db.cursor()
        sql = "SELECT * FROM daidui WHERE user_name	 = %s and team_name	= %s"
        # 使用参数化查询
        if teamName == '':
            teamName = 任务记录["战斗-房主名称"]
        cursor.execute(sql, (任务记录['玩家名称'], teamName))
        results = cursor.fetchall()
        for row in results:
            count = row[2]
            last_time = row[3]
            team_fight_num = row[4]

        # 执行完之后要记得关闭游标和数据库连接
        cursor.close()
        # 执行完毕后记得关闭db,不然会并发连接失败哦
        db.close()

        if needUpdate:
            p = threading.Thread(target=self.daiDuiUpdate, args=(count, 任务记录["战斗-房主名称"], now_time))
            p.start()

        if count == 0:
            count = 1
        else:
            count = count + 1

        任务记录['带队次数'] = count
        任务记录['战斗-房主战力'] = team_fight_num
        任务记录['战斗-房主上次相遇'] = last_time
        return count, last_time

    def daiDuiUpdate(self, count, teamName, now_time):
        db = pymysql.connect(
            host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
            port=3307,  # 开发者后台,创建的数据库 “端口”
            user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
            password='233233',  # 开发者后台,创建的数据库 “初始密码”
            database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
            charset='utf8mb4'  ""
        )  # 连接数据库
        cursor = db.cursor()

        # 插入
        if count == 0:
            count = 1
            # 构造 SQL 语句
            sql = f"Insert into daidui (user_name,team_name,count,last_time) Values (%s,%s,%s,%s)"
            # 使用参数化查询
            cursor.execute(sql, (任务记录["玩家名称"], teamName, count, now_time))
            db.commit()  # 不要忘了提交,不然数据上不去哦
        else:
            count = count + 1
            # 构造 SQL 语句
            sql = "UPDATE daidui SET count = %s, last_time = %s WHERE user_name = %s and team_name = %s"
            # 使用参数化查询
            cursor.execute(sql, (count, now_time, 任务记录["玩家名称"], teamName))
            db.commit()  # 不要忘了提交,不然数据上不去哦

        # 执行完之后要记得关闭游标和数据库连接
        cursor.close()
        # 执行完毕后记得关闭db,不然会并发连接失败哦
        db.close()
