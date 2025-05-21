# 导包
import math
from time import sleep

from PIL.ImageChops import offset

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .daily import DailyTask
from ascript.android.screen import Ocr
from .baseUtils import *
import re as repattern
from ascript.android.screen import FindColors


class LvTuanTask:
    def __init__(self):
        self.dailyTask = DailyTask()

    def lvtuanTask(self):
        if 功能开关["旅团总开关"] == 0:
            return

        self.dailyTask.homePage(needQuitTeam=True)

        # 旅团签到
        self.lvTuanWater()

        # 旅团许愿墙
        self.lvTuanXuYuan()

        # 旅团任务
        self.lvTuanRenWu()

        # 旅团大采购
        self.lvTuanDaCaiGou()

        # 旅团商店
        self.lvTuanShop()

        # 旅团调查队
        self.lvTuanDiaoCha()

    # 旅团调查队
    def lvTuanDiaoCha(self):
        if 功能开关["旅团调查队"] == 0:
            return
        if 任务记录["旅团-调查队-完成"] == 1:
            return
        Toast("旅团 - 调查队 - 开始")

        loopCount = 0
        needCount = safe_int(功能开关["调查队挑战次数"])
        if needCount == '':
            needCount = 1
        while loopCount < needCount:
            Toast(f"旅团 - 调查队重复挑战第 {loopCount}/{needCount} 次")
            loopCount = loopCount + 1
            res1, _ = TomatoOcrText(636, 97, 670, 119, "秘钥")  # 识别调查队组队中 - 右上角 - 每日补给调查秘钥
            res2, _ = TomatoOcrText(501, 191, 581, 218, "离开队伍")  # 识别调查队组队中 - 右上角 - 离开队伍
            if res1 or res2:
                # 组队中，对出队伍重新开启调查；保证重新匹配队友
                TomatoOcrTap(501, 191, 581, 218, "离开队伍")  # 离开队伍
                TomatoOcrTap(331, 727, 387, 758, "确定")  # 离开队伍 - 确定
            else:
                # 重新进入调查队，重新选择队友；避免队友不足
                for i in range(1, 3):
                    res = TomatoOcrFindRangeClick("调查队", x1=634, y1=602, x2=701, y2=1033, offsetX=20,
                                                  offsetY=-20, sleep1=0.7)
                    if not res:
                        res = TomatoOcrTap(647, 576, 689, 597, "旅团", sleep1=2)
                        if not res:
                            res = TomatoOcrTap(647, 592, 689, 614, "旅团", sleep1=2)
                        if not res:
                            # 返回首页
                            self.dailyTask.homePage()
                            # 退出组队
                            self.dailyTask.quitTeam()
                        else:
                            res = TomatoOcrFindRangeClick("调查队", x1=634, y1=602, x2=701, y2=1033, offsetX=20,
                                                          offsetY=-20, sleep1=0.7)
                            if res:
                                break
                    else:
                        break

            sleep(1)
            # 领取前一次宝箱
            self.openTreasure()

            # 检查剩余钥匙
            if 功能开关['调查队无钥匙继续'] == "" or 功能开关['调查队无钥匙继续'] == 0:
                res1, _ = TomatoOcrText(618, 83, 651, 101, "0/7")
                if res1:
                    Toast('调查队 - 钥匙用尽 - 结束挑战')
                    return

            # 领取累积奖励
            for k in range(4):
                re = CompareColors.compare("535,134,#F25F41|535,132,#F46042|535,134,#F25F41")
                if re:
                    tapSleep(514, 172, 0.8)
                    TomatoOcrTap(333, 719, 386, 752, '领取')
                    tapSleep(175, 956)  # 返回
                    tapSleep(175, 956)
                    tapSleep(175, 956)

            res = TomatoOcrTap(307, 964, 412, 1002, "开启调查", sleep1=0.7)
            if res:
                tapSleep(205, 760, 0.5)  # 添加队友
                tapSleep(530, 435, 1)  # 添加队友1
                tapSleep(530, 556, 1)  # 添加队友2
                tapSleep(531, 674, 1)  # 添加队友3
                tapSleep(532, 794, 1)  # 添加队友4
                tapSleep(530, 910, 1)  # 添加队友5
                res = TomatoOcrTap(70, 1200, 123, 1231, "返回", 10, 10, sleep1=1)
                res = TomatoOcrTap(331, 976, 386, 1005, "开始")
                sleep(5)
                if res:
                    # 战斗中
                    self.fighting()
                    sleep(2)
        任务记录['旅团-调查队-完成'] = 1

    # 判断是否战斗中
    def fighting(self):
        totalWait = 500
        start_time = int(time.time())
        failNum = 0  # 战斗中状态识别失败次数
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                Toast(f'调查队战斗超时 - 退出组队')
                self.quitTeamFighting()
                break
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
            if res1 or (teamName1 != "" or teamName2 != ""):
                Toast(f'调查队战斗中,战斗时长{elapsed}/{totalWait}秒')
            else:
                if failNum > 3:
                    Toast(f"调查队战斗中状态 - 识别失败 - 退出战斗")
                    break  # 识别失败，退出循环
                failNum = failNum + 1
            self.fight_fail_alert()
            sleep(0.5)

        # 战斗结束
        self.openTreasure()

    # 战斗中退出组队
    def quitTeamFighting(self):
        for i in range(2):
            # sleep(0.5)
            self.fight_fail_alert()
            res = TomatoOcrTap(649, 319, 694, 342, "队伍", sleep1=0.8)
            res = TomatoOcrTap(501, 191, 581, 217, "离开队伍", sleep1=0.8)
            res = TomatoOcrTap(329, 726, 391, 761, "确定", sleep1=0.8)
        quitRes = self.dailyTask.quitTeam()
        # sleep(0.5)

    def fight_fail_alert(self):
        res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击确认战败
        res = TomatoOcrTap(588, 637, 630, 661, "同意")  # 点击同意重新开始
        res = TomatoOcrTap(453, 961, 549, 989, "再次挑战")  # 点击同意再次挑战

    # 领取宝箱（调查队）
    def openTreasure(self):
        attempts = 0
        maxAttempts = 2

        while attempts < maxAttempts:
            attempts = attempts + 1
            # 调查队宝箱
            # 战斗结束页
            res1 = TomatoOcrTap(340, 1019, 378, 1039, "开启", 10, 20)
            res2 = TomatoOcrTap(340, 1019, 378, 1039, "开户", 10, 20)
            if res1 or res2:
                sleep(3)
                tapSleep(56, 1237)
                tapSleep(56, 1237)
                tapSleep(56, 1237)

            # 结算页
            res1 = TomatoOcrTap(339, 756, 379, 776, "开启")
            res2 = TomatoOcrTap(339, 756, 379, 776, "开户")
            if res1 or res2:
                Toast("战斗结束 - 开启宝箱")
                sleep(2)
                tapSleep(129, 995)
                tapSleep(129, 995)  # 点击空白处
                tapSleep(129, 995)  # 点击空白处
            if not res1 and not res2:
                re = TomatoOcrFindRangeClick('开启', x1=99, y1=697, x2=626, y2=1152)
                if re:
                    Toast("战斗结束 - 开启宝箱")
                    sleep(3)
                    tapSleep(56, 1237)
                    tapSleep(56, 1237)
                    tapSleep(56, 1237)

            # -- 钥匙不足退出
            res1, _ = TomatoOcrText(535, 767, 566, 798, "0")
            res2, _ = TomatoOcrText(301, 1023, 417, 1048, "调查秘钥不足")
            res3, _ = TomatoOcrText(303, 755, 414, 778, "调查秘钥不足")
            res4, _ = TomatoOcrText(295, 992, 421, 1019, "调查秘钥不足")
            if res1 or res2 or res3 or res4:
                Toast("钥匙不足")
                res = TomatoOcrTap(68, 1201, 130, 1232, "返回", sleep1=0.8)
                if res:
                    res = TomatoOcrTap(329, 723, 391, 762, "确定")
                else:
                    # 提前退出
                    tapSleep(60, 1150, 0.8)  # 点击空白处
                    res = TomatoOcrTap(329, 727, 388, 759, "确定")

    # 旅团商店
    def lvTuanShop(self):
        if 功能开关["旅团商店开关"] == 0:
            return

        if 任务记录["旅团-商店-完成"] == 1:
            return

        Toast("旅团 - 商店兑换 - 开始")
        # 判断是否在旅团页面
        isLvtuan = False
        for i in range(2):
            res = TomatoOcrFindRangeClick("服务区", x1=630, y1=560, x2=705, y2=1147, offsetX=25, offsetY=-15)
            if not res:
                # 返回首页
                self.dailyTask.homePage()
                res = TomatoOcrTap(647, 576, 689, 597, "旅团")
                # 判断是否在旅团页面
                res = TomatoOcrFindRangeClick("服务区", x1=626, y1=648, x2=709, y2=986, offsetX=25, offsetY=-15)
                if res:
                    isLvtuan = True
                    break
            else:
                isLvtuan = True
                break
        if not isLvtuan:
            Toast("旅团 - 商店兑换 - 未找到任务入口")
            return

        sleep(3)  # 等待跳转动画

        # 检查剩余叶子
        availableCount = ''
        re = CompareColors.compare("573,91,#F2D44F|577,89,#F7E769|579,96,#E9B63A")
        if re:
            res, availableCount = TomatoOcrText(598, 80, 682, 104, "叶子")
        if availableCount == '':
            res, availableCount = TomatoOcrText(607, 82, 669, 102, "叶子")
        availableCount = safe_int_v2(availableCount)
        if availableCount < 100:
            Toast("旅团 - 商店兑换 - 剩余叶子不足")
            任务记录["旅团-商店-完成"] = 1
            tapSleep(90, 1202)  # 返回
            return

        # 翻页（先返回上面）
        swipe(360, 750, 360, 850)
        sleep(2.5)
        for i in range(11):
            re = FindColors.find("258,928,#DBA636|259,921,#FDEF88|263,923,#F7DD62|257,932,#CC8F30",
                                 rect=[85, 538, 491, 1092], diff=0.9)
            if re:  # 有可购买商品时，继续判断
                if 功能开关['旅团唤兽琴弦']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '唤兽', 'match_mode': 'fuzzy'}], x1=93, y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '唤兽', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('唤兽 - 已购买')

                if 功能开关['旅团全价兽粮']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '全价兽粮', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '全价兽粮', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('全价兽粮 - 已购买')

                if 功能开关['旅团超级成长零食']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '超级成长零食', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '超级成长零食', 'match_mode': 'fuzzy'}],
                                                    x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('超级成长零食 - 已购买')

                if 功能开关['旅团原材料']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '原材料', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '原材料', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('原材料 - 已购买')

                if 功能开关['旅团史诗经验']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '史诗经验', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '史诗经验', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('史诗经验 - 已购买')

                if 功能开关['旅团优秀经验']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '优秀经验', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '优秀经验', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('优秀经验 - 已购买')

                if 功能开关['旅团普通经验']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '普通经验', 'match_mode': 'fuzzy'}], x1=93,
                                                  y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '普通经验', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('普通经验 - 已购买')

                if 功能开关['旅团金币']:
                    re, x, y = TomatoOcrFindRange(keywords=[{'keyword': '金币', 'match_mode': 'fuzzy'}], x1=93, y1=561,
                                                  x2=630, y2=1084)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick(keywords=[{'keyword': '金币', 'match_mode': 'fuzzy'}], x1=93,
                                                    y1=561,
                                                    x2=630, y2=1084)
                            self.shopBuy()
                        else:
                            Toast('金币 - 已购买')

            # 检查剩余叶子
            availableCount = ''
            re = CompareColors.compare("573,91,#F2D44F|577,89,#F7E769|579,96,#E9B63A")
            if re:
                res, availableCount = TomatoOcrText(598, 80, 682, 104, "叶子")
            if availableCount == '':
                res, availableCount = TomatoOcrText(607, 82, 669, 102, "叶子")
            availableCount = safe_int_v2(availableCount)
            if availableCount < 100:
                Toast("旅团 - 商店兑换 - 剩余叶子不足")
                任务记录["旅团-商店-完成"] = 1
                tapSleep(90, 1202)  # 返回
                return

            # 翻页
            swipe(360, 850, 360, 770)
            Toast("旅团 - 商店兑换 - 翻页")
            sleep(3)

        res = TomatoOcrTap(66, 1186, 121, 1220, "返回")  # 返回旅团首页
        任务记录['旅团-商店-完成'] = 1

    def shopBuy(self):
        re = TomatoOcrFindRangeClick('最大', whiteList='最大', x1=45, y1=460, x2=656, y2=1095)
        # if not re:
        #     return
        # ldE.element('旅团-购买').click().execute(sleep=1)
        re = TomatoOcrFindRangeClick('购买', whiteList='购买', x1=45, y1=460, x2=656, y2=1095)
        if not re:
            tapSleep(362, 866)  # 点击购买
            tapSleep(362, 843)  # 点击购买
        tapSleep(360, 1210)  # 点击空白处

    # 旅团大采购
    def lvTuanDaCaiGou(self):
        if 功能开关["旅团大采购"] == 0:
            return
        if 任务记录["旅团-大采购-完成"] == 1:
            return

        Toast("旅团 - 旅团大采购领取 - 开始")
        # 判断是否在旅团页面
        isLvtuan = False
        for i in range(2):
            res = TomatoOcrFindRangeClick("大采购", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-20)
            if not res:
                # 返回首页
                self.dailyTask.homePage()
                res = TomatoOcrTap(647, 576, 689, 597, "旅团", sleep1=1.5)
                # 判断是否在旅团页面
                res = TomatoOcrFindRangeClick("大采购", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-20)
                if res:
                    isLvtuan = True
                    break
            else:
                isLvtuan = True
                break
        if not isLvtuan:
            Toast("旅团 - 旅团大采购 - 未找到任务入口")
            return

        # 2025.5.8 游戏已支持一键领取。翻页领取下线
        re = FindColors.find("615,138,#F56042|619,135,#F86247|621,139,#F45E42|618,141,#F05E40",
                             rect=[479, 85, 649, 214], diff=0.95)
        if re:
            Toast("旅团 - 旅团大采购 - 领取奖励")
            tapSleep(588, 168)
        # 滑到最左
        # swipe(281, 1191, 656, 1194)
        # sleep(0.8)
        # swipe(281, 1191, 656, 1194)
        # sleep(0.8)
        # swipe(281, 1191, 656, 1194)
        # sleep(0.8)
        # swipe(281, 1191, 656, 1194)
        # sleep(0.8)

        # for k in range(35):
        #     re = FindColors.find("448,1164,#F35E41|450,1161,#F76143|450,1164,#F35E41", diff=0.97,
        #                          rect=[153, 1141, 717, 1246])
        #     if re:
        #         Toast('领取采购单')
        #         print(re)
        #         tapSleep(re.x - 10, re.y + 10)  # 点击待领取
        #         re2 = CompareColors.compare("562,314,#F3A84B|558,303,#F3A84B|571,315,#F6B35E")  # 判断可领取
        #         if re2:
        #             tapSleep(522, 310, 1)  # 点击领取
        #             tapSleep(344, 1251)  # 点击空白
        #             tapSleep(344, 1251)  # 点击空白
        #             tapSleep(344, 1251)  # 点击空白
        #     else:
        #         Toast('寻找待领取采购单')
        #         swipe(656, 1194, 450, 1191)  # 右滑
        #         sleep(1)
        #         re = FindColors.find_all(
        #             "203,1165,#A3A0AA|194,1217,#A4A1AB|216,1227,#A6A1AE|274,1222,#A6A1AD|279,1207,#8D8297|280,1167,#A6A1AD|279,1184,#A6A1AD",
        #             rect=[153, 1133, 699, 1243], diff=0.96)
        #         if re:
        #             break

    # 旅团任务
    def lvTuanRenWu(self):
        if 功能开关["旅团任务"] == 0:
            return
        if 任务记录["旅团-任务-完成"] == 1:
            return

        Toast("旅团 - 旅团任务领取 - 开始")
        # 判断是否在旅团页面
        isLvtuan = False
        for i in range(2):
            res = TomatoOcrFindRangeClick("旅团任务", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-20)
            if not res:
                # 返回首页
                self.dailyTask.homePage()
                res = TomatoOcrTap(647, 592, 689, 614, "旅团")
                # 判断是否在旅团页面
                res = TomatoOcrFindRangeClick("旅团任务", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-20)
                if res:
                    isLvtuan = True
                    break
            else:
                isLvtuan = True
                break
        if not isLvtuan:
            Toast("旅团 - 旅团任务领取 - 未找到任务入口")
            return

        for i in range(1, 5):
            re = TomatoOcrFindRangeClick('领取', whiteList='领取')
            if re:
                tapSleep(360, 1100)  # 点击空白处关闭
            else:
                break
        # 点击宝箱（从右到左）
        tapSleep(570, 390)
        tapSleep(490, 390)
        tapSleep(410, 390)
        tapSleep(330, 390)
        tapSleep(250, 390)

        res = tapSleep(97, 1218)  # 返回旅团首页
        任务记录["旅团-任务-完成"] = 1

    # 旅团许愿墙
    def lvTuanXuYuan(self):
        if 功能开关["旅团许愿墙"] == 0:
            return

        if 任务记录["旅团-许愿墙-完成"] == 1:
            return

        Toast("旅团 - 许愿墙 - 开始")

        chongWuName = ''
        if 功能开关['旅团自动许愿'] == 1:
            Toast("旅团 - 许愿墙 - 寻找主战宠物")
            for p in range(3):
                # 返回首页
                self.dailyTask.homePage()
                re = TomatoOcrTap(527, 1207, 593, 1232, '麦乐兽')
                if re:
                    tapSleep(350, 359)  # 点击主战宠物
                    re, chongWuName = TomatoOcrText(287, 388, 437, 423, '主战宠物')
                    if chongWuName != "":
                        Toast(f"旅团 - 许愿墙 - 主战宠物{chongWuName}")
                        break

        # 判断是否在旅团页面
        isLvtuan = False
        for i in range(2):
            res = TomatoOcrFindRangeClick("许愿墙", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-30)
            if not res:
                # 返回首页
                self.dailyTask.homePage()
                res = TomatoOcrTap(647, 592, 689, 614, "旅团")
                # 判断是否在旅团页面
                res = TomatoOcrFindRangeClick("许愿墙", x1=626, y1=648, x2=709, y2=986, offsetX=20, offsetY=-30)
                if res:
                    isLvtuan = True
                    break
            else:
                isLvtuan = True
                break
        if not isLvtuan:
            Toast("旅团 - 许愿墙 - 未找到任务入口")
            return

        # if not CompareColors.compare("690,822,#EF5C3F|686,815,#FA6547|691,814,#FA6545") and not CompareColors.compare("691,776,#F05C3F|691,778,#F45842|693,774,#F46043"):
        #     Toast("旅团 - 许愿墙 - 已送满 - 跳过任务")
        #     任务记录["旅团-许愿墙-完成"] = 1
        #     return

        # res = TomatoOcrTap(636,858,699,887, "许愿墙", 20, -20)
        # if not res:
        #     res = TomatoOcrTap(637, 859, 697, 882, "许愿墙", 20, -20)
        #     if not res:
        #         res = TomatoOcrTap(636, 817, 701, 839, "许愿墙", 20, -20)
        #         if not res:
        #             return

        # 自动许愿
        if 功能开关['旅团自动许愿'] == 1 and chongWuName != '':
            re = CompareColors.compare("143,336,#9D7D51|140,337,#9D7D51|142,339,#9D7D51")  # 判断能否许愿
            if re:
                tapSleep(140, 331, 1)  # 点击许愿
                re = TomatoOcrFindRangeClick(f'{chongWuName}拼图', x1=127, y1=190, x2=611, y2=973)
                if re:
                    tapSleep(359, 1024)  # 确认选择

        for i in range(4):
            Toast(f'旅团 - 许愿墙 - 捐献中{i}/5')
            TomatoOcrTap(116, 402, 164, 424, '领取', offsetX=10, offsetY=10)
            re = TomatoOcrFindRangeClick('捐献', whiteList='捐献')
            if re:
                # # 点击最大
                # tapSleep(504, 659)
                # tapSleep(504, 718)
                # tapSleep(504, 781)
                # 点击捐赠
                res = TomatoOcrTap(328, 822, 389, 854, "捐献")
                # res = TomatoOcrTap(97, 1200, 129, 1231, "回")  # 返回许愿墙首页
                tapSleep(365, 1214)  # 点击空白处
            else:
                if 功能开关['旅团许愿墙不捐公共'] == 0:
                    re = TomatoOcrFindRangeClick('公共捐献', whiteList='公共捐献')
                    if re:
                        res = TomatoOcrTap(328, 822, 389, 854, "捐献")
                    break

        res = TomatoOcrTap(96, 1183, 132, 1223, "回")  # 返回旅团首页
        任务记录["旅团-许愿墙-完成"] = 1
        return

    # 旅团签到
    def lvTuanWater(self):
        if 功能开关["旅团浇树"] == 0:
            return

        if 任务记录["旅团-浇树-完成"] == 1:
            return

        Toast("旅团 - 浇树 - 开始")

        self.dailyTask.homePage()

        res = TomatoOcrTap(641, 572, 691, 599, "旅团")
        if not res:
            self.dailyTask.homePage()
            res = TomatoOcrTap(641, 572, 691, 599, "旅团")
            if not res:
                return
        sleep(3)

        # 判断浇树已完成
        re, x, y = imageFind('旅团-浇水-已领取', x1=307, y1=172, x2=462, y2=329)
        if re:
            Toast('旅团 - 浇树 - 识别已完成')
            任务记录["旅团-浇树-完成"] = 1
            sleep(1)
            return

        tapSleep(400, 250, 3)  # 点击旅团浇水

        res, _ = TomatoOcrText(312, 627, 407, 655, "旅团之树")
        needCount = safe_int(功能开关["付费浇灌次数"])
        if needCount == '':
            needCount = 0
        buyCount = 0
        if res:
            while 1:
                res, buyCount = TomatoOcrText(400, 1137, 416, 1153, "已购买次数")  # 1/5
                buyCount = safe_int(buyCount)
                if buyCount == "" or buyCount - 1 >= needCount:
                    任务记录["旅团-浇树-完成"] = 1
                    break
                if buyCount == 0:
                    # 免费浇灌
                    tapSleep(360, 1100)
                    tapSleep(510, 1216, 0.3)  # 点击空白处关闭
                    sleep(1)

                    res, buyCount = TomatoOcrText(400, 1137, 416, 1153, "已购买次数")  # 1/5
                    buyCount = safe_int(buyCount)
                    # 付费浇灌
                    if buyCount != "" and buyCount - 1 < needCount:
                        tapSleep(360, 1100, 1.5)
                        tapSleep(465, 750, 1.5)
                        tapSleep(465, 750, 1.5)
                        tapSleep(510, 1216, 0.3)  # 点击空白处关闭
                        # tapSleep(510,1216,0.3)  # 点击空白处关闭
                else:
                    # 付费浇灌
                    if buyCount - 1 < needCount:
                        tapSleep(360, 1100, 1.5)
                        tapSleep(465, 750, 1.5)
                        tapSleep(465, 750, 1.5)
                        tapSleep(510, 1216, 0.3)  # 点击空白处关闭
                        # tapSleep(510,1216,0.3)  # 点击空白处关闭

            res = TomatoOcrTap(173, 1186, 205, 1218, "回")  # 返回旅团首页
            tapSleep(121, 1216)
            tapSleep(121, 1216)
