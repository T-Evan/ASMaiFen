# 导包
import math
from time import sleep

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .daily import DailyTask
from ascript.android.screen import Ocr
from .baseUtils import *
import re as repattern
from ascript.android.screen import FindColors


class LvRenTask:
    def __init__(self):
        self.dailyTask = DailyTask()

    def lvrenTask(self):
        if 功能开关["日常总开关"] == 0:
            return

        self.dailyTask.homePage(needQuitTeam=True)

        # 旅人相关
        # 自动转职
        self.updateLevel()

        # 自动更换装备
        self.changeEquip()

        # 自动使用经验补剂
        self.useLevelPotion()

        # 自动强化装备
        self.updateEquip()

        # 自动分解装备
        self.deleteEquip()

        # 自动升级技能
        self.updateSkill()

        # 自动升星秘宝
        self.updateMiBao()

        # 自动点亮天赋
        self.updateTianFu()

        # 稚星道途
        self.zhiXingDaoTu()

        # 猫猫包
        self.maomaobao()

    # 自动转职
    def updateLevel(self):
        if 功能开关["自动转职"] == 0:
            return

        if 任务记录['自动转职-完成']:
            return

        Toast('自动转职 - 开始')
        for p in range(5):
            self.dailyTask.homePage()
            re = CompareColors.compare(
                "353,1202,#FCF8EE|361,1202,#FCF8EE|353,1190,#9F7A53|364,1186,#A5855C|356,1182,#9F7D57")  # 匹配已回到首页
            if re:
                re, _ = TomatoOcrText(105, 116, 175, 134, '待转职')
                if not re:
                    Toast('自动转职 - 未开启转职')
                    任务记录['自动转职-完成'] = 1
                    return

            res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
            res = TomatoOcrFindRangeClick("转职任务", x1=448, y1=233, x2=560, y2=528, sleep1=0.8, offsetX=10,
                                          offsetY=-10)
            if not res:
                Toast('自动转职 - 未找到任务入口')
                return

            # 匹配可转职
            re = CompareColors.compare("306,1068,#F3A84B|311,1079,#F3A84B|408,1068,#F3A84B|405,1084,#F3A84B")
            if re:
                Toast('自动转职 - 开始转职')
                tapSleep(360, 1077, 0.8)  # 点击转职
                tapSleep(360, 1077, 0.8)  # 点击转职
                for t in range(10):
                    re = TomatoOcrTap(293, 1237, 421, 1257, '点击空白处关闭')
                    if re:
                        break
                    Toast('等待动画')
                    sleep(2)
                    tapSleep(358, 1266)  # 点击跳过
                任务记录['自动转职-完成'] = 1
                return

            tapSleep(558, 1212, 0.8)  # 点击英雄诗篇
            for k in range(8):
                Toast('跳过对话')
                tapSleep(347, 1256)  # 点击空白处

            for k in range(12):
                re = TomatoOcrFindRangeClick('领取', x1=465, y1=123, x2=623, y2=1096)
                if re:
                    Toast('领取任务')
                else:
                    re = FindColors.find("606,163,#B4835E|609,163,#B4835E|618,155,#F56042|617,152,#FF5C45", diff=0.95)
                    if re:
                        Toast('切换任务')
                        tapSleep(re.x, re.y)
                        swipe(415, 795, 352, 526)
                        sleep(1)
                tapSleep(347, 1256)  # 点击空白处

    # 稚星道途
    def zhiXingDaoTu(self):
        if 功能开关["稚星道途领取"] == 0 and 功能开关["稚星道途升级"] == 0:
            return

        if 任务记录['旅人-稚星道途-完成']:
            Toast('旅人 - 稚星道途 - 已完成')
            return

        Toast('旅人 - 星墟文物 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        res = TomatoOcrFindRangeClick("星墟文物", x1=448, y1=233, x2=560, y2=528, sleep1=2, offsetX=10,
                                      offsetY=-10)
        if not res:
            任务记录['旅人-稚星道途-完成'] = 1
            Toast('稚星道途 - 未找到任务入口')
        if res:
            tapSleep(273, 1115)  # 点击激活阶段
            re = TomatoOcrTap(554, 689, 636, 710, '充能任务', sleep1=0.8, offsetX=10, offsetY=-20)
            if re:
                Toast('旅人 - 星墟文物 - 领取激活任务')
                for i in range(5):
                    TomatoOcrTap(486, 299, 540, 329, '领取')
                    tapSleep(358, 1049)  # 点击空白处
                    tapSleep(358, 1049)  # 点击空白处
                tapSleep(323, 1199, 0.8)  # 点击空白处返回
                re = FindColors.find("497,765,#EF5C40|500,765,#F05E40|502,765,#EF5C40", rect=[86, 741, 623, 988],
                                     diff=0.9)  # 领取累积奖励
                if re:
                    Toast('旅人 - 星墟文物 - 领取累积奖励')
                    tapSleep(re.x - 20, re.y + 20)
                    tapSleep(323, 1199, 0.8)  # 点击空白处
                    tapSleep(323, 1199)  # 点击空白处

            re = CompareColors.compare("505,1104,#EF5D40|510,1103,#EF5C40")  # 充盈阶段红点
            if re:
                tapSleep(440, 1119)  # 点击充盈阶段
                re = TomatoOcrTap(554, 689, 636, 710, '充能任务', sleep1=0.8, offsetX=10, offsetY=-20)
                if re:
                    Toast('旅人 - 星墟文物 - 领取充盈任务')
                    for i in range(5):
                        TomatoOcrTap(486, 299, 540, 329, '领取')
                        tapSleep(358, 1049)  # 点击空白处
                        tapSleep(358, 1049)  # 点击空白处
                    tapSleep(323, 1199, 0.8)  # 点击空白处返回
                    re = FindColors.find("497,765,#EF5C40|500,765,#F05E40|502,765,#EF5C40", rect=[86, 741, 623, 988],
                                         diff=0.9)  # 领取累积奖励
                    if re:
                        Toast('旅人 - 星墟文物 - 领取累积奖励')
                        tapSleep(re.x - 20, re.y + 20)
                        tapSleep(323, 1199, 0.8)  # 点击空白处
                        tapSleep(323, 1199)  # 点击空白处

            for k in range(4):
                re = CompareColors.compare("606,1185,#EF5C40|603,1185,#F05D40")  # 文物库红点
                if re:
                    Toast('旅人 - 星墟文物 - 切换文物')
                    tapSleep(582, 1207, 1)  # 点击文物
                    tapSleep(281, 1119)
                    re = CompareColors.compare("498,763,#F45F42|500,765,#F05E40")  # 激活阶段红点
                    if re:
                        tapSleep(281, 1115)  # 点击激活阶段
                        re = TomatoOcrTap(554, 689, 636, 710, '充能任务', sleep1=0.8, offsetX=10, offsetY=-20)
                        if re:
                            Toast('旅人 - 星墟文物 - 领取激活任务')
                            for i in range(5):
                                TomatoOcrTap(486, 299, 540, 329, '领取')
                                tapSleep(358, 1049)  # 点击空白处
                                tapSleep(358, 1049)  # 点击空白处
                            tapSleep(323, 1199, 0.8)  # 点击空白处返回
                            re = FindColors.find("497,765,#EF5C40|500,765,#F05E40|502,765,#EF5C40",
                                                 rect=[86, 741, 623, 988], diff=0.9)  # 领取累积奖励
                            if re:
                                Toast('旅人 - 星墟文物 - 领取累积奖励')
                                tapSleep(re.x - 20, re.y + 20)
                                tapSleep(323, 1199, 0.8)  # 点击空白处
                                tapSleep(323, 1199)  # 点击空白处
                    re = CompareColors.compare("505,1104,#EF5D40|510,1103,#EF5C40")  # 充盈阶段红点
                    if re:
                        tapSleep(440, 1119)  # 点击充盈阶段
                        re = TomatoOcrTap(554, 689, 636, 710, '充能任务', sleep1=0.8, offsetX=10, offsetY=-20)
                        if re:
                            Toast('旅人 - 星墟文物 - 领取充盈任务')
                            for i in range(5):
                                TomatoOcrTap(486, 299, 540, 329, '领取')
                                tapSleep(358, 1049)  # 点击空白处
                                tapSleep(358, 1049)  # 点击空白处
                            tapSleep(323, 1199, 0.8)  # 点击空白处返回
                            re = FindColors.find("497,765,#EF5C40|500,765,#F05E40|502,765,#EF5C40",
                                                 rect=[86, 741, 623, 988], diff=0.9)  # 领取累积奖励
                            if re:
                                Toast('旅人 - 星墟文物 - 领取累积奖励')
                                tapSleep(re.x - 20, re.y + 20)
                                tapSleep(323, 1199, 0.8)  # 点击空白处
                                tapSleep(323, 1199)  # 点击空白处
                else:
                    Toast('旅人 - 星墟文物 - 无需切换文物')

            tapSleep(112, 1201)  # 返回首页

        Toast('旅人 - 稚星道途 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        res = TomatoOcrFindRangeClick("稚星道途", x1=448, y1=233, x2=560, y2=528, sleep1=2, offsetX=10,
                                      offsetY=-10)
        if not res:
            任务记录['旅人-稚星道途-完成'] = 1
            Toast('稚星道途 - 未找到任务入口')
            return

        TomatoOcrTap(333, 923, 386, 956, '解锁', sleep1=0.8)  # 首次解锁
        if 功能开关["稚星道途领取"] == 1:
            re, time = TomatoOcrText(596, 1055, 626, 1075, '累计时间')
            time = time.replace(':', '')
            time = safe_float_v2(time)
            if time > 8:
                re = TomatoOcrTap(614, 1090, 660, 1112, '领取')
                tapSleep(345, 1238)  # 点击空白处
                tapSleep(345, 1238)  # 点击空白处
            else:
                Toast('集忆时间不足8h，跳过领取')

        if 功能开关["稚星道途升级"] == 1:
            for i in range(30):
                Toast('旅人 - 稚星道途 - 启明升级')
                reAll = FindColors.find_all("133,460,#EC5535|134,455,#F45F42|131,456,#F25E41|136,456,#F25E41",
                                            rect=[16, 324, 701, 874])
                if reAll:
                    for re in reAll:
                        tapSleep(re.x, re.y)
                        TomatoOcrTap(333, 1077, 387, 1102, '升星')
                        tapSleep(360, 945, 0.2)  # 点击升级
                        tapSleep(360, 945, 0.2)  # 点击升级
                        tapSleep(360, 945, 0.2)  # 点击升级
                        tapSleep(360, 945, 0.2)  # 点击升级
                        tapSleep(360, 945, 0.2)  # 点击升级
                        tapSleep(345, 1238)  # 点击空白处
                else:
                    break

            # 匹配权能红点
            re = CompareColors.compare("683,1169,#F15E41|686,1167,#F46042")
            if re:
                tapSleep(661, 1204)  # 点击权能
                for i in range(30):
                    reAll = FindColors.find_all(
                        "119,301,#F66043|121,303,#F35E42|119,305,#EF5D40|116,305,#EF5C40|122,300,#FA6243",
                        rect=[80, 274, 704, 915])
                    if reAll:
                        Toast('旅人 - 稚星道途 - 权能进阶')
                        for re in reAll:
                            tapSleep(re.x, re.y)
                            TomatoOcrTap(339, 1084, 380, 1107, '升星')
                            tapSleep(360, 945, 0.2)  # 点击升级
                            tapSleep(360, 945, 0.2)  # 点击升级
                            tapSleep(360, 945, 0.2)  # 点击升级
                            tapSleep(360, 945, 0.2)  # 点击升级
                            tapSleep(360, 945, 0.2)  # 点击升级
                            tapSleep(345, 1238)  # 点击空白处
                    else:
                        break

        任务记录['旅人-稚星道途-完成'] = 1

    # 升级天赋
    def updateTianFu(self):
        if 功能开关["自动点亮天赋"] == 0:
            return

        if 任务记录['旅人-点亮天赋-完成']:
            Toast('旅人 - 点亮天赋 - 已完成')
            return

        Toast('旅人 - 点亮天赋 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        res, _ = TomatoOcrText(573, 498, 622, 522, "天赋")
        if res:
            re = CompareColors.compare("615,462,#F05D41|618,460,#F35E41|618,462,#F25E3E", diff=0.8)  # 天赋红点
            if not re:
                Toast('旅人 - 点亮天赋 - 已完成')
                任务记录['旅人-点亮天赋-完成'] = 1
                return
        res = TomatoOcrTap(573, 498, 622, 522, "天赋", sleep1=2)
        if not res:
            Toast('旅人-点亮天赋-未找到入口')
            return

        # 匹配天赋1未装备
        re = CompareColors.compare("118,160,#F56042|118,164,#F15E42")
        if re:
            tapSleep(156, 181)

        for k in range(3):
            re = TomatoOcrFindRangeClick('领取', x1=78, y1=295, x2=647, y2=1122)
            if not re:
                break
            tapSleep(607, 1030)

        tapSleep(210, 1243)  # 关闭领取技能弹窗
        tapSleep(210, 1243)

        # 匹配天赋1未装备
        re, _ = TomatoOcrText(293, 625, 339, 650, '暂未')
        if re:
            tapSleep(156, 181, 0.8)  # 点击天赋1
            tapSleep(173, 495, 0.8)  # 装备天赋
            tapSleep(353, 864, 0.8)  # 确认装备

        tapSleep(210, 1243)  # 关闭领取技能弹窗
        tapSleep(210, 1243)

        for p in range(5):
            re = FindColors.find("358,677,#97999D|367,688,#F15C3E|371,686,#F45F42|375,699,#83868A",
                                 rect=[82, 364, 682, 1164], diff=0.85, ori=1)  # 匹配可升星-未点击状态
            if not re:
                re = FindColors.find("296,675,#F56143|298,678,#F25E41|300,680,#EF5A3D|293,678,#F35C42|290,670,#83878C",
                                     rect=[53, 252, 623, 1130], diff=0.9, ori=1)  # 匹配可升星-未点击状态
            if re:
                tapSleep(re.x, re.y + 10, 1)  # 点击天赋
                res = TomatoOcrTap(320, 1122, 396, 1152, '解锁', sleep1=2)
                if res:
                    tapSleep(108, 553, 1)  # 关闭解锁页面，继续点亮
        tapSleep(90, 1199)  # 返回
        tapSleep(90, 1199)

    # 秘宝
    def updateMiBao(self):
        if 功能开关["自动升星秘宝"] == 0:
            return

        if 任务记录['旅人-秘宝升星-完成']:
            Toast('旅人 - 秘宝升星 - 已完成')
            return

        Toast('旅人 - 秘宝升星 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        re = CompareColors.compare("620,375,#F05C3F|615,374,#F15D40|622,375,#FF5544")  # 秘宝红点
        if not re:
            Toast('旅人 - 秘宝升星 - 已完成')
            任务记录['旅人-秘宝升星-完成'] = 1
            return
        res = TomatoOcrTap(575, 413, 618, 434, "秘宝", sleep1=0.8)
        if not re:
            Toast('旅人 - 秘宝升星 - 未找到秘宝入口')
            return

        re = CompareColors.compare("344,149,#4DAE3A|348,149,#4EAF3A|350,146,#4BAF39")  # 匹配可升星- 点击状态
        if not re:
            tapSleep(348, 143, 0.8)  # 点击可升星

        reAll = FindColors.find_all("235,363,#F46042|237,363,#F46042|236,366,#ED5B40", rect=[91, 222, 639, 956])
        if reAll:
            for re in reAll:
                tapSleep(re.x - 10, re.y + 10, 0.8)  # 点击待升星秘宝
                res = TomatoOcrTap(322, 1024, 391, 1054, "合成")
                res = TomatoOcrTap(322, 1024, 391, 1054, "升星")
                tapSleep(153, 1071)  # 点击空白处
                tapSleep(153, 1071)  # 点击空白处
                tapSleep(210, 1185)  # 点击返回
        任务记录['旅人-秘宝升星-完成'] = 1

    # 猫猫包
    def maomaobao(self):
        if 功能开关["领取猫猫包果木"] == 0 and 功能开关['猫猫包自动升温'] == 0 and 功能开关['猫猫包自动融合'] == 0:
            return

        if 任务记录['旅人-猫猫果木-完成']:
            Toast('旅人 - 猫猫果 - 已完成')
            return

        Toast('旅人 - 猫猫包 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
        res = tapSleep(551, 915)  # 点击猫包
        sleep(1)

        if 功能开关['领取猫猫包果木']:
            # 点击果木
            re = imageFindClick('猫猫果木')
            if re:
                # res = TomatoOcrTap(265, 863, 452, 893, "点击空白处可领取奖励", 30, 100)
                tapSleep(216, 1224)  # 点击空白处可领取奖励

            # 领取4代果木
            tapSleep(577, 1218)  # 点击4代烤箱
            tapSleep(577, 1218)  # 点击4代烤箱
            tapSleep(369, 160, 0.3)  # 点击4代烤箱
            tapSleep(367, 175, 0.3)  # 点击4代烤箱
            tapSleep(216, 1224)  # 点击空白处可领取奖励

            # 快捷兑换
            res = TomatoOcrTap(557, 188, 639, 214, "快速兑换", 30, -30)
            needCount = safe_int(功能开关["钻石兑换果木次数"])
            if needCount == '':
                needCount = 0
            if res:
                任务记录['旅人-猫猫果木-完成'] = 1
                while 1:
                    # 钻石兑换果木
                    res, buyCount = TomatoOcrText(277, 533, 434, 569, needCount)  # 1/9
                    buyCount = (buyCount.replace("每日限购", "").replace("/9", "").
                                replace("(", "").replace(")", "").replace("（", "").
                                replace("）", "").replace("/", "").replace("9", "").replace(" ", ""))
                    buyCount = safe_int(buyCount)
                    if buyCount == "" or buyCount >= needCount:
                        tapSleep(155, 1020)  # 点击空白处关闭
                        tapSleep(155, 1020)  # 点击空白处关闭
                        tapSleep(350, 1205)  # 点击空白处关闭
                        break
                    re, ct = TomatoOcrText(334, 389, 396, 416, '准备购买次数')
                    Toast(f'准备购买{ct}次')
                    ct = safe_int(ct)
                    if ct < needCount:
                        tapSleep(421, 402)  # 点击+1
                    res = TomatoOcrTap(334, 462, 383, 487, "购买", 10, 10, sleep1=0.8)
                    tapSleep(155, 1020)  # 点击空白处关闭

        if 功能开关['猫猫包自动升温'] == 1:
            for i in range(10):
                res, availableGuoMu = TomatoOcrText(607, 80, 662, 102, "剩余果木")
                availableGuoMu = safe_int(availableGuoMu)
                if availableGuoMu == "" or availableGuoMu <= 100:
                    Toast('猫猫包 - 剩余果木不足')
                    break
                Toast('猫猫包 - 自动烘焙')
                res = TomatoOcrTap(326, 1017, 389, 1047, "出炉")
                if res:
                    re, _ = TomatoOcrText(206, 610, 276, 639, '陈列柜')
                    tapSleep(136, 1051)  # 点击空白处
                    tapSleep(136, 1051)  # 点击空白处
                    tapSleep(136, 1051)  # 点击空白处
                    tapSleep(136, 1051)  # 点击空白处
                    if re:
                        break
                res, _ = TomatoOcrText(320, 1006, 399, 1033, "自动烘焙")
                if not res:
                    res, _ = TomatoOcrText(320, 1006, 399, 1033, "自动升温")
                    if not res:
                        # 开启自动升温
                        tapSleep(515, 1030)
                res = TomatoOcrTap(320, 1006, 399, 1033, "自动烘焙")
                if not res:
                    res = TomatoOcrTap(320, 1006, 399, 1033, "自动升温")
                if res:
                    for k in range(1, 5):
                        res = TomatoOcrTap(326, 1017, 389, 1047, "出炉")
                        if res:
                            re, _ = TomatoOcrText(206, 610, 276, 639, '陈列柜')
                            if re:
                                break
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            break
                        sleep(3)

        if 功能开关['猫猫包自动融合'] == 1:
            re = TomatoOcrTap(513, 1089, 610, 1119, '风味融合', offsetX=10, offsetY=10, sleep1=0.8)
            if re:
                for i in range(10):
                    res, availableCount = TomatoOcrText(365, 928, 416, 955, "剩余次数")
                    if availableCount == '0/15':
                        Toast('猫猫包 - 剩余次数不足')
                        break

                    # 匹配第一个格子空白
                    noMaoBao = CompareColors.compare(
                        "233,812,#7C6347|249,817,#DBD5C9|247,823,#FCF8EE|221,825,#FCF8EE|247,801,#FCF8EE|247,801,#FCF8EE")
                    if noMaoBao:
                        tapSleep(238, 809, 1)  # 点击第一个格子
                        re, _ = TomatoOcrText(183, 438, 211, 457, '等级')
                        if not re:
                            Toast('猫猫包融合 - 剩余猫包不足')
                            break
                        else:
                            tapSleep(241, 1224)  # 点击空白处

                    Toast('猫猫包 - 自动融合')

                    # 五代猫包手动选择四代猫包融合
                    re = CompareColors.compare(
                        "489,803,#B2A799|487,812,#7C6347|487,825,#7C6347|473,823,#FCF8EE|500,820,#FCF8EE")  # 第二个猫包为空
                    if re:
                        tapSleep(233, 825, 0.6)  # 点击空白猫包1
                        tapSleep(172, 781, 0.6)  # 选择最后一个猫包
                        TomatoOcrTap(323, 967, 361, 995, '选')  # 确认选择
                        tapSleep(241, 1224)  # 点击空白处

                        tapSleep(481, 812, 0.6)  # 点击空白猫包2
                        re, _ = TomatoOcrText(296, 633, 333, 652, '空空')
                        if re:
                            Toast('猫猫包融合 - 剩余猫包不足')
                            break
                        tapSleep(296, 785, 0.6)  # 选择最后一个猫包
                        TomatoOcrTap(323, 967, 361, 995, '选')  # 确认选择
                        tapSleep(241, 1224)  # 点击空白处

                    res = TomatoOcrTap(453, 1016, 510, 1049, "融合", offsetX=5, offsetY=5)
                    res = TomatoOcrTap(333, 1019, 385, 1047, "融合", offsetX=5, offsetY=5)
                    TomatoOcrTap(600, 31, 642, 53, '跳过', offsetX=5, offsetY=5)
                    tapSleep(217, 1204)  # 点击空白处
                    tapSleep(217, 1204)  # 点击空白处
                    tapSleep(217, 1204)  # 点击空白处

        # 返回猫包首页
        TomatoOcrTap(99, 1188, 128, 1216, '回', offsetX=5, offsetY=5, sleep1=1)
        re = CompareColors.compare("468,170,#F35F42|468,167,#F66143|468,173,#F05A3F")  # 匹配烘焙坊红点
        if re:
            # 升级烘焙坊
            tapSleep(362, 197, 1)
            TomatoOcrTap(326, 1130, 394, 1158, '升级')
            TomatoOcrTap(99, 1188, 128, 1216, '回', offsetX=5, offsetY=5, sleep1=1)
        TomatoOcrTap(99, 1188, 128, 1216, '回', offsetX=5, offsetY=5, sleep1=1)

    # 自动升级技能
    def updateSkill(self):
        if 功能开关["自动升级技能"] == 0:
            return

        if 任务记录["技能升级-倒计时"] > 0:
            diffTime = time.time() - 任务记录["技能升级-倒计时"]
            if diffTime < 10 * 60:
                Toast(f'日常 - 技能升级 - 倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["技能升级-倒计时"] = time.time()

        Toast('旅人 - 升级技能 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        if not res:
            return

        # 装备技能
        for i in range(5):
            res, x, y = imageFind('旅人-装备技能', confidence1=0.85, x1=82, y1=628, x2=653, y2=1070)
            if res:
                Toast('旅人 - 装备技能 - 开始')
                tapSleep(x, y)
                tapSleep(168, 591)  # 装备第1个技能
                tapSleep(358, 959)  # 确认装备
                tapSleep(96, 1065)  # 确认装备
                tapSleep(96, 1065)  # 确认装备
            else:
                break

        # 继承技能
        for p in range(8):
            re = FindColors.find(
                "260,967,#F2A94A|257,970,#F2A94A|254,972,#FFF8F0|255,976,#F2A94A|268,973,#FFFCF6|263,983,#F3AB4B",
                rect=[86, 576, 639, 1087], diff=0.9)
            if re:
                Toast('旅人 - 继承技能 - 开始')
                tapSleep(re.x, re.y, 0.8)
                tapSleep(361, 797)  # 点击继承装备
                tapSleep(53, 1238)
                tapSleep(53, 1238)

        # 技能升星
        for i in range(8):
            # 匹配技能右上角小红点
            point = FindColors.find("378,645,#F46042|380,645,#F56142|383,645,#F46042|382,650,#F15A41",
                                    rect=[94, 632, 609, 1060], diff=0.95)
            if point:
                Toast('旅人 - 技能升星')
                tapSleep(point.x, point.y)
                TomatoOcrTap(328, 962, 388, 984, '升星', sleep1=1.5)
                tapSleep(317, 1134)
                tapSleep(317, 1134)

        if 功能开关['优先升级同一技能'] == 0:
            for i in range(5):
                re = imageFindClick('技能升级', confidence1=0.7, x1=97, y1=571, x2=630, y2=1079, offsetX=10, offsetY=20)
                if re:
                    TomatoOcrFindRangeClick('最大', whiteList='最大')
                    tapSleep(365, 985)  # 点击升级按钮
                    tapSleep(317, 1134)
                    tapSleep(317, 1134)

        if 功能开关['优先升级同一技能'] == 1:
            skills = [
                {'x': 356, 'y': 827},  # 核心技能
                {'x': 225, 'y': 735},  # 1技能 主动
                {'x': 360, 'y': 674},  # 2技能
                {'x': 490, 'y': 737},  # 3技能
                {'x': 142, 'y': 935},  # b1技能 被动
                {'x': 244, 'y': 1001},  # b2技能
                {'x': 358, 'y': 1026},  # b3技能
                {'x': 474, 'y': 1001},  # b4技能
                {'x': 570, 'y': 936}  # b5技能
            ]
            skill_levels = []
            skill_level_map = {}

            for skill in skills:
                Toast('旅人 - 升级技能 - 检索优先升阶的技能')
                tapSleep(skill['x'], skill['y'])
                # 识别当前等级
                res, skill_level = TomatoOcrText(391, 524, 423, 542, "技能等级")
                skill_level = safe_int(skill_level)
                if skill_level == "":
                    skill_level = 0
                skill_levels.append(skill_level)
                skill_level_map[skill_level] = skill
                res = TomatoOcrTap(85, 1188, 141, 1219, "返回", 10, 10)  # 返回继续查找

            cloest_level = self.closestToNextMultipleOf30(skill_levels)
            tapSleep(skill_level_map[cloest_level]['x'], skill_level_map[cloest_level]['y'])

            # 匹配哪个最接近30
            res = TomatoOcrTap(505, 916, 548, 944, "最大", 2, 2)
            tapSleep(365, 985)  # 点击升级按钮

    def closestToNextMultipleOf30(self, numbers):
        closest_number = None
        min_difference = float('inf')  # 初始化最小差距为极大值

        for number in numbers:
            # 找到比 `number` 大的最近的30的倍数
            next_multiple = math.ceil(number / 10) * 10
            # 计算差距
            difference = next_multiple - number

            # 更新最接近的数字
            if difference < min_difference:
                min_difference = difference
                closest_number = number

        return closest_number

    # 自动分解装备
    def deleteEquip(self, needDelete=False):
        if 功能开关["满包裹分解装备"] == 0 and not needDelete:
            return

        if 任务记录["分解装备-倒计时"] > 0 and not needDelete:
            diffTime = time.time() - 任务记录["分解装备-倒计时"]
            if diffTime < 10 * 60:
                print(f'日常 - 分解装备 - 倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        if 任务记录['装备数量'] != "" and 任务记录['装备数量'] < 190:
            Toast(f'旅人 - 无需分解装备 {任务记录["装备数量"]}/200')
            return

        if needDelete:
            Toast('检查背包装备是否已满')
        else:
            Toast('旅人 - 分解装备 - 开始')

        res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
        if not res:
            self.dailyTask.homePage()
            res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
            if not res:
                return

        任务记录["分解装备-倒计时"] = time.time()

        res, _ = TomatoOcrText(339, 461, 379, 481, '熔炼')
        if res:
            res = TomatoOcrTap(211, 765, 285, 793, '取消')

        re, equipNum = TomatoOcrText(498, 1042, 588, 1072, '装备数量')
        equipNum = equipNum.replace("/200", "")
        equipNum = safe_int(equipNum)
        任务记录["装备数量"] = equipNum
        if equipNum == "":
            return

        # 超过140件时分解
        if (needDelete and equipNum > 185) or (not needDelete and equipNum > 190):
            Toast('旅人 - 分解装备')
            re = TomatoOcrTap(156, 1046, 203, 1073, '熔炼', sleep1=1)
            if re:
                # 用户未配置自动熔炼，仅删除一件
                # 未勾选史诗+
                re = CompareColors.compare("121,869,#4EAE3C|359,1183,#F8F7FB")
                if not re:
                    tapSleep(123, 864)
                # 未勾选常见
                re = CompareColors.compare("494,899,#52AF41|497,904,#55B244|500,899,#64B655")
                if not re:
                    tapSleep(500, 896)
                # 未勾选普通
                re = CompareColors.compare("369,902,#4CAD3B|371,905,#6EB961|374,902,#51AD40")
                if not re:
                    tapSleep(375, 898)
                # 未勾选优秀
                re = CompareColors.compare("247,901,#4CAE39|251,904,#4EB13A|252,899,#62B653")
                if not re:
                    tapSleep(252, 894)
                re = CompareColors.compare("118,901,#68B55C|121,902,#4EB13A|127,898,#4DB138")
                # 未勾选史诗
                if not re:
                    tapSleep(124, 899)

                # 判断是否有可选的分解装备
                re = FindColors.find("138,329,#4EAE3B|134,336,#FFFFFF|130,343,#4EAF3A|127,339,#4EAF3A",
                                     rect=[91, 232, 612, 808], diff=0.9)
                if not re:
                    # 选中低等级装备
                    swipe(358, 722, 360, 574)
                    swipe(358, 722, 360, 574)
                    swipe(358, 722, 360, 574)
                    swipe(358, 722, 360, 574)
                    sleep(1)
                    tapSleep(551, 710)
                    tapSleep(472, 713)
                    tapSleep(404, 718)
                    tapSleep(312, 710)
                    tapSleep(238, 705)
                tapSleep(353, 926)  # 点击转化
                tapSleep(356, 1208)  # 点击空白
                tapSleep(356, 1208)  # 点击空白
                tapSleep(356, 1208)  # 点击空白
        else:
            Toast(f'旅人 - 无需分解装备 {任务记录["装备数量"]}/200')

    # 自动使用经验补剂
    def useLevelPotion(self):
        if 功能开关["自动使用经验补剂"] == 0:
            return

        if 任务记录["自动使用经验补剂-完成"] == 1:
            return

        Toast('旅人 - 自动使用经验补剂 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
        res = TomatoOcrTap(405, 1103, 472, 1136, "道具", sleep1=0.8)
        if not res:
            return

        for i in range(10):
            res1 = FindColors.find(
                "316,969,#3B97EF|316,961,#2578DA|322,950,#AAD8F5|326,945,#BFF4FB|322,964,#378FF1|337,984,#F4AA4B",
                rect=[112, 643, 611, 1054], diff=0.9)
            if res1:
                tapSleep(res1.x, res1.y, 1)
                tapSleep(540, 887)  # 最大
                tapSleep(356, 935, 2)  # 使用
                break
            swipe(358, 894, 358, 744)
            sleep(0.5)
        tapSleep(363, 1218)  # 返回首页
        tapSleep(363, 1218)
        tapSleep(363, 1218)

        任务记录["自动使用经验补剂-完成"] = 1

    # 自动更换装备
    def changeEquip(self):
        if 功能开关["自动更换装备"] == 0:
            return

        if 任务记录["更换装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["更换装备-倒计时"]
            if diffTime < 2 * 60:
                Toast(f'日常 - 更换装备 - 倒计时{round((2 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        Toast('旅人 - 更换装备 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
        if not res:
            return

        TomatoOcrTap(202, 762, 271, 798, '取消')
        任务记录["更换装备-倒计时"] = time.time()

        # 识别战力提升红点
        for i in range(7):
            res1, x, y = imageFind('旅人-更换装备', x1=61, y1=101, x2=637, y2=568, confidence1=0.8)
            if res1:
                tapSleep(x, y, 1)
                tapSleep(544, 337, 2)  # 确认装备

            res2 = FindColors.find("191,654,#F45F42|189,656,#F15D40|189,654,#F45F42|191,658,#F64E44",
                                   rect=[64, 620, 644, 1085], diff=0.97)
            if res2:
                tapSleep(res2.x - 5, res2.y + 10)  # 点击装备
                tapSleep(366, 995, 5)  # 确认装备

            if not res1 and not res2:
                break

        # 识别装备等级提升
        tapSleep(135, 173, 0.8)  # 点击武器
        self.changeEquipUtil()
        tapSleep(576, 176, 0.8)  # 点击头盔
        self.changeEquipUtil()
        tapSleep(140, 287, 0.8)  # 点击胸甲
        self.changeEquipUtil()
        tapSleep(577, 284, 0.8)  # 点击护腕
        self.changeEquipUtil()
        tapSleep(134, 396, 0.8)  # 点击腿甲
        self.changeEquipUtil()
        tapSleep(579, 394, 0.8)  # 点击鞋子
        self.changeEquipUtil()
        tapSleep(227, 503, 0.8)  # 点击戒指
        self.changeEquipUtil()
        tapSleep(356, 505, 0.8)  # 点击项链
        self.changeEquipUtil()
        tapSleep(486, 505, 0.8)  # 点击护符
        self.changeEquipUtil()

    def changeEquipUtil(self):
        re = TomatoOcrTap(503, 312, 581, 337, '更换装备')
        if re:
            re, nowLevel = TomatoOcrText(210, 337, 339, 380, '当前等级')
            nowLevel = safe_int_v2(nowLevel.replace('等级', ''))
            if nowLevel > 0:
                _, newLevel1 = TomatoOcrText(232, 754, 328, 784, '新装备1等级')
                if newLevel1 == "" or '等级' not in newLevel1 or len(newLevel1) == 3:
                    _, newLevel1 = TomatoOcrText(240, 722, 317, 757, '新装备1等级')
                if newLevel1 == "" or '等级' not in newLevel1 or len(newLevel1) == 3:
                    _, newLevel1 = TomatoOcrText(236, 626, 330, 664, '新装备1等级')
                if newLevel1 == "" or '等级' not in newLevel1 or len(newLevel1) == 3:
                    _, newLevel1 = TomatoOcrText(232, 661, 330, 697, '新装备1等级')
                if newLevel1 == "" or '等级' not in newLevel1 or len(newLevel1) == 3:
                    _, newLevel1 = TomatoOcrText(233, 669, 328, 697, '新装备1等级')
                newLevel1 = safe_int_v2(newLevel1.replace('等级', ''))
                if newLevel1 > nowLevel:
                    TomatoOcrFindRangeClick(keyword='装备', x1=457, y1=525, x2=598, y2=804)
                    return
                _, newLevel2 = TomatoOcrText(236, 991, 322, 1022, '新装备2等级')
                if newLevel2 == "" or '等级' not in newLevel2 or len(newLevel2) == 3:
                    _, newLevel2 = TomatoOcrText(238, 962, 320, 994, '新装备2等级')
                if newLevel2 == "" or '等级' not in newLevel2 or len(newLevel2) == 3:
                    _, newLevel2 = TomatoOcrText(232, 995, 326, 1022, '新装备2等级')
                if newLevel2 == "" or '等级' not in newLevel2 or len(newLevel2) == 3:
                    _, newLevel2 = TomatoOcrText(228, 945, 326, 973, '新装备2等级')
                if newLevel2 == "" or '等级' not in newLevel2 or len(newLevel2) == 3:
                    _, newLevel2 = TomatoOcrText(227, 940, 325, 975, '新装备2等级')
                newLevel2 = safe_int_v2(newLevel2.replace('等级', ''))
                if newLevel2 > nowLevel:
                    TomatoOcrFindRangeClick(keyword='装备', x1=462, y1=817, x2=604, y2=1041)
                    return
                if newLevel1 == 0 and newLevel2 == 0:
                    Toast('未识别到新装备等级')
                else:
                    Toast(f'新装备等级{newLevel1}低于当前装备{nowLevel}')
            if nowLevel == 0:
                Toast('未识别到当前装备等级')
        TomatoOcrTap(97, 1188, 129, 1220, '回')

    # 自动强化装备
    def updateEquip(self):
        if 功能开关["自动强化装备"] == 0 and 功能开关["自动进阶装备"] == 0:
            return

        if 任务记录["强化装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["强化装备-倒计时"]
            if diffTime < 10 * 60:
                Toast(f'日常 - 强化装备 - 倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        if 功能开关["自动强化装备"] == 1:
            Toast('旅人 - 强化装备 - 开始')
            self.dailyTask.homePage()
            res = TomatoOcrTap(233, 1205, 281, 1234, "行李")
            if not res:
                return

            res, _ = TomatoOcrText(339, 461, 379, 481, '熔炼')
            if res:
                # 返回首页
                tapSleep(364, 1212)
                tapSleep(364, 1212)
                # 自动分解装备
                Toast('背包装备已满，自动分解装备')
                self.deleteEquip(needDelete=True)

            任务记录["强化装备-倒计时"] = time.time()

            yiJianRes = True
            if 功能开关['仅强化武器戒指护腕'] == 0 and 功能开关['仅强化防御装备'] == 0:
                yiJianRes = imageFindClick('一键强化')
                # if yiJianRes:
                #     return
            if 功能开关['仅强化武器戒指护腕'] == 1:
                for i in range(2):
                    tapSleep(140, 175, 0.6)  # 点击武器
                    self.updateEquipTool()

                    tapSleep(579, 287, 0.6)  # 点击护腕
                    self.updateEquipTool()

                    tapSleep(228, 506, 0.6)  # 点击戒指
                    self.updateEquipTool()
            if 功能开关['仅强化防御装备'] == 1:
                for i in range(2):
                    tapSleep(574, 178, 0.6)  # 点击头盔
                    self.updateEquipTool()
                    tapSleep(140, 285, 0.6)  # 点击胸甲
                    self.updateEquipTool()
                    tapSleep(135, 394, 0.6)  # 点击腿甲
                    self.updateEquipTool()
                    tapSleep(577, 391, 0.6)  # 点击鞋子
                    self.updateEquipTool()
                    tapSleep(352, 505, 0.6)  # 点击项链
                    self.updateEquipTool()
                    tapSleep(489, 505, 0.6)  # 点击护符
                    self.updateEquipTool()

            # 适配新手无一键强化按钮
            if 功能开关['仅强化武器戒指护腕'] == 0 and 功能开关['仅强化防御装备'] == 0 and not yiJianRes:
                waitUpdate = FindColors.find_all(
                    "326,463,#F0706D|318,468,#FFFFFF|315,461,#FC694C|319,463,#FDFDFD|331,464,#FC694C|323,471,#F9715A|322,478,#FC694C|333,468,#FC694C",
                    rect=[69, 110, 650, 566], diff=0.9)
                if waitUpdate:
                    for p in waitUpdate:
                        tapSleep(p.x, p.y, 0.6)  # 点击待操作装备
                        self.updateEquipTool()

        if 功能开关["自动进阶装备"] == 1:
            Toast('旅人 - 装备进阶 - 开始')
            TomatoOcrTap(94, 1188, 127, 1216, "回")
            self.dailyTask.homePage()
            res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
            if not res:
                return

            res, _ = TomatoOcrText(339, 461, 379, 481, '熔炼')
            if res:
                # 返回首页
                tapSleep(364, 1212)
                tapSleep(364, 1212)
                # 自动分解装备
                Toast('背包装备已满，自动分解装备')
                self.deleteEquip(needDelete=True)

            任务记录["强化装备-倒计时"] = time.time()

            # 识别可强化标识
            needUpdate = FindColors.find_all(
                "326,463,#F0706D|318,468,#FFFFFF|315,461,#FC694C|319,463,#FDFDFD|331,464,#FC694C|323,471,#F9715A|322,478,#FC694C|333,468,#FC694C",
                rect=[69, 110, 650, 566], diff=0.85)
            if not needUpdate:
                needUpdate = FindColors.find_all(
                    "554,357,#FF0000|561,357,#FDC1BA|573,359,#FF100F|578,361,#FF4542|584,364,#FF6863|602,359,#FF5754",
                    rect=[91, 118, 631, 566], diff=0.9)
                if not needUpdate:
                    Toast('旅人 - 装备进阶 - 无可进阶装备')
            if needUpdate:
                for p in needUpdate:
                    tapSleep(p.x, p.y, 0.8)
                    # 识别可打造标识
                    re = FindColors.find("587,967,#F25E41|587,967,#F25E41|587,967,#F25E41", diff=0.95)
                    if re:
                        Toast('旅人 - 装备进阶 - 准备打造装备')
                        tmp = TomatoOcrTap(525, 965, 574, 988, '打造', sleep1=4)
                        if tmp:
                            Toast('旅人 - 装备进阶 - 开始打造装备')
                            TomatoOcrTap(326, 991, 391, 1021, '打造', sleep1=3)
                            tapSleep(167, 1090, 0.8)  # 点击空白处
                            TomatoOcrTap(330, 825, 385, 855, '装备')  # 装备

                    # 识别可进阶标识
                    for i in range(4):
                        re = CompareColors.compare("604,1065,#EC5D44|609,1063,#F05C3F|607,1060,#F46043", diff=0.7)
                        if re:
                            Toast('旅人 - 装备进阶 - 开始进阶装备')
                            tapSleep(554, 1076, 1)
                            res = TomatoOcrTap(328, 980, 391, 1008, "进阶", sleep1=0.8)
                            if res:
                                TomatoOcrTap(200, 762, 301, 797, '继续进阶')
                                TomatoOcrTap(442, 760, 516, 797, '确认')
                                tapSleep(483, 778, 1)  # 确认进阶
                                tapSleep(129, 1023, 0.3)
                                tapSleep(129, 1023, 0.3)
                            res = TomatoOcrTap(328, 980, 391, 1008, "进阶", sleep1=0.8)
                            if res:
                                TomatoOcrTap(200, 762, 301, 797, '继续进阶')
                                TomatoOcrTap(442, 760, 516, 797, '确认')
                                tapSleep(129, 1023, 0.3)
                                tapSleep(129, 1023, 0.3)
                    tapSleep(652, 1234, 0.2)
                    tapSleep(652, 1234, 0.2)

    def updateEquipTool(self):
        for p in range(10):
            re = FindColors.find(
                "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                rect=[94, 705, 627, 1092], diff=0.9)
            if not re:
                Toast('旅人 - 强化装备 - 材料用尽')
                break
            if re:
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
        tapSleep(129, 1023, 0.3)
        TomatoOcrTap(94, 1188, 127, 1216, "回")
