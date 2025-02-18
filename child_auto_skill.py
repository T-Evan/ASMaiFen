# 导包
from .baseUtils import *
from .res.ui.ui import 功能开关
from ascript.android.screen import FindColors


class AutoSkill:
    def __init__(self):
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

        self.SkillChongWu = time.time()
        self.Skill1 = time.time()
        self.Skill2 = time.time()
        self.Skill3 = time.time()

        self.fighting = 0
        self.lastCheckFighting = 0

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

        self.SkillChongWu = time.time()
        self.Skill1 = time.time()
        self.Skill2 = time.time()
        self.Skill3 = time.time()

    def autoSkill(self):
        while 1:
            if 任务记录['喊话-并发锁'] == 1:
                sleep(0.2)
                continue

            # 间隔2s检查战斗中状态
            if self.fighting == 0 or time.time() - self.lastCheckFighting > 5:
                re1 = CompareColors.compare(
                    "657,324,#F3EDDD|659,324,#F3EDDD|664,331,#F3EDDD|676,329,#F3EDDD|681,337,#F3EDDD|687,334,#F3EDDD")  # 战斗内队伍图标
                if re1:
                    res3, _ = TomatoOcrText(647, 879, 686, 904, '自动')  # 辅助施法-识别战斗状态
                    res4, _ = TomatoOcrText(647, 879, 686, 904, '手动')  # 辅助施法-识别战斗状态
                    # print('辅助施法-识别战斗状态')
                    # if res1 or res2 or res3 or res4:
                    if res3 or res4:
                        print('辅助施法-识别战斗状态-开始战斗')
                        self.fighting = 1
                        if self.SkillCount >= self.SkillNeedCount:
                            res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                        else:
                            res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                    else:
                        sleep(0.2)
                        self.fighting = 0
                else:
                    sleep(0.2)
                    self.fighting = 0  # 主线推图不辅助施法
                self.lastCheckFighting = time.time()

            if self.fighting == 0:
                self.initAutoSkill()
                continue

            if self.SkillCount >= self.SkillNeedCount:
                res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                self.SkillCount = 0
                continue

            if 功能开关["技能定时释放"] == 1:
                re1 = CompareColors.compare(
                    "290,255,#FEDD45|292,258,#FEDD45|292,254,#FEDD45|295,257,#FEDD45")  # boss黄色血条
                if not re1:
                    re1 = CompareColors.compare("661,1047,#39F7FF")  # 主动技能图标蓝色圈圈，判断进入战斗；开始释放技能
                if re1:
                    if self.SkillTimeNeedInit == 1:
                        # 进入战斗状态，初始化释放时间
                        self.SkillChongWu = time.time()
                        self.Skill1 = time.time()
                        self.Skill2 = time.time()
                        self.Skill3 = time.time()
                        self.SkillTimeNeedInit = 0

                    # res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                    # if self.SkillCount >= self.SkillNeedCount:
                    # res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                    if 0:
                        sleep(0.05)
                    else:
                        # 技能1
                        if (time.time() - self.Skill1) > self.Skill1Time:
                            # 判断依赖技能是否已释放
                            flag = False
                            if 功能开关['技能1释放依赖'] == '冷却后立即释放':
                                flag = True
                            if 功能开关['技能1释放依赖'] == '宠物技能后释放':
                                gray = CompareColors.compare("400,1054,#FFFFC7|444,1051,#FFFFCC")  # 宠物技能能量条满
                                if not gray:
                                    # 宠物技能能量条不为满，说明在等待宠物技能冷却 or 宠物技能未释放
                                    # Toast('等待宠物技能冷却')
                                    flag = True
                            if 功能开关['技能1释放依赖'] == '2技能后释放':
                                gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                                       rect=[509, 938, 573, 1003], diff=0.9)  # 2技能灰色
                                if gray:
                                    flag = True
                            if 功能开关['技能1释放依赖'] == '3技能后释放':
                                gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                                                       rect=[617, 928, 683, 984])  # 3技能灰色
                                if gray:
                                    flag = True

                            # 判断当前技能是否冷却
                            gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                                   rect=[486, 1044, 547, 1112], diff=0.9)
                            if not gray and flag:  # 技能已冷却 & 依赖技能已释放
                                tapSleep(511, 1076, 0.1)  # 1技能
                                tapSleep(531, 1026, 0.1)  # 1技能

                                # 衔接释放2技能（因2技能无需考虑前置1技能冷却）
                                if 功能开关['技能2释放依赖'] == '1技能后释放':
                                    tapSleep(543, 974, 0.1)  # 2技能
                                    tapSleep(513, 924, 0.1)  # 2技能
                                    self.Skill2Flag = True
                                    self.Skill2 = time.time()
                                self.Skill1Flag = True
                                self.Skill1 = time.time()
                                self.SkillNeedCount = self.SkillNeedCount + 1
                        else:
                            a = 1  # debug
                            # text = self.Skill1Time - (time.time() - self.Skill1)
                            # Toast(f'1技能倒计时{text}s')

                        if (time.time() - self.SkillChongWu) > self.SkillChongWuTime:
                            gray = CompareColors.compare("391,1068,#F0DF95|431,1046,#F1E3A0")  # 宠物技能黄条是否已满
                            if gray:
                                tapSleep(421, 1077, 0.1)  # 宠物技能
                                # tapSleep(426, 1067, 0.1)  # 宠物技能
                                self.SkillChongWuFlag = True
                                self.SkillChongWu = time.time()
                        else:
                            a = 1
                            # text = self.SkillChongWuTime - (time.time() - self.SkillChongWu)
                            # Toast(f'宠物技能倒计时{text}s')

                        # # 2技能
                        # if (time.time() - self.Skill2) > self.Skill2Time:
                        #     # 判断依赖技能是否已释放
                        #     flag = False
                        #     if 功能开关['技能2释放依赖'] == '冷却后立即释放':
                        #         flag = True
                        #     if 功能开关['技能2释放依赖'] == '1技能后释放':
                        #         gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                        #                                rect=[476, 1030, 556, 1122])  # 1技能灰色
                        #         if gray:
                        #             flag = True
                        #     if 功能开关['技能2释放依赖'] == '3技能后释放':
                        #         gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                        #                                rect=[606, 916, 688, 995])  # 3技能灰色
                        #         if gray:
                        #             flag = True
                        #
                        #     gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B", rect=[487, 926, 595, 1021])
                        #     if not gray and flag:  # 技能已冷却 & 依赖技能已释放
                        #         tapSleep(543, 974, 0.1)  # 2技能
                        #         tapSleep(513, 924, 0.1)  # 2技能
                        #         self.Skill2Flag = True
                        #         self.Skill2 = time.time()
                        # else:
                        #     text = self.Skill2Time - (time.time() - self.Skill2)
                        #     Toast(f'2技能倒计时{text}s')
                        #
                        # # 3技能
                        # if (time.time() - self.Skill3) > self.Skill3Time:
                        #     # 判断依赖技能是否已释放
                        #     flag = False
                        #     if 功能开关['技能3释放依赖'] == '冷却后立即释放':
                        #         flag = True
                        #     if 功能开关['技能3释放依赖'] == '1技能后释放':
                        #         gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                        #                                rect=[476, 1030, 556, 1122])  # 1技能灰色
                        #         if gray:
                        #             flag = True
                        #     if 功能开关['技能3释放依赖'] == '2技能后释放':
                        #         gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                        #                                rect=[487, 926, 595, 1021])  # 2技能灰色
                        #         if gray:
                        #             flag = True
                        #
                        #     gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B", rect=[606, 916, 688, 995])
                        #     if not gray and flag:  # 技能已冷却 & 依赖技能已释放
                        #         tapSleep(649, 953, 0.1)  # 3技能
                        #         tapSleep(628, 965, 0.1)  # 3技能
                        #         self.Skill3Flag = True
                        #         self.Skill3 = time.time()
                        # else:
                        #     text = self.Skill3Time - (time.time() - self.Skill3)
                        #     Toast(f'3技能倒计时{text}s')
                        #
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
                    Toast('释放三技能打断')
                    tapSleep(649, 953, 0.3)  # 3技能 # 打断技
                    tapSleep(659, 942, 0.3)  # 3技能 # 打断技
                re2 = FindColors.find(
                    "283,271,#6D6D6D|284,269,#7A7172|286,269,#7A7172|283,272,#696969|286,272,#696969|285,270,#7C7173",
                    rect=[197, 200, 541, 333])  # 灰色技能条
                if re2:
                    Toast('释放三技能护盾')
                    tapSleep(649, 953, 0.3)  # 3技能 # 护盾技
                    tapSleep(659, 942, 0.3)  # 3技能 # 护盾技
                tapSleep(511, 1076, 0.1)  # 1技能
                tapSleep(521, 1070, 0.1)  # 1技能
                tapSleep(543, 974, 0.1)  # 2技能
                tapSleep(544, 962, 0.1)  # 2技能
                tapSleep(421, 1077, 0.1)  # 宠物技能
                tapSleep(426, 1067, 0.1)  # 宠物技能
            if 功能开关["技能定时释放"] == 0 and 功能开关["主动释放技能"] == 1:
                res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                tapSleep(511, 1076, 0.3)  # 1技能
                tapSleep(521, 1070, 0.3)  # 1技能
                tapSleep(543, 974, 0.3)  # 2技能
                tapSleep(544, 962, 0.3)  # 2技能
                tapSleep(659, 942, 0.3)  # 3技能
                tapSleep(659, 942, 0.3)  # 3技能
                tapSleep(421, 1077, 0.3)  # 宠物技能
                tapSleep(426, 1067, 0.3)  # 宠物技能
                self.SkillNeedCount = self.SkillNeedCount + 1

    def autoSkill2(self):
        while 1:
            if self.fighting == 0:
                # print(f'辅助施法-技能2-等待中{self.fighting}')
                sleep(1)
                continue

            sleep(0.05)
            if 功能开关["技能定时释放"] == 1:
                if 功能开关['技能2释放依赖'] == '1技能后释放':
                    re1 = True  # 2技能有前置依赖，不需要单独判断是否进入战斗
                else:
                    re1 = CompareColors.compare(
                        "290,255,#FEDD45|292,258,#FEDD45|292,254,#FEDD45|295,257,#FEDD45")  # boss黄色血条
                    if not re1:
                        re1 = CompareColors.compare("661,1047,#39F7FF")  # 主动技能图标蓝色圈圈，判断进入战斗；开始释放技能
                if re1:
                    if self.SkillTimeNeedInit == 1:
                        # 进入战斗状态，初始化释放时间
                        self.SkillChongWu = time.time()
                        self.Skill1 = time.time()
                        self.Skill2 = time.time()
                        self.Skill3 = time.time()
                        self.SkillTimeNeedInit = 0

                    # res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
                    # if self.SkillCount >= self.SkillNeedCount:
                    # res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
                    if 0:
                        sleep(0.05)
                    else:
                        # 2技能
                        if (time.time() - self.Skill2) > self.Skill2Time:
                            # 判断依赖技能是否已释放
                            flag = False
                            if 功能开关['技能2释放依赖'] == '冷却后立即释放':
                                flag = True
                            if 功能开关['技能2释放依赖'] == '1技能后释放':
                                gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                                       rect=[486, 1044, 547, 1112], diff=0.9)  # 1技能灰色
                                if gray:
                                    flag = True

                                # 判断1技能冷却大于2
                                # 1技能 1
                                skill1CoolTime = 0
                                re = CompareColors.compare(
                                    "513,1068,#F9F9F9|514,1068,#FFFFFF|517,1068,#FFFFFF|520,1072,#9D9D9D|520,1080,#9F9F9F|517,1085,#FFFFFF",
                                    diff=0.95)
                                if re:
                                    skill1CoolTime = 1

                                if not re:
                                    # 1技能 2
                                    re = CompareColors.compare(
                                        "511,1069,#FEFEFE|514,1068,#FFFFFF|521,1071,#FFFFFF|518,1078,#FFFFFF|512,1085,#FFFFFF|522,1085,#FAFAFA",
                                        diff=0.95)
                                    if re:
                                        skill1CoolTime = 2

                                if not re:
                                    # 1技能 3
                                    re = CompareColors.compare(
                                        "511,1068,#FFFFFF|514,1067,#FFFFFF|519,1070,#FFFFFF|514,1075,#FFFFFF|519,1079,#FFFFFF|516,1084,#FEFEFE|511,1085,#FFFFFF",
                                        diff=0.95)
                                    if re:
                                        skill1CoolTime = 3
                                # print(f'1技能冷却-{skill1CoolTime}')
                                # re, skill2CoolTime = TomatoOcrText(495, 1056, 537, 1095, '1技能冷却')  # 1技能冷却时间
                                # # 误识别修正
                                # skill2CoolTime = self.coolTimeFix(skill2CoolTime)
                                # skill2CoolTime = safe_int_v2(skill2CoolTime)
                                if 0 < skill1CoolTime < 4:  # 等待1技能重新进入冷却，避免在1技能还有1秒时释放2技能，导致的先后顺序错位
                                    flag = False

                            # if 功能开关['技能2释放依赖'] == '3技能后释放':
                            #     gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B",
                            #                            rect=[617, 928, 683, 984])  # 3技能灰色
                            #     if gray:
                            #         flag = True

                            gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                                   rect=[509, 938, 573, 1003], diff=0.9)
                            if not gray and flag:  # 技能已冷却 & 依赖技能已释放
                                tapSleep(543, 974, 0.1)  # 2技能
                                tapSleep(513, 924, 0.1)  # 2技能
                                # 衔接释放2技能（因2技能无需考虑前置1技能冷却）
                                if 功能开关['技能3释放依赖'] == '2技能后释放':
                                    tapSleep(649, 953, 0.1)  # 3技能
                                    tapSleep(628, 965, 0.1)  # 3技能
                                    self.Skill3Flag = True
                                    self.Skill3 = time.time()
                                self.Skill2Flag = True
                                self.Skill2 = time.time()

                            # 衔接3技能，减少线程数
                            # self.autoSkill3V2()
                        else:
                            a = 1  # debug
                            # text = self.Skill2Time - (time.time() - self.Skill2)
                            # Toast(f'2技能倒计时{text}s')
                else:
                    # 退出战斗状态，重置技能时间
                    self.SkillTimeNeedInit = 1

    def autoSkill3V2(self):
        sleep(0.05)
        if self.SkillTimeNeedInit == 1:
            # 进入战斗状态，初始化释放时间
            self.SkillChongWu = time.time()
            self.Skill1 = time.time()
            self.Skill2 = time.time()
            self.Skill3 = time.time()
            self.SkillTimeNeedInit = 0

        # res = TomatoOcrTap(644, 878, 687, 902, "自动", 10, -10)
        # if self.SkillCount >= self.SkillNeedCount:
        # res = TomatoOcrTap(644, 878, 687, 902, "手动", 10, -10)
        if 0:
            sleep(0.05)
        else:
            # 3技能
            if (time.time() - self.Skill3) > self.Skill3Time:
                # 判断依赖技能是否已释放
                flag1 = False
                if 功能开关['技能3释放依赖'] == '冷却后立即释放':
                    flag1 = True
                if 功能开关['技能3释放依赖'] == '1技能后释放':
                    gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                           rect=[486, 1044, 547, 1112], diff=0.9)  # 1技能灰色
                    if gray:
                        flag1 = True
                if 功能开关['技能3释放依赖'] == '2技能后释放':
                    gray = FindColors.find("527,1002,#121219|528,1001,#030303|528,1002,#0A0A0F",
                                           rect=[509, 938, 573, 1003], diff=0.9)  # 2技能灰色
                    # print(gray)
                    if gray:
                        flag1 = True

                # 识别前置技能冷却时间
                flag2 = True
                needCoolTime = safe_int_v2(功能开关['技能3前置技能冷却'])
                if needCoolTime > 0:
                    flag2 = False

                    skill2CoolTime = 0
                    # 2技能 11
                    re = CompareColors.compare(
                        "536,967,#F8F8F8|540,967,#FFFFFF|540,980,#FFFFFF|549,967,#FFFFFF|551,981,#FFFFFF", diff=0.95)
                    if re:
                        skill2CoolTime = 11

                    if not re:
                        # 2技能 10
                        re = CompareColors.compare("532,967,#F8F8F8|535,978,#FFFFFF|543,975,#FFFFFF|555,975,#FFFFFF")
                        if re:
                            skill2CoolTime = 10

                    # 2技能 9
                    if not re:
                        re = CompareColors.compare(
                            "538,969,#FFFFFF|543,965,#FEFEFE|549,970,#FFFFFF|547,976,#FFFFFF|541,983,#FCFCFC",
                            diff=0.95)
                        if re:
                            skill2CoolTime = 9

                    # 2技能 8
                    if not re:
                        re = CompareColors.compare(
                            "544,980,#828282|538,967,#FFFFFF|543,965,#FDFDFD|549,980,#FDFDFD|543,972,#FFFFFF|538,981,#FFFFFF|544,984,#F5F5F5",
                            diff=0.9)
                        if re:
                            skill2CoolTime = 8

                    # 2技能 7
                    if not re:
                        re = CompareColors.compare(
                            "538,964,#FFFFFF|541,964,#FFFFFF|547,964,#FFFFFF|544,972,#FFFFFF|541,978,#FFFFFF|540,983,#FFFFFF",
                            diff=0.95)
                        if re:
                            skill2CoolTime = 7

                    # 2技能 6
                    re = CompareColors.compare(
                        "546,965,#FFFFFF|541,970,#FEFEFE|538,978,#FFFFFF|540,983,#FEFEFE|546,981,#FDFDFD|546,975,#FFFFFF",
                        diff=0.95)
                    if re:
                        skill2CoolTime = 6

                    # 2技能 5
                    if not re:
                        re = CompareColors.compare(
                            "544,965,#FFFFFF|540,967,#FFFFFF|540,973,#FBFBFB|546,973,#FFFFFF|546,980,#FFFFFF|538,983,#FDFDFD",
                            diff=0.95)
                        if re:
                            skill2CoolTime = 5

                    # 2技能 4
                    if not re:
                        re = CompareColors.compare(
                            "543,973,#CDCDCD|546,967,#FFFFFF|541,970,#FFFFFF|538,975,#FFFFFF|538,978,#F9F9F9|549,978,#F9F9F9|546,981,#FFFFFF",
                            diff=0.95)
                        if re:
                            skill2CoolTime = 4

                    # 2技能 3
                    # if not re:
                    #     re = CompareColors.compare(
                    #         "540,965,#FDFDFD|544,965,#FFFFFF|546,970,#FFFFFF|541,973,#FFFFFF|547,976,#FFFFFF|541,983,#FFFFFF",
                    #         diff=0.95)
                    #     if re:
                    #         skill2CoolTime = 3

                    # # 2技能 2
                    # if not re:
                    #     re = CompareColors.compare(
                    #         "538,967,#F4F4F4|546,967,#FFFFFF|541,983,#FFFFFF|547,983,#FFFFFF|544,976,#FFFFFF")
                    #     if re:
                    #         skill2CoolTime = 2

                    # 2技能 1
                    # re = CompareColors.compare("541,967,#F8F8F8|544,965,#FFFFFF|544,972,#FFFFFF|544,981,#FFFFFF|538,943,#222222",diff=0.95)
                    # if re:
                    #     skill2CoolTime = 1

                    # re, skill2CoolTime = TomatoOcrText(522, 948, 565, 999, '2技能冷却')  # 2技能冷却时间
                    # 误识别修正
                    # skill2CoolTime = self.coolTimeFix(skill2CoolTime)
                    # skill2CoolTime = safe_int_v2(skill2CoolTime)
                    # print(f'2技能冷却-{skill2CoolTime}')
                    if skill2CoolTime > 0 and skill2CoolTime >= needCoolTime:
                        flag2 = True

                gray = FindColors.find("524,953,#1D1D1D|521,953,#1B1B1B", rect=[617, 928, 683, 984])
                if not gray and flag1 and flag2:  # 技能已冷却 & 依赖技能已释放
                    tapSleep(649, 953, 0.1)  # 3技能
                    tapSleep(628, 965, 0.1)  # 3技能
                    self.Skill3Flag = True
                    self.Skill3 = time.time()
            else:
                a = 1  # debug
                # text = self.Skill3Time - (time.time() - self.Skill3)
                # Toast(f'3技能倒计时{text}s')

    def autoSkill3(self):
        while 1:
            if self.fighting == 0:
                # print(f'辅助施法-技能3-等待中{self.fighting}')
                sleep(1)
                continue

            if 功能开关["技能定时释放"] == 1:
                if 功能开关['技能3释放依赖'] == '2技能后释放':
                    re1 = True  # 3技能有前置依赖，不需要单独判断是否进入战斗
                else:
                    re1 = CompareColors.compare(
                        "290,255,#FEDD45|292,258,#FEDD45|292,254,#FEDD45|295,257,#FEDD45")  # boss黄色血条
                    if not re1:
                        re1 = CompareColors.compare("661,1047,#39F7FF")  # 主动技能图标蓝色圈圈，判断进入战斗；开始释放技能
                if re1:
                    self.autoSkill3V2()
                else:
                    # 退出战斗状态，重置技能时间
                    self.SkillTimeNeedInit = 1

    def coolTimeFix(self, skill2CoolTime):
        # 误识别修正
        if skill2CoolTime == "n":
            skill2CoolTime = 11
        if skill2CoolTime == "防":
            skill2CoolTime = 4
        if skill2CoolTime == "头":
            skill2CoolTime = 3
        return skill2CoolTime
