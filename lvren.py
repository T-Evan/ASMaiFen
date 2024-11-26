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
        # 自动更换装备
        self.changeEquip()

        # 自动强化装备
        self.updateEquip()

        # 自动分解装备
        self.deleteEquip()

        # 自动升级技能
        self.updateSkill()

        # 猫猫包
        self.maomaobao()

    # 猫猫包
    def maomaobao(self):
        if 功能开关["领取猫猫包果木"] == 0:
            if 功能开关['猫猫包自动升温'] == 0:
                return

        if 任务记录['旅人-猫猫果木-完成']:
            Toast('旅人 - 猫猫果 - 已完成')
            return

        Toast('旅人 - 猫猫包 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(434, 1205, 484, 1234, "旅人", sleep1=0.8)
        res = TomatoOcrTap(564, 238, 630, 263, "猫猫包")
        sleep(1)
        res = TomatoOcrTap(615, 1030, 696, 1055, "猫猫烤箱")
        if not res:
            return

        if 功能开关['领取猫猫包果木']:
            # 点击果木
            re = imageFindClick('猫猫果木')
            if re:
                # res = TomatoOcrTap(265, 863, 452, 893, "点击空白处可领取奖励", 30, 100)
                tapSleep(216, 1224)  # 点击空白处可领取奖励

            # 领取4代果木
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
                        break
                    re, ct = TomatoOcrText(334, 389, 396, 416, '准备购买次数')
                    Toast(f'准备购买{ct}次')
                    ct = safe_int(ct)
                    if ct < needCount:
                        tapSleep(533, 565)  # 点击+1
                    res = TomatoOcrTap(334, 462, 383, 487, "购买", 10, 10, sleep1=0.8)
                    tapSleep(155, 1020)  # 点击空白处关闭

        if 功能开关['猫猫包自动升温'] == 1:
            for i in range(1, 10):
                res, availableGuoMu = TomatoOcrText(607, 80, 662, 102, "剩余果木")
                availableGuoMu = safe_int(availableGuoMu)
                if availableGuoMu == "" or availableGuoMu <= 100:
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
                    for i in range(1, 5):
                        res = TomatoOcrTap(326, 1017, 389, 1047, "出炉")
                        if res:
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            tapSleep(136, 1051)  # 点击空白处
                            break
                        sleep(3)
        任务记录['旅人-猫猫果木-完成'] = 1

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

        # 技能升星
        for i in range(5):
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
            next_multiple = math.ceil(number / 30) * 30
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

        if 任务记录["分解装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["分解装备-倒计时"]
            if diffTime < 10 * 60:
                print(f'日常 - 分解装备 - 倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        if needDelete:
            Toast('检查背包装备是否已满')
        else:
            Toast('旅人 - 分解装备 - 开始')

        self.dailyTask.homePage()
        res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
        if not res:
            return

        任务记录["分解装备-倒计时"] = time.time()

        res, _ = TomatoOcrText(339, 461, 379, 481, '熔炼')
        if res:
            res = TomatoOcrTap(211, 765, 285, 793, '取消')

        re, equipNum = TomatoOcrText(510, 1043, 597, 1074, '装备数量')
        equipNum = equipNum.replace("/150", "")
        equipNum = safe_int(equipNum)
        if equipNum == "":
            return

        # 超过140件时分解
        if (needDelete and equipNum > 145) or (not needDelete and equipNum > 140):
            Toast('旅人 - 分解装备')
            re = TomatoOcrTap(156, 1046, 203, 1073, '熔炼')
            if re:
                # 用户未配置自动熔炼，仅删除一件
                if 功能开关["满包裹分解装备"] == 0 and needDelete:
                    tapSleep(162, 572)
                else:
                    tapSleep(162, 572)
                    tapSleep(235, 574)
                    tapSleep(320, 579)
                    tapSleep(396, 572)
                    tapSleep(480, 577)
                    tapSleep(563, 574)
                tapSleep(353, 926)  # 点击转化
                tapSleep(356, 1208)  # 点击空白
                tapSleep(356, 1208)  # 点击空白
        else:
            Toast('旅人 - 无需分解装备')

    # 自动更换装备
    def changeEquip(self):
        if 功能开关["自动更换装备"] == 0:
            return

        if 任务记录["更换装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["更换装备-倒计时"]
            if diffTime < 5 * 60:
                Toast(f'日常 - 更换装备 - 倒计时{round((5 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        Toast('旅人 - 更换装备 - 开始')
        self.dailyTask.homePage()
        res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.8)
        if not res:
            return

        任务记录["更换装备-倒计时"] = time.time()

        for i in range(5):
            res1, x, y = imageFind('旅人-更换装备', x1=61, y1=101, x2=637, y2=568, confidence1=0.8)
            if res1:
                tapSleep(x, y, 1)
                tapSleep(544, 337, 2)  # 确认装备

            res2 = FindColors.find("194,654,#FF6D49|189,653,#F66042|191,656,#F05C3F|189,658,#EE5432",
                                   rect=[88, 620, 652, 825], diff=0.9)
            if res2:
                tapSleep(res2.x - 5, res2.y + 10)  # 点击装备
                tapSleep(366, 995, 2)  # 确认装备

            if not res1 and not res2:
                break

    # 自动强化装备
    def updateEquip(self):
        if 功能开关["自动强化装备"] == 0:
            return

        if 任务记录["强化装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["强化装备-倒计时"]
            if diffTime < 10 * 60:
                Toast(f'日常 - 强化装备 - 倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

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

        yiJianRes = False
        if 功能开关['仅强化武器戒指护腕'] == 0:
            yiJianRes = imageFindClick('一键强化')
            if yiJianRes:
                return
        if 功能开关['仅强化武器戒指护腕'] == 1 or not yiJianRes:
            for i in range(6):
                tapSleep(140, 175, 0.6)  # 点击武器
                re = FindColors.find(
                    "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                    rect=[94, 705, 627, 1092], diff=0.9)
                if not re:
                    Toast('旅人 - 强化装备 - 材料用尽')
                    break
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(129, 1023, 0.3)
                TomatoOcrTap(94, 1188, 127, 1216, "回")

                tapSleep(579, 287, 0.6)  # 点击护腕
                re = FindColors.find(
                    "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                    rect=[94, 705, 627, 1092], diff=0.9)
                if not re:
                    Toast('旅人 - 强化装备 - 材料用尽')
                    break
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(129, 1023, 0.3)
                TomatoOcrTap(94, 1188, 127, 1216, "回")

                tapSleep(228, 506, 0.6)  # 点击戒指
                re = FindColors.find(
                    "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                    rect=[94, 705, 627, 1092], diff=0.9)
                if not re:
                    Toast('旅人 - 强化装备 - 材料用尽')
                    break
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(re.x, re.y)
                tapSleep(129, 1023, 0.3)
                TomatoOcrTap(94, 1188, 127, 1216, "回")

                if not yiJianRes:
                    tapSleep(574, 178, 0.6)  # 点击面具
                    re = FindColors.find(
                        "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                        rect=[94, 705, 627, 1092], diff=0.9)
                    if not re:
                        Toast('旅人 - 强化装备 - 材料用尽')
                        break
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(129, 1023, 0.3)
                    TomatoOcrTap(94, 1188, 127, 1216, "回")

                    tapSleep(140, 285, 0.6)  # 点击胸甲
                    re = FindColors.find(
                        "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                        rect=[94, 705, 627, 1092], diff=0.9)
                    if not re:
                        Toast('旅人 - 强化装备 - 材料用尽')
                        break
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(129, 1023, 0.3)
                    TomatoOcrTap(94, 1188, 127, 1216, "回")

                    tapSleep(135, 394, 0.6)  # 点击腿甲
                    re = FindColors.find(
                        "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                        rect=[94, 705, 627, 1092], diff=0.9)
                    if not re:
                        Toast('旅人 - 强化装备 - 材料用尽')
                        break
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(129, 1023, 0.3)
                    TomatoOcrTap(94, 1188, 127, 1216, "回")

                    tapSleep(577, 391, 0.6)  # 点击鞋子
                    re = FindColors.find(
                        "427,954,#FC694C|432,954,#F26B5E|436,952,#FFFFFF|428,962,#F17473|435,962,#F76D58|440,961,#FCF2F2",
                        rect=[94, 705, 627, 1092], diff=0.9)
                    if not re:
                        Toast('旅人 - 强化装备 - 材料用尽')
                        break
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(re.x, re.y)
                    tapSleep(129, 1023, 0.3)
                    TomatoOcrTap(94, 1188, 127, 1216, "回")
