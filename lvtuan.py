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


class LvTuanTask:
    def __init__(self):
        self.dailyTask = DailyTask()

    def lvtuanTask(self):
        if 功能开关["旅团总开关"] == 0:
            return

        # 旅团签到
        self.lvTuanWater()

        # 旅团许愿墙
        self.lvTuanXuYuan()

        # 旅团任务
        self.lvTuanRenWu()

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
            needCount = 0
        while loopCount < needCount:
            loopCount = loopCount + 1
            Toast(f"旅团 - 调查队重复挑战第 {loopCount}/{needCount} 次")
            res1, _ = TomatoOcrText(636, 97, 670, 119, "秘钥")  # 识别调查队组队中 - 右上角 - 每日补给调查秘钥
            res2, _ = TomatoOcrText(501, 191, 581, 218, "离开队伍")  # 识别调查队组队中 - 右上角 - 离开队伍
            if res1 or res2:
                # 组队中，对出队伍重新开启调查；保证重新匹配队友
                TomatoOcrTap(501, 191, 581, 218, "离开队伍")  # 离开队伍
                TomatoOcrTap(331, 727, 387, 758, "确定")  # 离开队伍 - 确定
            else:
                # 重新进入调查队，重新选择队友；避免队友不足
                for i in range(1, 3):
                    res = TomatoOcrTap(632, 916, 702, 947, "调查队")
                    if not res:
                        res = TomatoOcrTap(647, 592, 689, 614, "旅团")
                        if not res:
                            # 返回首页
                            self.dailyTask.homePage()
                            # 退出组队
                            self.dailyTask.quitTeam()
                        else:
                            res = TomatoOcrTap(637, 947, 697, 971, "调查队", 30, -20)
                            if res:
                                break
                    else:
                        break

            res = TomatoOcrTap(307, 964, 412, 1002, "开启调查")
            if res:
                tapSleep(205, 760)  # 添加队友
                tapSleep(530, 435, 1)  # 添加队友1
                tapSleep(530, 556, 1)  # 添加队友2
                tapSleep(531, 674, 1)  # 添加队友3
                tapSleep(532, 794, 1)  # 添加队友4
                tapSleep(530, 910, 1)  # 添加队友5
                res = TomatoOcrTap(70, 1200, 123, 1231, "返回", 10, 10)
                res = TomatoOcrTap(331, 976, 386, 1005, "开始")
                sleep(5)
                if res:
                    # 战斗中
                    self.fighting()
                    sleep(5)
        任务记录['旅团-调查队-完成'] = 1

    # 判断是否战斗中
    def fighting(self):
        attempts = 0  # 初始化尝试次数
        maxAttempts = 30  # 设置最大尝试次数

        while attempts < maxAttempts:
            res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
            res, teamName2 = TomatoOcrText(8, 146, 52, 166, "队友名称")
            res1, _ = TomatoOcrText(642, 461, 702, 483, "麦克风")
            if res1 or (teamName1 != "" or teamName2 != ""):
                Toast("战斗中")
            else:
                break  # 识别失败，退出循环
            attempts = attempts + 1
            sleep(5)

        # 战斗结束
        self.openTreasure()

    # 领取宝箱（调查队）
    def openTreasure(self):
        attempts = 0
        maxAttempts = 2

        Toast("战斗结束 - 开启宝箱")
        while attempts < maxAttempts:
            attempts = attempts + 3
            # 调查队宝箱
            # 战斗结束页
            res = TomatoOcrTap(330, 1024, 390, 1051, "开启", 10, 20)
            if res:
                sleep(2)
                tapSleep(56, 1237)
                tapSleep(56, 1237)
            # 结算页
            res = TomatoOcrTap(333, 752, 388, 781, "开启")
            if res:
                sleep(1)
                tapSleep(340, 930)

            # -- 钥匙不足退出
            res1, _ = TomatoOcrText(535, 767, 566, 798, "0")
            res2, _ = TomatoOcrText(301, 1023, 417, 1048, "调查秘钥不足")
            res3, _ = TomatoOcrText(303, 755, 414, 778, "调查秘钥不足")
            if res1 or res2 or res3:
                Toast("钥匙不足")
                res = TomatoOcrTap(68, 1201, 130, 1232, "返回")
                if res:
                    res = TomatoOcrTap(329, 723, 391, 762, "确定")
                else:
                    # 提前退出
                    tapSleep(60, 1150)  # 点击空白处
                    res = TomatoOcrTap(329, 727, 388, 759, "确定")

    # 旅团商店
    def lvTuanShop(self):
        if 功能开关["旅团商店开关"] == 0:
            return

        if 任务记录["旅团-商店-完成"] == 1:
            return

        Toast("旅团 - 商店兑换 - 开始")
        self.dailyTask.homePage()
        res = TomatoOcrTap(647, 592, 689, 614, "旅团")
        res = TomatoOcrTap(635, 697, 700, 724, "服务区", 20)
        if not res:
            return
        sleep(4)  # 等待跳转动画

        # 翻页（先返回上面）
        swipe(360, 750, 360, 850)
        sleep(2.5)
        for i in range(1, 5):
            if 功能开关['旅团唤兽琴弦']:
                re = imageFindClick('旅团-唤兽琴弦')
                if re:
                    self.shopBuy()
            if 功能开关['旅团全价兽粮']:
                re = imageFindClick('旅团-全价兽粮')
                if re:
                    self.shopBuy()
            if 功能开关['旅团超级成长零食']:
                re = imageFindClick('旅团-超级成长零食')
                if re:
                    self.shopBuy()
            if 功能开关['旅团原材料']:
                re = imageFindClick('旅团-原材料')
                if re:
                    self.shopBuy()
            if 功能开关['旅团史诗经验']:
                re = imageFindClick('旅团-史诗经验')
                if re:
                    self.shopBuy()
            if 功能开关['旅团优秀经验']:
                re = imageFindClick('旅团-优秀经验')
                if re:
                    self.shopBuy()
            if 功能开关['旅团普通经验']:
                re = imageFindClick('旅团-普通经验')
                if re:
                    self.shopBuy()
            if 功能开关['旅团金币']:
                re = imageFindClick('旅团-金币')
                if re:
                    self.shopBuy()
            # 翻页
            swipe(360, 850, 360, 750)
            sleep(3.5)
        任务记录['旅团-商店-完成'] = 1

    def shopBuy(self):
        TomatoOcrFindRangeClick('最大', whiteList='最大')
        # ldE.element('旅团-购买').click().execute(sleep=1)
        tapSleep(362, 866)  # 点击购买
        tapSleep(360, 1210)  # 点击空白处

    # 旅团任务
    def lvTuanRenWu(self):
        if 功能开关["旅团任务"] == 0:
            return
        if 任务记录["旅团-任务-完成"] == 1:
            return

        Toast("旅团 - 旅团任务领取 - 开始")
        self.dailyTask.homePage()
        res = TomatoOcrTap(647, 592, 689, 614, "旅团")
        sleep(1)
        res = TomatoOcrTap(625, 769, 708, 797, "旅团任务", 20, -20)
        if not res:
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
        任务记录["旅团-任务-完成"] = 1

    # 旅团许愿墙
    def lvTuanXuYuan(self):
        if 功能开关["旅团许愿墙"] == 0:
            return

        if 任务记录["旅团-许愿墙-完成"] == 1:
            return

        Toast("旅团 - 许愿墙 - 开始")
        self.dailyTask.homePage()
        res = TomatoOcrTap(647, 592, 689, 614, "旅团")

        if not CompareColors.compare("690,822,#EF5C3F|686,815,#FA6547|691,814,#FA6545"):
            Toast("旅团 - 许愿墙 - 已送满 - 跳过任务")
            任务记录["旅团-许愿墙-完成"] = 1
            return

        res = TomatoOcrTap(637, 859, 697, 882, "许愿墙", 20, -20)
        if not res:
            return

        for i in range(1, 5):
            Toast(f'旅团 - 许愿墙 - 捐赠中{i}/5')
            re = TomatoOcrFindRangeClick('捐献', whiteList='捐献')
            if re:
                # # 点击最大
                # tapSleep(504, 659)
                # tapSleep(504, 718)
                # tapSleep(504, 781)
                # 点击捐赠
                res = TomatoOcrTap(328, 822, 389, 854, "捐赠")
                # res = TomatoOcrTap(97, 1200, 129, 1231, "回")  # 返回许愿墙首页
                tapSleep(365, 1214)  # 点击空白处
            else:
                break
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

        res = TomatoOcrTap(647, 592, 689, 614, "旅团")
        sleep(3)

        # 判断浇树已完成
        re, x, y = imageFind('旅团-浇水-已领取', x1=307, y1=172, x2=462, y2=329)
        if re:
            Toast('旅团 - 浇树 - 识别已完成')
            任务记录["旅团-浇树-完成"] = 1
            sleep(1)
            return

        tapSleep(400, 250, 3) # 点击旅团浇水

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
                    tapSleep(360, 1100)  # 点击空白处关闭
                    sleep(2)

                # 付费浇灌
                if buyCount - 1 < needCount:
                    tapSleep(360, 1100, 3)
                    tapSleep(465, 750, 3)
                    tapSleep(465, 750, 1)
                    tapSleep(355, 1220)  # 点击空白处关闭
