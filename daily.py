# 导包
from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .shilian import ShiLianTask
from .res.ui.ui import 任务记录
from .baseUtils import *
from ascript.android import action
from .res.ui.ui import switch_lock
from .thread import *


class DailyTask:
    def __init__(self):
        self.shilianTask = ShiLianTask()

    def homePage(self):
        while True:
            # todo 区分是否进入的摸鱼活动
            res6 = self.shilianTask.WaitFight()

            # 避免首页识别到冒险手册，但存在未关闭的返回弹窗；兜底识别1次
            return3 = TomatoOcrTap(91,1185,127,1221, '回', 10, 10)
            if return3:
                Toast('返回首页')

            # 判断是否已在首页
            res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1 = ocrFindRange('冒险手册',  0.9, 360, 0, 720, 1280)
                if not shou_ye1:
                    shou_ye2 = ocrFindRange('试炼',  0.9, 360, 0, 720, 1280)
            if res2 or shou_ye1 or shou_ye2:
                with switch_lock:
                    功能开关["needHome"] = 0
                功能开关["fighting"] = 0
                Toast('已返回首页')
                sleep(0.5)
                return True

            # 开始异步处理返回首页
            with switch_lock:
                if not thread2.is_alive():
                    runThread2()
                功能开关["needHome"] = 1

            # 点击首页-冒险
            re = TomatoOcrTap(330,1201,389,1238, '冒险')
            # ldE.element('首页-冒险').click().execute(sleep=1)

            quitTeamRe = self.quitTeam()
            if not quitTeamRe:
                # 判断战败页面
                self.shilianTask.fight_fail()

            # 判断宝箱开启
            self.shilianTask.openTreasure()
            sleep(0.5)

    # 日常任务聚合
    def dailyTask(self):
        if 功能开关["日常总开关"] == 0:
            return

        # 日常相关

        # 活动

        # 领取相关
        # 邮件领取
        self.youJian()
        # 招式创造
        self.zhaoShiChuangZao()
        # 骑兽乐园
        self.qiShouLeYuan()
        # 世界喊话
        self.shijieShout()


    def shijieShout(self):
        if 功能开关['世界喊话'] == "":
            return 1

        Toast("世界喊话")

        self.homePage()

        # 识别是否进入首页
        shou_ye1 = ocrFindRange('冒险手册',  0.9, 360, 0, 720, 1280)
        shou_ye2 = False
        if not shou_ye1:
            shou_ye2 = ocrFindRange('试炼',  0.9, 360, 0, 720, 1280)
        if shou_ye1 or shou_ye2:
            with switch_lock:
                功能开关["needHome"] = 0
            Toast('已返回首页')
        else:
            Toast('返回首页失败')
            return

        res1 = TomatoOcrTap(18,1098,97,1134, "点击输入", 10, 10)
        res2 = False
        if not res1:
            res2 = TomatoOcrTap(17,1103,96,1134, "点击输入", 10, 10)
        sleep(2.5)  # 等待输入法弹窗
        if res1 or res2:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            sleep(1)
            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
            action.input(功能开关["世界喊话"])
            tapSleep(360, 104)  # 点击空白处确认输入
            res = TomatoOcrTap(555, 1156, 603, 1188, "发送")
            if res:
                tapSleep(101,337)
                return 1

        tapSleep(101,337)
        return 0

    def dailyTaskEnd(self):
        if 功能开关["日常总开关"] == 0:
            return

        # 日常相关

        # 活动
        # 摸鱼时间到
        self.huoDongMoYu()
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

        # 前往新地图
        self.newMap()

        # 冒险手册
        self.maoXianShouCe()

    # 冒险手册
    def maoXianShouCe(self):
        if 功能开关["冒险手册领取"] == 0:
            return
        Toast("日常 - 冒险手册领取 - 开始")
        self.homePage()
        res = TomatoOcrTap(626, 379, 711, 405, "冒险手册", 30, -20)
        if not res:
            Toast("识别冒险手册失败")
            return

        # 主线领取
        res = TomatoOcrTap(156, 1101, 206, 1129, "主线")
        while 1:
            # 识别黄色领取按钮
            re, x, y = imageFind('手册-领取')
            if re:
                tapSleep(x,y,1)
                tapSleep(320, 1180)  # 点击空白处关闭
            else:
                break

        # 日常领取
        res = TomatoOcrTap(274, 1102, 326, 1130, "每日")
        if res:
            # 识别黄色领取按钮
            re, x, y = imageFind('手册-领取')
            if re:
                tapSleep(x,y,1)
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
                tapSleep(x,y,1)
                tapSleep(357, 1224)  # 点击空白处关闭
                # 点击宝箱（从右到左）
                tapSleep(570, 390)
                tapSleep(490, 390)
                tapSleep(410, 390)
                tapSleep(330, 390)
                tapSleep(250, 390)

        # 成就领取
        res = TomatoOcrTap(514, 1099, 570, 1132, "成就")
        while 1:
            # 识别黄色领取按钮
            re, x, y = imageFind('手册-领取')
            if re:
                tapSleep(x,y,3)
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
                    tapSleep(x+25,y+25,1)
            if res1 or res2:
                sleep(10)  # 等待动画

        if 功能开关["自动换图"] == 1:
            Toast("日常 - 前往新地图 - 开始")
            self.homePage()
            # 直接点击图标切换
            newMapOK, x, y = imageFind('首页-前往新关卡')
            if newMapOK:
                tapSleep(x, y, 1)
                res = TomatoOcrTap(422, 622, 494, 646, "单人前往")
                if res:
                    if 功能开关["队员不满足单飞"] == 1:
                        res = TomatoOcrTap(187, 727, 284, 757, "离队前往")
                    else:
                        res = TomatoOcrTap(435, 727, 529, 759, "留在队伍")
            if not newMapOK:
                res1, _ = TomatoOcrText(573, 200, 694, 238, "新关卡已解锁")
                res2 = False
                if not res1:
                    res2, _ = TomatoOcrText(573, 200, 694, 238, "新地图已解锁")
                if res1 or res2:
                    # 结伴入口切换
                    res = TomatoOcrTap(647, 450, 689, 474, "结伴")
                    res = TomatoOcrTap(373, 1106, 471, 1141, "关卡大厅")
                    for i in range(1, 5):
                        re, x, y = imageFind('当前地图')
                        x = 0
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
            Toast("日常 - 寻找结伴 - 开始")
            self.homePage()
            res = TomatoOcrTap(646, 451, 689, 474, "结伴", 10, -10)
            if res:
                isTeam, x, y = imageFind('组队增益')
                if isTeam:
                    Toast("日常 - 寻找结伴 - 已有结伴")
                else:
                    res = TomatoOcrTap(408, 1037, 509, 1068, "寻找队伍")
                    re, x, y = imageFind('结伴-加入')
                    if re:
                        tapSleep(x,y,1)
                        Toast("日常 - 寻找结伴 - 加入队伍")
                        sleep(4)  # 等待动画
                        res = TomatoOcrTap(359, 741, 391, 775, "确认跟随")

    # 限时特惠
    def XianShiTeHui(self):
        if 功能开关["限时特惠"] == 0:
            return
        Toast('日常 - 限时特惠 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrTap(96, 1024, 176, 1046, "限时特惠")
        if not res:
            res = TomatoOcrTap(96, 938, 178, 960, "限时特惠")
            if not res:
                return

        tapSleep(595, 150)  # 点击特惠宝箱
        tapSleep(350, 1125)  # 点击空白处

    # 登录好礼
    def dengLuHaoLi(self):
        if 功能开关["登录好礼"] == 0:
            return
        Toast('日常 - 登录好礼 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

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

        Toast('日常 - 宝藏湖 - 开始')
        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return
        res = TomatoOcrTap(20, 937, 84, 960, "宝藏湖")
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

        res = TomatoOcrTap(96, 1024, 176, 1046, "BBQ派对")  # 进入BBQ派对
        if not res:
            res = TomatoOcrTap(96, 938, 178, 960, "BBQ派对")  # 进入BBQ派对
            if not res:
                return

        while True:
            res, availableCount = TomatoOcrText(615, 81, 653, 102, "烤刷数量")  # 1/9
            availableCount = safe_int(availableCount)
            if availableCount == "" or availableCount == 0:
                res, _ = TomatoOcrText(96, 1200, 129, 1232, "回", 10, 10)  # 返回
                break

            res = TomatoOcrTap(433, 1093, 533, 11236, "连续烧烤")
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

        res = TomatoOcrTap(98, 1022, 177, 1048, "火力全开")  # 进入火力全开
        if not res:
            res = TomatoOcrTap(96, 938, 178, 960, "火力全开")  # 进入火力全开
            if not res:
                return
        # todo：找图领取按钮
        tapSleep(480, 1100)  # 点击空白处

    # 活动 - 摸鱼
    def huoDongMoYu(self):
        if 功能开关["摸鱼时间到"] == 0:
            return

        Toast('日常 - 摸鱼时间到 - 开始')

        for i in range(1, 3):
            self.homePage()

            # res = TomatoOcrTap(566, 379, 609, 404, "摸鱼")
            res1 = TomatoOcrTap(566, 379, 609, 404, "摸鱼", 15, -20)
            res2 = TomatoOcrTap(551, 462, 622, 488, "摸鱼", 15, -20)
            res3 = TomatoOcrTap(553, 546, 620, 570, "摸鱼", 15, -20)
            if not res1 and not res2 and not res3:
                return

            res = TomatoOcrTap(325, 1095, 427, 1128, "开始匹配")
            res = TomatoOcrTap(451, 603, 505, 635, "准备")
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
                        Toast("摸鱼中")
                        tapSleep(203, 744, 0.4)  # 顺时针点击
                        tapSleep(236, 765, 0.4)  # 顺时针点击
                        tapSleep(236, 765, 0.4)  # 顺时针点击
                        if (res2 or res3) and hasShout1 == 0:
                            hasShout1 = self.moyuTeamShout("顺时针 左下角")
                        tapSleep(588, 1100, 0.4)  # 选中离手
                        tapSleep(588, 1100, 0.4)  # 选中离手
                    else:
                        res = TomatoOcrTap(313, 1105, 411, 1136, "领取奖励")
                        if res:
                            tapSleep(140, 1000, 1)  # 点击空白处关闭
                            sleep(1)
                            break
                        doneCt = doneCt + 1
                        if doneCt > 4:  # 连续两次未识别到时退出
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
        res1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")
        if not res1 and not res2:
            # 返回首页
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
            # 判断是否在营地页面
            hd1, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            hd2, _ = TomatoOcrText(11, 1111, 92, 1134, "旅行活动")
            if not hd1 and not hd2:
                return
            tapSleep(200, 545, 3)  # 芙芙小铺
            res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")

        if res2:
            tapSleep(188, 321, 2)  # 点击门票（固定位置）
            tapSleep(540, 655)  # 点击空白处关闭
            tapSleep(540, 655)  # 点击空白处关闭

            # 兑换门票
            needCount = safe_int(功能开关["钻石兑换门票次数"])
            if needCount == '':
                needCount = 0
            if needCount > 0:
                for i in range(1, 5):
                    TomatoOcrTap(570, 261, 645, 285, "兑换门票")
                    res, buyCount = TomatoOcrText(377, 944, 389, 959, "已购买次数")  # 1/9
                    buyCount = safe_int(buyCount)
                    if buyCount != "" and buyCount >= needCount:
                        TomatoOcrTap(70, 1202, 122, 1232, "返回", 10, 10)  # 返回芙
                        break
                    TomatoOcrTap(318, 876, 398, 898, "购买道具")
                    tapSleep(550, 1080)  # 点击空白处关闭
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

        tapSleep(200, 545, 4)  # 芙芙小铺
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
                res = TomatoOcrTap(568, 260, 645, 285, "兑换卢恩")
                res, buyCount = TomatoOcrText(375, 944, 387, 960, "已购买次数")  # 1/9
                buyCount = safe_int(buyCount)
                if buyCount != "" and buyCount >= needCount:
                    res = TomatoOcrTap(70, 1202, 122, 1232, "返回", 10, 10)  # 返回芙芙小铺，继续
                    break
                res = TomatoOcrTap(318, 876, 398, 898, "购买道具")
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
            res, _ = TomatoOcrText(528, 1070, 609, 1103, "批量讲述")
            if res:
                tapSleep(516, 1087)
                sleep(1)
            while attempt < needCount:
                res = TomatoOcrTap(319, 1062, 398, 1083, "讲述故事")
                sleep(2)
                res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                tapSleep(170, 1090)  # 点击空白处
                attempt = attempt + 1

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

        tapSleep(300, 740, 4)  # 邮件
        res = TomatoOcrTap(463, 1030, 510, 1061, "领取")
        if not res:
            TomatoOcrTap(67,1182,121,1221, "返回", 10, 10)
            return
        else:
            任务记录["邮件领取-完成"] = 1
        sleep(2)
        tapSleep(120, 1030)  # 点击空白处
        tapSleep(110, 1204)  # 点击返回

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
            teamStatus = TomatoOcrTap(632, 570, 684, 598, "匹配中")
            if teamStatus:
                Toast('取消匹配')

            teamExist = ocrFindRangeClick('离开队伍')
            if teamExist:
                teamExist = ocrFindRangeClick('确定')
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

        res1, text1 = TomatoOcrText(19, 1104, 94, 1128, "点击输入")
        res2 = False
        res3 = False
        if not res1:
            res2, text2 = TomatoOcrText(543, 104, 622, 142, "倒计时")
            if not res2:
                res3, text3 = TomatoOcrText(598, 84, 636, 104, "回合")
        if not res1 and not res2 and not res3:
            return

        Toast("队伍发言")

        res1 = TomatoOcrTap(19, 1101, 94, 1135, "点击输入", 10, 10)
        if not res1:
            res2 = TomatoOcrTap(16, 1100, 96, 1135, "点击输入", 10, 10)
        sleep(2.5)  # 等待输入法弹窗
        if res1 or res2:
            # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
            sleep(1)
            # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
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
