# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .daily import DailyTask
from ascript.android.screen import Ocr
from .baseUtils import *
import re as repattern


class YingDiTask:
    def __init__(self):
        self.dailyTask = DailyTask()

    def yingdiTask(self):
        if 功能开关["营地总开关"] == 0:
            return

        # 每日商店
        self.yingDiShop()

        # 秘宝
        self.yingDiMiBao()

        # 露营打卡点
        self.luYingDaKa()

        # 月签到
        self.yueqiandao()

        # 日礼包
        self.riLiBao()

        # 月卡
        self.yueKa()

    def yingdiTaskEnd(self):
        if 功能开关["营地总开关"] == 0:
            return

        # 纸翼大作战
        self.zhiFeiJi()

        # 星辰同行
        self.xingChenTongXing()

    # 活动 - 星辰同行
    def xingChenTongXing(self):
        if 功能开关["星辰同行"] == 0:
            return
        Toast('营地任务 - 星辰同行 - 开始')
        # 判断是否在营地页面
        res1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = OCRTapV2(500, 1201, 545, 1228, "同行")
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()
            res = OCRTapV2(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = OCRTapV2(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return
        res = OCRTapV2(500, 1201, 545, 1228, "同行")
        if res:
            TomatoOcrTap(549, 313, 589, 336, "任务")
            OCRTapV2(255, 1076, 350, 1104, "每日任务")
            OCRTapV2(496, 304, 547, 332, "领取")
            tapSleep(345, 1058)  # 点击空白处关闭

            OCRTapV2(374, 1077, 472, 1106, "每周任务")
            OCRTapV2(496, 304, 547, 332, "领取")
            tapSleep(345, 1058)  # 点击空白处关闭

            OCRTapV2(94, 1186, 125, 1217, "回")  # 返回活动首页
            res = OCRTapV2(232, 1093, 283, 1124, "领取")  # 一键领取
            if res:
                tapSleep(232, 1093)  # 点击空白处

    # 活动 - 纸飞机
    def zhiFeiJi(self):
        if 功能开关["纸飞机"] == 0:
            return

        Toast('营地任务 - 纸飞机 - 开始')

        # 判断是否在营地页面
        res = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        if not res:
            # 返回首页
            self.dailyTask.homePage()
            res = OCRTapV2(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = OCRTapV2(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return

        isFind = ldE.element_exist('营地-纸飞机')
        if not isFind:
            # -- 返回活动第一屏
            ldE.swipe([680, 451], [680, 804])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804])
            ldE.sleep(2)

            for i in range(1, 5):
                # 下翻第二屏，继续识别
                ldE.swipe([680, 804], [680, 451])
                ldE.sleep(3)
                isFind = ldE.element_exist('营地-纸飞机')
                if isFind:
                    break
        if isFind:
            isFind.click().execute(sleep=1)
            res = OCRTapV2(566, 228, 604, 250, "任务")
            res = OCRTapV2(496, 304, 547, 332, "领取")
            tapSleep(345, 1058)  # 点击空白处关闭
            res = OCRTapV2(94, 1186, 125, 1217, "回")  # 返回纸飞机首页
            res = OCRTapV2(359, 1056, 409, 1087, "领取")  # 一键领取
            tapSleep(345, 1058)  # 点击空白处关闭
            res = OCRTapV2(94, 1186, 125, 1217, "回")  # 返回活动首页

    # 月卡
    def yueKa(self):
        if 功能开关["月卡"] == 0:
            return

        if 任务记录["月卡-完成"] == 1:
            return
        Toast('营地任务 - 月卡 - 开始')

        # 判断是否在营地页面
        res1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = OCRTapV2(393, 1202, 439, 1229, "月卡")
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()

            res = OCRTapV2(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
            hd2 = OCRTapV2(11, 1111, 92, 1134, "旅行活动", 40, -20)
            if not hd1 and not hd2:
                return
        res = OCRTapV2(393, 1202, 439, 1229, "月卡")
        if res:
            res = OCRTapV2(333, 1054, 385, 1086, "领取")
            if res:
                任务记录["月卡-完成"] = 1
                tapSleep(60, 1135)  # 点击空白处关闭
            # 支付页兜底
            tapSleep(665, 142)
            res = OCRTapV2(91, 1184, 126, 1222, "回")  # 返回

    # 日礼包
    def riLiBao(self):
        if 功能开关["日礼包"] == 0:
            return

        if 任务记录["日礼包-完成"] == 1:
            return
        Toast('营地任务 - 日礼包 - 开始')
        # 判断是否在营地页面
        res1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        res2 = OCRTapV2(286, 1202, 340, 1229, "礼包")
        if not res1 and not res2:
            # 返回首页
            self.dailyTask.homePage()

        res = OCRTapV2(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = OCRTapV2(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if not hd1 and not hd2:
            return

        res = OCRTapV2(286, 1202, 340, 1229, "礼包")
        if res:
            res = OCRTapV2(148, 671, 198, 700, "免费")
            if res:
                res = OCRTapV2(339, 743, 379, 764, "免费")
                if res:
                    任务记录["日礼包-完成"] = 1
                    tapSleep(345, 1058)  # 点击空白处关闭

    # 月签到
    def yueqiandao(self):
        if 功能开关["月签到"] == 0:
            return

        if 任务记录["月签到-完成"] == 1:
            return
        Toast('营地任务 - 月签到 - 开始')

        # 返回首页
        self.dailyTask.homePage()

        res = OCRTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = OCRTapV2(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = OCRTapV2(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        isFind = ldE.element_exist('营地-月签到')
        if not isFind:
            # -- 返回活动第一屏
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)

            for i in range(1, 5):
                # 下翻第二屏，继续识别
                ldE.swipe([680, 804], [680, 451])
                ldE.sleep(3)
                isFind = ldE.element_exist('营地-月签到')
                if isFind:
                    break
        if isFind:
            isFind.click().execute(sleep=1)
            OCRTapV2(310, 977, 408, 1009, "点击签到")
            任务记录["月签到-完成"] = 1
            tapSleep(36, 1123)  # 点击空白处关闭
        return

    # 露营打卡点
    def luYingDaKa(self):
        if 功能开关["露营打卡点"] == 0:
            return

        if 任务记录["露营打卡点-完成"] == 1:
            return
        Toast('营地任务 - 露营打卡点 - 开始')

        # 返回首页
        self.dailyTask.homePage()

        res = OCRTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = OCRTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = OCRTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        # todo: 找图露营打卡点
        isFind = False
        if not isFind:
            # -- 返回活动第一屏
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)
            ldE.swipe([680, 451], [680, 804, 120])
            ldE.sleep(2)

            for i in range(1, 5):
                # 下翻第二屏，继续识别
                ldE.swipe([680, 804], [680, 451])
                ldE.sleep(3)
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

        # 判断是否在营地页面
        re = ldE.element_exist('营地-旅行活动')
        if not re:
            # 返回首页
            self.dailyTask.homePage()
            ldE.element('首页-营地').click().execute(sleep=1)
            # 判断是否在营地页面
            hd1 = ldE.element_exist('营地-旅行活动')
            if not hd1:
                return

        # 点击秘宝
        tapSleep(330, 170, 4)  # 秘宝

        # 领取秘宝能量
        re = ldE.element_exist('秘宝-能量')
        if re:
            re.click().execute(sleep=1)
            tapSleep(360, 1100)  # 点击空白处关闭
        else:
            # 先找右侧
            ldE.swipe([525, 1070], [180, 1070], 0.3)
            ldE.sleep(3)
            # 领取秘宝能量
            re = ldE.element_exist('秘宝-能量')
            if re:
                re.click().execute(sleep=1)
                tapSleep(360, 1100)  # 点击空白处关闭
            else:
                # 再找左侧
                ldE.swipe([180, 1070], [525, 1070], 0.3)
                ldE.sleep(3)
                # 领取秘宝能量
                re = ldE.element_exist('秘宝-能量')
                if re:
                    re.click().execute(sleep=1)
                    tapSleep(360, 1100)  # 点击空白处关闭

        # 购买秘宝能量
        needNengLiang = False
        res, availableNengLiang = TomatoOcrText(603, 80, 672, 101, "剩余能量")  # 210
        availableNengLiang = safe_int(availableNengLiang)
        if availableNengLiang != '' and availableNengLiang < 200:  # 识别剩余体力不足200时，尝试补充
            needNengLiang = True

        if needNengLiang:
            tapSleep(690, 90, 3)
            needCount = safe_int(功能开关["秘宝钻石兑换次数"])
            if needCount == '':
                needCount = 0
            for i in range(1, 3):
                res, buyCount = TomatoOcrText(497, 815, 509, 834, "已购买次数")  # 1 / 9
                buyCount = safe_int(buyCount)
                if buyCount != "" and buyCount >= needCount:
                    OCRTapV2(94, 1186, 125, 1218, "回")  # 返回秘宝首页，等待抽取
                    break
                if buyCount != "":
                    TomatoOcrTap(440, 869, 514, 896, "购买")

        findMap = self.miBaoChangeMap(0, 0)
        if findMap:
            for i in range(1, 4):
                res, availableNengLiang = TomatoOcrText(603, 80, 672, 101, "剩余能量")  # 210
                availableNengLiang = safe_int(availableNengLiang)
                if availableNengLiang != '' and availableNengLiang < 50:  # 识别剩余体力不足100时，退出寻宝循环
                    break
                    # 返回秘宝首页，避免寻宝页卡死

                if availableNengLiang != '' and availableNengLiang >= 100:
                    tapSleep(580, 880)  # 拉满10次
                res1 = OCRTapV2(420, 1117, 470, 1145, "寻宝")  # 能力足够多次10连时，右侧寻宝多次按钮
                res2 = OCRTapV2(228, 1118, 280, 1145, "寻宝")  # 能力足够多次10连时，左侧单次寻宝按钮
                res3 = OCRTapV2(331, 1119, 386, 1147, "寻宝")  # 能量不足10次时，只展示单次寻宝按钮
                if res1 or res2 or res3:
                    # 判断能源是否用尽
                    res, _ = OCRTextV2(316, 343, 404, 370, "补充能源")
                    if res:
                        return

                    while True:
                        res, _ = OCRTextV2(93, 1184, 127, 1220, "回")  # 寻宝页，返回按钮
                        if res:  # 识别到返回按钮，确认寻宝结束，退出
                            tapSleep(65, 1120, 1)  # 点击空白处关闭
                            tapSleep(65, 1120, 1)  # 点击空白处关闭
                            break
                        OCRTapV2(587, 78, 631, 105, "跳过")
                        OCRTapV2(586, 77, 631, 105, "跳过")
                        tapSleep(65, 1120, 1)  # 点击空白处关闭
                        tapSleep(65, 1120, 1)  # 点击空白处关闭
        # 返回营地
        OCRTapV2(94, 1183, 125, 1220, "回")
        ldE.sleep(2)
        OCRTapV2(94, 1183, 125, 1220, "回")
        ldE.sleep(3)

    def miBaoChangeMap(self, left, right):
        # 抽取秘宝
        selectMap = 功能开关["秘宝地图"]
        findMap = False
        # 先找右侧
        if left == 0 and right == 1:
            ldE.swipe([420, 200], [420, 600], 1.2, False, 0.01)
            ldE.sleep(2)
            ldE.swipe([600, 1070], [100, 1070], 1.2, False, 0.01)
            ldE.sleep(2)

        # 再找左侧
        if left == 1 and right == 1:
            ldE.swipe([420, 200], [420, 600], 1.2, False, 0.01)
            ldE.sleep(2)
            ldE.swipe([100, 1070], [600, 1070], 1.2, False, 0.01)
            ldE.sleep(2)

        if selectMap == "暗月深林":
            re = ldE.element_exist('秘宝-暗月深林')
            if re:
                re.click().execute(sleep=3)
                findMap = True

        if selectMap == "艾特拉火山":
            re = ldE.element_exist('秘宝-艾特拉火山')
            if re:
                re.click().execute(sleep=3)
                findMap = True

        if selectMap == "鲁尔绿洲":
            re = ldE.element_exist('秘宝-鲁尔绿洲')
            if re:
                re.click().execute(sleep=3)
                findMap = True

        if selectMap == "燃烧塔":
            re = ldE.element_exist('秘宝-燃烧塔')
            if re:
                re.click().execute(sleep=3)
                findMap = True

        if not findMap:
            # 左右均未找到
            if left == 1 and right == 1:
                return findMap

            # 再找左侧
            if right == 1:
                return self.miBaoChangeMap(1, 1)

            # 先找右侧
            return self.miBaoChangeMap(0, 1)
        return findMap

    def yingDiShop(self):
        if 功能开关["仓鼠百货"] == 0:
            return

        if 任务记录["仓鼠百货-完成"] == 1:
            return

        Toast('营地任务 - 仓鼠百货 - 开始')

        # 判断是否在营地页面
        re = ldE.element_exist('营地-旅行活动')
        if not re:
            # 返回首页
            self.dailyTask.homePage()
            ldE.element('首页-营地').click().execute(sleep=1)
            # 判断是否在营地页面
            hd1 = ldE.element_exist('营地-旅行活动')
            if not hd1:
                return

        # 点击仓鼠百货
        tapSleep(475, 285, 3)

        # 判断是否进入商店
        re = ldE.element_exist('仓鼠百货-仓鼠百货')
        if not re:
            Toast('营地任务 - 仓鼠百货 - 进入失败')
            return

        # 开始购买
        # 返回第一屏
        ldE.swipe([360,805], [360,965])
        ldE.sleep(2)

        # 免费金币箱
        res, _ = OCRText(122, 694, 184, 718, "已售罄")
        if not res:
            tapSleep(145, 630)  # 金币箱
            tapSleep(360, 825)  # 购买
            tapSleep(360, 1100, 1)  # 点击空白处关闭

        # 星星经验
        if 功能开关['商店星星经验'] == 1:
            ldE.element('仓鼠百货-星星经验').click().execute(sleep=1)
            re = ldE.element_exist('仓鼠百货-购买')
            if re:
                ldE.element('仓鼠百货-最大').click().execute(sleep=1)
                tapSleep(360, 825)  # 购买
                tapSleep(360, 1100, 1)  # 点击空白处关闭

        if 功能开关['商店全价兽粮'] == 1:
            ldE.element('仓鼠百货-全价兽粮').click().execute(sleep=1)
            re = ldE.element_exist('仓鼠百货-购买')
            if re:
                ldE.element('仓鼠百货-最大').click().execute(sleep=1)
                tapSleep(360, 855)  # 购买
                tapSleep(360, 1100, 1)  # 点击空白处关闭

        if 功能开关['商店超级成长零食三折'] == 1:
            ldE.element('仓鼠百货-超级成长零食三折').click().execute(sleep=1)
            re = ldE.element_exist('仓鼠百货-购买')
            if re:
                ldE.element('仓鼠百货-最大').click().execute(sleep=1)
                tapSleep(360, 820)  # 购买
                tapSleep(360, 1100, 1)  # 点击空白处关闭

        if 功能开关['商店黑烬突破石五折'] == 1:
            ldE.element('仓鼠百货-黑烬突破石五折').click().execute(sleep=1)
            re = ldE.element_exist('仓鼠百货-购买')
            if re:
                ldE.element('仓鼠百货-最大').click().execute(sleep=1)
                tapSleep(360, 820)  # 购买
                tapSleep(360, 1100, 1)  # 点击空白处关闭

        if 功能开关['商店经验补剂五折'] == 1:
            ldE.element('仓鼠百货-经验补剂五折').click().execute(sleep=1)
            re = ldE.element_exist('仓鼠百货-购买')
            if re:
                ldE.element('仓鼠百货-最大').click().execute(sleep=1)
                tapSleep(360, 855)  # 购买
                tapSleep(360, 1100, 1)  # 点击空白处关闭

        # 返回营地
        OCRTap(66, 1185, 121, 1219, "返回")
        ldE.sleep(2)
        任务记录["仓鼠百货-完成"] = 1
        return
