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
        }

        self.SkillChongWuFlag = False
        self.SkillChongWuTime = safe_int_v2(功能开关['宠物技能释放间隔'])
        self.Skill1Flag = False
        self.Skill1Time = safe_int_v2(功能开关['技能1释放间隔'])
        self.Skill2Flag = False
        self.Skill2Time = safe_int_v2(功能开关['技能2释放间隔'])
        self.Skill3Flag = False
        self.Skill3Time = safe_int_v2(功能开关['技能3释放间隔'])
        self.SkillCount = 0
        self.SkillNeedCount = safe_int_v2(功能开关['技能释放循环次数'])
        self.SkillTimeNeedInit = 1
        if self.SkillNeedCount == 0:
            self.SkillNeedCount = 1

    def initAutoSkill(self):
        self.SkillChongWuFlag = False
        self.SkillChongWuTime = safe_int_v2(功能开关['宠物技能释放间隔'])
        self.Skill1Flag = False
        self.Skill1Time = safe_int_v2(功能开关['技能1释放间隔'])
        self.Skill2Flag = False
        self.Skill2Time = safe_int_v2(功能开关['技能2释放间隔'])
        self.Skill3Flag = False
        self.Skill3Time = safe_int_v2(功能开关['技能3释放间隔'])
        self.SkillCount = 0
        self.SkillNeedCount = safe_int_v2(功能开关['技能释放循环次数'])
        self.SkillTimeNeedInit = 1
        if self.SkillNeedCount == 0:
            self.SkillNeedCount = 1

    def shilian(self):
        if 功能开关['大暴走开关'] == 1 and 功能开关['暴走自动接收邀请'] == 0:
            self.daBaoZou()

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
            self.elong()
            # 兜个底
            self.homePage()
            self.quitTeam()

        if 功能开关['梦魇开关'] == 1 and 功能开关['梦魇自动接收邀请'] == 0:
            self.mengYan()
            # 兜个底
            self.homePage()
            self.quitTeam()

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
                fightStatu2, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
                if "等级" in teamName1 or "等级" in teamName2 or fightStatus or fightStatu2:
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

        # 结算前一次的宝箱（兜底）
        res = TomatoOcrTap(333, 715, 384, 745, "开启")  # 领取宝箱
        if not res:
            res = TomatoOcrTap(330, 752, 388, 782, "开启")  # 领取宝箱
        if res:
            Toast("开启宝箱")
            sleep(2)
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白
            tapSleep(125, 1050)  # 领取后，点击空白

        hdPage, _ = TomatoOcrText(279, 574, 440, 606, 功能开关['史莱姆选择'])
        if not hdPage:
            name = 功能开关['史莱姆选择']
            Toast(f'大暴走 - 选择({name})未开启 - 请检查')
            sleep(2)
            return

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
            re, level = TomatoOcrText(118, 1021, 202, 1046, "阶段")
            level = level.replace("阶", "")
            level = safe_int_v2(level)
            if level >= toLevel:
                Toast("大暴走 - 已达到目标等阶")
                任务记录["大暴走-完成"] = 1
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

            Toast(f"大暴走任务 - 匹配中 - 等待{elapsed // 1000}/150s")
            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(231, 624, 305, 645, "匹配超时")
            if res:
                Toast("大暴走 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(451, 727, 510, 757, "确定")
                # if res:
                # elapsed = 0

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

            sleep(5)
            elapsed = elapsed + 5 * 1000

    # 梦魇狂潮
    def mengYan(self):
        Toast('梦魇任务 - 开始')
        self.homePage()
        self.quitTeam()
        res = TomatoOcrTap(650, 522, 688, 544, "试炼")
        if res:
            re = imageFindClick('梦魇狂潮', sleep1=2.5, x1=101, y1=140, x2=618, y2=1087)
            if not re:
                Toast("秘境任务 - 未找到梦魇入口 - 重新尝试")
                return
        else:
            Toast("秘境任务 - 未找到试炼入口 - 重新尝试")
            return

        # 判断是否添加佣兵
        if 功能开关["梦魇添加佣兵"] == 1:
            Toast("梦魇任务 - 添加佣兵")
            re = imageFindClick('秘境-创建队伍', confidence1=0.85)
            if re:
                tapSleep(554, 858)  # 点击 创建队伍 - 添加佣兵
                TomatoOcrFindRangeClick("创建队伍", 0.9, 0.9, 60, 511, 652, 1153)
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                return self.fighting()

        # 开始匹配
        re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
        if re1:
            res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
            if res:
                Toast("梦魇任务 - 选择职业")
                if 功能开关["职能优先输出"] == 1:
                    tapSleep(280, 665)  # 职能输出
                elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                    tapSleep(435, 665)  # 坦克
                else:
                    tapSleep(280, 665)  # 职能输出
                res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                Toast("梦魇任务 - 匹配超时")

                teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中')
                teamStatus2 = imageFindClick('队伍-匹配中')
                if teamStatus1 or teamStatus2:
                    Toast('梦魇任务 - 匹配超时 - 取消匹配')
                break

            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(229, 621, 305, 646, "匹配超时")
            if res:
                res = TomatoOcrTap(454, 727, 508, 758, "确定")
                if res:
                    Toast("梦魇任务 - 匹配超时 - 无队伍")
                    elapsed = 0

            waitStatus1 = TomatoOcrFindRange('匹配中')
            waitStatus2, x, y = imageFind('队伍-匹配中')
            res1 = self.WaitFight()
            # if res1:
            #     任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
            if res1 == True or (not waitStatus1 and not waitStatus2):  # 成功准备战斗 或 未匹配到
                break

            elapsed = elapsed + 5
            Toast(f"匹配中,已等待{round(elapsed / 60, 2)}/{totalWait / 60}分")
            sleep(5)

    # 恶龙大通缉
    def elong(self):
        if 任务记录['恶龙任务'] == 1:
            return

        Toast('恶龙任务 - 开始')
        self.homePage()
        self.quitTeam()
        res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
        if res:
            re = imageFindClick('恶龙大通缉', x1=101, y1=140, x2=618, y2=1087, confidence1=0.7)
            if not re:
                Toast("秘境任务 - 未找到恶龙入口 - 重新尝试")
                return self.elong()

        # 判断是否重复挑战（已开启过宝箱）
        re1, x, y = imageFind('恶龙-宝箱金币')
        # re1 = TomatoOcrFindRange('最高', match_mode='fuzzy')
        if re1:
            if 功能开关["恶龙重复挑战"] == 0:
                Toast("恶龙任务 - 已领取宝箱 - 退出挑战")
                任务记录['恶龙任务'] = 1
                sleep(1.5)
                return

        # 判断是否添加佣兵
        if 功能开关["恶龙添加佣兵"] == 1:
            Toast("恶龙任务 - 添加佣兵")
            re = imageFindClick('秘境-创建队伍', confidence1=0.8)
            if re:
                tapSleep(551, 858)  # 点击 创建队伍 - 添加佣兵
                res = TomatoOcrTap(311, 915, 407, 950, "创建队伍", 10, 10, sleep1=1.5)  # 创建队伍 - 创建队伍
                res = TomatoOcrTap(326, 969, 390, 1000, "开始", 10, 10, sleep1=1.5)
                if not res:
                    res = TomatoOcrFindRangeClick("开始", x1=232, y1=885, x2=484, y2=1123, offsetX=10, offsetY=10,
                                                  sleep1=1.5)
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
                return self.fighting()

        # 开始匹配
        re1 = TomatoOcrFindRangeClick('开始匹配', whiteList='开始匹配')
        if re1:
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
                res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                Toast("恶龙任务 - 匹配超时")

                teamStatus1 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中')
                teamStatus2 = imageFindClick('队伍-匹配中')
                if teamStatus1 or teamStatus2:
                    Toast('恶龙任务 - 匹配超时 - 取消匹配')
                break

            # 判断无合适队伍，重新开始匹配
            res, _ = TomatoOcrText(229, 621, 305, 646, "匹配超时")
            if res:
                res = TomatoOcrTap(454, 727, 508, 758, "确定")
                if res:
                    Toast("恶龙任务 - 匹配超时 - 无队伍")
                    elapsed = 0

            waitStatus1 = TomatoOcrFindRange('匹配中')
            waitStatus2, x, y = imageFind('队伍-匹配中')
            res1 = self.WaitFight()
            if res1:
                任务记录["试炼-恶龙-完成次数"] = 任务记录["试炼-恶龙-完成次数"] + 1
            if res1 == True or (not waitStatus1 and not waitStatus2):  # 成功准备战斗 或 未匹配到
                break

            sleep(5)
            elapsed = elapsed + 5 * 1000

    def mijing(self):
        if 任务记录['试炼-秘境-体力消耗完成'] == 1 and 功能开关["秘境无体力继续"] == 0:
            return

        Toast('秘境任务 - 开始')

        selectMap = 功能开关['秘境地图']
        selectStage = 功能开关['秘境关卡']

        isFind = False
        for k in range(4):
            self.homePage()
            self.quitTeam()
            res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
            if res:
                re = imageFindClick('秘境之间', x1=85, y1=53, x2=636, y2=700)
                if re:
                    isFind = True
                    break
                if not re:
                    re = imageFindClick('秘境之间', x1=374, y1=101, x2=562, y2=156, confidence1=0.8)
                if not re:
                    Toast("秘境任务 - 未找到试炼入口 - 重新尝试")
                    res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）
            else:
                Toast("秘境任务 - 未找到试炼入口 - 重新尝试")
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李")  # 尝试点击旅人切换页面，解决长时间停留首页，试炼按钮异常消失的情况（反作弊策略？）

        if not isFind:
            return

        self.openTreasure()

        # 判断是否已在当前地图
        if selectMap != '最新地图':
            res = TomatoOcrFindRange(selectMap, x1=80, y1=214, x2=637, y2=599, match_mode='fuzzy')
            if not res:
                res = self.changeMap(selectMap, selectStage)
                if not res:
                    return
        else:
            Toast('默认挑战最新关卡')
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
                sleep(2)
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

                tapSleep(549, 857)  # 点击 创建队伍 - 添加佣兵
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
                re2 = TomatoOcrFindRangeClick('创建队伍', whiteList='创建队伍', offsetX=10, offsetY=10)
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
                while 1:
                    功能开关["fighting"] = 0
                    self.openTreasure()
                    # 返回房间
                    res1 = TomatoOcrTap(618, 552, 686, 585, "正在组队")
                    if not res1:
                        res2 = TomatoOcrTap(551, 595, 597, 617, "秘境")
                        if not res2:
                            res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
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
                        res = TomatoOcrFindRange('点击空白处', 0.9, 113, 831, 720, 1280, whiteList='点击空白处')
                        if res:
                            tapSleep(45, 1245)
                            Toast('关闭弹窗')
                        res, _ = TomatoOcrText(502, 192, 581, 215, "离开队伍")
                        if not res:
                            sleep(3)
                            failTeamStatus = failTeamStatus + 1
                            if failTeamStatus > 3:
                                Toast("秘境任务 - 已离开队伍 - 结束")
                                break
                    else:
                        failTeamStatus = 0

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
                    Toast(f"秘境任务 - 创建房间 - 等待队友{elapsed}/120s")
                    # 检查是否队友全为佣兵
                    if elapsed < 20:
                        # 等待队友结算完成
                        self.quitAi()

                    res = TomatoOcrTap(333, 974, 383, 1006, "开始")
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
                                re2 = TomatoOcrTap(72, 1199, 124, 1232, '返回', sleep1=0.6)
                                if not re2:
                                    tapSleep(91, 1210)
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
                            if wait1:
                                Toast('队友离开，重新等待')
                                break
                            waitTime = 3 * i
                            Toast(f"秘境任务 - 匹配成功 - 等待进入战斗 - {waitTime}/45s")
                            sleep(3)

                            if i == 14:
                                Toast(f"秘境任务 - 匹配成功 - 等待进入战斗失败 - 重新等待队友")
                                sleep(1)

                            # 返回房间
                            res1 = TomatoOcrTap(635, 628, 705, 653, "正在组队")
                            if not res1:
                                res2 = TomatoOcrTap(551, 595, 597, 617, "秘境")
                                if not res2:
                                    res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")

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
                            if "等级" in teamName1 or "等级" in teamName2:
                                Toast("秘境任务 - 匹配成功 - 进入战斗")
                                self.fighting()
                                sleep(2)
                                self.quitAi()
                                aleadyFightCt = aleadyFightCt + 1
                                功能开关["fighting"] = 0
                                elapsed = 0  # 初始化等待队员时间
                                fightDone = 1
                                break
                    # 等待队员
                    sleep(2)
                    elapsed = elapsed + 2
            return

        resStart1 = TomatoOcrTap(311, 697, 405, 725, "开始匹配", sleep1=0.8)  # 图1
        resStart2 = False
        resStart3 = False
        resStart4 = False
        if not resStart1:
            resStart2 = TomatoOcrTap(309, 892, 407, 918, "开始匹配", sleep1=0.8)  # 图2
            if not resStart2:
                resStart3 = TomatoOcrTap(311, 1084, 405, 1116, "开始匹配", sleep1=0.8)  # 图3
                if not resStart3:
                    resStart4 = TomatoOcrFindRangeClick("开始匹配", x1=83, y1=260, x2=650, y2=1137)

        if not resStart1 and not resStart2 and not resStart3 and not resStart4:
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
                res = TomatoOcrTap(64, 1200, 128, 1234, "返回", 10, 10)
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
            res = TomatoOcrTap(332, 754, 387, 789, "确定", sleep1=0.8)

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
                        if not res4:
                            TomatoOcrFindRangeClick("匹配中", x1=83, y1=260, x2=650, y2=1137)
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
                        res5 = TomatoOcrFindRange("匹配中", x1=83, y1=260, x2=650, y2=1137)

            res1 = self.WaitFight()
            if res1 == True or (res2 == False and res3 == False and res4 == False and res5 == False):  # 成功准备战斗 或 未匹配到
                break

            sleep(5)
            elapsed = elapsed + 5 * 1000

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

        resJ, _ = TomatoOcrText(346, 811, 376, 825, '镜像')  # 第二位队友为镜像
        if resJ:
            Toast('等待不足20s，踢出佣兵')
            tapSleep(353, 800)
            tapSleep(353, 800)

        resJ, _ = TomatoOcrText(503, 810, 532, 825, '镜像')  # 第三位队友为镜像
        if resJ:
            Toast('等待不足20s，踢出佣兵')
            tapSleep(513, 806)
            tapSleep(513, 806)

    def tili(self):
        Toast("体力购买 - 开始")
        tapSleep(690, 90)  # 点击补充体力加号
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

        Toast("体力购买 - 结束")
        tapSleep(61, 1187)  # 返回

        # 切换地图

    def changeMap(self, selectMap, selectStage):
        Toast("秘境任务 - 切换地图")
        tapSleep(74, 160, 1.5)  # 点击地图列表
        res = CompareColors.compare("254,650,#BBBBBB|251,643,#BDBDBD|246,637,#BDBDBC|254,632,#BFBFBE|255,628,#BDBDBD")
        if not res:
            tapSleep(74, 160, 2)  # 点击地图列表
        # mapPoi = self.mapPoi[selectMap]
        maps_to_check = ('原野', '森林', '沙漠', '海湾', '深林', '冰原', '火山', '高原', '绿洲')
        if selectMap not in maps_to_check:
            swipe(150, 1000, 150, 300)
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
        res = TomatoOcrFindRange(selectMap, x1=80, y1=214, x2=637, y2=599, match_mode='fuzzy')
        if res:
            return True
        else:
            Toast(f'切换地图失败')
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
        # res1, _ = TomatoOcrText(313, 622, 404, 656, "通关奖励")  # 战斗结束页。宝箱提示
        bitmap = screen.capture(x=108, y=462, x1=618, y1=1120)
        res1 = TomatoOcrFindRange("", x1=108, y1=462, x2=618, y2=1120,
                                  bitmap=bitmap, keywords=[{'keyword': '通关奖励', 'match_mode': 'fuzzy'},
                                                           {'keyword': '开启', 'match_mode': 'fuzzy'}])  # 战斗结束页。宝箱提示
        # if not res1:
        # res2, _ = TomatoOcrText(267, 755, 313, 783, "开启")  # 战斗结束页。宝箱提示
        # res2 = TomatoOcrFindRange("开启", x1=108, y1=462, x2=618, y2=1120, match_mode='fuzzy',
        #                           bitmap=bitmap)  # 战斗结束页。宝箱提示
        # if not res2:
        # res3, _ = TomatoOcrText(273, 397, 360, 425, "是否开启")  # 结算页，宝箱提示
        # res3 = TomatoOcrFindRange("是否开启", x1=108, y1=462, x2=618, y2=1120)  # 结算页，宝箱提示
        if res1 or res2 or res3:
            isTreasure = 1
        if 功能开关['秘境不开宝箱'] == 1:
            openStatus = 0
            if isTreasure == 1:
                if 功能开关['秘境点赞队友'] == 1:
                    Toast('点赞队友')
                    res = TomatoOcrTap(514, 511, 592, 538, "一键全赞", 5, 5)  # 一键点赞
                    if not res:
                        res = TomatoOcrTap(513, 570, 594, 594, "一键全赞", 5, 5)  # 一键点赞
                    if not res:
                        for i in range(1, 4):
                            imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                            imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                Toast('返回房间')
                # 加锁兜底
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                tapSleep(645, 1235, 0.5)  # 战斗结束页确认不领取
                res = TomatoOcrTap(329, 728, 389, 758, "确定", 10, 10)  # 确定
                if not res:
                    tapSleep(645, 1235, 1)  # 战斗结束页确认不领取
                    res = TomatoOcrTap(329, 728, 389, 758, "确定", 10, 10)  # 确定
                if not res:
                    Toast('返回房间-2')
                    res = TomatoOcrTap(96, 1199, 130, 1232, "回", 10, 10, 0.8)  # 返回
                    res = TomatoOcrTap(329, 728, 386, 759, "确定", 10, 10)  # 确定
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
            return openStatus

        # 点赞队友
        if 功能开关['秘境点赞队友'] == 1:
            if isTreasure == 1:
                Toast('点赞队友')
                res = TomatoOcrTap(514, 511, 592, 538, "一键全赞", 5, 5)  # 一键点赞
                if not res:
                    res = TomatoOcrTap(513, 570, 594, 594, "一键全赞", 5, 5)  # 一键点赞
                if not res:
                    for i in range(1, 4):
                        imageFindClick('点赞1', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)
                        imageFindClick('点赞2', confidence1=0.8, x1=107, y1=279, x2=633, y2=809, sleep1=0.7)

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
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # res = TomatoOcrTap(459, 1040, 524, 1068, "开启")  # 战斗页，宝箱2
                # if res:
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # # 结算页
                # # 结算页，单宝箱
                # res = TomatoOcrTap(340, 756, 380, 777, "开启")
                # if res:
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # res = TomatoOcrTap(335, 755, 380, 777, "开启")
                # if res:
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                #
                # # 领取宝箱1
                # res = TomatoOcrTap(214, 748, 257, 767, "开启")
                # if res:
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # # 领取宝箱2
                # res = TomatoOcrTap(460, 747, 503, 767, "开启")
                # if res:
                #     sleep(3.5)
                #     tapSleep(340, 930)
                #     openStatus = 1
                # 图色识别兜底
                res = imageFindClick('宝箱-开启')
                if res:
                    sleep(2)
                    tapSleep(340, 930)
                    openStatus = 1

                res = imageFindClick('宝箱-开启2')
                if res:
                    sleep(2)
                    tapSleep(340, 930)
                    openStatus = 1

        if openStatus == 1:
            Toast('开启宝箱 - 成功')

        # 开启宝箱后，返回
        if openStatus == 1 or isTreasure == 1:
            Toast("返回房间")
            res = TomatoOcrTap(96, 1199, 130, 1232, "回", sleep1=0.8)  # 返回
            res = TomatoOcrTap(330, 726, 387, 759, "确定")  # 确定返回
            if not res:
                res = TomatoOcrTap(331, 727, 388, 761, "确定")  # 确定返回
            if not res:
                # 识别战斗结束页提前返回
                res1 = False
                res1 = TomatoOcrFindRange("通关奖励", x1=112, y1=456, x2=620, y2=1032)  # 战斗结束页。宝箱提示
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
        return openStatus

    # 等待匹配
    def WaitFight(self, fightType='秘境'):
        res1 = TomatoOcrTap(457, 607, 502, 631, "准备")  # 秘境准备
        res2 = TomatoOcrTap(453, 650, 505, 684, "准备")  # 恶龙准备
        res3 = False
        res4 = False
        if not res1 and not res2:
            res4 = TomatoOcrFindRangeClick('准备', x1=94, y1=276, x2=633, y2=1089)  # 全屏识别准备按钮

        # 队伍满员，开始挑战
        res, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        if res:
            res = TomatoOcrTap(455, 726, 509, 760, "确定")  # 队伍已满员，准备开启挑战 - 确定
            res3 = TomatoOcrTap(333, 974, 383, 1006, "开始")

        if res1 or res2 or res3 or res4:
            Toast("匹配成功 - 等待进入战斗")
            totalWait = 20 * 1000
            elapsed = 0
            # 等待进入战斗
            while elapsed <= totalWait:
                if elapsed >= totalWait:
                    Toast("进入战斗失败 - 队友未准备")
                    return False

                TomatoOcrFindRangeClick('跳过', sleep1=1, confidence1=0.9, x1=522, y1=17, x2=685, y2=110, offsetX=10,
                                        offsetY=10)
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
                Toast("等待进入战斗")
                if "等级" in teamName1 or "等级" in teamName2:
                    Toast("进入战斗成功 - 开始战斗", 500)
                    if fightType == "秘境" or fightType == "秘境带队":
                        self.fighting(fightType)
                    if fightType == "暴走":
                        self.fightingBaoZou()
                    if fightType == "梦魇带队" or fightType == "梦魇挑战":
                        self.fightingMengYanTeam(fightType)
                    if fightType == "恶龙带队" or fightType == "恶龙挑战":
                        self.fightingELongTeam(fightType)
                    if fightType == "绝境带队":
                        self.fightingJueJingTeam()
                    if fightType == "终末战带队":
                        self.fightingZhongMoTeam()
                    if fightType == "调查队带队":
                        self.fightingDiaoChaTeam()
                    if fightType == "暴走带队":
                        self.fightingBaoZouTeam()
                    return True
                res = TomatoOcrTap(333, 974, 383, 1006, "开始")
                TomatoOcrFindRangeClick('准备')  # 避免点击开始瞬间队友离队，错误点击了开始匹配，兜底准备按钮
                sleep(1)
                elapsed = elapsed + 1 * 1000
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

    def fightingBaoZouTeam(self):
        totalWait = 30
        elapsed = 0
        teamShoutDone = 0
        if 功能开关["暴走自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["暴走自动离队时间"])
            if totalWait == 0:
                totalWait = 30
        Toast("战斗开始 - 暴走组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 暴走超时退出组队")
                self.teamShoutAI(f'大暴走-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                功能开关["fighting_baozou"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                功能开关["fighting_baozou"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                功能开关["fighting_baozou"] = 1
                Toast(f'暴走战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    self.teamShoutAI(f'大暴走-开始战斗-留镜像后离队,0/{totalWait}秒~祝你武运昌隆~', shoutType="fight")
                    teamName = 任务记录['房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")

                # 战斗逻辑
                for i in range(1, 10):
                    if 功能开关["史莱姆选择"] == '暴走雷电大王':
                        self.daBaoZouLeidian()
                    if 功能开关["史莱姆选择"] == '暴走烈焰大王':
                        self.daBaoZouLieYan()
                    if 功能开关["史莱姆选择"] == '暴走深林大王':
                        self.daBaoZouShenLin()
                    if 功能开关["史莱姆选择"] == '暴走水波大王':
                        self.daBaoZouShuiBo()
                sleep(0.5)
            else:
                # 战斗结束
                openStatus = self.openTreasure()
                if openStatus == 1:
                    Toast("暴走战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

                # 兼容恶龙战斗结算页
                res = TomatoOcrTap(322, 1049, 394, 1077, "开启")
                if res:
                    tapSleep(365, 1135)
                    tapSleep(365, 1135)
                    tapSleep(365, 1135)
                    tapSleep(365, 1135, 3)
                else:
                    tapSleep(365, 1135, 3)
                Toast("暴走任务 - 战斗胜利 - 结算页返回房间")
                break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            if elapsed > 180 * 1000 or ("等级" not in teamName1 and "等级" not in teamName2):
                Toast(f"暴走战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"暴走战斗中状态 - 识别失败 - 退出战斗")
                    功能开关["fighting_baozou"] = 0
                    break
                if failNum > 7:
                    failStatus = self.fight_fail()
                    功能开关["fighting_baozou"] = 0
                    break
            sleep(3)
            elapsed = elapsed + 4

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
            if "等级" in teamName1 or "等级" in teamName2:
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
            if elapsed > 240 * 1000 or ("等级" not in teamName1 and "等级" not in teamName2):
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
            elapsed = elapsed + 4

    def fightingJueJingTeam(self):
        totalWait = 90
        if 功能开关["绝境自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["绝境自动离队时间"])
            if totalWait == 0:
                totalWait = 90
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 绝境组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 绝境超时退出组队")
                self.teamShoutAI(f'绝境-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break
            if elapsed >= 15:
                self.teamShoutAI(f'绝境-战斗即将结束-期待下次相遇', shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'绝境战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    self.teamShoutAI(f'绝境-开始战斗~祝你武运昌隆~', shoutType="fight")
                    teamName = 任务记录['房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                self.AIContent()
            else:
                # 战斗结束
                # 战斗结束
                res, _ = TomatoOcrText(303, 962, 412, 1002, "通关奖励")
                if res:
                    tapSleep(364, 1136, 0.3)
                    tapSleep(364, 1136, 0.3)
                    Toast("绝境战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if elapsed > 180 or ("等级" not in teamName1 and "等级" not in teamName2):
                Toast(f"绝境战斗中状态 - 识别失败 - 次数 {failNum}/5")
                failNum = failNum + 1
                if failNum > 3:
                    Toast(f"绝境战斗中状态 - 识别失败 - 退出战斗")
                if failNum > 5:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break

            # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
            allQuit = self.allQuit()
            if allQuit:
                break
            sleep(3)
            elapsed = elapsed + 4

    def fightingZhongMoTeam(self):
        totalWait = 90
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 终末战组队邀请")
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 终末战超时退出组队")
                self.teamShoutAI(f'终末战-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            if elapsed >= 15:
                self.teamShoutAI(f'终末战-战斗即将结束-期待下次相遇', shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2:
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'终末战战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    self.teamShoutAI(f'终末战-开始战斗~祝你武运昌隆~', shoutType="fight")
                    teamName = 任务记录['房主名称']
                    teamCount = 任务记录['带队次数']
                    self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                self.AIContent()
            else:
                # 战斗结束
                res, _ = TomatoOcrText(303, 962, 412, 1002, "通关奖励")
                if res:
                    tapSleep(364, 1136, 0.3)
                    tapSleep(364, 1136, 0.3)
                    Toast("终末战战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if elapsed > 180 or ("等级" not in teamName1 and "等级" not in teamName2):
                Toast(f"终末战战斗中状态 - 识别失败 - 次数 {failNum}/8")
                failNum = failNum + 1
                if failNum > 7:
                    Toast(f"终末战战斗中状态 - 识别失败 - 退出战斗")
                if failNum > 9:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break

            # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
            allQuit = self.allQuit()
            if allQuit:
                break
            sleep(3)
            elapsed = elapsed + 4

    def fightingELongTeam(self, fightType='恶龙带队'):
        totalWait = 30
        if fightType == '恶龙挑战':
            totalWait = 360
        if 功能开关["恶龙自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["恶龙自动离队时间"])
            if totalWait == 0:
                totalWait = 30
                if fightType == '恶龙挑战':
                    totalWait = 360
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 恶龙组队邀请")
        self.changeChongWu(fightType)
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 恶龙超时退出组队")
                self.teamShoutAI(f'恶龙-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            if elapsed >= 15:
                self.teamShoutAI(f'恶龙-战斗即将结束-期待下次相遇', shoutType="fight")

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2:
                Toast(f'恶龙战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    if fightType == '恶龙挑战':
                        self.teamShoutAI(f'恶龙-开始战斗-等待战斗结束,0/{totalWait}秒~祝你武运昌隆~', shoutType="fight")
                        teamName = 任务记录['房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                    else:
                        self.teamShoutAI(f'恶龙-开始战斗-留镜像后离队,0/{totalWait}秒~祝你武运昌隆~', shoutType="fight")
                        teamName = 任务记录['房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                self.AIContent()
            else:
                # 战斗结束
                # 兼容恶龙战斗结算页
                res, _ = TomatoOcrText(301, 577, 412, 613, "战斗详情")
                if res:
                    res = TomatoOcrTap(331, 1049, 385, 1077, "开启")
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

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if elapsed > 180 or ("等级" not in teamName1 and "等级" not in teamName2):
                Toast(f"恶龙战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"恶龙战斗中状态 - 识别失败 - 退出战斗")
                if failNum > 10:
                    self.fight_fail()
                    功能开关["fighting"] = 0
                    break
            sleep(3)
            elapsed = elapsed + 4

    def fightingMengYanTeam(self, fightType='梦魇带队'):
        totalWait = 30  # 30000 毫秒 = 30 秒
        if fightType == '梦魇挑战':
            totalWait = 360
        if 功能开关["梦魇自动离队时间"] != "":
            totalWait = safe_int_v2(功能开关["梦魇自动离队时间"])
            if totalWait == 0:
                totalWait = 30
                if fightType == '梦魇挑战':
                    totalWait = 360
        elapsed = 0
        teamShoutDone = 0

        Toast("战斗开始 - 梦魇组队邀请")
        self.changeChongWu(fightType)
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.teamShoutAI(f'梦魇-即将离队-期待下次相遇', shoutType="fight")
                功能开关["fighting"] = 1
                sleep(2)
                self.quitTeamFighting()  # 退出队伍
                功能开关["fighting"] = 0
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res3 = TomatoOcrTap(327, 1205, 389, 1233, "冒险")
            if "等级" in teamName1 or "等级" in teamName2:
                # if teamShoutDone == 0:
                #     teamShoutDone = self.teamShout()
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                Toast(f'梦魇战斗中,战斗时长{elapsed}/{totalWait}秒')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    if fightType == '梦魇挑战':
                        self.teamShoutAI(f'梦魇-开始战斗-等待战斗结束,0/{totalWait}秒~祝你武运昌隆~', shoutType="fight")
                        teamName = 任务记录['房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                    else:
                        self.teamShoutAI(f'梦魇-开始战斗-留镜像后离队,0/{totalWait}秒~祝你武运昌隆~', shoutType="fight")
                        teamName = 任务记录['房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                self.AIContent()
            else:
                # 战斗结束
                openStatus = self.openTreasure()
                if openStatus == 1:
                    Toast("梦魇战斗结束 - 战斗胜利")
                    功能开关["fighting"] = 0
                    break

                res, _ = TomatoOcrText(307, 929, 410, 964, "通关奖励")
                if res:
                    tapSleep(358, 1137, 3)
                    Toast("梦魇任务 - 战斗胜利 - 结算页返回房间")
                    功能开关["fighting"] = 0
                    break

            # 判断是否战斗失败（战斗4分钟后）
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if elapsed > 180 or ("等级" not in teamName1 and "等级" not in teamName2):
                Toast(f"梦魇战斗中状态 - 识别失败 - 次数 {failNum}/4")
                failNum = failNum + 1
                if failNum > 4:
                    Toast(f"梦魇战斗中状态 - 识别失败 - 退出战斗")
                    break
                if failNum > 7:
                    failStatus = self.fight_fail()
                    break
            sleep(3)
            elapsed = elapsed + 4

    def fighting(self, fightType='秘境'):
        totalWait = 240  # 30000 毫秒 = 30 秒
        elapsed = 0
        teamShoutDone = 0

        failNum = 0  # 战斗中状态识别失败次数

        self.initAutoSkill()

        TomatoOcrFindRangeClick('跳过', sleep1=1, confidence1=0.9, x1=522, y1=17, x2=685, y2=110, offsetX=10,
                                offsetY=10)

        任务记录['战斗-上一次移动'] = time.time()
        while 1:
            if elapsed >= totalWait:
                Toast("战斗结束 - 超时退出组队")
                self.quitTeamFighting()  # 退出队伍
                break

            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if "等级" in teamName1 or "等级" in teamName2:
                Toast(f'秘境战斗中,战斗时长{elapsed}/{totalWait}秒')
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
                    if fightType == '秘境带队':
                        self.teamShoutAI(f'秘境-开始战斗-~祝你武运昌隆~', shoutType="fight")
                        teamName = 任务记录['房主名称']
                        teamCount = 任务记录['带队次数']
                        self.teamShoutAI(f'{teamName}-第{teamCount}次相遇~祝你游戏开心~', shoutType="fight")
                if elapsed > 15 and fightType == '秘境带队':
                    self.teamShoutAI("秘境-战斗即将结束-期待下次相遇", shoutType="fight")
                self.AIContent()
                # 切换攻击目标
                point = FindColors.find(
                    "580,547,#7DA2E2|581,556,#7DA2E2|565,555,#7BA0E0|596,558,#7DA2E2|584,571,#7DA1E2",
                    rect=[74, 273, 642, 729])
                if point:
                    print(point.x, point.y)
                    tapSleep(point.x, point.y)
                # 移动走位
                if time.time() - 任务记录['战斗-上一次移动'] > 8:
                    imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
                    任务记录['战斗-上一次移动'] = time.time()

                # 切换手动操作
                if 功能开关["主动释放技能"] == 1:
                    self.autoSkill()
                else:
                    res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
            else:
                # 战斗结束
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
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            if elapsed > 200 or ("等级" not in teamName1 and "等级" not in teamName2):
                shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                if shou_ye1:
                    break
                failNum = failNum + 1
                if failNum > 8:
                    Toast(f"战斗中状态 - 识别失败 - {failNum}/15")
                if failNum > 13:
                    Toast(f"战斗中状态 - 识别失败 - 退出战斗")
                    failStatus = self.fight_fail()
                    if failStatus:
                        break
                    break
            else:
                # 重置战败计算
                failNum = 0

            # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)
            allQuit = self.allQuit()
            if allQuit:
                break
            sleep(1)
            elapsed = elapsed + 1
        功能开关["fighting"] = 0

    def autoSkill(self):
        if 功能开关["技能定时释放"] == 1:
            if CompareColors.compare("648,1041,#39F8FE|650,1043,#38F6FD|650,1043,#38F6FD",
                                     diff=0.8):  # 主动技能图标蓝色圈圈，判断进入战斗；开始释放技能
                if self.SkillTimeNeedInit == 1:
                    # 进入战斗状态，初始化释放时间
                    SkillChongWu = time.time()
                    Skill1 = time.time()
                    Skill2 = time.time()
                    Skill3 = time.time()
                    self.SkillTimeNeedInit = 0

                res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                if self.SkillCount >= self.SkillNeedCount:
                    res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                else:
                    if (time.time() - SkillChongWu) > self.SkillChongWuTime:
                        tapSleep(421, 1077, 0.6)  # 宠物技能
                        tapSleep(426, 1067, 0.6)  # 宠物技能
                        self.SkillChongWuFlag = True
                        SkillChongWu = time.time()
                    else:
                        text = self.SkillChongWuTime - (time.time() - SkillChongWu)
                        Toast(f'宠物技能倒计时{text}s')
                    if (time.time() - Skill1) > self.Skill1Time:
                        res, num = TomatoOcrText(494, 1051, 536, 1101, "倒计时")
                        if num == "":  # 技能已冷却
                            tapSleep(511, 1076, 0.6)  # 1技能
                            self.Skill1Flag = True
                            Skill1 = time.time()
                    else:
                        text = self.Skill1Time - (time.time() - Skill1)
                        Toast(f'1技能倒计时{text}s')
                    if (time.time() - Skill2) > self.Skill2Time:
                        res, num = TomatoOcrText(522, 948, 563, 995, "倒计时")
                        if num == "":  # 技能已冷却
                            tapSleep(543, 974, 0.6)  # 2技能
                            self.Skill2Flag = True
                            Skill2 = time.time()
                    else:
                        text = self.Skill2Time - (time.time() - Skill2)
                        Toast(f'2技能倒计时{text}s')
                    if (time.time() - Skill3) > self.Skill3Time:
                        res, num = TomatoOcrText(628, 934, 672, 980, "倒计时")
                        if num == "":  # 技能已冷却
                            tapSleep(649, 953, 0.4)  # 3技能
                            tapSleep(649, 953, 0.4)  # 3技能
                            self.Skill3Flag = True
                            Skill3 = time.time()
                    else:
                        text = self.Skill3Time - (time.time() - Skill3)
                        Toast(f'3技能倒计时{text}s')
                    if self.SkillChongWuFlag and self.Skill1Flag and self.Skill2Flag and self.Skill3Flag:
                        self.SkillCount = self.SkillCount + 1
                        self.SkillChongWuFlag = self.Skill1Flag = self.Skill2Flag = self.Skill3Flag = False
            else:
                # 退出战斗状态，重置技能时间
                self.SkillTimeNeedInit = 1

            if 功能开关["三技能自动释放"] == 1:
                res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                re1 = CompareColors.compare("284,273,#43F6FE|290,271,#4CF2FE|309,271,#6FEBFE")  # 彩色技能条
                if re1:
                    tapSleep(649, 953, 0.6)  # 3技能 # 打断技
                    tapSleep(659, 942, 0.6)  # 3技能 # 打断技
                re2 = CompareColors.compare("287,271,#756B6C|292,268,#7B7273|284,266,#706667")  # 灰色技能条
                if re2:
                    tapSleep(649, 953, 0.6)  # 3技能 # 护盾技
                    tapSleep(659, 942, 0.6)  # 3技能 # 护盾技
            if 功能开关["技能定时释放"] == 0 and 功能开关["三技能自动释放"] == 0:
                res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                tapSleep(511, 1076, 0.6)  # 1技能
                tapSleep(521, 1070, 0.6)  # 1技能
                tapSleep(543, 974, 0.6)  # 2技能
                tapSleep(544, 962, 0.6)  # 2技能
                tapSleep(659, 942, 0.6)  # 3技能
                tapSleep(659, 942, 0.6)  # 3技能
                tapSleep(421, 1077, 0.6)  # 宠物技能
                tapSleep(426, 1067, 0.6)  # 宠物技能

    def fightingBaoZou(self):
        totalWait = 330 * 1000  # 30000 毫秒 = 30 秒
        elapsed = 0

        teamShoutDone = 0
        while 1:
            # 识别战斗中状态
            res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
            res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")

            # 大暴走可跟队友影子继续战斗，无需判断队友是否在队伍中
            if res1 or ("等级" in teamName1 or "等级" in teamName2):
                # Toast("战斗中")
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                功能开关["fighting_baozou"] = 1
                Toast('暴走史莱姆 - 战斗中')
                if teamShoutDone == 0:
                    teamShoutDone = self.teamShout()
            else:
                功能开关["fighting"] = 0
                功能开关["fighting_baozou"] = 0

            # 战斗逻辑
            # 循环10次，优先处理战斗中走位
            if res1 or (teamName1 != "" or teamName2 != ""):
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
                sleep(0.5)

            # 判断是否战斗失败（战斗5分钟后）
            if not res1 and (teamName1 == "" and teamName2 == ""):
                功能开关["fighting"] = 0
                功能开关["fighting_baozou"] = 0
                # 战斗结束
                res1 = TomatoOcrTap(333, 716, 384, 744, "开启")  # 领取宝箱
                res2 = TomatoOcrTap(334, 1090, 385, 1117, "开启")  # 领取宝箱
                res3 = TomatoOcrTap(332, 1067, 387, 1096, "开启")  # 领取宝箱
                if res1 or res2 or res3:
                    Toast("暴走史莱姆 - 战斗结束 - 战斗胜利")
                    sleep(2)
                    tapSleep(55, 1140)  # 领取后，点击空白
                    tapSleep(55, 1140)  # 领取后，点击空白
                    break
                res3, _ = TomatoOcrText(499, 191, 581, 215, "离开队伍")  # 已返回队伍
                if res3:
                    Toast("暴走史莱姆 - 战斗结束")
                    break
                quitStatus = self.quitTeam()
                if quitStatus:
                    break
                功能开关["fighting"] = 0
                功能开关["fighting_baozou"] = 0
        功能开关["fighting"] = 0
        功能开关["fighting_baozou"] = 0

    # 大暴走（雷电大王）
    def daBaoZouLeidian(self):
        def 草():
            point = FindColors.find(
                "145,673,#B9D6AB|153,672,#BFD7AD|159,672,#95B48C|151,680,#A1D8A1|138,681,#98D99D|148,688,#2D4645",
                rect=[9, 637, 202, 803], diff=0.94)
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
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                功能开关['当前职业'] = '战士'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
            if re:
                # Toast('识别当前职业-服事')
                功能开关['当前职业'] = '服事'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                功能开关['当前职业'] = '刺客'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                功能开关['当前职业'] = '法师'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                功能开关['当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '' and 功能开关['userColor'] == '':
            Toast('暴走史莱姆 - 战斗中 - 等待走位')
            # if 当前职业 == '战士':
            #     Toast('战士-战斗中-自动走位火')
            #     火()
            if 功能开关['当前职业'] == '服事' and 功能开关['暴走职能优先治疗'] == 1:
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
                rect=[9, 637, 202, 803], diff=0.94)
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
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.95, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                功能开关['当前职业'] = '战士'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.95, 4, 41, 72, 118)
            if re:
                # Toast('识别当前职业-服事')
                功能开关['当前职业'] = '服事'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.95, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                功能开关['当前职业'] = '刺客'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.95, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                功能开关['当前职业'] = '法师'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.95, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                功能开关['当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '' and 功能开关['bossColor1'] == '' and 功能开关['bossColor2'] == '':
            # if 当前职业 == '战士':
            #     Toast('战士-战斗中-自动走位火')
            #     火()
            if 功能开关['当前职业'] == '服事':
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
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-战士", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-战士')
                功能开关['当前职业'] = '战士'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-服事", 0.85, 4, 41, 72, 118)
            if re:
                # Toast('识别当前职业-服事')
                功能开关['当前职业'] = '服事'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-刺客", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-刺客')
                功能开关['当前职业'] = '刺客'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-法师", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-法师')
                功能开关['当前职业'] = '法师'
        if 功能开关['当前职业'] == '':
            re, x, y = imageFind("职业-游侠", 0.85, 4, 41, 72, 118)
            if re:
                Toast('识别当前职业-游侠')
                功能开关['当前职业'] = '游侠'

        sleep(0.5)
        if 功能开关['bossColor'] == '':
            Toast('暴走史莱姆 - 战斗中 - 等待走位')
            if 功能开关['当前职业'] == '服事' and 功能开关['暴走职能优先治疗'] == 1:
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

    def teamShoutAI(self, content="", shoutType=""):
        sleep(0.5)
        if 任务记录["自动入队-AI发言"] == 0:
            return

        if content in 任务记录['AI发言-上一次发言']:
            return
        res = self.teamShout(content, shoutType)
        if res:
            任务记录['AI发言-上一次发言'].append(content)
        print(任务记录['AI发言-上一次发言'])
        sleep(0.5)

    def teamShout(self, content="", shoutType=""):
        if 功能开关['喊话内容'] == "" and content == "":
            return 1

        contentTemp = content

        # 指定喊话内容时，不记入倒计时
        if content == "":
            if 功能开关['喊话内容'] != "":
                contentTemp = 功能开关['喊话内容']

            need_dur_minute = safe_int(功能开关.get("队伍喊话间隔", 0))  # 分钟
            if need_dur_minute == '':
                need_dur_minute = 0
            if need_dur_minute > 0 and 任务记录["队伍喊话-倒计时"] > 0:
                diffTime = time.time() - 任务记录["队伍喊话-倒计时"]
                if diffTime < need_dur_minute * 60:
                    Toast(f'日常 - 队伍喊话 - 倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                    return

        point = CompareColors.compare("108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)

        Toast("队伍发言")
        # print(contentTemp)

        res1 = False
        res2 = False
        res3 = False
        res4 = False

        # 判断是否战斗中
        if shoutType == "fight":
            res, _ = TomatoOcrText(644, 785, 688, 806, '喊话')  # 战斗内喊话
            if not res:
                Toast('战斗内喊话 - 不在战斗中')
                return 1

        if shoutType == "room":
            res4, _ = TomatoOcrText(311, 967, 407, 1002, '开始匹配')  # 房间内喊话
            if not res4:
                res4, _ = TomatoOcrText(290, 972, 431, 1006, '等待队长开始')  # 房间内喊话
            if not res4:
                res4, _ = TomatoOcrText(290, 972, 431, 1006, '等待队长开启')  # 房间内喊话
            if res4:
                tapSleep(219, 986, 1)
        else:
            res1 = TomatoOcrTap(19, 1104, 94, 1128, "点击输入", 10, 10, sleep1=0.6)
            if not res1:
                res2 = TomatoOcrTap(19, 1102, 90, 1127, "点击输入", 10, 10, sleep1=0.6)
                if not res2:
                    res3 = TomatoOcrTap(25, 1096, 104, 1133, "点击输入", 10, 10, sleep1=0.6)

        # if not res1 and not res2 and not res3 and not res4:
        #     tapSleep(74, 1120)
        #     res1 = True
        # sleep(1.5)  # 等待输入法弹窗
        if res1 or res2 or res3 or res4:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            sleep(0.3)
            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
            action.input(contentTemp)
            tapSleep(360, 104, 0.3)  # 点击空白处确认输入
            for i in range(1, 3):
                # 检查是否已输入
                notInput = TomatoOcrTap(78, 1155, 156, 1191, "点击输入", 5, 5)
                if not notInput:
                    notInput = TomatoOcrTap(79, 1157, 118, 1190, "点击", 5, 5)
                if notInput:
                    sleep(1)
                    action.input(contentTemp)
                    sleep(1)
                    tapSleep(360, 104, 0.5)  # 点击空白处确认输入
                else:
                    break

            res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
            if not res:
                sleep(0.5)
                res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
            if res:
                res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
                if res:
                    sleep(2)
                    res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
                # 关闭喊话窗口
                point = FindColors.find(
                    "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                    rect=[11, 26, 364, 489])
                if point:
                    tapSleep(point.x, point.y, 1)

                # 关闭喊话窗口
                point = CompareColors.compare(
                    "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
                if point:
                    Toast('收起喊话窗口')
                    tapSleep(107, 93)
                # 关闭喊话窗口
                point = FindColors.find(
                    "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                    rect=[11, 26, 364, 489])
                if point:
                    Toast('收起喊话窗口')
                    tapSleep(point.x, point.y, 1)
                if content == "":
                    任务记录["队伍喊话-倒计时"] = time.time()
                return 1

        # 关闭喊话窗口
        point = FindColors.find(
            "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
            rect=[11, 26, 364, 489])
        if point:
            Toast('收起喊话窗口')
            tapSleep(point.x, point.y, 1)

        point = CompareColors.compare("108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)
        return 0

    # 战斗中退出组队
    def quitTeamFighting(self):
        功能开关["fighting"] = 1
        for i in range(3):
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            res = TomatoOcrTap(649, 319, 694, 342, "队伍", sleep1=0.8)
            if res:
                res = TomatoOcrTap(501, 191, 581, 217, "离开队伍", sleep1=0.8)
                res = TomatoOcrTap(329, 726, 391, 761, "确定", sleep1=0.8)
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍", sleep1=0.8)
            res = TomatoOcrTap(329, 726, 391, 761, "确定", sleep1=0.8)
        功能开关["fighting"] = 0

    def fight_fail(self):
        res1, _ = TomatoOcrText(246, 459, 327, 482, "你被击败了")
        res2, _ = TomatoOcrText(475, 1038, 527, 1065, "放弃")
        res, teamName1 = TomatoOcrText(7, 148, 52, 163, "队友名称")
        res, teamName2 = TomatoOcrText(7, 198, 52, 213, "队友名称")
        if res1 or res2 or ("等级" not in teamName1 and "等级" not in teamName2):  # 战败提示 or 队友全部离队
            # Toast("战斗结束 - 战斗失败")
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            self.quitTeamFighting()  # 退出队伍
            return True
        return False

    def homePage(self):
        tryTimes = 0
        while True:
            tryTimes = tryTimes + 1
            if tryTimes > 3:
                point = FindColors.find(
                    "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
                    rect=[61, 34, 322, 623], diff=0.93)
                if point:
                    Toast('收起喊话窗口')
                    tapSleep(point.x, point.y)
            if tryTimes > 5:
                system.open("com.xd.cfbmf")
                # 暂不处理战败页启动，提高执行效率
                # 判断战败页面
                self.fight_fail()
                quitTeamRe = self.quitTeam()
            if tryTimes > 10:
                # Toast('尝试重启游戏')
                # 结束应用
                # r = system.shell("am kill com.xd.cfbmf")
                # r = system.shell("am force-stop com.xd.cfbmf")
                任务记录['试炼-秘境-体力消耗完成'] = 1
                return

            res6 = self.WaitFight()

            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
            if return3:
                Toast('返回首页')

            # 判断是否已在首页
            res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
                if not shou_ye1:
                    shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            if res2 or shou_ye1 or shou_ye2:
                功能开关["needHome"] = 0
                功能开关["fighting"] = 0
                Toast('已返回首页')
                sleep(0.5)
                return True

            # 开始异步处理返回首页
            # runThreadReturnHome()
            功能开关["needHome"] = 1

            # 点击首页-冒险
            re = TomatoOcrTap(330, 1201, 389, 1238, '冒险')
            # ldE.element('首页-冒险').click().execute(sleep=1)

            # 判断战败页面
            self.fight_fail()

            # 判断宝箱开启
            self.openTreasure()
            sleep(0.5)

    def quitTeam(self):
        res5 = False

        # 返回房间 - 队伍满员，开始挑战提醒
        wait1, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        wait2 = False
        if not wait1:
            wait2, _ = TomatoOcrText(240, 610, 344, 653, "队伍已满员")  # 队伍已满员，准备开启挑战
        if wait1 or wait2:
            res5 = TomatoOcrTap(453, 727, 511, 760, "确定", 10, 10)  # 队伍已满员，准备开启挑战 - 确定

        res1 = False
        res2 = False
        res3 = False
        res4 = False
        res1 = TomatoOcrTap(651, 559, 682, 577, "组队")
        if not res1:
            res2 = TomatoOcrFindRangeClick('正在组队', whiteList='正在组队', x1=549, y1=340, x2=699, y2=696)
            # res2 = TomatoOcrTap(631, 558, 699, 581, "正在组队")
            if not res2:
                # res3 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中')
                res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
                if not res3:
                    res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中")  # 大暴走匹配中
        res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
        if res1 or res2 or res3 or res4 or res5 or res6:
            功能开关["needHome"] = 0
            功能开关["fighting"] = 1
            teamStatus = TomatoOcrTap(632, 570, 684, 598, "匹配中")
            if teamStatus:
                Toast('取消匹配')

            teamExist = TomatoOcrTap(500, 184, 579, 214, "离开队伍", 20, 20)
            if not teamExist:
                teamExist = TomatoOcrFindRangeClick('离开队伍', whiteList='离开队伍', x1=416, y1=126, x2=628, y2=284)
            if teamExist:
                teamExist = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=105, y1=304, x2=631, y2=953)
                if teamExist:
                    Toast('退出组队')
                    功能开关["fighting"] = 0
                    return True

            res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中")  # 大暴走匹配中
            if res4:
                Toast("取消匹配")
                功能开关["fighting"] = 0
                return True
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍")
            if not res:
                tapSleep(540, 200, 0.8)
            res = TomatoOcrTap(329, 726, 391, 761, "确定")
            if not res:
                tapSleep(360, 740, 0.8)
            if res:
                Toast("退出组队")
                功能开关["fighting"] = 0
                return True

        功能开关["fighting"] = 0
        return False

    def AIContent(self):
        zanList = ['棒', '厉害', '谢', '哇', '牛', '6']
        re, teamText1 = TomatoOcrText(62, 1023, 251, 1052, "队友发言")
        re, teamText2 = TomatoOcrText(58, 1049, 244, 1079, "队友发言")
        re, teamText3 = TomatoOcrText(63, 965, 252, 994, "队友发言")
        contains_zan1 = any(zan in teamText1 for zan in zanList)
        contains_zan2 = any(zan in teamText2 for zan in zanList)
        contains_zan3 = any(zan in teamText3 for zan in zanList)
        if contains_zan1 or contains_zan2 or contains_zan3:
            # 回复夸赞
            self.teamShoutAI("自动回复~蟹蟹")

        wenList = ['脚本', '科技', '狠活', '高级', '群', '挂']
        contains_zan1 = any(zan in teamText1 for zan in wenList)
        contains_zan2 = any(zan in teamText2 for zan in wenList)
        contains_zan3 = any(zan in teamText3 for zan in wenList)
        if contains_zan1 or contains_zan2 or contains_zan3:
            # 回复夸赞
            self.teamShoutAI("自动回复~欢迎加鹅了解喔~372~270~534")

        blackList = ['*']
        contains_zan1 = any(zan in teamText1 for zan in blackList)
        contains_zan2 = any(zan in teamText2 for zan in blackList)
        contains_zan3 = any(zan in teamText3 for zan in blackList)
        if contains_zan1 or contains_zan2 or contains_zan3:
            # 回复夸赞
            self.teamShoutAI("自动回复~请文明发言哟")

        moveList = ['动','左','右']
        contains_zan1 = any(zan in teamText1 for zan in moveList)
        contains_zan2 = any(zan in teamText2 for zan in moveList)
        contains_zan3 = any(zan in teamText3 for zan in moveList)
        if contains_zan1 or contains_zan2 or contains_zan3:
            # 移动走位
            imageFindClick('战斗-向左移动', x1=11, y1=565, x2=206, y2=778)
            任务记录['战斗-上一次移动'] = time.time()

        # 判断当前时间，回复吉祥话
        from datetime import datetime
        now = datetime.now()
        hour = now.hour
        # 根据时间段选择吉祥话
        if 5 <= hour < 12:
            return "早上好，愿你今天元气满满！"
        elif 12 <= hour < 18:
            return "下午好，愿你此间战无不胜！"
        elif 18 <= hour < 22:
            return "晚上好，愿你开心顺利又一天！"
        else:
            return "夜深了，愿你今晚有个好梦！"


    # 判断角色死亡 & 队伍仅剩佣兵(名字长度均为2个)；离队
    def allQuit(self):
        res1, _ = TomatoOcrText(246, 459, 327, 482, "你被击败了")
        res2, _ = TomatoOcrText(475, 1038, 527, 1065, "放弃")
        res3, _ = TomatoOcrText(451, 959, 551, 989, "再次挑战")
        if res1 or res2 or res3:
            res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
            self.teamShoutAI(f'战斗失败QAQ~期待下次相遇~', shoutType="fight")
            self.teamShoutAI(f'提示~可以提醒我进行移动哟~', shoutType="fight")
            team2, name2 = TomatoOcrText(58, 123, 140, 149, '队友2名称')
            team3, name3 = TomatoOcrText(56, 173, 131, 197, '队友3名称')
            team4, name4 = TomatoOcrText(54, 222, 134, 248, '队友4名称')
            if (name2 == "" or len(name2) == 2) and (name3 == "" or len(name3) == 2) and (
                    name4 == "" or len(name4) == 2):
                res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
                self.quitTeamFighting()  # 退出队伍
                return True
            if (name2 == "" or len(name2) == 3) and (name3 == "" or len(name3) == 3) and (
                    name4 == "" or len(name4) == 3):
                res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认
                self.quitTeamFighting()  # 退出队伍
                return True
        return False
