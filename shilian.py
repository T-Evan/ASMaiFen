# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .child_return_home import *
from .baseUtils import *
from ascript.android import action
from ascript.android.screen import CompareColors
from .thread import *
from ascript.android.screen import FindColors


class ShiLianTask:
    def __init__(self):
        # 定义环境和关卡名称的配对
        self.map = [
            "原野",
            "森林",
            "沙漠",
            "海湾",
            "深林",
            "冰原",
            "火山",
            "高原",
            "绿洲",
            "火原",
            "下城"
            "上城"
            "万象"
            "旷野"
            "悬崖"
            "群岛"
        ]

        self.mapPoi = {
            "原野": [113, 235, 170, 268],
            "森林": [114, 336, 171, 366],
            "沙漠": [112, 435, 172, 468],
            "海湾": [113, 535, 171, 567],
            "深林": [110, 634, 176, 666],
            "冰原": [113, 733, 172, 767],
            "火山": [114, 271, 172, 304],
            "高原": [112, 371, 172, 403],
            "绿洲": [113, 470, 171, 503],
            "火原": [112, 569, 173, 603],
            "下城": [113, 669, 172, 702]
        }

        self.stage = [
            ["古遗迹上的幽影"],
            ["旧国之王的野心"],
            ["三宝齐聚黄金船"],
            ["海洋征服计划"],
            ["噩兆降临之谷"],
            ["永冻禁区矿场", "尤弥尔深渊"],
            ["蒸汽炎池浴场", "艾特拉之心"],
            ["雷电焦土深处", "九王角斗场"],
            ["溪谷大暴走", "躁动绿洲之丘", "白沙渊下的鼓动"],
            ["浴火燃墟伐木场", "激战构造体工厂", "无始无终燃烧塔"],
            ["魔偶师赌局", "下城危险警报", "无夜大王驾到"]
        ]

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
        }

    def shilian(self):
        if 功能开关['冒险总开关'] == 0:
            return

        # 开始试炼

        if 功能开关['秘境开关'] == 1:
            if 功能开关['秘境地图'] == "" or 功能开关['秘境关卡'] == "":
                return
            while 1:
                self.mijing()
                # 不开宝箱时无需循环
                # 开启宝箱时循环至体力用尽
                if 功能开关["秘境不开宝箱"] == 1 or 任务记录['试炼-秘境-体力消耗完成'] == 1:
                    break

        if 功能开关['恶龙开关'] == 1:
            self.elong()

        if 功能开关['大暴走开关'] == 1:
            self.daBaoZou()

    def daBaoZou(self):
        Toast('暴走史莱姆 - 开始')
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
                with switch_lock:
                    功能开关["needHome"] = 0
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                fightStatus = ldE.element_exist('战斗中-喊话')
                fightStatu2, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
                if teamName1 != '' or teamName2 != '' or fightStatus or fightStatu2:
                    Toast("进入战斗成功 - 开始战斗")
                    self.fightingBaoZou()
                    return True
                ldE.sleep(5)
                elapsed = elapsed + 5 * 1000
            return False

        self.homePage()
        self.quitTeam()
        # 开始暴走
        res = TomatoOcrTap(556, 380, 618, 404, "大暴走", 30, -10)
        ldE.sleep(2)
        if res == False:
            res = TomatoOcrTap(554, 464, 622, 487, "大暴走", 30, -10)  # 适配新手试炼 - 下方大暴走入口
        ldE.sleep(2)

        # 结算前一次的宝箱（兜底）
        res = TomatoOcrTap(333, 715, 384, 745, "开启")  # 领取宝箱
        if res:
            Toast("开启宝箱")
            ldE.sleep(2)
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白

        hdPage, _ = TomatoOcrText(383, 573, 436, 605, "大王")
        if hdPage == False:
            return

        self.startFightBaoZou()

    def startFightBaoZou(self):
        # 直接开始匹配
        res = TomatoOcrTap(311, 1156, 407, 1182, "开始匹配", 40, -40)
        Toast("大暴走 - 开始匹配")

        # 判断职业选择
        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
        if res:
            Toast("大暴走 - 选择职业")
            if 功能开关["职能优先输出"] == 1:
                tapSleep(280, 665, 1)  # 职能输出
            elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                tapSleep(435, 665, 1)  # 坦克
            else:
                tapSleep(280, 665, 1)  # 职能输出
            res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(311, 1156, 407, 1182, "匹配中", 40, -40)
                if res == False:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if res == False:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            Toast("秘境任务 - 匹配中")

            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(231, 624, 305, 645, "匹配超时")
            if res:
                Toast("大暴走 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(451, 727, 510, 757, "确定")
                if res:
                    elapsed = 0

            waitStatus, _ = TomatoOcrText(311, 1156, 407, 1182, "匹配中")
            if waitStatus == False:
                waitStatus, _ = TomatoOcrText(325, 1156, 390, 1182, "匹配中")
                if waitStatus == False:
                    res, waitTime = TomatoOcrText(334, 1184, 383, 1201, "等待时间")
                    if waitTime != "":
                        waitStatus = True

            res1 = self.WaitFight("暴走")
            if res1 == True or (waitStatus == False):  # 成功准备战斗 或 未匹配到
                # 超时取消匹配
                res = TomatoOcrTap(311, 1156, 407, 1182, "匹配中", 40, -40)
                if res == False:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if res == False:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            ldE.sleep(5)
            elapsed = elapsed + 5 * 1000

    # 恶龙大通缉
    def elong(self):
        Toast('恶龙任务 - 开始')
        self.homePage()
        self.quitTeam()
        res = TomatoOcrTap(650, 522, 688, 544, "试炼")
        if res:
            re = ldE.element_exist('试炼-恶龙大通缉')
            if re:
                re.click().execute(sleep=1)
            else:
                Toast("秘境任务 - 未找到恶龙入口 - 重新尝试")
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）
                return self.shilian()

        # 判断是否重复挑战（已开启过宝箱）
        re = ldE.element_exist('恶龙-宝箱已开启')
        if re:
            if 功能开关["恶龙重复挑战"] == 0:
                Toast("恶龙任务 - 已领取宝箱 - 退出挑战")
                ldE.sleep(1.5)
                return

        # 判断是否添加佣兵
        if 功能开关["恶龙添加佣兵"] == 1:
            Toast("恶龙任务 - 添加佣兵")
            re = ldE.element_exist('秘境-创建队伍')
            if re:
                re.click().execute(sleep=1)
                tapSleep(365, 820)  # 点击 创建队伍 - 添加佣兵
                res = TomatoOcrTap(313, 876, 407, 907, "创建队伍")  # 创建队伍 - 创建队伍
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
                return self.fighting()

        # 开始匹配
        re1 = ldE.element_exist('恶龙-开始匹配')
        re2 = ldE.element_exist('恶龙-开始匹配2')
        if re1 or re2:
            if re1:
                re1.click().execute(sleep=1)
            if re2:
                re2.click().execute(sleep=1)
            res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
            if res:
                Toast("恶龙任务 - 选择职业")
                if 功能开关["职能优先输出"] == 1:
                    tapSleep(280, 665)  # 职能输出
                elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                    tapSleep(435, 665)  # 坦克
                else:
                    tapSleep(280, 665)  # 职能输出
                res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                Toast("恶龙任务 - 匹配超时")
                teamStatus1 = ldE.element_exist('队伍-匹配中')
                teamStatus2 = ldE.element_exist('队伍-匹配中2')
                if teamStatus1 or teamStatus2:
                    if teamStatus1:
                        teamStatus1.click().execute(sleep=1)
                    if teamStatus2:
                        teamStatus2.click().execute(sleep=1)
                    Toast('恶龙任务 - 匹配超时 - 取消匹配')
                break

            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(229, 621, 305, 646, "匹配超时")
            if res:
                res = TomatoOcrTap(454, 727, 508, 758, "确定")
                if res:
                    Toast("恶龙任务 - 匹配超时 - 无队伍")
                    elapsed = 0

            waitStatus1 = ldE.element_exist('队伍-匹配中')
            waitStatus2 = ldE.element_exist('队伍-匹配中2')
            res1 = self.WaitFight()
            if res1:
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
            if res1 == True or (not waitStatus1 and not waitStatus2):  # 成功准备战斗 或 未匹配到
                break

            ldE.sleep(5)
            elapsed = elapsed + 5 * 1000

    def mijing(self):
        Toast('秘境任务 - 开始')

        self.homePage()
        self.quitTeam()

        selectMap = 功能开关['秘境地图']
        selectStage = 功能开关['秘境关卡']
        res = TomatoOcrTap(650, 522, 688, 544, "试炼")
        if res:
            re = ldE.element_exist('试炼-秘境之间')
            if re:
                re.click().execute(sleep=1)
            else:
                Toast("秘境任务 - 未找到试炼入口 - 重新尝试")
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）
                return self.shilian()

        self.openTreasure()

        res = self.changeMap(selectMap, selectStage)
        if not res:
            return
        self.startFight()

    # 开始匹配
    def startFight(self):
        # 识别剩余体力不足40时，尝试补充
        res2, availableTiLi = TomatoOcrText(605, 81, 630, 100, "剩余体力")  # 20/60
        availableTiLi = safe_int(availableTiLi)
        if 功能开关["秘境不开宝箱"] == 0 and (availableTiLi == "" or availableTiLi < 40):  # 识别剩余体力不足40时，尝试补充
            self.tili()

        # 判断体力不足，退出挑战
        res2, availableTiLi = TomatoOcrText(605, 81, 630, 100, "剩余体力")  # 20/60
        availableTiLi = safe_int(availableTiLi)
        if availableTiLi == "" or availableTiLi < 20:  # 识别剩余体力不足20时
            # 体力消耗完成
            任务记录["试炼-秘境-体力消耗完成"] = 1
            if 功能开关["秘境无体力继续"] == 0:
                Toast("秘境任务 - 体力不足 - 退出挑战")
                ldE.sleep(2)
                return

        # 判断是否添加佣兵
        if 功能开关["秘境添加佣兵"] == 1:
            Toast("秘境任务 - 添加佣兵")
            re = ldE.element_exist('秘境-创建队伍')
            if re:
                re.click().execute(sleep=1)

                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回")
                        self.tili()

                tapSleep(365, 820)  # 点击 创建队伍 - 添加佣兵
                res = TomatoOcrTap(313, 876, 407, 907, "创建队伍")  # 创建队伍 - 创建队伍
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")

                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回")
                        self.tili()
                return self.fighting()

        # 判断是否创建房间
        if 功能开关["秘境创建房间"] == 1:
            Toast("秘境任务 - 创建房间")
            re1 = ldE.element_exist('秘境-创建队伍')
            re2 = False
            if not re1:
                re2 = ldE.element_exist('秘境-创建队伍2')
            if re1 or re2:
                if re1:
                    re1.click().execute(sleep=1)
                if re2:
                    re2.click().execute(sleep=1)
                # 判断体力用尽提示
                res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
                if res1:
                    if 功能开关["秘境无体力继续"]:
                        Toast("秘境任务 - 体力不足继续挑战")
                        res = TomatoOcrTap(334, 743, 385, 771, "确定")
                    else:
                        Toast("秘境任务 - 体力不足")
                        res = TomatoOcrTap(64, 1200, 128, 1234, "返回")
                        self.tili()

                res = TomatoOcrTap(313, 876, 407, 907, "创建队伍")  # 创建队伍 - 创建队伍
                # 等待队员（120s超时）
                totalWait = 120 * 1000  # 30000 毫秒 = 30 秒
                elapsed = 0
                aleadyFightCt = 0
                needFightCt = safe_int(功能开关["秘境建房重复挑战次数"])
                if needFightCt == '':
                    needFightCt = 1  # 默认挑战1次
                while 1:
                    self.openTreasure()
                    # 返回房间
                    res1 = TomatoOcrTap(635, 628, 705, 653, "正在组队")
                    if not res1:
                        res2 = TomatoOcrTap(631, 558, 699, 581, "正在组队")
                        if not res2:
                            res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
                    # 返回房间 - 队伍满员，开始挑战提醒
                    res, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
                    if res:
                        res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
                        res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

                    # 等待开始
                    if aleadyFightCt >= needFightCt or elapsed > totalWait:
                        if aleadyFightCt >= needFightCt:
                            Toast(f"秘境任务 - 挑战次数{aleadyFightCt}/{needFightCt}达成 - 结束")
                        if elapsed > totalWait:
                            Toast("秘境任务 - 等待队友2min超时 - 结束")
                        res = TomatoOcrTap(502, 192, 581, 215, "离开队伍")  # 点击离开队伍
                        res = TomatoOcrTap(330, 728, 385, 759, "确定")  # 确定离开队伍
                        self.quitTeamFighting()
                        break
                    res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                    Toast("秘境任务 - 创建房间 - 等待队友")
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
                                res = TomatoOcrTap(64, 1200, 128, 1234, "返回")
                                self.tili()

                        # 等待进入战斗
                        for i in range(1, 4):
                            # 返回房间
                            res1 = TomatoOcrTap(635, 628, 705, 653, "正在组队")
                            if not res1:
                                res2 = TomatoOcrTap(631, 558, 699, 581, "正在组队")
                                if not res2:
                                    res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
                            # 返回房间 - 队伍满员，开始挑战提醒
                            res, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
                            if res:
                                res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
                                res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

                            res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                            fightStatus = ldE.element_exist('战斗中-喊话')
                            fightStatu2, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
                            if teamName1 != '' or teamName2 != '' or fightStatus or fightStatu2:
                                Toast("秘境任务 - 匹配成功 - 进入战斗")
                                self.fighting()
                                aleadyFightCt = aleadyFightCt + 1
                                elapsed = 0  # 初始化等待队员时间
                                fightDone = 1
                                break
                            # 进入战斗失败，重新匹配
                            ldE.sleep(5)
                    # 等待队员
                    ldE.sleep(4)
                    elapsed = elapsed + 4 * 1000
            return

        resStart1 = TomatoOcrTap(311, 697, 405, 725, "开始匹配")  # 图1
        resStart2 = False
        resStart3 = False
        if not resStart1:
            resStart2 = TomatoOcrTap(309, 892, 407, 918, "开始匹配")  # 图2
            if not resStart2:
                resStart3 = TomatoOcrTap(311, 1084, 405, 1116, "开始匹配")  # 图3

        if not resStart1 and not resStart2 and not resStart3:
            return
        Toast("秘境任务 - 开始匹配", 500)
        # 判断体力用尽提示
        res1, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
        if res1:
            if 功能开关["秘境无体力继续"]:
                Toast("秘境任务 - 体力不足继续挑战")
                res = TomatoOcrTap(334, 743, 385, 771, "确定")
            else:
                Toast("秘境任务 - 体力不足")
                res = TomatoOcrTap(64, 1200, 128, 1234, "返回")
                self.tili()

        # 判断职业选择
        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
        if res:
            Toast("秘境任务 - 选择职业")
            if 功能开关["职能优先输出"] == 1:
                tapSleep(280, 665, 1)  # 职能输出
            elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                tapSleep(435, 665, 1)  # 坦克
            else:
                tapSleep(280, 665, 1)  # 职能输出
            res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(320, 692, 392, 716, "匹配中")  # 图1
                if not res:
                    res = TomatoOcrTap(323, 886, 394, 910, "匹配中")  # 图2
                    if not res:
                        res4 = TomatoOcrTap(324, 1080, 392, 1103, "匹配中")  # 图3
                break
            Toast("秘境任务 - 匹配中")

            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(303, 607, 418, 632, "暂无合适队伍")
            if res:
                Toast("秘境任务 - 匹配超时 - 无合适队伍")
                res = TomatoOcrTap(210, 727, 262, 758, "取消")
                if res:
                    elapsed = 0

            res2, _ = TomatoOcrText(320, 692, 392, 716, "匹配中")  # 图1
            res3 = False
            res4 = False
            res5 = False
            if not res2:
                res3, _ = TomatoOcrText(323, 886, 394, 910, "匹配中")  # 图2
                if not res3:
                    res4, _ = TomatoOcrText(324, 1080, 392, 1103, "匹配中")  # 图3
                    if not res4:
                        res5 = ldE.element_exist('秘境-匹配中')

            res1 = self.WaitFight()
            if res1 == True or (res2 == False and res3 == False and res4 == False and res5 == False):  # 成功准备战斗 或 未匹配到
                break

            ldE.sleep(5)
            elapsed = elapsed + 5 * 1000

    def tili(self):
        Toast("体力购买 - 开始")
        tapSleep(690, 90)  # 点击补充体力加号
        for i in range(1, 3):
            res, count = TomatoOcrText(500, 817, 515, 834, "0")
            buyCount = safe_int(count)
            needCount = safe_int(功能开关["补充体力次数"])
            if buyCount != "" and buyCount < needCount:
                res = TomatoOcrTap(456, 873, 499, 898, "购买")
                Toast("体力购买 - 成功")
            else:
                break

        Toast("体力购买 - 结束")
        tapSleep(61, 1187)  # 返回

        # 切换地图

    def changeMap(self, selectMap, selectStage):
        Toast("秘境任务 - 切换地图")
        tapSleep(74, 160, 2.5)  # 点击地图列表
        mapPoi = self.mapPoi[selectMap]
        maps_to_check = ('原野', '森林', '沙漠', '海湾', '深林', '冰原', '火山', '高原', '绿洲')
        if selectMap not in maps_to_check:
            ldE.swipe([150, 1000], [150, 300], 0.5)
            ldE.sleep(2)
        else:
            # 判断是否已在第一屏
            res, _ = TomatoOcrText(110, 235, 175, 267, "原野")
            if res:
                ldE.sleep(0.5)
            else:
                # 向上滚动第一屏
                ldE.swipe([150, 300], [150, 700], 1.2, False, 0.01)
                ldE.sleep(2)
        selectMapName = '秘境-地图-' + selectMap
        res = ldE.element(selectMapName).click().execute(sleep=1)
        # res = TomatoOcrTap(mapPoi[0], mapPoi[1], mapPoi[2], mapPoi[3], selectMap, 3, 3)

        stagePoi = self.stagePoi[selectStage]
        res = TomatoOcrTap(stagePoi[0], stagePoi[1], stagePoi[2], stagePoi[3], selectStage)
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
        res, mapText = TomatoOcrText(329, 223, 388, 253, selectMap)
        if res:
            return True
        else:
            Toast(f'切换地图失败 - 识别地图为：{mapText}')
            return False

        # 开启宝箱

    def openTreasure(self):
        isTreasure = 0  # 是否在宝箱页

        res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱尚未开启")  # 避免前置错误点击弹出宝箱尚未开启
        if res:
            res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

        res1 = False
        res2 = False
        res3 = False
        res4 = False
        res5 = False
        res6 = False
        res7 = False
        res1, _ = TomatoOcrText(313, 622, 404, 656, "通关奖励")  # 战斗结束页。宝箱提示
        if not res1:
            res2, _ = TomatoOcrText(267, 755, 313, 783, "开启")  # 战斗结束页。宝箱提示
            if not res2:
                res3, _ = TomatoOcrText(273, 397, 360, 425, "是否开启")  # 结算页，宝箱提示
                if not res3:
                    res4, _ = TomatoOcrText(265, 457, 314, 488, "开启")  # 结算页，宝箱提示
                    if not res4:
                        res5, _ = TomatoOcrText(312, 563, 404, 596, "通关奖励")  # 战斗结束页。宝箱提示
                        if not res5:
                            res6, _ = TomatoOcrText(309, 551, 406, 588, "通关奖励")  # 战斗结束页。宝箱提示
                            if not res6:
                                res7, _ = TomatoOcrText(264, 453, 356, 482, "开启宝箱")  # 战斗结束页。宝箱提示
        if res1 or res2 or res3 or res4 or res5 or res6 or res7:
            isTreasure = 1
        if 功能开关['秘境不开宝箱'] == 1:
            openStatus = 0
            if isTreasure == 1:
                if 功能开关['秘境点赞队友'] == 1:
                    Toast('点赞队友')
                    for i in range(1, 2):
                        # ldE.element('战斗结束-点赞队友1').click().execute(sleep=0.7)
                        # ldE.element('战斗结束-点赞队友2').click().execute(sleep=0.7)
                        tapSleep(300, 520, 0.7)
                        tapSleep(413, 541, 0.7)
                        tapSleep(538, 522, 0.7)
                Toast('返回房间')
                tapSleep(645, 1235, 3)  # 战斗结束页确认不领取
                res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 战斗结束页确认退出
                if not res:
                    res = TomatoOcrTap(96, 1199, 130, 1232, "回")  # 返回
                    res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 确定
                    if not res:
                        res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                    if res:
                        openStatus = 1
                else:
                    openStatus = 1
            return openStatus

        # 点赞队友
        if 功能开关['秘境点赞队友'] == 1:
            if isTreasure == 1:
                Toast('点赞队友')
                for i in range(1, 2):
                    # ldE.element('战斗结束-点赞队友1').click().execute(sleep=0.7)
                    # ldE.element('战斗结束-点赞队友2').click().execute(sleep=0.7)
                    tapSleep(300, 520, 0.7)
                    tapSleep(413, 541, 0.7)
                    tapSleep(538, 522, 0.7)

        attempts = 0  # 初始化尝试次数
        maxAttempts = 3  # 设置最大尝试次数

        openStatus = 0
        if isTreasure == 1:
            while attempts < maxAttempts:
                res, _ = TomatoOcrText(300, 606, 417, 634, "宝箱尚未开启")  # 避免前置错误点击弹出宝箱尚未开启
                if res:
                    res = TomatoOcrTap(99, 1199, 128, 1234, "回")  # 关闭确认弹窗，返回待领取页

                attempts = attempts + 1
                # # 战斗结束页
                # res = TomatoOcrTap(202, 1041, 258, 1068, "开启")  # 战斗页，宝箱1
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # res = TomatoOcrTap(459, 1040, 524, 1068, "开启")  # 战斗页，宝箱2
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # # 结算页
                # # 结算页，单宝箱
                # res = TomatoOcrTap(340, 756, 380, 777, "开启")
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # res = TomatoOcrTap(335, 755, 380, 777, "开启")
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                #
                # # 领取宝箱1
                # res = TomatoOcrTap(214, 748, 257, 767, "开启")
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # # 领取宝箱2
                # res = TomatoOcrTap(460, 747, 503, 767, "开启")
                # if res:
                #     ldE.sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # 图色识别兜底
                res = ldE.element_exist('战斗结束-开启宝箱')
                if res:
                    res.click().execute(sleep=0.7)
                    ldE.sleep(2.5)
                    tapSleep(340, 930)
                    openStatus = 1

                res = ldE.element_exist('战斗结束-开启宝箱2')
                if res:
                    res.click().execute(sleep=0.7)
                    ldE.sleep(2.5)
                    tapSleep(340, 930)
                    openStatus = 1

        if openStatus == 1:
            Toast('开启宝箱 - 成功')

        # 开启宝箱后，返回
        if openStatus == 1 or isTreasure == 1:
            Toast("返回房间")
            res = TomatoOcrTap(96, 1199, 130, 1232, "回")  # 返回
            res = TomatoOcrTap(330, 726, 387, 759, "确定")  # 确定返回
            if not res:
                res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
            if not res:
                # 识别战斗结束页提前返回
                res1 = False
                res2 = False
                res3 = False
                res1, _ = TomatoOcrText(313, 622, 404, 656, "通关奖励")  # 战斗结束页。宝箱提示
                if not res1:
                    res2, _ = TomatoOcrText(312, 563, 404, 596, "通关奖励")  # 战斗结束页。宝箱提示
                if not res2:
                    res3, _ = TomatoOcrText(309, 551, 406, 588, "通关奖励")  # 战斗结束页。宝箱提示
                if res1 or res2 or res3:
                    tapSleep(645, 1235, 3)  # 战斗结束页确认不领取
                    res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 战斗结束页确认退出
                    if not res:
                        res = TomatoOcrTap(96, 1199, 130, 1232, "回")  # 返回
                        res = TomatoOcrTap(329, 728, 386, 759, "确定")  # 确定
                        if not res:
                            res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
                            openStatus = 1
        return openStatus

    # 等待匹配
    def WaitFight(self, fightType='秘境'):
        res1 = TomatoOcrTap(457, 607, 502, 631, "准备")  # 秘境准备
        res2 = TomatoOcrTap(453, 650, 505, 684, "准备")  # 恶龙准备
        res3 = False

        # 队伍满员，开始挑战
        res, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        if res:
            res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
            res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

        if res1 or res2 or res3:
            Toast("匹配成功 - 等待进入战斗")
            totalWait = 20 * 1000
            elapsed = 0
            # 等待进入战斗
            while elapsed <= totalWait:
                if elapsed >= totalWait:
                    Toast("进入战斗失败 - 队友未准备")
                    return False

                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                if teamName1 != '' or teamName2 != '':
                    Toast("进入战斗成功 - 开始战斗", 500)
                    if fightType == "秘境":
                        self.fighting()
                    if fightType == "暴走":
                        self.fightingBaoZou()
                    return True
                ldE.sleep(5)
                elapsed = elapsed + 5 * 1000
        return False

    def fighting(self):
        totalWait = 300 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0
        teamShoutDone = 0

        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            fightStatus = ldE.element_exist('战斗中-喊话')
            if teamName1 != "" or teamName2 != "" or fightStatus:
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()

                # 切换手动操作
                if 功能开关["主动释放技能"] == 1:
                    if 功能开关["三技能自动释放"] == 1:
                        # todo：识别打断条
                        tapSleep(649, 953, 0.6)  # 3技能 # 打断技
                        tapSleep(659, 942, 0.6)  # 3技能 # 打断技
                        re = CompareColors.compare("285,268,#7B7277|293,268,#797373|296,269,#787272|309,271,#746C6A")
                        if re:
                            tapSleep(649, 953, 0.6)  # 3技能 # 护盾技
                            tapSleep(659, 942, 0.6)  # 3技能 # 护盾技
                    else:
                        tapSleep(649, 953, 0.6)  # 3技能
                        tapSleep(659, 942, 0.6)  # 3技能
                    res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                    tapSleep(511, 1076, 0.6)  # 1技能
                    tapSleep(521, 1070, 0.6)  # 1技能
                    tapSleep(543, 974, 0.6)  # 2技能
                    tapSleep(544, 962, 0.6)  # 2技能
                    tapSleep(421, 1077, 0.6)  # 宠物技能
                    tapSleep(426, 1067, 0.6)  # 宠物技能
                else:
                    res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                Toast('战斗中')
            else:
                # 战斗结束
                openStatus = self.openTreasure()
                if openStatus == 1:
                    Toast("战斗结束 - 战斗胜利")
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
                    break
                # 兼容恶龙战斗后领取宝箱页
                # todo：识别战斗结束页
                if 0:
                    tapSleep(112, 818)  # 点击空白处确认
                    Toast("恶龙任务 - 战斗胜利 - 房间页宝箱确认")
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            fightStatus = ldE.element_exist('战斗中-喊话')
            if elapsed > 240 * 1000 or (teamName1 == "" and teamName2 == "" and not fightStatus):
                failStatus = self.fight_fail()
                if failStatus:
                    break
            ldE.sleep(3)
            elapsed = elapsed + 3 * 1000

    def fightingBaoZou(self):
        totalWait = 330 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0

        teamShoutDone = 0
        while 1:
            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1 or (teamName1 != "" or teamName2 != ""):
                # Toast("战斗中")
                功能开关["fighting"] = 1
            else:
                功能开关["fighting"] = 0

            # 战斗逻辑
            # 循环10次，优先处理战斗中走位
            if res1 or (teamName1 != "" or teamName2 != ""):
                for i in range(1, 10):
                    if 功能开关["史莱姆选择"] == '暴走烈焰大王':
                        self.daBaoZouLieYan()

                # 战斗结束
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(332, 1067, 387, 1096, "开启")  # 领取宝箱
                if res2 or res3:
                    Toast("战斗结束 - 战斗胜利")
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(55, 1140)  # 领取后，点击空白
                    break
                ldE.sleep(1)

            # 判断是否战斗失败（战斗5分钟后）
            if res1 or (teamName1 != "" or teamName2 != ""):
                功能开关["fighting"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(332, 1067, 387, 1096, "开启")  # 领取宝箱
                if res1 or res2 or res3:
                    Toast("战斗结束 - 战斗胜利")
                    ldE.sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("战斗结束")
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
        功能开关["fighting"] = 0

    # 大暴走（烈焰大王）
    def daBaoZouLieYan(self):
        for i in range(1, 5):
            def 往左():
                tapSleep(63, 680, 4)

            def 往右():
                tapSleep(148, 675, 4)

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

            # if 功能开关['bossNumber0'] == '' and 功能开关['bossNumber1'] == '' and 功能开关['bossNumber2'] == '':
            #     Toast('等待返回水地块')
            #     for i in range(1, 3):
            #         # 返回水地块
            #         isShui1 = ldE.element_exist('暴走-水地块')
            #         isShui2 = ldE.element_exist('暴走-水地块2')
            #         isShui3 = ldE.element_exist('暴走-水地块3')
            #         isShui4 =  FindColors.find("532,751,#D2E4E8|542,749,#67BBD2|563,751,#6EC3D8|570,744,#5BB2CB|575,734,#4DA3BF|552,735,#68AAC1")
            #         if not isShui1 and not isShui2 and not isShui3 and not isShui4:
            #             往左()
            #         else:
            #             Toast('已返回水地块')
            #             break

    def teamShout(self):
        if 功能开关['喊话内容'] == "":
            return 1

        Toast("队伍发言")

        res1 = TomatoOcrTap(19, 1104, 94, 1128, "点击输入")
        res2 = False
        if not res1:
            res2 = TomatoOcrTap(19, 1102, 90, 1127, "点击输入")
        ldE.sleep(2.5)  # 等待输入法弹窗
        if res1 or res2:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            ldE.sleep(1)
            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
            action.input(功能开关["喊话内容"])
            tapSleep(360, 104)  # 点击空白处确认输入
            res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
            if res:
                # todo 确认关闭聊天框
                return 1

        # todo 确认关闭聊天框
        return 0

    # 战斗中退出组队
    def quitTeamFighting(self):
        res = TomatoOcrTap(649, 319, 694, 342, "队伍")
        if res:
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍")
            res = TomatoOcrTap(329, 726, 391, 761, "确定")

    def fight_fail(self):
        res1, _ = TomatoOcrText(246, 459, 327, 482, "你被击败了")
        res2, _ = TomatoOcrText(475, 1038, 527, 1065, "放弃")
        if res1 or res2:
            Toast("战斗结束 - 战斗失败")
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            self.quitTeamFighting()  # 退出队伍
            return True
        return False

    def homePage(self):
        while True:
            res6 = self.WaitFight()

            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            return3 = ldE.element_exist('返回-3')
            if return3:
                return3.click(rx=5, ry=5).execute(sleep=1)
                Toast('返回首页')

            # 判断是否已在首页
            res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1 = ldE.element_exist('首页-冒险手册')
                if not shou_ye1:
                    shou_ye2 = ldE.element_exist('首页-新手试炼')
            if res2 or shou_ye1 or shou_ye2:
                with switch_lock:
                    功能开关["needHome"] = 0
                功能开关["fighting"] = 0
                Toast('已返回首页')
                ldE.sleep(0.5)
                return True

            # 开始异步处理返回首页
            with switch_lock:
                if not thread2.is_alive():
                    runThread2()
                功能开关["needHome"] = 1

            # 点击首页-冒险
            ldE.element('首页-冒险').click().execute(sleep=1)

            quitTeamRe = self.quitTeamFighting()
            if not quitTeamRe:
                # 判断战败页面
                self.fight_fail()

            # 判断宝箱开启
            self.openTreasure()
            ldE.sleep(0.5)

    def quitTeam(self):
        res1 = False
        res2 = False
        res3 = False
        res4 = False
        res1 = TomatoOcrTap(635, 628, 705, 653, "正在组队")
        if not res1:
            res2 = TomatoOcrTap(631, 558, 699, 581, "正在组队")
            if not res2:
                res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
                if not res3:
                    res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中")  # 大暴走匹配中
        if res1 or res2 or res3 or res4:
            功能开关["needHome"] = 0
            teamStatus = ldE.element_exist('队伍-匹配中')
            if teamStatus:
                teamStatus.click().execute(sleep=1)
                Toast('取消匹配')

            res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中")  # 大暴走匹配中
            if res4:
                Toast("取消匹配")
                return True
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍")
            if not res:
                tapSleep(540, 200, 0.8)
            res = TomatoOcrTap(329, 726, 391, 761, "确定")
            if not res:
                tapSleep(360, 740, 0.8)
            if res:
                Toast("退出组队")
                return True
        return False
