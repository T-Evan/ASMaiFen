# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .daily import DailyTask
from ascript.android.screen import Ocr
from .baseUtils import *
import re as repattern
from ascript.android.screen import FindColors


class YingDiTask:
    def __init__(self):
        self.dailyTask = DailyTask()

    def yingdiTask(self):
        if 功能开关["营地总开关"] == 0:
            return

        self.dailyTask.homePage(needQuitTeam=True)

        # 开启隐身
        self.HaoYouYinShen(needOpen=True)

        # 秘宝
        self.yingDiMiBao()

        # 每日商店
        self.yingDiShop()

    def yingdiTask2(self):
        # 露营打卡点
        self.luYingDaKa()

        # 舞会签到簿
        self.wuHuiQianDaoBu()

        if 功能开关["营地总开关"] == 0:
            return

        self.dailyTask.homePage(needQuitTeam=True)

        # 月签到
        self.yueqiandao()

        # 日礼包
        self.riLiBao()

        # 月卡
        self.yueKa()

    def yingdiTaskEnd(self):
        if 功能开关["营地总开关"] == 0:
            return

        self.dailyTask.homePage(needQuitTeam=True)

        # 纸翼大作战
        self.zhiFeiJi()

        # 星辰同行
        self.xingChenTongXing()

    # 好友隐身
    def HaoYouYinShen(self, needOpen=True):
        if 任务记录['隐身任务-完成'] == 1:
            return
        if needOpen:
            Toast('开始日常任务 - 开启隐身')
        if not needOpen:
            Toast('开始带队任务 - 关闭隐身')

        功能开关["fighting"] = 1
        功能开关["needHome"] = 0
        # 判断是否在营地页面
        res = False
        for k in range(3):
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if not res:
                # 返回首页
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
            else:
                break
        if not res:
            功能开关["fighting"] = 0
            Toast('好友隐身 - 未找到活动入口')
            return

        re = TomatoOcrTap(28, 276, 74, 301, '好友', offsetX=10, offsetY=-20, sleep1=0.8)
        if re:
            re, _ = TomatoOcrText(315, 1030, 366, 1062, '隐身')
            if re:
                open = CompareColors.compare("293,1049,#4AAD39|298,1052,#4CAE39|300,1049,#4AAD39")
                if (needOpen and not open) or (not needOpen and open):
                    tapSleep(300, 1046)  # 点击隐身
            re, _ = TomatoOcrText(315, 1030, 366, 1062, '隐身')
            if re:
                open = CompareColors.compare("293,1049,#4AAD39|298,1052,#4CAE39|300,1049,#4AAD39")
                if (needOpen and open) or (not needOpen and not open):
                    任务记录['隐身任务-完成'] = 1
            tapSleep(653, 1242)  # 返回
        tapSleep(360, 1193)  # 返回
        tapSleep(360, 1193)  # 返回
        功能开关["fighting"] = 0

    # 活动 - 星辰同行
    def xingChenTongXing(self):
        if 功能开关["星辰同行"] == 0:
            return

        if 任务记录['星辰同行-完成'] == 1:
            return

        Toast('营地任务 - 星辰同行 - 开始')
        # 判断是否在营地页面
        res1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = TomatoOcrTap(500, 1201, 545, 1228, "同行")
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return
        res = TomatoOcrTap(500, 1201, 545, 1228, "同行", sleep1=0.8)

        if res:
            # 开启新生星辰
            TomatoOcrTap(292, 1086, 426, 1117, "开启新生星辰")

            TomatoOcrTap(549, 313, 589, 336, "任务", sleep1=0.8)
            re, _ = TomatoOcrText(472, 301, 570, 336, '已领取')
            if re:
                Toast('星辰同行 - 已完成')
                任务记录['星辰同行-完成'] = 1
                TomatoOcrTap(94, 1186, 125, 1217, "回", sleep1=0.8)  # 返回活动首页
                res = TomatoOcrTap(232, 1093, 283, 1124, "领取", sleep1=0.8)  # 一键领取
                if res:
                    tapSleep(232, 1093)  # 点击空白处
                return

            TomatoOcrTap(255, 1076, 350, 1104, "每日任务", sleep1=0.8)
            TomatoOcrTap(496, 304, 547, 332, "领取", sleep1=0.8)
            tapSleep(345, 1058)  # 点击空白处关闭

            TomatoOcrTap(374, 1077, 472, 1106, "每周任务", sleep1=0.8)
            TomatoOcrTap(496, 304, 547, 332, "领取", sleep1=0.8)
            tapSleep(345, 1058)  # 点击空白处关闭

            # 赛季任务红点
            re = CompareColors.compare("596,1076,#F66245|598,1079,#F45F42|596,1079,#F36042")
            if re:
                tapSleep(541, 1095, 0.8)
                TomatoOcrTap(496, 304, 547, 332, "领取", sleep1=0.8)
                tapSleep(345, 1058)  # 点击空白处关闭

            TomatoOcrTap(94, 1186, 125, 1217, "回", sleep1=0.8)  # 返回活动首页
            res1 = TomatoOcrTap(232, 1093, 283, 1124, "领取", sleep1=0.8)  # 一键领取
            res2 = TomatoOcrTap(358, 1096, 412, 1122, "领取", sleep1=0.8)  # 一键领取
            if res1 or res2:
                tapSleep(232, 1093)  # 点击空白处
        tapSleep(96, 1201)  # 点击空白处
        tapSleep(96, 1201)  # 点击空白处
        tapSleep(356, 1205)  # 点击空白处

    # 活动 - 纸飞机
    def zhiFeiJi(self):
        if 功能开关["纸飞机"] == 0:
            return

        if 任务记录['纸飞机-完成'] == 1:
            return

        Toast('营地任务 - 纸飞机 - 开始')

        # 判断是否在营地页面
        res = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        if not res:
            # 返回首页
            self.dailyTask.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
            # 判断是否在营地页面
            hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                Toast('营地任务 - 纸飞机 - 未找到活动入口')
                return

        isFind = TomatoOcrFindRangeClick('纸翼大作战', sleep1=1)
        if not isFind:
            # -- 返回活动最后一屏
            self.huoDongSwipeDown()

            for i in range(1, 5):
                # 上翻第二屏，继续识别
                swipe(680, 451, 680, 804)
                sleep(3)
                isFind = TomatoOcrFindRangeClick('纸翼大作战', sleep1=1)
                if isFind:
                    break
        if isFind:
            # 判断限时特卖是否领取
            re = CompareColors.compare("680,1122,#EE5C3F|683,1122,#F05C3F|680,1117,#F56043")
            if re:
                Toast('领取免费特卖礼包')
                TomatoOcrTap(584, 1115, 677, 1145, "限时特卖", sleep1=0.8)
                TomatoOcrTap(145, 587, 200, 620, "免费", sleep1=0.8)
                TomatoOcrTap(339, 744, 381, 762, "免费", sleep1=0.8)
                tapSleep(394, 1133)  # 关闭弹窗
                tapSleep(394, 1133)  # 返回积分奖励页
                tapSleep(394, 1133, 0.8)

            # 自动购买礼包
            if 功能开关['纸飞机礼包购买'] == 1:
                Toast('购买钻石自选礼包')
                for k in range(3):
                    TomatoOcrTap(584, 1115, 677, 1145, "限时特卖", sleep1=0.8)
                    re = TomatoOcrFindRangeClick('星钻自选礼包', x1=85, y1=351, x2=636, y2=642, sleep1=0.8)
                    if not re:
                        re = TomatoOcrTap(101, 478, 226, 508, '星钻自选礼包', sleep1=0.8)
                    if re:
                        TomatoOcrTap(337, 719, 382, 741, "购买", sleep1=0.8)
                    tapSleep(394, 1133)  # 关闭弹窗
                    tapSleep(394, 1133)  # 返回积分奖励页
                    tapSleep(394, 1133, 0.8)
                    if not re:
                        break

            # 自动购买礼包
            if 功能开关['纸飞机信物兑换'] == 1:
                Toast('信物兑换')
                TomatoOcrTap(461, 1115, 560, 1149, "信物兑换", sleep1=0.8)
                tapSleep(358, 991, 0.8)
                re = TomatoOcrTap(336, 804, 383, 827, "购买", sleep1=0.8)
                tapSleep(394, 1133)  # 关闭弹窗
                tapSleep(394, 1133, 0.8)  # 返回积分奖励页

            # 判断是否完成
            res, _ = TomatoOcrText(549, 282, 625, 303, '100/100')
            if res:
                Toast('纸翼大作战 - 已完成')
                res = TomatoOcrTap(359, 1056, 409, 1087, "领取")  # 一键领取
                tapSleep(345, 1058)  # 点击空白处关闭
                res = TomatoOcrTap(94, 1186, 125, 1217, "回")  # 返回活动首页
                任务记录['纸飞机-完成'] = 1
                return

            res, _ = TomatoOcrText(554, 233, 595, 254, "任务")
            if res:
                tapSleep(575, 226, 0.8)
            res = TomatoOcrTap(496, 304, 547, 332, "领取")
            tapSleep(345, 1058)  # 点击空白处关闭
            res = TomatoOcrTap(94, 1186, 125, 1217, "回")  # 返回纸飞机首页
            res = TomatoOcrTap(359, 1056, 409, 1087, "领取")  # 一键领取
            res = TomatoOcrTap(359, 1056, 409, 1087, "领取")  # 一键领取
            tapSleep(345, 1058)  # 点击空白处关闭
            res = TomatoOcrTap(94, 1186, 125, 1217, "回")  # 返回活动首页

    # 月卡
    def yueKa(self):
        if 功能开关["月卡"] == 0:
            return

        if 任务记录["月卡-完成"] == 1:
            return
        Toast('营地任务 - 月卡 - 开始')

        # 判断是否在营地页面
        res1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = TomatoOcrTap(366, 1196, 442, 1232, "月月卡")
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()

            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return
        res = TomatoOcrTap(366, 1196, 442, 1232, "月月卡")
        sleep(1)
        if res:
            res = TomatoOcrTap(315, 1044, 410, 1090, "领取", 10, 10)
            if res:
                任务记录["月卡-完成"] = 1
                tapSleep(60, 1135)  # 点击空白处关闭
            res2, _, _ = TomatoOcrFindRange('续卡')
            res3, _, _ = TomatoOcrFindRange('未激活')
            if res2 or res3:
                任务记录["月卡-完成"] = 1
            # 支付页兜底
            tapSleep(665, 142)
            res = TomatoOcrTap(91, 1184, 126, 1222, "回")  # 返回

    # 日礼包
    def riLiBao(self):
        if 功能开关["日礼包"] == 0:
            return

        if 任务记录["日礼包-完成"] == 1:
            return
        Toast('营地任务 - 日礼包 - 开始')
        # 判断是否在营地页面
        res1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = TomatoOcrTap(286, 1202, 340, 1229, "礼包", sleep1=0.8)
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return

        res = TomatoOcrTap(286, 1202, 340, 1229, "礼包", sleep1=0.8)
        sleep(1)
        if res:
            res = TomatoOcrTap(148, 671, 198, 700, "免费", sleep1=0.8)
            if res:
                res = TomatoOcrTap(339, 743, 379, 764, "免费", sleep1=0.8)
                if res:
                    任务记录["日礼包-完成"] = 1
                    tapSleep(345, 1058)  # 点击空白处关闭

    # 旅行活动翻页
    def huoDongSwipeDown(self):
        # -- 返回活动最后一屏
        for i in range(5):
            swipe(364, 1133, 680, 51, dur=400)
            sleep(2)
            re = CompareColors.compare("276,1128,#EBE4D3|296,1126,#ECE4D3|311,1125,#EBE4D3|339,1125,#EEE7D6")
            if re:
                break

    # 月签到
    def yueqiandao(self):
        if 功能开关["月签到"] == 0:
            return

        if 任务记录["月签到-完成"] == 1:
            return
        Toast('营地任务 - 月签到 - 开始')

        # 返回首页
        self.dailyTask.homePage()

        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1)
        # 判断是否在营地页面
        hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        isFind = TomatoOcrFindRangeClick('月签到', x1=82, y1=61, x2=653, y2=1153)
        if not isFind:
            # -- 返回活动最后一屏
            self.huoDongSwipeDown()

            for i in range(1, 5):
                # 上翻第二屏，继续识别
                swipe(680, 451, 680, 804)
                sleep(3)
                isFind = TomatoOcrFindRangeClick('月签到', x1=82, y1=61, x2=653, y2=1153)
                if isFind:
                    break
        if isFind:
            sleep(1.5)
            TomatoOcrTap(315, 980, 407, 1010, "点击签到")
            # re, x, y = imageFind('月签到-累计奖励', confidence1=0.7)
            point = FindColors.find("361,232,#E65638|361,225,#F46042|366,224,#F55E42", rect=[91, 200, 622, 355],
                                    diff=0.8)
            if point:
                print(point.x, point.y)
                tapSleep(point.x, point.y, 1)
            任务记录["月签到-完成"] = 1
            tapSleep(36, 1123)  # 点击空白处关闭
        return

    # 舞会签到簿
    def wuHuiQianDaoBu(self):
        if 功能开关["舞会签到簿"] == 0:
            return

        if 任务记录["舞会签到簿-完成"] == 1:
            return
        Toast('营地任务 - 舞会签到簿 - 开始')

        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        isFind = TomatoOcrFindRangeClick('舞会签到簿')
        if not isFind:
            # -- 返回活动最后一屏
            self.huoDongSwipeDown()

            for i in range(1, 5):
                # 上翻第二屏，继续识别
                swipe(680, 451, 680, 804)
                sleep(3)
                isFind = TomatoOcrFindRangeClick('舞会签到簿')
                if isFind:
                    break
        if isFind:
            for i in range(3):
                res = TomatoOcrFindRangeClick('领取', x1=457, y1=538, x2=618, y2=875, sleep1=0.7)
                if res:
                    tapSleep(342, 1145)  # 点击空白处关闭
            任务记录["舞会签到簿-完成"] = 1
            TomatoOcrTap(94, 1186, 126, 1220, '回')

    # 露营打卡点
    def luYingDaKa(self):
        if 功能开关["露营打卡点"] == 0:
            return

        if 任务记录["露营打卡点-完成"] == 1:
            return
        Toast('营地任务 - 露营打卡点 - 开始')

        # 返回首页
        self.dailyTask.homePage()

        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        # todo: 找图露营打卡点
        isFind = False
        if not isFind:
            # -- 返回活动第一屏
            swipe(680, 451, 680, 804)
            sleep(2)
            swipe(680, 451, 680, 804)
            sleep(2)
            swipe(680, 451, 680, 804)
            sleep(2)

            for i in range(1, 5):
                # 下翻第二屏，继续识别
                swipe(680, 804, 680, 451)
                sleep(3)
                # todo: 找图露营打卡点
                if isFind:
                    break
        if isFind:
            # todo: 点击露营打卡点
            # todo: 点击领取按钮
            任务记录["露营打卡点-完成"] = 1
            tapSleep(35, 1054)  # 点击空白处关闭
        return

    # 秘宝收集
    def yingDiMiBao(self):
        if 功能开关["秘宝收集"] == 0:
            return

        Toast('营地任务 - 秘宝收集 - 开始')
        if 任务记录["秘宝领取-完成"] == 1:
            Toast('营地任务 - 秘宝领取 - 任务已执行 - 跳过')
            return

        # 判断是否在营地页面
        res = False
        for k in range(3):
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if not res:
                # 返回首页
                Toast('营地任务 - 秘宝收集 - 重新寻找活动入口')
                self.dailyTask.homePage()
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.6)
            else:
                break
        if not res:
            Toast('营地任务 - 秘宝收集 - 未找到活动入口')

        # 判断秘宝已完成
        isDone = CompareColors.compare(
            "235,162,#334654|246,173,#A5A9AC|241,181,#FFFFFF|247,181,#9FA2A6|257,178,#8C9296|262,175,#384153")
        if not isDone:
            isDone = CompareColors.compare(
                "266,162,#425D7A|249,179,#FFFFFF|255,173,#FFFFFF|247,162,#FEFEFE|258,170,#FFFFFF|262,187,#FFFFFF|271,165,#3D5775")
        if not isDone:
            isDone = CompareColors.compare(
                "247,176,#E9EAEA|251,181,#F4F5F5|241,184,#FFFFFF|252,183,#F2F3F3|262,190,#E4E6E6|257,168,#FFFFFF")
        # re, x, y = imageFind('营地-秘宝-已领取', x1=194, y1=123, x2=315, y2=232, timeLock=10)
        if isDone:
            Toast('营地任务 - 秘宝领取 - 识别已完成')
            任务记录["秘宝领取-完成"] = 1
            # sleep(1)
            # return

        # 点击秘宝
        re = False
        for i in range(5):
            re, _ = TomatoOcrText(613, 172, 695, 191, '补充能源')
            if not re:
                Toast('营地任务 - 秘宝收集 - 识别活动入口')
                tapSleep(241, 192, 0.5)  # 秘宝
                tapSleep(67, 33)  # 兜底点击太快，错误进入寻宝页
            else:
                tapSleep(67, 33)  # 兜底点击太快，错误进入寻宝页
                break

        if not re:
            tapSleep(194, 178, 2.5)  # 秘宝
            re, _ = TomatoOcrText(630, 1210, 680, 1237, '秘宝')
            if not re:
                tapSleep(282, 178, 2.5)  # 秘宝
                re, _ = TomatoOcrText(527, 1212, 609, 1237, '秘宝产出')
                if not re:
                    Toast('营地任务 - 秘宝领取 - 识别未开启')
                    任务记录["秘宝领取-完成"] = 1
                    sleep(1)
                    return

        # 识别最新地图
        if 功能开关["秘宝地图"] == "最新地图":
            res = TomatoOcrTap(527, 1212, 609, 1237, "秘宝产出", sleep1=2.5)
            if res:
                res, 功能开关["秘宝地图"] = TomatoOcrText(465, 1014, 581, 1046, '秘宝地图')
                if 功能开关["秘宝地图"] == "":
                    res, 功能开关["秘宝地图"] = TomatoOcrText(270, 1008, 475, 1055, '秘宝地图')
                tapSleep(373, 1166)  # 返回
                Toast(f'识别最新地图 - {功能开关["秘宝地图"]}')

        # 判断能量是否已满；能量已满暂不领取能源
        res, availableNengLiang = TomatoOcrText(607, 80, 661, 102, "剩余能量")  # 右上角剩余嫩俩
        availableNengLiang = safe_int(availableNengLiang.replace("x", ""))
        if not isDone and (availableNengLiang == '' or availableNengLiang < 200):  # 识别剩余体力>200时，无需领取和补充能源
            # 领取秘宝能量
            findNL = False
            findNum = 0

            for i in range(2):
                Toast('寻找秘宝能量')
                re, x, y = imageFind('秘宝能量', 0.78)
                if re:
                    findNL = True
                    tapSleep(x, y, 2)
                    tapSleep(360, 1100)  # 点击空白处关闭
                if findNL:
                    break

            # 返回上半屏
            if not findNL:
                if 功能开关["秘宝地图"] in ["巨像的旷野", "白帆之都", "石松沼泽", "天鹅仙宫", "妖精旷野", "地底浓林",
                                            "翡翠浦", "罗马尼安"]:
                    re = FindColors.find("186,1262,#B18457|191,1262,#AD8053|195,1265,#AE8155", rect=[44, 8, 626, 45],
                                         diff=0.96)
                    if not re:
                        Toast("返回上半屏")
                        swipe(361, 547, 380, 918, 800)
                        sleep(1)
                        tapSleep(67, 33)

                for i in range(4):
                    Toast('寻找秘宝能量')
                    re, x, y = imageFind('秘宝能量', 0.78)
                    if re:
                        findNL = True
                        tapSleep(x, y, 2)
                        tapSleep(360, 1100)  # 点击空白处关闭
                    else:
                        # 先找右侧
                        swipe(525, 1070, 180, 1070, 800)
                        sleep(2.2)
                        # 领取秘宝能量
                        re, x, y = imageFind('秘宝能量', 0.78)
                        if re:
                            findNL = True
                            tapSleep(x, y, 2)
                            tapSleep(360, 1100)  # 点击空白处关闭
                    if findNL:
                        break
                    findNum = i

                # 返回左侧
                for j in range(1, findNum):
                    swipe(180, 1070, 525, 1070, 800)
                    sleep(2.5)

                if not findNL:
                    for i in range(4):
                        re, x, y = imageFind('秘宝能量', 0.78)
                        if re:
                            tapSleep(x, y, 2.5)
                            tapSleep(360, 1100)  # 点击空白处关闭
                            break
                        else:
                            # 再找左侧
                            swipe(180, 1070, 525, 1070, 800)
                            sleep(2.2)
                            # 领取秘宝能量
                            re, x, y = imageFind('秘宝能量', 0.78)
                            if re:
                                tapSleep(x, y, 2)
                                tapSleep(360, 1100)  # 点击空白处关闭

            # 返回下半屏地图
            # if 功能开关["秘宝地图"] == "白帆之都" or 功能开关["秘宝地图"] == "石松沼泽" or 功能开关[
            #     "秘宝地图"] == "天鹅仙宫":
            #     re = FindColors.find("186,1262,#B18457|191,1262,#AD8053|195,1265,#AE8155", rect=[103, 1245, 573, 1273],
            #                          diff=0.96)  # 底部牛皮纸
            #     if not re:
            #         Toast("返回下半屏")
            #         swipe(380, 918, 361, 547)
            #         sleep(1)
        else:
            if isDone:
                Toast('秘宝能量已领取 - 跳过领取')
            else:
                Toast('秘宝能量已满 - 跳过领取')

        # 购买秘宝能量
        needNengLiang = False
        res, availableNengLiang = TomatoOcrText(593, 82, 672, 104, "剩余能量")  # 210
        availableNengLiang = safe_int(availableNengLiang.replace("x", ""))
        if availableNengLiang != '' and availableNengLiang < 200:  # 识别剩余体力不足200时，尝试补充
            needNengLiang = True

        if needNengLiang:
            tapSleep(690, 90, 1.5)
            needCount = safe_int(功能开关["秘宝钻石兑换次数"])
            if needCount == '':
                needCount = 0
            for i in range(1, 5):
                buyCount = ""
                for j in range(1, 5):
                    res, buyCount = TomatoOcrText(398, 595, 559, 628, "已购买次数")  # 1 / 9
                    buyCount = (buyCount.replace("每日限购", "").replace("/15", "").
                                replace("(", "").replace(")", "").replace("（", "").
                                replace("）", "").replace("/", "").replace("15", "").replace(" ", ""))
                    buyCount = safe_int(buyCount)
                    if buyCount != "":
                        break
                if buyCount == "" or buyCount >= needCount:
                    TomatoOcrTap(93, 1185, 127, 1220, "回", 10, 10, sleep1=0.8)  # 返回芙
                    break
                if buyCount != "":
                    re, ct = TomatoOcrText(456, 552, 503, 582, '准备购买次数')
                    Toast(f'准备购买{ct}次')
                    ct = safe_int(ct)
                    if ct < needCount:
                        tapSleep(533, 565)  # 点击+1
                    re = TomatoOcrTap(445, 642, 511, 669, "购买", 10, 10, sleep1=0.8)

        tapSleep(326, 1216)  # 点击空白处
        tapSleep(326, 1216)
        res, availableNengLiang = TomatoOcrText(593, 82, 672, 104, "剩余能量")  # 210
        availableNengLiang = safe_int(availableNengLiang.replace("x", ""))
        if availableNengLiang != '' and availableNengLiang < 50:  # 识别剩余体力不足50时，退出寻宝循环
            Toast('秘宝能量不足 - 跳过寻宝')
            # 返回营地
            TomatoOcrTap(94, 1183, 125, 1220, "回")
            sleep(2)
            TomatoOcrTap(94, 1183, 125, 1220, "回")
            sleep(3)
            return

        findMap = self.miBaoChangeMap(0, 0)
        if findMap:
            for i in range(3):
                res, availableNengLiang = TomatoOcrText(593, 82, 672, 104, "剩余能量")  # 210
                availableNengLiang = safe_int(availableNengLiang.replace("x", ""))
                if availableNengLiang != '' and availableNengLiang < 50:  # 识别剩余体力不足100时，退出寻宝循环
                    # 购买秘宝能量
                    tapSleep(690, 90, 1.5)
                    needCount = safe_int(功能开关["秘宝钻石兑换次数"])
                    if needCount == '':
                        needCount = 0
                    for k in range(1, 5):
                        buyCount = ""
                        for j in range(1, 5):
                            res, buyCount = TomatoOcrText(398, 595, 559, 628, "已购买次数")  # 1 / 9
                            buyCount = (buyCount.replace("每日限购", "").replace("/15", "").
                                        replace("(", "").replace(")", "").replace("（", "").
                                        replace("）", "").replace("/", "").replace("15", "").replace(" ", ""))
                            buyCount = safe_int(buyCount)
                            if buyCount != "":
                                break
                        if buyCount == "" or buyCount >= needCount:
                            TomatoOcrTap(93, 1185, 127, 1220, "回", 10, 10, sleep1=0.8)  # 返回芙
                            break
                        if buyCount != "":
                            re, ct = TomatoOcrText(454, 550, 503, 585, '准备购买次数')
                            Toast(f'准备购买{ct}次')
                            ct = safe_int(ct)
                            if ct < needCount:
                                tapSleep(527, 571)  # 点击+1
                            re = TomatoOcrTap(445, 642, 511, 669, "购买", 10, 10, sleep1=0.8)
                    res, availableNengLiang = TomatoOcrText(593, 82, 672, 104, "剩余能量")  # 210
                    availableNengLiang = safe_int(availableNengLiang.replace("x", ""))
                    if availableNengLiang != '' and availableNengLiang < 50:  # 识别剩余体力不足100时，退出寻宝循环
                        break
                    # 返回秘宝首页，避免寻宝页卡死

                if availableNengLiang != '' and availableNengLiang >= 100:
                    tapSleep(580, 880)  # 拉满10次
                res1 = TomatoOcrTap(420, 1117, 470, 1145, "寻宝")  # 能力足够多次10连时，右侧寻宝多次按钮
                res2 = TomatoOcrTap(228, 1118, 280, 1145, "寻宝")  # 能力足够多次10连时，左侧单次寻宝按钮
                res3 = TomatoOcrTap(331, 1119, 386, 1147, "寻宝")  # 能量不足10次时，只展示单次寻宝按钮
                if res1 or res2 or res3:
                    # 判断能源是否用尽
                    res, _ = TomatoOcrText(316, 343, 404, 370, "补充能源")
                    if res:
                        return

                    sleep(0.5)
                    while True:
                        res, _ = TomatoOcrText(93, 1184, 127, 1220, "回")  # 寻宝页，返回按钮
                        if res:  # 识别到返回按钮，确认寻宝结束，退出
                            tapSleep(65, 1120, 1)  # 点击空白处关闭
                            tapSleep(65, 1120, 1)  # 点击空白处关闭
                            break
                        TomatoOcrTap(584, 58, 633, 83, "跳过")
                        tapSleep(65, 1120, 1)  # 点击空白处关闭
                        tapSleep(65, 1120, 1)  # 点击空白处关闭
        # 返回营地
        TomatoOcrTap(94, 1183, 125, 1220, "回")
        sleep(1)

    def has_common_chars(self, A, B):
        # 将字符串转换为集合以获取唯一字符
        set_A = set(A)
        set_B = set(B)

        # 计算两个集合的交集
        common_chars = set_A.intersection(set_B)

        # 检查交集的大小是否至少为2
        return len(common_chars) >= 2

    def miBaoChangeMap(self, left, right):
        # 抽取秘宝
        selectMap = 功能开关["秘宝地图"]
        findMap = False

        if selectMap in ["巨像的旷野", "白帆之都", "石松沼泽", "天鹅仙宫", "妖精旷野", "地底浓林", "翡翠浦",
                         "罗马尼安"]:
            re = FindColors.find("186,1262,#B18457|191,1262,#AD8053|195,1265,#AE8155", rect=[103, 1245, 573, 1273],
                                 diff=0.96)  # 底部牛皮纸
            if not re:
                Toast("返回下半屏")
                swipe(380, 918, 361, 547, 800)
                sleep(1)
                tapSleep(67, 33)

        # 先找右侧
        if left == 0 and 0 < right < 4:
            if selectMap in ["巨像的旷野", "白帆之都", "石松沼泽", "天鹅仙宫", "妖精旷野", "地底浓林", "翡翠浦",
                             "罗马尼安"]:
                re = FindColors.find("186,1262,#B18457|191,1262,#AD8053|195,1265,#AE8155", rect=[103, 1245, 573, 1273],
                                     diff=0.96)  # 底部牛皮纸
                if not re:
                    Toast("返回下半屏")
                    swipe(380, 918, 361, 547, 800)
                    sleep(1)
                    tapSleep(67, 33)
            else:
                swipe(420, 200, 420, 600, 800)
                sleep(2)
            swipe(600, 1070, 100, 1070, 800)
            sleep(2)

        # 再找左侧
        if left < 4 and right == 4:
            if selectMap in ["巨像的旷野", "白帆之都", "石松沼泽", "天鹅仙宫", "妖精旷野", "地底浓林", "翡翠浦",
                             "罗马尼安"]:
                re = FindColors.find("186,1262,#B18457|191,1262,#AD8053|195,1265,#AE8155", rect=[103, 1245, 573, 1273],
                                     diff=0.96)  # 底部牛皮纸
                if not re:
                    Toast("返回下半屏")
                    swipe(380, 918, 361, 547, 800)
                    sleep(1)
                    tapSleep(67, 33)
            else:
                swipe(420, 200, 420, 600, 800)
                sleep(2)
            swipe(100, 1070, 600, 1070, 800)
            sleep(2)

        if selectMap == "暗月深林":
            re, x, y = imageFind('暗月深林')
            if re:
                tapSleep(x, y, 2)
                findMap = True

        if selectMap == "艾特拉火山":
            re, x, y = imageFind('艾特拉火山')
            if re:
                tapSleep(x, y, 2)
                findMap = True

        if selectMap == "鲁尔绿洲":
            re, x, y = imageFind('鲁尔绿洲')
            if re:
                tapSleep(x, y, 2)
                findMap = True

        if selectMap == "燃烧塔":
            re, x, y = imageFind('燃烧塔')
            if re:
                tapSleep(x, y, 2)
                findMap = True

        if not findMap:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': selectMap, 'match_mode': 'fuzzy'},
                                                   {'keyword': selectMap[:2], 'match_mode': 'fuzzy'},
                                                   {'keyword': selectMap[-2:], 'match_mode': 'fuzzy'}], sleep1=2,
                                         whiteList=selectMap)
            if re:
                findMap = True

        if not findMap:
            # 左右均未找到
            if left >= 4 and right >= 4:
                return findMap

            # 再找左侧
            if right >= 4:
                return self.miBaoChangeMap(left + 1, 4)

            # 先找右侧
            return self.miBaoChangeMap(0, right + 1)
        return findMap

    def yingDiShop(self):
        if 功能开关["仓鼠百货"] == 0:
            return

        if 任务记录["仓鼠百货-完成"] == 1:
            return

        Toast('营地任务 - 仓鼠百货 - 开始')

        # 判断是否在营地页面
        res = False
        for k in range(3):
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if not res:
                # 返回首页
                Toast('营地任务 - 仓鼠百货 - 重新寻找活动入口')
                self.dailyTask.homePage()
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.6)
            else:
                break
        if not res:
            Toast('营地任务 - 仓鼠百货 - 未找到活动入口')

        # # 判断仓鼠百货已完成
        # re, x, y = imageFind('营地-仓鼠商店-已领取', x1=383, y1=202, x2=560, y2=370)
        # if re:
        #     Toast('营地任务 - 仓鼠百货 - 识别已完成')
        #     任务记录["仓鼠百货-完成"] = 1
        #     sleep(1)
        #     return

        # 点击仓鼠百货
        tapSleep(475, 285, 3)

        # 判断是否进入商店
        re, _ = TomatoOcrText(268, 1203, 359, 1236, '仓鼠百货')
        if not re:
            Toast('营地任务 - 仓鼠百货 - 进入失败')
            return

        # 开始购买
        # 返回第一屏
        swipe(360, 805, 360, 1165)
        sleep(1)

        # 判断是否已购买完成
        # re = CompareColors.compare(
        #     "145,714,#E1DBD1|420,718,#E6E1D8|557,718,#E6E1D8|146,916,#E6E1D8|282,913,#E6E1D8|420,915,#E6E1D8")
        # if re:
        #     任务记录["仓鼠百货-完成"] = 1
        #     Toast('营地任务 - 仓鼠百货 - 已购买完成')

        if 1:
            for i in range(2):
                # 免费金币箱
                res, _ = TomatoOcrText(122, 694, 184, 718, "已售罄")
                if not res:
                    tapSleep(145, 630)  # 金币箱
                    tapSleep(360, 825, 0.6)  # 购买
                    tapSleep(360, 1100, 1)  # 点击空白处关闭

                # 原材料
                if 功能开关['商店原材料'] == 1:
                    re, x, y = TomatoOcrFindRange('原材料', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 原材料')
                            imageFindClick('仓鼠-原材料', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('原材料 - 已购买')

                # 星星经验
                if 功能开关['商店星星经验'] == 1:
                    re, x, y = TomatoOcrFindRange('星星经验', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 星星经验')
                            imageFindClick('星星经验', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('星星经验 - 已购买')

                if 功能开关['商店全价兽粮'] == 1:
                    re, x, y = TomatoOcrFindRange('全价兽粮', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 全价兽粮')
                            imageFindClick('全价兽粮', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('全价兽粮 - 已购买')

                if 功能开关['商店超级成长零食三折'] == 1:
                    re, x, y = TomatoOcrFindRange('超级成长零食', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 超级成长零食三折')
                            imageFindClick('超级成长零食三折', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('超级成长零食三折 - 已购买')

                if 功能开关['商店黑烬突破石五折'] == 1:
                    re, x, y = TomatoOcrFindRange('黑烬突破石', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 黑烬突破石五折')
                            imageFindClick('黑烬突破石五折', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('黑烬突破石五折 - 已购买')

                if 功能开关['商店经验补剂五折'] == 1:
                    re, x, y = TomatoOcrFindRange('经验补剂', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 经验补剂五折')
                            imageFindClick('经验补剂五折', x1=55, y1=479, x2=655, y2=951, confidence1=0.8)
                            self.shopBuy()
                        else:
                            Toast('经验补剂五折 - 已购买')

                if 功能开关['商店无限棱镜五折'] == 1:
                    re, x, y = TomatoOcrFindRange('无限棱镜', x1=94, y1=560, x2=628, y2=950)
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 无限棱镜五折')
                            TomatoOcrFindRangeClick('无限棱镜', x1=94, y1=560, x2=628, y2=950)
                            self.shopBuy()
                        else:
                            Toast('无限棱镜五折 - 已购买')

                if 功能开关['商店金币箱五折'] == 1:
                    re, x, y = TomatoOcrFindRange('金币箱', x1=94, y1=560, x2=628, y2=950, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            Toast('营地任务 - 仓鼠百货 - 金币箱五折')
                            TomatoOcrFindRangeClick('金币箱', x1=78, y1=751, x2=637, y2=961, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('金币箱五折 - 已购买')

        # 秘境补给
        if 功能开关['秘境补给'] == 1:
            re = TomatoOcrTap(377, 1211, 469, 1235, "秘境补给", sleep1=0.8)
            if not re:
                TomatoOcrTap(483, 1205, 576, 1238, "秘境补给", sleep1=0.8)
            # 检查剩余能量
            res, availableNengLiang = TomatoOcrText(607, 80, 663, 104, "剩余补给劵")  # 210
            availableNengLiang = safe_int(availableNengLiang)
            if availableNengLiang != '' and availableNengLiang < 40:  # 识别剩余体力不足50时，退出寻宝循环
                Toast('秘境补给劵不足 - 跳过兑换')
            else:
                if 功能开关['秘境补给星钻'] == 1:
                    re, x, y = TomatoOcrFindRange('星钻', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('星钻', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('星钻 - 已购买')

                if 功能开关['秘境补给无限棱镜'] == 1:
                    re, x, y = TomatoOcrFindRange('无限棱镜', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('无限棱镜', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('无限棱镜 - 已购买')

                if 功能开关['秘境补给善意野兽积点卡'] == 1:
                    re, x, y = TomatoOcrFindRange('野兽积点', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('野兽积点', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('善意野兽积点卡 - 已购买')

                if 功能开关['秘境补给焕新刷具'] == 1:
                    re, x, y = TomatoOcrFindRange('焕新刷具', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('焕新刷具', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('焕新刷具 - 已购买')

                if 功能开关['秘境补给骑行兽基础晶石'] == 1:
                    re, x, y = TomatoOcrFindRange('基础晶石', x1=72, y1=542, x2=363, y2=959, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('基础晶石', x1=72, y1=542, x2=363, y2=959, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('焕新刷具 - 已购买')

                    re, x, y = TomatoOcrFindRange('基础晶石', x1=358, y1=550, x2=633, y2=959, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('基础晶石', x1=358, y1=550, x2=633, y2=959, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('焕新刷具 - 已购买')

                if 功能开关['秘境补给群星自选包'] == 1:
                    re, x, y = TomatoOcrFindRange('群星自选', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('群星自选', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('群星自选 - 已购买')

                swipe(356, 954, 352, 511)  # 下滑
                sleep(1)

                if 功能开关['秘境补给史诗经验'] == 1:
                    re, x, y = TomatoOcrFindRange('史诗经验', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('史诗经验', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('史诗经验 - 已购买')

                # swipe(356, 954, 352, 511)  # 下滑
                # sleep(1)

                # 兜底史诗经验在下一页
                if 功能开关['秘境补给史诗经验'] == 1:
                    re, x, y = TomatoOcrFindRange('史诗经验', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('史诗经验', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('史诗经验 - 已购买')

                if 功能开关['秘境补给绮想妙成真'] == 1:
                    re, x, y = TomatoOcrFindRange('妙成真', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('妙成真', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('妙成真 - 已购买')

                if 功能开关['秘境补给黑烬突破石'] == 1:
                    re, x, y = TomatoOcrFindRange('突破石', x1=94, y1=560, x2=628, y2=950, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('突破石', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('突破石 - 已购买')

                if 功能开关['秘境补给星星经验'] == 1:
                    re, x, y = TomatoOcrFindRange('星星经验', x1=94, y1=560, x2=628, y2=950, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('星星经验', x1=77, y1=542, x2=639, y2=1100, match_mode='fuzzy')
                            self.shopBuy()
                        else:
                            Toast('星星经验 - 已购买')

        # 返回营地
        TomatoOcrTap(67, 1182, 121, 1221, "返回")
        sleep(2)
        任务记录["仓鼠百货-完成"] = 1
        return

    def shopBuy(self):
        re1, _ = TomatoOcrText(282, 400, 434, 459, '购买道具')
        if not re1:
            re1, _ = TomatoOcrText(330, 836, 388, 858, '购买')
        if not re1:
            re1, _ = TomatoOcrText(331, 888, 385, 912, '购买')
        re2 = False
        if re1:
            re = TomatoOcrTap(475, 785, 513, 811, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrTap(473, 771, 514, 795, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrTap(472, 783, 514, 807, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrTap(472, 844, 513, 868, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrFindRangeClick('最大', whiteList='最大', x1=93, y1=643, x2=618, y2=1004)
            if not re:
                re, x, y = imageFind('商店购买', x1=52, y1=478, x2=634, y2=1149)
            if re:
                re = TomatoOcrTap(334, 842, 385, 867, '购买', offsetX=5, offsetY=5)
                if not re:
                    re = TomatoOcrTap(334, 828, 388, 852, '购买', offsetX=5, offsetY=5)
                if not re:
                    re = TomatoOcrTap(336, 817, 383, 841, '购买', offsetX=5, offsetY=5)
                if not re:
                    re = TomatoOcrTap(331, 888, 385, 912, '购买', offsetX=5, offsetY=5)
                if not re:
                    re = TomatoOcrFindRangeClick('购买', whiteList='购买', x1=93, y1=643, x2=618, y2=1004)
                # tapSleep(360, 855, 0.6)  # 购买
                if re:
                    tapSleep(360, 1100, 1)  # 点击空白处关闭
            tapSleep(360, 1100)  # 点击空白处关闭
            tapSleep(360, 1100)  # 点击空白处关闭
        tapSleep(360, 1100)  # 点击空白处关闭
