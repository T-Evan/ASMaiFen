# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .shilian import ShiLianTask
from .startUp import StartUp
from .res.ui.ui import 任务记录
from .baseUtils import *
from ascript.android import action
from .res.ui.ui import switch_lock
from .thread import *
import re as rePattern
from ascript.android.screen import FindColors
from ascript.android.action import Path


class DailyTask:
    def __init__(self):
        self.shilianTask = ShiLianTask()
        self.startupTask = StartUp("com.xd.cfbmf")

    def homePage(self, needQuitTeam=False):
        tryTimes = 0
        while True:
            tryTimes = tryTimes + 1
            # todo 区分是否进入的摸鱼活动
            # res6 = self.shilianTask.WaitFight()

            if tryTimes > 3:
                point = FindColors.find(
                    "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
                    rect=[61, 34, 322, 623], diff=0.93)
                if point:
                    Toast('收起喊话窗口')
                    tapSleep(point.x, point.y)

            if tryTimes > 10:
                # 暂不处理战败页启动，提高执行效率
                # 判断战败页面
                self.shilianTask.fight_fail()
                quitTeamRe = self.quitTeam()

            if tryTimes > 15:
                Toast('尝试退出待机状态')
                # 退出待机状态
                # reWait = CompareColors.compare(
                #     "63,1199,#EBEFA5|105,1197,#EBEFA5|180,1186,#EAEFA5|285,1193,#ECF0A6|331,1193,#ECF0A6|393,1182,#EBEEA4")
                # if reWait:
                swipe(213, 1104, 568, 1104)
                swipe(213, 1104, 568, 1104)
                tapSleep(666,1191)
                Toast('退出待机状态')

            if tryTimes > 20:
                Toast('尝试重启游戏')
                # 重启游戏
                self.startupTask.start_app()

            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            # return3 = TomatoOcrTap(91, 1185, 127, 1221, '回', 10, 10)
            # if return3:
            #     Toast('返回首页')

            if 功能开关["fighting"] == 1:
                sleep(2)
                continue

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
                shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                if not shou_ye1:
                    shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
                # 暂不处理，提高执行效率
                # if not shou_ye1:
                #     shou_ye2 = TomatoOcrFindRange('冒险手册', 0.9, 360, 0, 720, 1280, '冒险手册')
                # shou_ye2 = TomatoOcrFindRange('试炼', 0.9, 360, 0, 720, 1280, '试炼')
            if res2 or shou_ye1 or shou_ye2:
                # if TimeoutLock(switch_lock).acquire_lock():
                功能开关["needHome"] = 0
                # 功能开关["fighting"] = 0
                # TimeoutLock(switch_lock).release_lock()
                Toast('已返回首页')
                # sleep(0.5)
                if needQuitTeam:
                    quitTeamRe = self.quitTeam()
                return True

            # 开始异步处理返回首页
            # if TimeoutLock(switch_lock).acquire_lock():
            功能开关["needHome"] = 1
            # TimeoutLock(switch_lock).release_lock()

            # 判断宝箱开启
            self.shilianTask.openTreasure()
            sleep(0.5)

    # 日常任务聚合
    def dailyTask(self):
        # 世界喊话
        self.shijieShout()

        if 功能开关["日常总开关"] == 0:
            return

        self.homePage(needQuitTeam=True)

        # 日常相关

        # 活动
        # 前往新地图
        self.newMap()

        # 领取相关
        # 招式创造
        self.zhaoShiChuangZao()
        # 骑兽乐园
        self.qiShouLeYuan()
        # 邮件领取
        self.youJian()

    def dailyTask2(self):
        if 功能开关["日常总开关"] == 0:
            return

        self.homePage(needQuitTeam=True)

        # 释放1次战术技能
        self.meiRiJiNeng()
        # 洗练1次装备
        self.meiRiXiLian()
        # 升级1次麦乐兽
        self.meiRiMaiLeShou()

    # 每日任务 - 洗练1次装备
    def meiRiMaiLeShou(self):
        if not 功能开关['升级1次麦乐兽']:
            return

        if 任务记录["日常-升级1次麦乐兽-完成"] == 1:
            return

        Toast("每日任务 - 升级1次麦乐兽 - 开始")
        self.homePage()

        res = TomatoOcrTap(522, 1205, 598, 1235, "麦乐兽")

        tapSleep(551, 942)  # 仓库最后1个麦乐兽

        res = TomatoOcrTap(333, 1027, 358, 1049, "升")
        if res:
            tapSleep(138, 1051)  # 重置按钮
            res = TomatoOcrTap(440, 787, 513, 820, "重置")
            tapSleep(150, 1059)  # 点击空白处
            任务记录["日常-升级1次麦乐兽-完成"] = 1
        else:
            Toast("每日任务 - 升级1次麦乐兽 - 未找到升级入口")

    # 每日任务 - 洗练1次装备
    def meiRiXiLian(self):
        if not 功能开关['洗练1次装备']:
            return

        if 任务记录["日常-洗练1次装备-完成"] == 1:
            return

        Toast("每日任务 - 洗练1次装备 - 开始")
        self.homePage()

        res = TomatoOcrTap(233, 1205, 281, 1234, "行李")

        tapSleep(159, 680)  # 仓库第1件装备

        res1 = TomatoOcrTap(519, 1054, 595, 1090, "洗练", 10, 10)
        res2 = TomatoOcrTap(399, 1055, 473, 1090, "洗练", 10, 10)
        if res1 or res2:
            res = TomatoOcrTap(323, 978, 394, 1010, "洗练", 10, 10)
            tapSleep(249, 986)  # 保留原有
            任务记录["日常-洗练1次装备-完成"] = 1
        else:
            Toast("每日任务 - 洗练1次装备 - 未找到洗练入口")

    # 每日任务 - 释放1次战术技能
    def meiRiJiNeng(self):
        if not 功能开关['释放1次战术技能']:
            return

        if 任务记录["日常-释放1次战术技能-完成"] == 1:
            return

        Toast("每日任务 - 释放1次战术技能 - 开始")
        self.homePage()

        # 切为手动
        res = TomatoOcrTap(645, 882, 690, 902, "自动", 10, -10)
        # 点击技能
        for i in range(1, 5):
            Toast("每日任务 - 释放1次战术技能 - 进行中")
            self.homePage()
            tapSleep(511, 1076, 0.6)  # 1技能
            tapSleep(521, 1070, 0.6)  # 1技能
            tapSleep(543, 974, 0.6)  # 2技能
            tapSleep(544, 962, 0.6)  # 2技能
            tapSleep(649, 953, 0.6)  # 3技能
            tapSleep(659, 942, 0.6)  # 3技能
            sleep(3)
        # 切回自动
        res = TomatoOcrTap(645, 882, 690, 902, "手动", 10, -10)
        任务记录["日常-释放1次战术技能-完成"] = 1

    def shijieShout(self):
        if 功能开关['世界喊话'] == "":
            return 1

        Toast("世界喊话 - 开始")

        self.homePage()

        res1 = TomatoOcrTap(18, 1098, 97, 1134, "点击输入", 10, 10)
        res2 = False
        if not res1:
            res2 = TomatoOcrTap(17, 1103, 96, 1134, "点击输入", 10, 10)
        if res1 or res2:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            sleep(0.5)
            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
            action.input(功能开关["世界喊话"])
            tapSleep(360, 104, 0.5)  # 点击空白处确认输入
            shuru = TomatoOcrTap(78, 1156, 157, 1191, '点击输入')
            if shuru:
                action.input(功能开关["世界喊话"])
                tapSleep(360, 104, 0.5)  # 点击空白处确认输入
            res = TomatoOcrTap(555, 1156, 603, 1188, "发送", 10, 10)
            # if res:
            #     tapSleep(472, 771, 0.5)
        # 关闭喊话窗口
        tapSleep(472, 771, 0.5)

        if 功能开关['自动切换喊话频道']:
            for i in range(1, 10):
                # 关闭喊话窗口
                for j in range(3):
                    point = FindColors.find(
                        "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
                        rect=[61, 34, 322, 623], diff=0.93)
                    if point:
                        Toast('收起喊话窗口')
                        tapSleep(point.x, point.y)
                self.homePage()

                # print("切换喊话频道")
                Toast("切换喊话频道")
                # # 关闭喊话窗口
                # tapSleep(472, 771, 0.5)
                # 点击左下角聊天框，弹出上拉按钮
                tapSleep(123, 942, 0.5)
                tapSleep(28, 776, 0.5)
                # 点击世界频道
                # TomatoOcrTap(205, 75, 281, 108, '世界', 10, 10)
                tapSleep(236, 83, 0.4)
                res = TomatoOcrTap(546, 138, 625, 165, '切换频道', 10, 10)
                if not res:
                    continue

                res, 当前频道 = TomatoOcrText(148, 607, 266, 658, '当前频道')
                print('当前频道：' + 当前频道)
                当前频道数字 = rePattern.findall(r'\d+', 当前频道)
                # 检查列表是否为空
                if not 当前频道数字:
                    continue
                # print(当前频道数字)
                if 当前频道数字 == '':
                    continue
                当前频道数字 = safe_int(当前频道数字[0])

                res, 最大频道 = TomatoOcrText(405, 613, 517, 656, '最大频道')
                最大频道数字 = rePattern.findall(r'\d+', 最大频道)
                if not 最大频道数字 or 最大频道数字 == '':
                    最大频道数字 = 0
                else:
                    最大频道数字 = safe_int_v2(最大频道数字[0])
                    print('最大', 最大频道数字)

                下一频道数字 = 当前频道数字 - 1
                findNext = False
                if 下一频道数字 < 1:
                    tapSleep(442, 632)  # 点击最后一个频道
                    findNext = True
                else:
                    # print(下一频道数字)
                    下一频道 = '简体中文' + str(下一频道数字)
                    print('下一频道：' + 下一频道)
                    # 寻找下一频道
                    for k in range(8):
                        res = TomatoOcrFindRangeClick(下一频道, 0.9, 0.9, 101, 437, 617, 880)
                        if not res:
                            if 最大频道数字 > 0 and 最大频道数字 - 当前频道数字 > 40:
                                swipe(236, 828, 210, 381, 300)  # 翻20
                                sleep(0.8)
                                swipe(137, 699, 358, 634, 50)
                            elif 最大频道数字 > 0 and 最大频道数字 - 当前频道数字 > 20:
                                swipe(236, 828, 222, 568, 300)  # 翻10
                                sleep(0.5)
                                swipe(137, 699, 358, 634, 50)
                            elif 最大频道数字 - 当前频道数字 > 0:
                                swipe(225, 814, 225, 714, 300)  # 翻5
                                sleep(0.5)
                                swipe(137, 699, 358, 634, 50)
                            elif 最大频道数字 == 0 or 最大频道数字 - 当前频道数字 < 0:
                                swipe(225, 714, 225, 814, 300)  # 上翻5
                                sleep(0.5)
                                swipe(137, 699, 358, 634, 50)
                        if res:
                            findNext = True
                            break
                if findNext:
                    for q in range(3):
                        shuru1 = TomatoOcrTap(80, 1194, 118, 1226, '点击')
                        shuru2 = False
                        if not shuru1:
                            shuru2 = TomatoOcrTap(79, 1155, 118, 1191, '点击')
                        if shuru1 or shuru2:
                            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
                            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                            action.input(功能开关["世界喊话"])
                            Toast('输入文字结束')
                            sleep(0.5)
                            # tapSleep(353, 427, 0.5)  # 点击空白处确认输入
                            # re = TomatoOcrFindRangeClick('确定', 9, 591, 691, 1090)
                            shuru1 = TomatoOcrTap(80, 1194, 118, 1226, '点击')
                            shuru2 = False
                            if not shuru1:
                                shuru2 = TomatoOcrTap(79, 1155, 118, 1191, '点击')
                            if shuru1 or shuru2:
                                continue
                            else:
                                res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                                if not res:
                                    tapSleep(353, 427)  # 点击空白处确认输入
                                    res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                                # 关闭喊话窗口
                                point = FindColors.find(
                                    "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                                    rect=[11, 26, 364, 489])
                                if point:
                                    tapSleep(point.x, point.y, 1)
                                break
                        else:
                            res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                            if not res:
                                tapSleep(353, 427)  # 点击空白处确认输入
                                res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                            # 关闭喊话窗口
                            point = FindColors.find(
                                "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                                rect=[11, 26, 364, 489])
                            if point:
                                tapSleep(point.x, point.y, 1)
                            break
        return 0

    def dailyTaskEnd(self):
        # 摸鱼时间到
        self.huoDongMoYu()
        if 功能开关["日常总开关"] == 0:
            return

        self.homePage(needQuitTeam=True)
        # 日常相关

        # 活动
        # 火力全开
        self.huoLiQuanKai()
        # BBQ派对
        self.BBQParty()
        # 宝藏湖
        self.baoZangHu()
        # 登录好礼
        self.dengLuHaoLi()
        # 限时特惠
        self.XianShiTeHui()
        # 箱庭苗圃
        self.XiangTingMiaoPu()

        # 前往新地图
        self.newMap()

        # 冒险手册
        self.maoXianShouCe()

    # 冒险手册
    def maoXianShouCe(self):
        if 功能开关["日常总开关"] == 0 or 功能开关["冒险手册领取"] == 0:
            return
        Toast("日常 - 冒险手册领取 - 开始")
        self.homePage()
        res = TomatoOcrTap(626, 379, 711, 405, "冒险手册", 30, -20)
        if not res:
            Toast("识别冒险手册失败")
            return

        # 主线领取
        if CompareColors.compare("235,1104,#F05C3F|235,1101,#F45F42|233,1100,#F36042"):
            res = TomatoOcrTap(156, 1101, 206, 1129, "主线")
            while 1:
                # 识别黄色领取按钮
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 1)
                    tapSleep(320, 1180)  # 点击空白处关闭
                else:
                    break

        # 日常领取
        if CompareColors.compare("355,1104,#EF5C3F|355,1100,#F45F42|352,1103,#EF5C3F"):
            res = TomatoOcrTap(274, 1102, 326, 1130, "每日")
            if res:
                # 识别黄色领取按钮
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 1)
                    tapSleep(357, 1224)  # 点击空白处关闭
                    # 点击宝箱（从右到左）
                    tapSleep(570, 390)
                    tapSleep(490, 390)
                    tapSleep(410, 390)
                    tapSleep(330, 390)
                    tapSleep(250, 390)

        # 每周领取
        res = TomatoOcrTap(394, 1099, 448, 1132, "每周")
        if res:
            # 识别黄色领取按钮
            re, x, y = imageFind('手册-领取')
            if re:
                tapSleep(x, y, 1)
                tapSleep(357, 1224)  # 点击空白处关闭
                # 点击宝箱（从右到左）
                tapSleep(570, 390)
                tapSleep(490, 390)
                tapSleep(410, 390)
                tapSleep(330, 390)
                tapSleep(250, 390)

        # 成就领取
        if CompareColors.compare("593,1104,#EF5C40|593,1101,#F35F42|596,1101,#F35E41"):
            res = TomatoOcrTap(514, 1099, 570, 1132, "成就")
            while 1:
                # 识别黄色领取按钮
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 2)
                    tapSleep(360, 1070)  # 点击空白处关闭
                    tapSleep(360, 1070)  # 点击空白处关闭（再次点击，避免成就升级页）
                else:
                    break

    # 前往新地图
    def newMap(self):
        if 功能开关["自动挑战首领"] == 1:
            Toast("日常 - 挑战首领 - 开始")
            self.homePage()
            sleep(1)
            res1 = TomatoOcrTap(633, 766, 694, 788, "挑战首领")
            res2 = False
            if not res1:
                res2, x, y = imageFind('挑战首领')
                if res2:
                    tapSleep(x + 25, y + 25, 1)
            if res1 or res2:
                # 功能开关["fighting"] = 1
                sleep(10)  # 等待动画
                for i in range(1, 5):
                    res2, x, y = imageFind('首页-冒险')
                    # res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                    if res2:
                        break
                    else:
                        sleep(5)  # 等待动画
                # 功能开关["fighting"] = 0
                for i in range(15):
                    res1, _ = TomatoOcrText(636, 781, 691, 802, "等待中")
                    if res1:
                        Toast('等待挑战首领')
                        sleep(3)
                    res2, _ = TomatoOcrText(636, 781, 691, 802, "挑战中")
                    if res2:
                        Toast('挑战首领中')
                        sleep(3)
                    if not res1 and not res2:
                        # 检查是否挑战成功
                        res1, _ = TomatoOcrText(429, 542, 492, 606, "败")
                        if res1:
                            Toast('主线挑战首领 - 失败')
                        Toast('主线挑战首领 - 完成')
                        break

        if 功能开关["自动换图"] == 1:
            Toast("日常 - 前往新地图 - 开始")
            self.homePage()
            # 直接点击图标切换
            newMapOK, x, y = imageFind('首页-前往新关卡', confidence1=0.7, x1=565, y1=643, x2=705, y2=822)
            if newMapOK:
                tapSleep(x, y, 5)
            res = TomatoOcrTap(593,676,638,693, "前往")
            if not newMapOK:
                res1, _ = TomatoOcrText(573, 200, 694, 238, "新关卡已解锁")
                res2 = False
                if not res1:
                    res2, _ = TomatoOcrText(573, 200, 694, 238, "新地图已解锁")
                if res1 or res2:
                    # if 1:
                    # 结伴入口切换
                    res = TomatoOcrTap(647, 450, 689, 474, "结伴", 10, -10)
                    res = TomatoOcrTap(373, 1106, 471, 1141, "关卡大厅")
                    for i in range(1, 5):
                        x = 0
                        re, x, y = imageFind('当前地图')
                        if x == 0:
                            re, x, y = imageFind('当前地图2')
                        if x > 0:
                            # 当前地图（不在下方第1个，就是右边紧挨着；只需判断两次）
                            if x > 400:
                                tapSleep(x - 305, y + 147)  # 下行第1个
                            else:
                                tapSleep(x + 230, y + 0)  # 右侧第1个
                                TomatoOcrText(321, 1022, 394, 1044, "前往地图")

                            # 切换地图
                            res, _ = TomatoOcrText(321, 1022, 394, 1044, "前往地图")
                            if not res:
                                tapSleep(x + 0, y + 165)  # 切换下一地图
                                if x < 280:
                                    tapSleep(x + 50, y + 250)  # 最后一关在第一个位置，换地图后下方第1图）
                                if 280 < x < 400:
                                    tapSleep(x - 100, y + 250)  # 下行第1个（最后一关在第二个位置，换地图后下方第1图）
                                if x > 400:
                                    tapSleep(x - 250, y + 220)  # 最后一关在第三个位置，换地图后下行第1个

                            res = TomatoOcrTap(321, 1022, 394, 1044, "前往地图")
                            res = TomatoOcrTap(330, 1027, 389, 1058, "前往")

                            res = TomatoOcrTap(422, 622, 494, 646, "单人前往")
                            if res:
                                if 功能开关["队员不满足单飞"] == 1:
                                    res = TomatoOcrTap(187, 727, 284, 757, "离队前往")
                                else:
                                    res = TomatoOcrTap(435, 727, 529, 759, "留在队伍")
                                break
                        else:
                            swipe(500, 800, 500, 300)
                            sleep(4)

        if 功能开关["单飞后寻找结伴"] == 1:
            if 任务记录["寻找结伴-完成"] == 0:
                Toast("日常 - 寻找结伴 - 开始")
                self.homePage()
                res = TomatoOcrTap(646, 451, 689, 474, "结伴", 10, -10)
                if res:
                    isTeam = TomatoOcrFindRange('旅伴', 0.9, 143, 257, 568, 355)
                    if not isTeam:
                        Toast("日常 - 寻找结伴 - 已有结伴")
                        任务记录["寻找结伴-完成"] = 1
                        sleep(1)
                        TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
                    else:
                        res = TomatoOcrTap(407, 1036, 513, 1070, "寻找队伍", 25, 25)
                        re, x, y = imageFind('结伴-加入')
                        if re:
                            tapSleep(x, y, 1)
                            Toast("日常 - 寻找结伴 - 加入队伍")
                            sleep(4)  # 等待动画
                            res = TomatoOcrTap(359, 741, 391, 775, "确认跟随", 10, 10)
                            任务记录["寻找结伴-完成"] = 1

    # 箱庭苗圃
    def XiangTingMiaoPu(self):
        if 功能开关["箱庭苗圃"] == 0:
            return
        # if 任务记录["箱庭苗圃-完成"] == 1:
        #     return
        if 任务记录["箱庭苗圃-倒计时"] > 0:
            diffTime = time.time() - 任务记录["箱庭苗圃-倒计时"]
            if diffTime < 20 * 60:
                Toast(f'日常 - 箱庭苗圃 - 倒计时{20 - round(diffTime / 60, 2)}min')
                return
        Toast('日常 - 箱庭苗圃 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        # res = TomatoOcrFindRangeClick('箱庭苗圃', 0.9, 14, 98,1025,180,1051, offsetX=30, offsetY=-20)
        res = TomatoOcrTap(98, 1025, 180, 1051, '箱庭苗圃', offsetX=30, offsetY=-20)
        if not res:
            return

        sleep(3)  # 等待动画

        re1 = imageFindClick('花园苗圃-苗圃币', confidence1=0.7)
        re2 = False
        if not re1:
            re2 = imageFindClick('花园苗圃-苗圃币2', confidence1=0.7)
        if re1 or re2:
            tapSleep(473, 1076)  # 点击空白处
            tapSleep(473, 1076)  # 点击空白处
            tapSleep(473, 1076, 0.3)  # 点击空白处

        for i in range(1, 5):
            res = TomatoOcrTap(595, 1025, 642, 1052, '浇水')
            sleep(2)

            res1 = TomatoOcrFindRangeClick('可收获', 0.9, 0.9, 114, 482, 575, 1010, offsetY=-40)
            if res1:
                res = TomatoOcrFindRangeClick('全部收获', 0.9, 0.9, 85, 980, 643, 1123, 1010, offsetX=20, offsetY=-20)
                tapSleep(473, 1076)  # 点击空白处
                tapSleep(473, 1076)  # 点击空白处
                tapSleep(473, 1076, 0.3)  # 点击空白处

            res1 = TomatoOcrFindRangeClick('可种植', 0.9, 0.9, 114, 482, 575, 1010, offsetY=-20)
            sleep(1)
            if res1:
                line1 = Path(0, 3000)
                # 移动初始点
                line1.moveTo(129, 1046)
                # 使用二次贝塞尔曲线 从点(500,800) 到 (250,900)
                line1.quadTo(129, 1046, 203, 891)
                line1.quadTo(203, 891, 236, 565)
                line1.quadTo(236, 565, 560, 557)
                line1.quadTo(560, 557, 214, 560)
                action.gesture([line1])
                sleep(4)

            res2 = TomatoOcrFindRangeClick('可种植', 0.9, 14, 114, 482, 575, 1010, offsetY=-20)
            sleep(1)
            if res2:
                line2 = Path(0, 5000)
                # 移动初始点
                line2.moveTo(219, 1040)
                # 拖动种子拖动到对应位置
                line2.quadTo(219, 1040, 353, 890)
                line2.quadTo(353, 890, 322, 691)
                line2.quadTo(322, 691, 508, 700)
                line2.quadTo(508, 700, 336, 703)
                line2.quadTo(336, 703, 521, 703)
                line2.quadTo(521, 703, 532, 885)
                line2.quadTo(532, 885, 356, 883)
                action.gesture([line2])
                sleep(6)

            if res1 or res2:
                TomatoOcrTap(595, 1025, 642, 1052, '浇水')
                sleep(2)

            tapSleep(660, 689, 3)  # 翻下一页

        # 拜访
        for i in range(1, 5):
            tapSleep(617, 1139, 2)  # 点击拜访
            res = TomatoOcrTap(246, 348, 287, 374, '旅团')
            if res:
                tapSleep(527, 455 + 120 * i, 2)  # 点击拜访
                available, _ = TomatoOcrText(643, 1062, 672, 1080, '0/2')
                if available:
                    Toast('箱庭苗圃-旅团浇水完成')
                    break
                tapSleep(615, 1010, 2)  # 点击浇水
                tapSleep(339, 1223)  # 点击空白

        任务记录["箱庭苗圃-倒计时"] = time.time()
        任务记录["箱庭苗圃-完成"] = 1

    # 限时特惠
    def XianShiTeHui(self):
        if 功能开关["限时特惠"] == 0:
            return
        if 任务记录["限时特惠-完成"] == 1:
            return
        Toast('日常 - 限时特惠 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrFindRangeClick('限时特惠', 0.9, 14, 11, 778, 197, 1057, offsetX=30, offsetY=-20)
        if not res:
            return

        tapSleep(595, 150)  # 点击特惠宝箱
        tapSleep(350, 1125)  # 点击空白处
        任务记录["限时特惠-完成"] = 1

    # 登录好礼
    def dengLuHaoLi(self):
        if 功能开关["登录好礼"] == 0:
            return
        if 任务记录["登录好礼-完成"] == 1:
            return
        Toast('日常 - 登录好礼 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return
        任务记录["登录好礼-完成"] = 1

        # todo：识图登录好礼
        # re = ldE.element_exist('活动-登录好礼')
        # if not re:
        #     return

        # re.click().execute(sleep=1)
        # todo：识图领取按钮
        # re = ldE.element_exist('活动-登录好礼-领取')
        # if re:
        #     re.click().execute(sleep=1)
        #     tapSleep(355, 1005)  # 点击空白处关闭
        #     tapSleep(350, 1145)  # 点击空白处关闭

    # 宝藏湖
    def baoZangHu(self):
        if 功能开关["宝藏湖"] == 0:
            return

        if 任务记录["日常-宝藏湖-完成"] == 1:
            return

        Toast('日常 - 宝藏湖 - 开始')
        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return
        res = TomatoOcrFindRangeClick('宝藏湖', 0.9, 14, 11, 778, 197, 1057, offsetX=30, offsetY=-20)
        if not res:
            return

        res = TomatoOcrTap(395, 1076, 496, 1100, "大容量充磁")
        sleep(8)  # 等待动画
        tapSleep(360, 1040)  # 点击空白处
        tapSleep(360, 1040)  # 点击空白处

        tapSleep(75, 325)  # 领取回收物进度奖励
        tapSleep(76, 335)  # 领取回收物进度奖励
        tapSleep(360, 1040)  # 点击空白处

        res = TomatoOcrTap(554, 1239, 636, 1265, "伊尼兰特")
        if res:
            res = TomatoOcrTap(321, 1073, 402, 1096, "高压充磁", 10, 10)
            sleep(8)  # 等待动画
            tapSleep(360, 1040)  # 点击空白处
            tapSleep(360, 1040)  # 点击空白处

        任务记录["日常-宝藏湖-完成"] = 1

    # BBQ派对
    def BBQParty(self):
        if 功能开关["BBQ派对"] == 0:
            return

        Toast('日常 - BBQ派对 - 开始')
        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrFindRangeClick('BBQ派对', 0.9, 14, 11, 778, 197, 1057, offsetX=30, offsetY=-20)
        if not res:
            return

        while True:
            res, availableCount = TomatoOcrText(615, 81, 653, 102, "烤刷数量")  # 1/9
            availableCount = safe_int(availableCount)
            if availableCount == "" or availableCount == 0:
                res = TomatoOcrTap(96, 1200, 129, 1232, "回", 10, 10)  # 返回
                break

            res = TomatoOcrTap(433, 1091, 533, 1122, "连续烧烤")
            sleep(5)
            tapSleep(360, 1220)  # 点击空白处

    # 火力全开
    def huoLiQuanKai(self):
        if 功能开关["火力全开"] == 0:
            return

        Toast('日常 - 火力全开 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrTap(98, 1022, 177, 1048, "火力全开", 20, 20)  # 进入火力全开
        if not res:
            res = TomatoOcrTap(96, 938, 178, 960, "火力全开", 20, 20)  # 进入火力全开
            if not res:
                return
        # todo：找图领取按钮
        tapSleep(480, 1100)  # 点击空白处

    # 活动 - 摸鱼
    def huoDongMoYu(self):
        if 功能开关["摸鱼时间到"] == 0:
            return

        Toast('日常 - 摸鱼时间到 - 开始')
        needCount = safe_int(功能开关["摸鱼重复次数"])
        if needCount == '':
            needCount = 5
        for i in range(needCount):
            # res = TomatoOcrTap(566, 379, 609, 404, "摸鱼")
            res1 = TomatoOcrTap(566, 379, 609, 404, "摸鱼", 15, -20)
            res2 = TomatoOcrTap(551, 462, 622, 488, "摸鱼", 15, -20)
            res3 = TomatoOcrTap(553, 546, 620, 570, "摸鱼", 15, -20)
            res4 = TomatoOcrTap(325, 1095, 427, 1128, "开始匹配")
            if not res1 and not res2 and not res3 and not res4:
                self.homePage()
                res1 = TomatoOcrTap(566, 379, 609, 404, "摸鱼", 15, -20)
                res2 = TomatoOcrTap(551, 462, 622, 488, "摸鱼", 15, -20)
                res3 = TomatoOcrTap(553, 546, 620, 570, "摸鱼", 15, -20)
                if not res1 and not res2 and not res3:
                    return

            res1 = TomatoOcrTap(325, 1095, 427, 1128, "开始匹配")
            res2 = TomatoOcrTap(451, 603, 505, 635, "准备")
            if not res1 and not res2:
                self.quitTeam()

            attempts = 0  # 初始化尝试次数
            maxAttempts = 4  # 设置最大尝试次数

            resStart = False
            failCount = 0
            while attempts < maxAttempts:
                resStart = TomatoOcrTap(451, 603, 505, 635, "准备")
                startStatus = TomatoOcrTap(325, 1095, 427, 1128, "开始匹配")
                waitStatus, _ = TomatoOcrText(334, 1082, 418, 1115, "匹配中")
                if resStart:
                    Toast("匹配成功 - 已准备")
                    for j in range(1, 10):
                        res1, text1 = TomatoOcrText(19, 1104, 94, 1128, "点击输入")
                        res2 = False
                        res3 = False
                        res4 = False
                        if not res1:
                            res2, text2 = TomatoOcrText(543, 104, 622, 142, "倒计时")
                            if not res2:
                                res3, text3 = TomatoOcrText(598, 84, 636, 104, "回合")
                                if not res3:
                                    res4, x, y = imageFind('摸鱼中')
                        if res1 or res2 or res3 or res4:
                            break
                        sleep(2)  # 等待进入
                    break
                elif waitStatus == 0 and startStatus == 0:
                    res1, text1 = TomatoOcrText(19, 1104, 94, 1128, "点击输入")
                    res2 = False
                    res3 = False
                    res4 = False
                    if not res1:
                        res2, text2 = TomatoOcrText(543, 104, 622, 142, "倒计时")
                        if not res2:
                            res3, text3 = TomatoOcrText(598, 84, 636, 104, "回合")
                            if not res3:
                                res4, x, y = imageFind('摸鱼中')
                    if res1 or res2 or res3 or res4:
                        resStart = True
                        break

                    failCount = failCount + 1
                    if failCount > 4:
                        Toast("匹配失败，重新开始")
                        break
                else:
                    Toast("匹配中")
                    attempts = attempts + 1
                    sleep(3)

            if resStart:
                doneCt = 0
                hasShout1 = 0
                for j in range(1, 30):
                    res3 = False
                    res4 = False
                    res2, text2 = TomatoOcrText(543, 104, 622, 142, "倒计时")
                    if not res2:
                        res3, text3 = TomatoOcrText(598, 84, 636, 104, "回合")
                        if not res3:
                            res4, x, y = imageFind('摸鱼中')
                    if res2 or res3 or res4:
                        Toast("摸鱼中 - 顺时针点击")
                        if (res2 or res3) and hasShout1 == 0:
                            hasShout1 = self.moyuTeamShout(功能开关["摸鱼队伍喊话"])
                        tapSleep(203, 744, 0.2)  # 顺时针点击
                        tapSleep(236, 765, 0.2)  # 顺时针点击
                        tapSleep(236, 765, 0.2)  # 顺时针点击
                        tapSleep(588, 1100, 0.2)  # 选中离手
                        tapSleep(588, 1100, 0.2)  # 选中离手
                        Toast("摸鱼中 - 等待队友点击")
                    else:
                        res = TomatoOcrTap(313, 1105, 411, 1136, "领取奖励")
                        if res:
                            Toast('摸鱼结束 - 领取奖励')
                            tapSleep(535, 1218, 0.5)  # 点击空白处关闭
                            tapSleep(535, 1218, 0.5)  # 点击空白处关闭
                            break
                        res, _ = TomatoOcrText(325, 1095, 427, 1128, "开始匹配")
                        if res:
                            Toast('摸鱼结束 - 已返回摸鱼活动页')
                            break
                        res = FindColors.find(
                            "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
                            rect=[301, 1130, 421, 1273])
                        if res:
                            Toast('摸鱼结束 - 已返回首页')
                            break
                        doneCt = doneCt + 1
                        if doneCt > 5:  # 连续两次未识别到时退出
                            break

                    sleep(2)  # 等待3s

    #  骑兽乐园
    def qiShouLeYuan(self):
        if 功能开关["骑兽乐园"] == 0:
            return

        if 任务记录["日常-骑兽乐园-完成"] == 1:
            return

        Toast('日常 - 骑兽乐园 - 开始')

        # 判断是否在营地页面
        # 判断是否在营地页面
        isYingDi = False
        for i in range(1, 3):
            res1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")
            if not res1 and not res2:
                # 返回首页
                self.homePage()
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
                # 判断是否在营地页面
                hd1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
                hd2, _ = TomatoOcrText(11, 1111, 92, 1134, "旅行活动")
                if hd1 or hd2:
                    isYingDi = True
                    tapSleep(200, 545, 3)  # 芙芙小铺
                    res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")
                    break
            else:
                isYingDi = True
                break
        if not isYingDi:
            return

        res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")
        if res2:
            point = FindColors.find("184,318,#9D9D9D|189,312,#939393|183,334,#ABABAB|189,323,#E1E1E1|194,320,#E8E8E8",
                                    rect=[115, 244, 262, 432], diff=0.9)  # 已领取门票，灰色状态
            if point:
                Toast('骑兽乐园 - 已领取门票')
            else:
                Toast('骑兽乐园 - 领取门票')
                tapSleep(188, 321, 2)  # 点击门票（固定位置）
                tapSleep(540, 655, 1.7)  # 点击空白处关闭
                tapSleep(540, 655, 1.7)  # 点击空白处关闭

            # 兑换门票
            needCount = safe_int(功能开关["钻石兑换门票次数"])
            if needCount == '':
                needCount = 0
            if needCount > 0:
                for i in range(1, 5):
                    TomatoOcrTap(570, 261, 645, 285, "兑换门票", 10, 10)
                    res, _ = TomatoOcrText(320, 372, 401, 399, "兑换门票")
                    if not res:
                        TomatoOcrTap(570, 261, 645, 285, "兑换门票", 10, 10)

                    buyCount = ""
                    for j in range(1, 5):
                        # res, buyCount = TomatoOcrText(379, 930, 394, 947, "每日限购次数")  # 1/9
                        res, buyCount = TomatoOcrText(274, 923, 438, 956, "每日限购次数")  # 1/9
                        buyCount = buyCount.replace("每日限购（", "")
                        buyCount = buyCount.replace("/9）", "")
                        buyCount = safe_int(buyCount)
                        if buyCount != "":
                            break
                    if buyCount != 0 and (buyCount == "" or buyCount >= needCount):
                        if buyCount != "" and buyCount >= needCount:
                            任务记录["日常-骑兽乐园-完成"] = 1
                        TomatoOcrTap(70, 1202, 122, 1232, "返回", 10, 10)  # 返回芙
                        break
                    TomatoOcrTap(318, 863, 401, 883, "购买道具", 10, 10)
                    tapSleep(550, 1080)  # 点击空白处关闭
            else:
                任务记录["日常-骑兽乐园-完成"] = 1

        # 骑兽探索
        needCount = safe_int(功能开关["骑兽探索次数"])
        if needCount == '':
            needCount = 0
        if needCount > 0:
            attempt = 0
            while attempt < needCount:
                TomatoOcrTap(204, 917, 245, 940, "探索")
                sleep(2)
                TomatoOcrTap(597, 28, 642, 53, "跳过")  # 跳过动画
                sleep(2)
                TomatoOcrTap(597, 28, 642, 53, "跳过")  # 跳过动画
                tapSleep(90, 980, 3)  # 点击空白处
                tapSleep(90, 980)  # 点击空白处
                attempt = attempt + 1

    # 招式创造
    def zhaoShiChuangZao(self):
        if 功能开关["招式创造"] == 0:
            return

        if 任务记录["日常-招式创造-完成"] == 1:
            return

        Toast('日常 - 招式创造 - 开始')

        # 判断是否在营地页面
        isYingDi = False
        for i in range(1, 3):
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if not res:
                # 返回首页
                self.homePage()
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
                # 判断是否在营地页面
                hd1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
                hd2, _ = TomatoOcrText(11, 1111, 92, 1134, "旅行活动")
                if hd1 or hd2:
                    isYingDi = True
                    break
            else:
                isYingDi = True
                break
        if not isYingDi:
            return

        tapSleep(200, 545, 2.5)  # 芙芙小铺
        res = TomatoOcrTap(389, 1133, 489, 1163, "招式创造")
        if res:
            re, x, y = imageFind('招式创造能量', 0.8)
            if re:
                tapSleep(x, y, 3)
                tapSleep(185, 1024)  # 点击空白处关闭
                任务记录["日常-招式创造-完成"] = 1
            else:
                re, x, y = imageFind('招式创造能量2', 0.8)
                if re:
                    tapSleep(x, y, 3)
                    tapSleep(185, 1024)  # 点击空白处关闭
                    任务记录["日常-招式创造-完成"] = 1

        # 兑换卢恩
        needCount = safe_int(功能开关["钻石兑换卢恩次数"])
        if needCount == '':
            needCount = 0
        if needCount > 0:
            for i in range(1, 5):
                res = TomatoOcrTap(571, 261, 645, 287, "兑换卢恩", 10, 10)
                buyCount = ""
                for j in range(1, 5):
                    # res, buyCount = TomatoOcrText(375, 944, 387, 960, "已购买次数")  # 1/9
                    res, buyCount = TomatoOcrText(284, 935, 425, 968, "已购买次数")  # 1/9
                    buyCount = buyCount.replace("每日限购（", "")
                    buyCount = buyCount.replace("/15）", "")
                    buyCount = safe_int(buyCount)
                    if buyCount != "":
                        break
                if buyCount != 0 and (buyCount == "" or buyCount >= needCount):
                    res = TomatoOcrTap(70, 1202, 122, 1232, "返回", 10, 10)  # 返回芙芙小铺，继续
                    break
                res = TomatoOcrTap(318, 876, 398, 898, "购买道具", 10, 10)
                if res:
                    tapSleep(185, 1024)  # 点击空白处关闭
                    任务记录["日常-招式创造-完成"] = 1
        # 讲述故事
        needCount = safe_int(功能开关["讲述故事次数"])
        if needCount == '':
            needCount = 0
        if needCount > 0:
            attempt = 0
            # 关闭批量讲述
            res = CompareColors.compare(
                "513,1090,#B8D3B1|517,1092,#BAD3B2|521,1085,#59B249|522,1084,#5BB34B")  # 勾选的绿色对勾
            if res:
                tapSleep(515, 1088)
            while attempt < needCount:
                res = TomatoOcrTap(319, 1062, 398, 1083, "讲述故事")
                sleep(2)
                res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                tapSleep(170, 1090)  # 点击空白处
                attempt = attempt + 1
        任务记录["日常-招式创造-完成"] = 1

    # 邮件领取
    def youJian(self):
        if 功能开关["邮件领取"] == 0:
            return

        if 任务记录["邮件领取-完成"] == 1:
            return

        Toast('日常 - 邮件领取 - 开始')

        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            # 返回首页
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            hd2, _ = TomatoOcrText(11, 1111, 92, 1134, "旅行活动")
            if not hd1 and not hd2:
                return

        # 判断邮件已完成
        re, x, y = imageFind('营地-邮箱-已领取', x1=194, y1=680, x2=383, y2=852)
        if re:
            Toast('营地任务 - 邮件领取 - 识别已完成')
            任务记录["邮件领取-完成"] = 1
            sleep(1)
            return

        tapSleep(300, 740, 4)  # 邮件
        res = TomatoOcrTap(463, 1030, 510, 1061, "领取")
        if not res:
            TomatoOcrTap(67, 1182, 121, 1221, "返回", 10, 10)
            return
        else:
            任务记录["邮件领取-完成"] = 1
        sleep(2)
        tapSleep(120, 1030)  # 点击空白处
        tapSleep(110, 1204)  # 点击返回

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
            teamStatus = TomatoOcrTap(632, 570, 684, 598, "匹配中")
            if teamStatus:
                Toast('取消匹配')

            teamExist = TomatoOcrFindRangeClick('离开队伍', whiteList='离开队伍', x1=416, y1=126, x2=628, y2=284)
            if teamExist:
                teamExist = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=105, y1=304, x2=631, y2=953)
                if teamExist:
                    Toast('退出组队')
                    return True

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

    def moyuTeamShout(self, shoutText):
        if shoutText == "":
            return 1

        res1 = TomatoOcrTap(19, 1101, 94, 1135, "点击输入", 10, 10)
        if not res1:
            res1 = TomatoOcrTap(16, 1100, 96, 1135, "点击输入", 10, 10)
        # res1, text1 = TomatoOcrText(19, 1104, 94, 1128, "点击输入")
        res2 = False
        res3 = False
        if not res1:
            res2, text2 = TomatoOcrText(543, 104, 622, 142, "倒计时")
            if not res2:
                res3, text3 = TomatoOcrText(598, 84, 636, 104, "回合")
        if not res1 and not res2 and not res3:
            return 0

        Toast("队伍发言")

        # res1 = TomatoOcrTap(19, 1101, 94, 1135, "点击输入", 10, 10)
        # if not res1:
        #     res2 = TomatoOcrTap(16, 1100, 96, 1135, "点击输入", 10, 10)
        # sleep(1.5)  # 等待输入法弹窗
        if res1:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            sleep(1.5)
            action.input(shoutText)
            action.input(shoutText)
            tapSleep(360, 104)  # 点击空白处确认输入
            res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
            if res:
                tapSleep(104, 342, 0.8)  # 确认关闭聊天框
                tapSleep(236, 765, 0.4)  # 顺时针点击
                tapSleep(588, 1100, 0.4)  # 选中离手
                return 1

        tapSleep(104, 342, 0.8)  # 确认关闭聊天框
        return 0
