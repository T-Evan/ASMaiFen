# 导包
from PIL.ImageChops import offset
from ascript.android.system import ShellListener

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
from ascript.android import system
import sys
import traceback


class DailyTask:
    def __init__(self):
        self.shilianTask = ShiLianTask()
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")

    def homePage(self, needQuitTeam=False):
        tryTimes = 0
        while True:
            tryTimes = tryTimes + 1
            # 避免战斗中直接退出
            if 功能开关["fighting"] == 1:
                if tryTimes < 10:
                    res, _ = TomatoOcrText(649, 321, 694, 343, '队伍')
                    if res:
                        sleep(30)
                        continue

                    Toast(f'返回首页 - 等待战斗结束{tryTimes * 10}/100')
                    sleep(10)
                    continue

            if tryTimes > 3:
                self.closeLiaoTian()

            if tryTimes > 10:
                system.open(f"{功能开关['游戏包名']}")
                # 暂不处理战败页启动，提高执行效率
                # 判断战败页面
                if 功能开关["fighting"] == 0:
                    self.shilianTask.fight_fail()
                    self.shilianTask.quitTeamFighting()
                    self.quitTeam()

            if tryTimes > 15:
                Toast(f'尝试返回游戏,{tryTimes}/20')
                system.open(f"{功能开关['游戏包名']}")
            if tryTimes > 20:
                res1, _ = TomatoOcrText(311, 588, 408, 637, "异地登录")
                res2, _ = TomatoOcrText(292, 691, 427, 722, "尝试重新连接")
                if not res2 and (res1 and 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0"):
                    return
                Toast('尝试重启游戏')
                # 结束应用
                # r = system.shell("am kill com.xd.cfbmf", L())
                r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
                # 重启游戏
                self.startupTask.start_app()
            if tryTimes > 23:
                return

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
            if res2 or shou_ye1 or shou_ye2:
                # 关闭喊话窗口
                point = FindColors.find(
                    "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                    rect=[11, 26, 364, 489])
                if point:
                    Toast('关闭喊话窗口')
                    tapSleep(point.x, point.y, 1)
                # if TimeoutLock(switch_lock).acquire_lock():
                功能开关["needHome"] = 0
                # 功能开关["fighting"] = 0
                # TimeoutLock(switch_lock).release_lock()
                if 任务记录["玩家名称"] == "":
                    res, name = TomatoOcrText(94, 78, 210, 102, '玩家名称')
                    任务记录["玩家名称"] = name
                    res, fightNum = TomatoOcrText(110, 99, 200, 118, '玩家战力')
                    if "万" in fightNum:
                        任务记录["玩家战力"] = float(fightNum.replace("万", "")) * 10000
                    else:
                        任务记录["玩家战力"] = float(fightNum.replace("万", ""))
                Toast('已返回首页')
                # sleep(0.5)
                if 功能开关["fighting"] == 0 and needQuitTeam:
                    quitTeamRe = self.quitTeam()

                status = self.checkGameStatus()
                if not status:
                    # 重启游戏
                    self.startupTask.start_app()
                return True

            # 开始异步处理返回首页
            # if TimeoutLock(switch_lock).acquire_lock():
            功能开关["needHome"] = 1
            # TimeoutLock(switch_lock).release_lock()

            # 判断宝箱开启
            # self.shilianTask.openTreasure()
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

        res = TomatoOcrTap(522, 1205, 598, 1235, "麦乐兽", sleep1=0.8)

        # tapSleep(551, 942)  # 仓库最后1个麦乐兽
        # res = TomatoOcrTap(333, 1027, 358, 1049, "升")
        # if res:
        #     tapSleep(138, 1051)  # 重置按钮
        #     res = TomatoOcrTap(440, 787, 513, 820, "重置")
        #     tapSleep(150, 1059)  # 点击空白处
        #     任务记录["日常-升级1次麦乐兽-完成"] = 1
        # else:
        #     Toast("每日任务 - 升级1次麦乐兽 - 未找到升级入口")

        # 升级主战麦乐兽
        tapSleep(352, 356)
        res = TomatoOcrTap(333, 1027, 358, 1049, "升")
        if res:
            tapSleep(200, 1100)  # 点击空白处
            任务记录["日常-升级1次麦乐兽-完成"] = 1
        else:
            Toast("每日任务 - 升级1次麦乐兽 - 未找到升级入口")
            tapSleep(200, 1100)  # 点击空白处

        # 升级辅助麦乐兽左
        tapSleep(241, 363)
        res = TomatoOcrTap(333, 1027, 358, 1049, "升")
        if res:
            tapSleep(200, 1100)  # 点击空白处
            任务记录["日常-升级1次麦乐兽-完成"] = 1
        else:
            Toast("每日任务 - 升级1次麦乐兽 - 未找到升级入口")
            tapSleep(200, 1100)  # 点击空白处

        # 升级辅助麦乐兽右
        tapSleep(473, 348)
        res = TomatoOcrTap(333, 1027, 358, 1049, "升")
        if res:
            tapSleep(200, 1100)  # 点击空白处
            任务记录["日常-升级1次麦乐兽-完成"] = 1
        else:
            Toast("每日任务 - 升级1次麦乐兽 - 未找到升级入口")
            tapSleep(200, 1100)  # 点击空白处

    # 每日任务 - 洗练1次装备
    def meiRiXiLian(self):
        if not 功能开关['洗练1次装备']:
            return

        if 任务记录["日常-洗练1次装备-完成"] == 1:
            return

        Toast("每日任务 - 洗练1次装备 - 开始")
        self.homePage()

        # 判断是否已洗练状态
        res = TomatoOcrTap(626, 379, 711, 405, "冒险手册", 30, -20, sleep1=1)
        if not res:
            Toast("识别冒险手册失败")
            return

        # 日常领取
        res = TomatoOcrTap(274, 1102, 326, 1130, "每日", sleep1=0.9)
        if res:
            swipe(358, 527, 353, 1215, 250)  # 返回最上面
            sleep(1.5)
            for k in range(6):
                # 识别黄色领取按钮
                pointsTask = FindColors.find_all(
                    "242,572,#F2A94A|303,573,#F2A94A|332,569,#FBFBFB|332,570,#F7F7F6|339,577,#F9F9F9|423,572,#F2A94A")
                if pointsTask:
                    for p in pointsTask:
                        re, taskName = TomatoOcrText(p.x - 80, p.y - 80, p.x + 70, p.y - 45, "任务名称")
                        if taskName == "洗练1次装备":
                            任务记录["日常-洗练1次装备-完成"] = 1
                            Toast('日常-洗练1次装备-完成')
                            return
                swipe(337, 860, 330, 648)
                sleep(1.5)

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

    def shijieShout(self, contentAI=""):
        if 功能开关['世界喊话'] == "" and 功能开关['世界喊话2'] == "" and 功能开关['世界喊话3'] == "" and 功能开关[
            '世界喊话4'] == "" and contentAI == "":
            return 1

        if 功能开关['世界喊话开关'] == "" or 功能开关['世界喊话开关'] == 0:
            Toast('世界喊话 - 开关关闭')
            return 1

        contentArr = []
        if contentAI != "":
            contentArr.append(contentAI)
        else:
            if 功能开关['世界喊话'] != "":
                contentArr.append(功能开关['世界喊话'])
            if 功能开关['世界喊话2'] != "":
                contentArr.append(功能开关['世界喊话2'])
            if 功能开关['世界喊话3'] != "":
                contentArr.append(功能开关['世界喊话3'])
            if 功能开关['世界喊话4'] != "":
                contentArr.append(功能开关['世界喊话4'])

        # 避免与自动入队识别冲突
        if 功能开关["fighting"] == 1:
            Toast("世界喊话 - 其他任务执行中 - 等待5s")
            sleep(3)
            if 功能开关["fighting"] == 1:
                Toast("世界喊话 - 其他任务执行中 - 返回")
                return

        Toast("世界喊话 - 开始")

        # 关闭喊话窗口
        self.closeLiaoTian()

        # AI回复世界频道发言
        if 功能开关['世界AI发言'] == 1 and contentAI == "":
            # 检查公屏发言关键词
            player_messages = shijieShoutText()
            for player, messages in player_messages.items():
                team_texts = [msg.replace('元旦快乐~', '').replace('新年快乐~', '').replace('早安~', '')
                              .replace('晚安~', '').replace('午安~', '') for msg in messages
                              if "回环" not in msg]
                if player == '默认':
                    player = ''
                colors = generate_random_color()
                zanList3 = ['狐巡司', '第一只']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~点开主线大地图，滑动上方找到藏匿妖怪喔~</COLOR>"]
                    return self.shijieShout(random.choice(content))
                zanList3 = ['火眼金睛', '找妖怪', '在哪']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~1.大地图 2.铁匠铺 3.秘境之间~</COLOR>"]
                    return self.shijieShout(random.choice(content))
                # zanList3 = ['元旦快乐', '新年快乐']
                # contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                # if contains_zan:
                #     content = [f"<color={colors}>{player}~元旦快乐~</COLOR>",
                #                f"<color={colors}>{player}~新年快乐~</COLOR>", ]
                #     return self.shijieShout(random.choice(content))
                zanList3 = ['早安', '早上好']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    return self.shijieShout(f"<color={colors}>{player}~早安~</COLOR>")
                zanList3 = ['晚安', '晚上好']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    return self.shijieShout(f"<color={colors}>{player}~晚安~</COLOR>")
                zanList3 = ['午安', '中午好']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    return self.shijieShout(f"<color={colors}>{player}~午安~</COLOR>")
                zhanLi = int(任务记录["玩家战力"] / 10000)
                职业映射 = {
                    '战士': '战',
                    '服事': '奶',
                    '刺客': '刺',
                    '法师': '法',
                    '游侠': '弓'
                }
                zhiye = 职业映射.get(任务记录["玩家-当前职业"], '')
                self.shilianTask.zhiYeZhanLi()
                extraContent = f'{zhanLi}w{zhiye}'
                zanList3 = ['在哪里', '来一个', '来人', '求个', '来个', '来打工', '来黑工', '来奶', '来t', '来输出',
                            '来打工']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~来了来了~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~来了~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~来啦~{extraContent}</COLOR>"]

                    return self.shijieShout(random.choice(content))
                zanList3 = ['有没有', '有人', '有打工', '帮帮', '有佬', '有帮忙', '可以帮忙', '还有', '有吗', '求佬']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~打工打工~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~打工~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~有的~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~来啦~{extraContent}</COLOR>"]
                    return self.shijieShout(random.choice(content))
                zanList = ['影子', '求带', '带个', '带带', '差个', '有大哥', '帮忙', '求求']
                contains_zan = any(any(zan in text for zan in zanList) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~拉我拉我~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~拉我~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~打工打工~{extraContent}</COLOR>",
                               f"<color={colors}>{player}~打工~{extraContent}</COLOR>"]
                    return self.shijieShout(random.choice(content))
                # zanList = ['*']
                # contains_zan = any(any(zan in text for zan in zanList) for text in team_texts)
                # if contains_zan:
                #     content = [f"<color={colors}>{player}~请文明发言喔~</COLOR>"]
                #     return self.shijieShout(random.choice(content))
                # zanList = ['机器人', 'AI', 'ai', '脚本']
                # contains_zan = any(any(zan in text for zan in zanList) for text in team_texts)
                # if contains_zan:
                #     content = [f"<color={colors}>{player}~新年快乐~(*^▽^*)~</COLOR>"]
                #     return self.shijieShout(random.choice(content))

        need_dur_minute = safe_int(功能开关.get("世界喊话间隔", 0))  # 分钟
        if need_dur_minute == '':
            need_dur_minute = 0
        if contentAI == "" and need_dur_minute > 0 and 任务记录["世界喊话-倒计时"] > 0:
            diffTime = time.time() - 任务记录["世界喊话-倒计时"]
            if diffTime < need_dur_minute * 60:
                Toast(f'日常 - 世界喊话 - 倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                return
        if contentAI != "" and 任务记录["世界喊话AI-倒计时"] > 0:
            diffTime = time.time() - 任务记录["世界喊话AI-倒计时"]
            if diffTime < random.randint(50, 60):
                Toast(f'日常 - 世界AI喊话 - 倒计时{round((60 - diffTime) / 60, 2)}min')
                return

        self.homePage(needQuitTeam=True)

        contents = random.choice(contentArr).split('|')
        print(contents)
        for content in contents:
            # print(content)
            res1 = TomatoOcrTap(18, 1098, 97, 1134, "点击输入", 10, 10)
            res2 = False
            if not res1:
                res2 = TomatoOcrTap(17, 1103, 96, 1134, "点击输入", 10, 10)
            if res1 or res2:
                # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
                sleep(0.5)
                # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                action.input(content)
                tapSleep(360, 104, 0.5)  # 点击空白处确认输入
                shuru = TomatoOcrTap(78, 1156, 157, 1191, '点击输入')
                if shuru:
                    action.input(content)
                    tapSleep(360, 104, 0.5)  # 点击空白处确认输入
                res = TomatoOcrTap(555, 1156, 603, 1188, "发送", 10, 10)
                if res:
                    if contentAI == "":
                        任务记录["世界喊话-倒计时"] = time.time()
                    if contentAI != "":
                        任务记录["世界喊话AI-倒计时"] = time.time()
                    # tapSleep(472, 771, 0.5)
            # 关闭喊话窗口
            tapSleep(472, 771, 0.8)

        if 功能开关['自动切换喊话频道'] == 1 and contentAI == "":
            for i in range(3):
                # 避免与自动入队识别冲突
                if 功能开关["fighting"] == 1:
                    return

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
                res = TomatoOcrTap(546, 138, 625, 165, '切换频道', -20, 10, sleep1=0.8)
                if not res:
                    continue

                res, 当前频道 = TomatoOcrText(154, 451, 263, 489, '当前频道')
                print('当前频道：' + 当前频道)
                当前频道数字 = rePattern.findall(r'\d+', 当前频道)
                # 检查列表是否为空
                if not 当前频道数字:
                    continue
                # print(当前频道数字)
                if 当前频道数字 == '':
                    continue
                当前频道数字 = safe_int(当前频道数字[0])

                # swipe(236, 828, 210, 381, 300)  # 下翻20
                # res, 最大频道 = TomatoOcrText(408, 814, 510, 841, '最大频道')
                # swipe(210, 381, 236, 828, 300)  # 上翻20
                # 最大频道数字 = rePattern.findall(r'\d+', 最大频道)
                # if not 最大频道数字 or 最大频道数字 == '':
                #     最大频道数字 = 0
                # else:
                #     最大频道数字 = safe_int_v2(最大频道数字[0])
                #     print('最大', 最大频道数字)
                最大频道数字 = 15

                # 每次喊话3个频道
                for j in range(4):
                    下一频道数字 = 当前频道数字 - 1
                    findNext = False
                    if 功能开关['世界喊话热点频道'] == 1:
                        Toast('开始切换热点频道')
                        for p in range(3):
                            point = FindColors.find("179,908,#F09C2F|180,914,#EF9B30|184,917,#E8962C",
                                                    rect=[104, 594, 610, 878], diff=0.95)  # 黄色
                            if point:
                                re, _ = TomatoOcrText(point.x + 170, point.y - 30, point.x + 220, point.y, '当前')
                                if not re:
                                    Toast('切换黄色热点频道')
                                    findNext = True
                                    tapSleep(point.x, point.y)
                                    break
                            point = FindColors.find(
                                "383,471,#ED5B3E|388,467,#ED5B3E|391,475,#E2543A",
                                rect=[115, 609, 164, 869], diff=0.95)  # 红色
                            if not point:
                                point = FindColors.find(
                                    "383,471,#ED5B3E|388,467,#ED5B3E|391,475,#E2543A",
                                    rect=[366, 609, 415, 875], diff=0.95)  # 红色
                            if point:
                                re, _ = TomatoOcrText(point.x + 170, point.y - 30, point.x + 220, point.y, '当前')
                                if not re:
                                    Toast('切换红色热点频道')
                                    findNext = True
                                    tapSleep(point.x, point.y)
                                    break
                        if not findNext:
                            Toast('未识别到热点频道')
                            tapSleep(101, 1200)  # 未切换频道，点击返回
                            break
                    else:
                        if 下一频道数字 < 1:
                            for k in range(8):
                                swipe(236, 828, 210, 381, 300)  # 翻20
                                sleep(1)
                                res, 最大频道右 = TomatoOcrText(408, 814, 510, 841, '最大频道')  # 底部右侧频道
                                res, 最大频道左 = TomatoOcrText(161, 812, 262, 842, '最大频道')  # 底部左侧频道
                                下一频道数字右 = rePattern.findall(r'\d+', 最大频道右)
                                下一频道数字左 = rePattern.findall(r'\d+', 最大频道左)
                                if len(下一频道数字右) > 0 or len(下一频道数字左) > 0:
                                    下一频道数字右 = safe_int_v2(下一频道数字右[0])
                                    下一频道数字左 = safe_int_v2(下一频道数字左[0])
                                    if 下一频道数字左 > 0 and 下一频道数字右 - 下一频道数字左 > 2:
                                        下一频道数字 = 下一频道数字左
                                    elif 下一频道数字右 > 0:
                                        下一频道数字 = 下一频道数字右
                                else:
                                    下一频道数字 = 3  # 默认3个频道
                                最大频道数字 = 下一频道数字
                                if 最大频道数字 > 0:
                                    break
                                # findNext = True
                                # 下一频道数字 = 5  # 尝试仍按指定频道切换，避免固定位置点击偶尔失效导致的刷屏
                        if 下一频道数字 > 0:
                            # print(下一频道数字)
                            下一频道 = '简体中文' + str(下一频道数字)
                            print('下一频道：' + 下一频道)
                            # 寻找下一频道
                            for k in range(8):
                                # 避免与自动入队识别冲突
                                if 功能开关["fighting"] == 1:
                                    return
                                re, _ = TomatoOcrText(318, 359, 397, 386, '选择频道')
                                if not re:
                                    res = TomatoOcrTap(546, 138, 625, 165, '切换频道', -20, 10, sleep1=0.8)

                                re, _ = TomatoOcrText(161, 454, 258, 486, '下一频道')  # 判断当前频道是否已切换为下一频道
                                if re:
                                    tapSleep(356, 1112)
                                    findNext = True
                                    break

                                res = TomatoOcrFindRangeClick(下一频道, 0.9, 0.9, 101, 437, 617, 880, offsetX=10,
                                                              offsetY=10)
                                sleep(0.8)
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
                                res, _ = TomatoOcrText(296, 129, 427, 176, 下一频道)
                                if not res:
                                    res, name = TomatoOcrText(296, 129, 427, 176, 下一频道)
                                    if not res:
                                        name = name.replace('简体中文', '')
                                        res = name == str(下一频道数字)
                                if res:
                                    findNext = True
                                    break
                    if findNext:
                        contents = random.choice(contentArr).split('|')
                        for content in contents:
                            for q in range(3):
                                # 避免与自动入队识别冲突
                                if 功能开关["fighting"] == 1:
                                    return
                                shuru1 = TomatoOcrTap(80, 1194, 118, 1226, '点击')
                                shuru2 = False
                                if not shuru1:
                                    shuru2 = TomatoOcrTap(79, 1155, 118, 1191, '点击')
                                if shuru1 or shuru2:
                                    # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
                                    # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                                    action.input(content)
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
                                        if res:
                                            tapSleep(333, 792, 0.5)
                                            break
                                else:
                                    res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                                    if not res:
                                        tapSleep(353, 427)  # 点击空白处确认输入
                                        res = TomatoOcrTap(554, 1160, 609, 1186, "发送", 10, 10)
                                    if res:
                                        tapSleep(333, 792, 0.5)
                                        break
                        # 关闭喊话窗口
                        point = FindColors.find(
                            "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                            rect=[11, 26, 364, 489])
                        if point:
                            Toast('关闭喊话窗口')
                            tapSleep(point.x, point.y, 1)
                        break

        # 关闭喊话窗口
        point = FindColors.find(
            "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
            rect=[11, 26, 364, 489])
        if point:
            Toast('关闭喊话窗口')
            tapSleep(point.x, point.y, 1)
        功能开关["fighting"] = 0
        return 0

    def dailyTaskEnd(self):
        # 摸鱼时间到
        self.huoDongMoYu()
        # 派对大师
        self.PaiDuiDaShi()
        # 箱庭苗圃
        self.XiangTingMiaoPu()
        # 箱庭苗圃
        self.QiTaQianDao()

        if 功能开关["日常总开关"] == 0:
            return

        self.homePage(needQuitTeam=True)
        # 日常相关

        # 活动
        # 火力全开
        self.huoLiQuanKai()
        # 紧急委托
        self.jinJiWeiTuo()
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
        if 功能开关["日常总开关"] == 0 or 功能开关["冒险手册领取"] == 0:
            return

        re = CompareColors.compare("683,351,#F35F42|686,351,#F15E40|690,351,#F65A41|686,353,#ED5B3D")  # 冒险手册红点
        if not re and 任务记录["冒险手册-倒计时"] > 0:
            diffTime = time.time() - 任务记录["冒险手册-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'日常 - 冒险手册 - 倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["冒险手册-倒计时"] = time.time()

        Toast("日常 - 冒险手册领取 - 开始")
        self.homePage()

        res = TomatoOcrTap(549, 381, 626, 403, '新手试炼', sleep1=1)
        if res:
            Toast("日常 - 新手试炼领取 - 开始")
            # 识别黄色领取按钮
            while 1:
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 2)
                    tapSleep(356, 1213)  # 点击空白处关闭
                    tapSleep(356, 1213)  # 点击空白处关闭（再次点击，避免成就升级页）
                else:
                    break

        res = TomatoOcrTap(626, 379, 711, 405, "冒险手册", 30, -20, sleep1=1)
        if not res:
            Toast("识别冒险手册失败")
            return

        # 主线领取
        if CompareColors.compare("235,1104,#F05C3F|235,1101,#F45F42|233,1100,#F36042"):
            res = TomatoOcrTap(156, 1101, 206, 1129, "主线", sleep1=0.8)
        if not res:
            if CompareColors.compare("476,1098,#F96244|476,1100,#F46042|476,1104,#F15A41|475,1104,#F15A41"):
                res = TomatoOcrTap(394, 1099, 448, 1132, "主线", sleep1=0.9)
        if res:
            while 1:
                # 识别黄色领取按钮
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 1)
                    tapSleep(320, 1180)  # 点击空白处关闭
                else:
                    break

        # 日常领取
        # if CompareColors.compare("355,1104,#EF5C3F|355,1100,#F45F42|352,1103,#EF5C3F"):
        res = TomatoOcrTap(274, 1102, 326, 1130, "每日", sleep1=0.9)
        if res:
            swipe(358, 527, 353, 1215, 250)  # 返回最上面
            sleep(1.5)

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
            else:
                # 点击宝箱（最右）
                tapSleep(570, 390)
                tapSleep(490, 390)
                tapSleep(410, 390)
                tapSleep(330, 390)

            if 功能开关['冒险手册完成后停止'] == 1:
                # 判断是否完成日常
                res = CompareColors.compare(
                    "573,394,#FAF3C5|579,391,#D97D6C|570,391,#CE9F82|574,399,#F7E0B4|579,394,#D4B887|546,392,#F2A94A|546,386,#F2A94A")
                if res:
                    Dialog.confirm("日常任务已完成")
                    system.exit()

        # 每周领取
        res = TomatoOcrTap(394, 1099, 448, 1132, "每周", sleep1=0.9)
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
            res = TomatoOcrTap(514, 1099, 570, 1132, "成就", sleep1=0.9)
            while 1:
                # 识别黄色领取按钮
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 2)
                    tapSleep(360, 1070)  # 点击空白处关闭
                    tapSleep(360, 1070)  # 点击空白处关闭（再次点击，避免成就升级页）
                else:
                    break

        # 返回首页
        self.homePage()

    # 前往新地图
    def newMap(self):
        if 功能开关["自动挑战首领"] == 1:
            Toast("日常 - 挑战首领 - 开始")
            self.homePage()
            sleep(1)
            res1 = TomatoOcrTap(626, 763, 702, 797, "挑战首领")
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
                        if 功能开关["优先推图到最新关卡"] == 1:
                            res = TomatoOcrTap(428, 1073, 521, 1100, "下一关卡", 10, 10)
                            if res:
                                Toast('前往下一关')
                        sleep(5)
                        break

        if 功能开关["自动换图"] == 1:
            Toast("日常 - 前往新地图 - 开始")
            self.homePage()
            # 直接点击图标切换
            newMapOK, x, y = imageFind('首页-前往新关卡', confidence1=0.7, x1=565, y1=643, x2=705, y2=822)
            if newMapOK:
                tapSleep(x, y, 5)
            res = TomatoOcrTap(593, 676, 638, 693, "前往")
            # 队员不满足时，才会不展示首页的前往下一关快速入口；因此判断开了单飞再从地图跳转下一关
            if not newMapOK and 功能开关["队员不满足单飞"] == 1:
                res1, _ = TomatoOcrText(573, 200, 694, 238, "新关卡已解锁")
                res2 = False
                if not res1:
                    res2, _ = TomatoOcrText(573, 200, 694, 238, "新地图已解锁")
                if res1 or res2:
                    # if 1:
                    # 结伴入口切换
                    res = TomatoOcrTap(647, 450, 689, 474, "结伴", 10, -10)
                    res = TomatoOcrTap(373, 1106, 471, 1141, "关卡大厅", 0.7)
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

                            res, _ = TomatoOcrText(432, 729, 530, 760, "留在队伍")
                            if res:
                                if 功能开关["队员不满足单飞"] == 1:
                                    res = TomatoOcrTap(187, 730, 282, 756, "离队前往")
                                else:
                                    res = TomatoOcrTap(435, 729, 532, 759, "留在队伍")
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

    # 派对大师
    def PaiDuiDaShi(self):
        for p in range(5):
            if 功能开关["派对大师"] == 0:
                return

            if 任务记录["派对大师-完成"] == 1:
                return

            Toast('日常 - 派对大师 - 开始')

            self.homePage()
            self.quitTeam()
            # 开始派对大师
            res1 = TomatoOcrTap(556, 380, 618, 404, "派对大师", 30, -10)
            res2 = TomatoOcrTap(556, 380, 618, 404, "舞会在即", 30, -10)
            if not res1 and not res2:
                res1 = TomatoOcrTap(554, 464, 622, 487, "派对大师", 30, -10)  # 适配新手试炼 - 下方入口
                res2 = TomatoOcrTap(554, 464, 622, 487, "舞会在即", 30, -10)  # 适配新手试炼 - 下方入口
                if not res1 and not res2:
                    res1 = TomatoOcrTap(548, 548, 626, 568, "派对大师", 30, -10)  # 适配新手试炼 - 下方入口
                    res2 = TomatoOcrTap(548, 548, 626, 568, "舞会在即", 30, -10)  # 适配新手试炼 - 下方入口
                    if not res1 and not res2:
                        res1 = TomatoOcrTap(546, 628, 630, 653, "派对大师", 30, -10)  # 适配新手试炼 - 下方入口
                        res2 = TomatoOcrTap(546, 628, 630, 653, "舞会在即", 30, -10)  # 适配新手试炼 - 下方入口
                        if not res1 and not res2:
                            res1 = TomatoOcrTap(550, 713, 569, 734, "派", 30, -20)  # 适配新手试炼 - 下方入口
                            res2 = TomatoOcrTap(550, 713, 569, 734, "舞", 30, -20)  # 适配新手试炼 - 下方入口
                            if not res1 and not res2:
                                Toast('日常 - 派对大师 - 未找到入口')
                                return
            sleep(1)

            # 领取累积奖励
            for k in range(3):
                re = CompareColors.compare("581,351,#F1A949|581,347,#F1A949|581,356,#F1A949")  # 最后一个奖励需右滑，根据橙色进度条特殊处理
                if re:
                    tapSleep(573, 303)
                    tapSleep(606, 992)

                re = FindColors.find("576,909,#F15D40|580,907,#F45F42|577,912,#ED5B3E", rect=[213, 887, 604, 980],
                                     diff=0.95)
                if re:
                    tapSleep(re.x, re.y + 10)
                    tapSleep(216, 872)  # 点击空白

                re = FindColors.find("454,283,#F45F42|449,286,#F05B3F|454,286,#F05C40", rect=[95, 246, 635, 400],
                                     diff=0.95)
                if re:
                    tapSleep(re.x, re.y + 10)
                    tapSleep(216, 872)  # 点击空白

            # 识别是否已完成
            if 功能开关['派对大师重复挑战'] == 0:
                re = CompareColors.compare("517,939,#F1A949|524,939,#F1A949")  # 第五格宝箱
                if re:
                    Toast('日常 - 派对大师 - 已完成')
                    tapSleep(549, 920)
                    tapSleep(519, 1136)
                    任务记录["派对大师-完成"] = 1
                    return

            re = TomatoOcrTap(302, 1054, 363, 1085, '开始', 50, 10)
            if not re:
                re = TomatoOcrTap(361, 1055, 418, 1086, '匹配', 30, 10)
                if not re:
                    Toast('派对大师 - 进入失败')
                    return

            Toast('派对大师 - 开始匹配')

            attempts = 0  # 初始化尝试次数
            maxAttempts = 10  # 设置最大尝试次数
            resStart = False
            failCount = 0
            while attempts < maxAttempts:
                resStart = TomatoOcrTap(453, 602, 503, 634, '准备', 50, 10)
                startStatus = TomatoOcrTap(302, 1054, 363, 1085, '开始', 50, 10)
                waitStatus, _ = TomatoOcrText(320, 1039, 399, 1066, "匹配中")
                if resStart:
                    Toast("匹配成功 - 已准备")
                    for j in range(10):
                        resStart = TomatoOcrTap(453, 602, 503, 634, '准备', 50, 10)
                        startStatus = TomatoOcrTap(302, 1054, 363, 1085, '开始', 50, 10)
                        res1, text1 = TomatoOcrText(93, 303, 176, 336, "本轮目标")
                        if res1:
                            Toast("匹配成功 - 开始游戏")
                            self.PaiDuiDaShiFighting()
                            break
                        sleep(2)  # 等待进入
                    break
                sleep(2)  # 等待进入

    def PaiDuiDaShiFighting(self):
        # 开始战斗
        功能开关['fighting'] = 1
        attempt = 0
        while True:
            re, text = TomatoOcrText(337, 118, 382, 137, '当前轮次')
            if "轮" not in text:
                attempt = attempt + 1
            if attempt > 3:
                Toast('派对大师-战斗结束')
                break
            res1, _ = TomatoOcrText(323, 842, 401, 865, "每日奖励")
            res2 = FindColors.find(
                "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
                rect=[301, 1130, 421, 1273])
            if res1 or res2:
                Toast('派对大师-战斗结束')
                break

            attempt2 = 0
            for i in range(15):
                object = ''

                re, x, y = imageFind('派对大师-绿人', 0.8, 78, 211, 192, 347)
                if re:
                    object = '绿人'
                    Toast(f'本轮目标-{object}')
                    break
                re, x, y = imageFind('派对大师-橙人', 0.8, 78, 211, 192, 347)
                if re:
                    object = '橙人'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-蓝人', 0.8, 78, 211, 192, 347)
                if re:
                    object = '蓝人'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-红人', 0.8, 78, 211, 192, 347)
                if re:
                    object = '红人'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-紫人', 0.8, 78, 211, 192, 347)
                if re:
                    object = '紫人'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-糖果', 0.8, 78, 211, 192, 347)
                if re:
                    object = '糖果'
                    Toast(f'本轮目标-{object}')
                    break
                re, x, y = imageFind('派对大师-猫咪', 0.8, 78, 211, 192, 347)
                if re:
                    object = '猫咪'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-帽子', 0.8, 78, 211, 192, 347)
                if re:
                    object = '帽子'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-幽灵', 0.8, 78, 211, 192, 347)
                if re:
                    object = '幽灵'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-南瓜', 0.8, 78, 211, 192, 347)
                if re:
                    object = '南瓜'
                    Toast(f'本轮目标-{object}')
                    break

                re, x, y = imageFind('派对大师-糖果', 0.8, 78, 211, 192, 347)
                if re:
                    object = '糖果'
                    Toast(f'本轮目标-{object}')
                    break

                if object != '':
                    Toast(f'本轮目标-{object}')
                    break

                re, text = TomatoOcrText(337, 118, 382, 137, '当前轮次')
                if "轮" not in text:
                    attempt2 = attempt2 + 1
                    if attempt2 > 5:
                        break
                Toast(f'等待下一轮开始')
                sleep(1)

            if object != '':
                sleep(2)
                re, 轮次 = TomatoOcrText(337, 118, 382, 137, '当前轮次')
                find = False
                isSwipe = False
                swipeArr = []
                points = ''
                points2 = ''
                attempt3 = 0
                for i in range(20):
                    tmpPoints = ''
                    tmpSwipeArr = []
                    # 识别卡牌
                    if not find:
                        if object == '绿人':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-绿人', 0.9, 82, 222, 674, 1112)
                        elif object == '蓝人':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-蓝人', 0.9, 82, 222, 674, 1112)
                        elif object == '橙人':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-橙人', 0.9, 82, 222, 674, 1112)
                        elif object == '红人':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-红人', 0.9, 82, 222, 674, 1112)
                        elif object == '紫人':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-紫人', 0.9, 82, 222, 674, 1112)
                        elif object == '猫咪':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-猫咪', 0.9, 82, 222, 674, 1112)
                        elif object == '帽子':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-帽子', 0.9, 82, 222, 674, 1112)
                        elif object == '幽灵':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-幽灵', 0.9, 82, 222, 674, 1112)
                        elif object == '南瓜':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-南瓜', 0.9, 82, 222, 674, 1112)
                        elif object == '糖果':
                            re, tmpPoints = imageFindAll('派对大师-卡牌-糖果', 0.9, 82, 222, 674, 1112)

                        if re:
                            find = True
                            points = tmpPoints
                            # centerArr = []
                            # for p in points:
                            #     centerX = p['center_x']
                            #     centerY = p['center_y']
                            #     centerArr.append({centerX, centerY})
                            Toast(f'已寻找到{object}')

                        # v2版本，识别指示标记，直接锚定自己的目标
                        tmpPoints2 = FindColors.find_all(
                            "331,574,#6FCB5A|331,569,#6FCB5A|333,569,#6FCB5A|333,574,#6FCB5A|336,576,#6FCB5A",
                            rect=[83, 227, 655, 1115])
                        if tmpPoints2:
                            find = True
                            points2 = tmpPoints2

                    re2, tmpPoints = imageFindAll('派对大师-卡牌-猫咪', 0.9, 82, 222, 674, 1112)
                    re3, tmpPoints = imageFindAll('派对大师-卡牌-绿人', 0.9, 82, 222, 674, 1112)
                    if not isSwipe and not re2 and not re3:
                        sleep(2)
                        if 轮次 == '第5轮':
                            Toast('等待旋转')
                            sleep(3)
                        # 卡牌关闭，开始检查旋转
                        # 识别旋转；从顶部第一个开始
                        # 第一排
                        re = CompareColors.compare("375,288,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 375, 'y': 285})
                        # 第二排
                        re = CompareColors.compare("230,396,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 230, 'y': 395})
                        re = CompareColors.compare("369,394,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 370, 'y': 395})
                        re = CompareColors.compare("508,396,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 510, 'y': 395})
                        # 第三排
                        re = CompareColors.compare("148,505,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 150, 'y': 505})
                        re = CompareColors.compare("293,503,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 295, 'y': 505})
                        re = CompareColors.compare("442,503,#ECBF7C")
                        if not re:
                            tmpSwipeArr.append({'x': 440, 'y': 505})
                        re = CompareColors.compare("581,506,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 580, 'y': 505})
                        # 第四排
                        re = CompareColors.compare("143,610,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 145, 'y': 610})
                        re = CompareColors.compare("574,613,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 575, 'y': 610})
                        # 第五排
                        re = CompareColors.compare("137,721,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 135, 'y': 720})
                        re = CompareColors.compare("568,724,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 565, 'y': 720})
                        # 第六排
                        re = CompareColors.compare("134,828,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 135, 'y': 830})
                        re = CompareColors.compare("277,828,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 275, 'y': 830})
                        re = CompareColors.compare("423,827,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 425, 'y': 830})
                        re = CompareColors.compare("563,827,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 565, 'y': 830})
                        # 第七排
                        re = CompareColors.compare("205,940,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 205, 'y': 940})
                        re = CompareColors.compare("345,937,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 345, 'y': 940})
                        re = CompareColors.compare("484,937,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 485, 'y': 940})
                        # 第八排
                        re = CompareColors.compare("336,1046,#ECBF7E")
                        if not re:
                            tmpSwipeArr.append({'x': 335, 'y': 1045})

                        for p in points2:
                            for swipe in tmpSwipeArr:
                                if swipe['x'] - 55 < p.x < swipe['x'] + 65 and swipe['y'] - 55 < p.y < swipe['y'] + 65:
                                    isSwipe = True
                                    swipeArr = tmpSwipeArr
                                    print('识别到卡牌交换')
                                    break

                        for p in points:
                            for swipe in tmpSwipeArr:
                                if swipe['x'] - 55 < p['center_x'] < swipe['x'] + 65 and swipe['y'] - 55 < p[
                                    'center_y'] < swipe['y'] + 65:
                                    isSwipe = True
                                    swipeArr = tmpSwipeArr
                                    print('识别到卡牌交换')
                                    break

                    # 等待进入选择
                    sleep(1)
                    if "轮" not in 轮次:
                        attempt3 = attempt3 + 1
                        if attempt3 > 5:
                            break
                    else:
                        attempt3 = 0

                    res, _ = TomatoOcrText(402, 1164, 445, 1184, '提示')
                    if res:
                        find = True
                        break

                if find:
                    # 开始选择
                    Toast('开始选牌')
                    # sleep(1)
                    for i in range(10):
                        if points:
                            for k in range(2):
                                tmpPoints = points
                                # 先选择自己的目标，后续几轮检查选择其余目标
                                if k == 0:
                                    tmpPoints = points2

                                for p in tmpPoints:
                                    # 检查队友是否提示卡牌
                                    pointsTeam = FindColors.find_all("421,776,#3AFF70|421,776,#3AFF70")
                                    if pointsTeam:
                                        for j in pointsTeam:
                                            Toast('选择队友提示的卡牌')
                                            tapSleep(j.x + 30, j.y + 30, 0.3)
                                            TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)
                                            tapSleep(j.x + 30, j.y - 30, 0.3)
                                            TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)
                                            tapSleep(j.x - 30, j.y - 30, 0.3)
                                            TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)

                                    # 选择记录的卡牌
                                    if k == 0:
                                        x = p.x
                                        y = p.y
                                    else:
                                        x = p['center_x']
                                        y = p['center_y']
                                    if 轮次 == '第1轮':
                                        Toast('第一轮')
                                    if 轮次 == '第3轮':
                                        if 95 < int(x) < 645 and 450 < int(y) < 885:
                                            Toast('第三轮，交换中间坐标')
                                            # 从左上开始计算
                                            if 450 < int(y) < 560:
                                                if 90 < int(x) < 210:
                                                    x = 580
                                                    y = 500
                                                if 240 < int(x) < 355:
                                                    x = 570
                                                    y = 615
                                                if 385 < int(x) < 500:
                                                    x = 570
                                                    y = 725
                                                if 525 < int(x) < 640:
                                                    x = 565
                                                    y = 830
                                            # 中间第二排
                                            if 555 < int(y) < 660:
                                                if 85 < int(x) < 210:
                                                    x = 435
                                                    y = 505
                                                if 525 < int(x) < 640:
                                                    x = 420
                                                    y = 830
                                            # 中间第三排
                                            if 660 < int(y) < 775:
                                                if 85 < int(x) < 210:
                                                    x = 295
                                                    y = 505
                                                if 525 < int(x) < 640:
                                                    x = 280
                                                    y = 830
                                            # 中间第四排
                                            if 775 < int(y) < 880:
                                                if 80 < int(x) < 195:
                                                    x = 150
                                                    y = 505
                                                if 220 < int(x) < 340:
                                                    x = 145
                                                    y = 615
                                                if 360 < int(x) < 485:
                                                    x = 135
                                                    y = 715
                                                if 505 < int(x) < 630:
                                                    x = 130
                                                    y = 830
                                    if 轮次 == '第4轮':
                                        Toast('第四轮，顺时针旋转180°')
                                        x = 720 - x
                                        y = 1280 - y
                                    if 轮次 == '第5轮':
                                        Toast('第五轮，顺时针旋转180°')
                                        x = 720 - x
                                        y = 1280 - y
                                    Toast('选择卡牌')
                                    tapSleep(x, y, 0.3)
                                    TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)

                        # 检查队友是否提示卡牌
                        pointsTeam = FindColors.find_all("421,776,#3AFF70|421,776,#3AFF70")
                        if pointsTeam:
                            for p in pointsTeam:
                                Toast('选择队友提示的卡牌')
                                tapSleep(p.x + 30, p.y + 30, 0.3)
                                TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)

                        # 检查交换后的卡牌
                        if isSwipe and (轮次 == '第1轮' or 轮次 == '第2轮' or 轮次 == '第3轮' or 轮次 == '第5轮'):
                            Toast('选择交换后的卡牌')
                            print(swipeArr)
                            for p in swipeArr:
                                tapSleep(p['x'], p['y'], 0.3)
                                TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)

                        res, _ = TomatoOcrText(402, 1164, 445, 1184, '提示')
                        if not res:
                            break

                        # 兜底选取任意卡牌
                        reAll, tmpPoints = imageFindAll('派对大师-卡背', 0.9, 101, 222, 650, 1122)
                        if reAll:
                            Toast('选择未翻开卡牌')
                            for tmpPoint in tmpPoints:
                                tapSleep(tmpPoint["center_x"], tmpPoint["center_y"], 0.3)
                                re = TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)
                                if not re:
                                    break
        功能开关['fighting'] = 0

    # 其他签到活动（简单活动合集）
    def QiTaQianDao(self):
        if 功能开关["其他签到活动"] == 0:
            return

        # 西行记
        if 任务记录["西行记签到"] == 0:
            self.homePage()
            res = TomatoOcrFindRangeClick('西行记', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=1.5, match_mode='fuzzy')
            if res:
                Toast('西行记活动 - 任务开始')
                re = TomatoOcrTap(168, 470, 285, 505, '火眼金睛', sleep1=1.5)
                if re:
                    re = TomatoOcrText(271, 620, 410, 659, '蓝力士')
                    if re:
                        Toast('火眼金睛 - 蓝力士 - 任务开始')
                        tapSleep(85, 1202, 0.8)  # 返回
                        tapSleep(162, 1201, 1.3)  # 营地
                        tapSleep(345, 421, 3)  # 铁匠铺
                        tapSleep(172, 329, 0.8)  # 妖怪
                        tapSleep(348, 1188)  # 点击空白
                        tapSleep(348, 1188)  # 点击空白
                        tapSleep(348, 1188)  # 点击空白
                        tapSleep(348, 1188)  # 点击空白
                        tapSleep(348, 1188)  # 点击空白

                    re = TomatoOcrText(271, 620, 410, 659, '狐巡司')
                    if re:
                        Toast('火眼金睛 - 狐巡司 - 任务开始')
                        tapSleep(85, 1202, 0.8)  # 返回
                        tapSleep(634, 164, 0.8)  # 大地图
                        tapSleep(311, 39, 0.8)  # 点击空白
                        for l in range(10):
                            swipe(350, 277, 380, 609)  # 上划
                            sleep(0.5)
                            if l > 5:
                                swipe(108, 599, 505, 577)  # 左滑
                            else:
                                swipe(505, 577, 108, 599)  # 右滑
                            sleep(1)

                            find = FindColors.find(
                                "375,250,#F7F3EA|369,230,#F7F3EA|347,244,#836E55|363,239,#8F7D69|393,243,#F7F3EA|397,243,#F7F3EA",
                                rect=[11, 31, 701, 523], diff=0.93)
                            if find:
                                tapSleep(find.x - 50, find.y + 40)
                                任务记录["西行记签到"] = 1
                                Toast('火眼金睛 - 已找到任务奖励')
                                break
                    re = FindColors.find("304,474,#F55F42|305,478,#F15B41|308,476,#F15D40", rect=[115, 440, 617, 572],
                                         diff=0.93)  # 累积奖励
                    if re:
                        tapSleep(re.x - 20, re.y + 20)
            else:
                Toast('西行记活动 - 未找到活动入口')

        # 双旦联欢
        if 任务记录["双旦联欢签到"] == 0:
            self.homePage()
            res = TomatoOcrFindRangeClick('双旦', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=1.5, match_mode='fuzzy')
            if res:
                Toast('双旦联欢签到 - 任务开始')
                任务记录["双旦联欢签到"] = 1
                res = CompareColors.compare("323,470,#F15D40|325,468,#F36042|326,470,#F15E41")  # 匹配红点
                if res:
                    tapSleep(211, 486, 0.8)
                    res = TomatoOcrFindRangeClick('领取', x1=459, y1=528, x2=625, y2=1150, offsetX=30, offsetY=-20,
                                                  sleep1=0.5)
                    tapSleep(92, 1218)  # 返回
                    tapSleep(92, 1218)
                    tapSleep(92, 1218)
            else:
                任务记录["双旦联欢签到"] = 1

        # 忆战回环
        if 任务记录["忆战回环签到"] == 0:
            self.homePage()
            res = TomatoOcrFindRangeClick('忆战', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=1.5, match_mode='fuzzy')
            if res:
                Toast('忆战回环签到 - 任务开始')
                任务记录["忆战回环签到"] = 1
                res = CompareColors.compare("620,110,#F66042|620,115,#F05E41|620,118,#EF5435")  # 匹配红点
                if res:
                    tapSleep(593, 127, 3)  # 点击排行榜
                    tapSleep(574, 1051, 0.1)  # 点击奖励
                    tapSleep(570, 1062, 0.1)  # 点击奖励
                    tapSleep(558, 1063, 0.1)  # 点击奖励
                    tapSleep(356, 1038, 0.1)  # 点击奖励
                    tapSleep(356, 1065, 0.1)  # 点击奖励
                    tapSleep(352, 1062, 0.1)  # 点击奖励
                    tapSleep(195, 1038, 0.1)  # 点击奖励
                    tapSleep(191, 1063, 0.1)  # 点击奖励
                    tapSleep(181, 1059, 0.1)  # 点击奖励
                    tapSleep(92, 1218)  # 返回
                    tapSleep(92, 1218)
            else:
                任务记录["半周年庆典签到"] = 1

        # 半周年庆典签到
        if 任务记录["半周年庆典签到"] == 0:
            self.homePage()
            res = TomatoOcrFindRangeClick('周年', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=0.8, match_mode='fuzzy')
            if res:
                Toast('半周年庆典签到 - 任务开始')
                任务记录["半周年庆典签到"] = 1
                res = CompareColors.compare("592,505,#F55F42|595,505,#F45F42|595,509,#F15A41")  # 匹配红点
                if res:
                    TomatoOcrTap(456, 509, 565, 544, '庆典签到', sleep1=0.8)
                    res = TomatoOcrFindRangeClick('领取', x1=7, y1=921, x2=701, y2=995, offsetX=30, offsetY=-20,
                                                  sleep1=0.5)
                    tapSleep(92, 1218)  # 返回
                    tapSleep(92, 1218)
                    tapSleep(92, 1218)
            else:
                任务记录["半周年庆典签到"] = 1

        # 大家的麦芬
        if 任务记录["大家的麦芬"] == 0:
            self.homePage()
            res = TomatoOcrFindRangeClick('大家', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=0.5, match_mode='fuzzy')
            if res:
                Toast('大家的麦芬 - 任务开始')
                tapSleep(609, 1059, 0.8)  # 铸造按钮
                TomatoOcrTap(328, 751, 390, 781, '铸造', sleep1=0.6)
                tapSleep(345, 1208)  # 点击空白
                tapSleep(345, 1208)  # 点击空白
                res = FindColors.find("235,295,#F85949|231,293,#F46042|232,292,#F56043", rect=[80, 243, 641, 369],
                                      diff=0.85)
                if res:
                    tapSleep(res.x, res.y + 10)
                    tapSleep(345, 1208)  # 点击空白
                    tapSleep(345, 1208)  # 点击空白
                re = CompareColors.compare("691,803,#F25E41|691,798,#F96245|693,806,#FF5B49", diff=0.85)  # 里程碑
                if re:
                    tapSleep(669, 815)
                    res = TomatoOcrFindRangeClick('领取', x1=435, y1=235, x2=606, y2=958, offsetX=30, offsetY=-20,
                                                  sleep1=0.5)
                    TomatoOcrTap(94, 1188, 126, 1218, '回')
                TomatoOcrTap(94, 1188, 126, 1218, '回')
                任务记录["大家的麦芬"] = 1
            else:
                Toast('大家的麦芬 - 未找到入口')
                任务记录["大家的麦芬"] = 1

        # 盛大公演
        if 任务记录["盛大公演"] == 0:
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
            # 判断是否在营地页面
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if res:
                res = TomatoOcrFindRangeClick('公演', match_mode='fuzzy', x1=7, y1=797, x2=96, y2=1144, offsetX=30,
                                              offsetY=-20,
                                              sleep1=0.8)
                if res:
                    Toast('盛大公演 - 任务开始')
                    res = TomatoOcrTap(624, 895, 713, 921, "登录奖励", sleep1=0.5)
                    res = TomatoOcrFindRangeClick('可领取', x1=101, y1=389, x2=622, y2=1068, offsetX=30, offsetY=-20,
                                                  sleep1=0.5)
                    tapSleep(90, 1204)  # 返回
                    tapSleep(90, 1204)
                    任务记录["盛大公演"] = 1
                else:
                    Toast('盛大公演 - 未找到入口')
                    任务记录["盛大公演"] = 1

        # 逍遥大圣
        if 任务记录["逍遥大圣"] == 0:
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
            # 判断是否在营地页面
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if res:
                res = TomatoOcrFindRangeClick('大圣', match_mode='fuzzy', x1=7, y1=797, x2=96, y2=1144, offsetX=30,
                                              offsetY=-20,
                                              sleep1=0.8)
                if res:
                    Toast('逍遥大圣 - 任务开始')
                    res = TomatoOcrTap(624, 895, 713, 921, "登录奖励", sleep1=0.5)
                    res = TomatoOcrFindRangeClick('可领取', x1=101, y1=389, x2=622, y2=1068, offsetX=30, offsetY=-20,
                                                  sleep1=0.5)
                    tapSleep(90, 1204)  # 返回
                    tapSleep(90, 1204)
                    任务记录["逍遥大圣"] = 1
                else:
                    Toast('逍遥大圣 - 未找到入口')
                    任务记录["逍遥大圣"] = 1

    # 箱庭苗圃
    def XiangTingMiaoPu(self):
        if 功能开关["箱庭苗圃"] == 0:
            return
        # if 任务记录["箱庭苗圃-完成"] == 1:
        #     return
        if 任务记录["箱庭苗圃-倒计时"] > 0:
            diffTime = time.time() - 任务记录["箱庭苗圃-倒计时"]
            if diffTime < 20 * 60:
                Toast(f'日常 - 箱庭苗圃 - 倒计时{round((20 * 60 - diffTime) / 60, 2)}min')
                return
        Toast('日常 - 箱庭苗圃 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        # res = TomatoOcrFindRangeClick('箱庭苗圃', 0.9, 14, 98,1025,180,1051, offsetX=30, offsetY=-20)
        res1 = TomatoOcrTap(98, 1025, 180, 1051, '箱庭苗圃', offsetX=30, offsetY=-20)
        res2 = TomatoOcrTap(96, 939, 178, 962, '箱庭苗圃', offsetX=30, offsetY=-20)
        if not res1 and not res2:
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

        for i in range(4):
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
                name = 功能开关['作物1']
                Toast(f'种植{name}')
                res, x, y = imageFind('箱庭-' + name, 0.87, 78, 1002, 634, 1128)
                if not res:
                    Toast(f'未找到{name}，种植默认作物')
                    x, y = 129, 1046  # 默认前两个
                line1 = Path(0, 3000)
                # 移动初始点
                line1.moveTo(x, y)
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
                name = 功能开关['作物2']
                Toast(f'种植{name}')
                res, x, y = imageFind('箱庭-' + name, 0.9, 78, 1002, 634, 1128)
                if not res:
                    Toast(f'未找到{name}，种植默认作物')
                    x, y = 219, 1040  # 默认前两个
                line2 = Path(0, 5000)
                # 移动初始点
                line2.moveTo(x, y)
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

            # 判断当前土地状态，判断是否继续翻页
            res3 = TomatoOcrFindRangeClick('开放', 0.9, 14, 114, 482, 575, 1010, offsetY=-20, match_mode='fuzzy')
            if res3:
                break
            tapSleep(660, 689, 3)  # 翻下一页

        # 拜访
        for i in range(4):
            tapSleep(617, 1139, 2)  # 点击拜访
            res = TomatoOcrTap(246, 348, 287, 374, '旅团')
            if res:
                tapSleep(527, 455 + 120 * i, 2)  # 点击拜访
                available, _ = TomatoOcrText(643, 1062, 672, 1080, '0/1')
                if not available:
                    available, _ = TomatoOcrText(643, 1062, 672, 1080, '0/2')
                if not available:
                    available, _ = TomatoOcrText(643, 1062, 672, 1080, '0/3')
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
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrFindRangeClick('特惠', match_mode='fuzzy', x1=97, y1=544, x2=180, y2=1051, offsetX=40,
                                      offsetY=-40)  # 进入紧急委托
        if not res:
            res = imageFindClick('营地-限时特惠', 0.9, 0.9, 94, 529, 182, 1053)
            if not res:
                Toast('限时特惠 - 未找到活动入口')
        if res:
            Toast('限时特惠 - 领取')
            tapSleep(595, 153)  # 点击特惠宝箱
            tapSleep(595, 153)  # 点击特惠宝箱
            tapSleep(341, 1136)  # 点击空白处
            tapSleep(86, 1202)  # 点击返回
            任务记录["限时特惠-完成"] = 1

        res = imageFindClick("营地-限时礼包", 0.9, 0.9, 94, 880, 187, 1057)
        if res:
            Toast('限时特惠 - 限时礼包')
            tapSleep(595, 153)  # 点击特惠宝箱
            tapSleep(595, 153)  # 点击特惠宝箱
            tapSleep(341, 1136)  # 点击空白处
            tapSleep(86, 1202)  # 点击返回
            任务记录["限时特惠-完成"] = 1

        # 新人特惠
        res = TomatoOcrFindRangeClick('新人特惠', x1=6, y1=780, x2=97, y2=1151, offsetX=10, offsetY=-20)
        if res:
            Toast('限时特惠 - 新人特惠')
            tapSleep(590, 148)
            tapSleep(360, 1212)
            tapSleep(360, 1212)
            tapSleep(360, 1212)
            任务记录["限时特惠-完成"] = 1

        任务记录["限时特惠-完成"] = 1

    # 登录好礼
    def dengLuHaoLi(self):
        if 功能开关["登录好礼"] == 0:
            return
        if 任务记录["登录好礼-完成"] == 1:
            return
        Toast('日常 - 登录好礼 - 开始')

        # 返回首页
        self.homePage()

        res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
        # 判断是否在营地页面
        hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        isFind, x, y = imageFind('登录好礼')
        if not isFind:
            # -- 返回活动最后一屏
            swipe(680, 804, 680, 251)
            sleep(2)
            swipe(680, 804, 680, 251)
            sleep(2)
            swipe(680, 804, 680, 251)
            sleep(2)
            swipe(680, 804, 680, 251)
            sleep(2)
            swipe(680, 804, 680, 251)
            sleep(2)

            for i in range(1, 5):
                # 上翻第二屏，继续识别
                swipe(680, 451, 680, 804)
                sleep(3)
                isFind, x, y = imageFind('登录好礼')
                if isFind:
                    break
        if isFind:
            tapSleep(x, y, 2)
            for i in range(3):
                TomatoOcrFindRangeClick('领取', x1=102, y1=935, x2=634, y2=994, sleep1=1)
                tapSleep(136, 281, 1)
            任务记录["登录好礼-完成"] = 1
            tapSleep(381, 1154)  # 点击空白处关闭
        return

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

        re = CompareColors.compare("547,1077,#F35E41|551,1079,#EF5C40|551,1076,#F46042")
        if not re:
            Toast('宝藏湖 - 能量用尽')
            return
        res = TomatoOcrTap(412, 1076, 511, 1101, "大容量充磁")
        sleep(8)  # 等待动画
        tapSleep(360, 1040)  # 点击空白处
        tapSleep(360, 1040)  # 点击空白处

        tapSleep(75, 325)  # 领取回收物进度奖励
        tapSleep(76, 335)  # 领取回收物进度奖励
        tapSleep(360, 1040)  # 点击空白处
        tapSleep(360, 1040)  # 点击空白处

        re = CompareColors.compare("682,1180,#F56043|683,1180,#F56143|682,1183,#F35E41")
        if not re:
            return
        if re:
            # res = TomatoOcrTap(554, 1239, 636, 1265, "伊尼兰特")
            tapSleep(660, 1227, 0.8)  # 伊尼兰特
            res = TomatoOcrTap(321, 1073, 402, 1096, "高压充磁", 10, 10)
            sleep(8)  # 等待动画
            tapSleep(360, 1040)  # 点击空白处
            tapSleep(360, 1040)  # 点击空白处

        任务记录["日常-宝藏湖-完成"] = 1

    # BBQ派对
    def BBQParty(self):
        if 功能开关["BBQ派对"] == 0:
            return

        if 任务记录["BBQ派对"] == 1:
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
                break
            res = TomatoOcrTap(433, 1091, 533, 1122, "连续烧烤")
            sleep(5)
        tapSleep(271, 282)
        tapSleep(271, 282)
        tapSleep(347, 277)
        tapSleep(347, 277)
        tapSleep(424, 271)
        tapSleep(424, 271)
        tapSleep(502, 276)
        tapSleep(502, 276)
        tapSleep(571, 274)
        tapSleep(571, 274)
        tapSleep(360, 1220)  # 点击空白处
        任务记录["BBQ派对"] = 1
        res = TomatoOcrTap(96, 1200, 129, 1232, "回", 10, 10)  # 返回

    # 紧急委托
    def jinJiWeiTuo(self):
        if 功能开关["紧急委托"] == 0:
            return

        if 任务记录["紧急委托-完成"] == 1:
            return

        Toast('日常 - 紧急委托 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            Toast('进入营地失败')
            return

        res = TomatoOcrFindRangeClick("紧急委托", x1=97, y1=544, x2=180, y2=1051, offsetX=40, offsetY=-40,
                                      sleep1=1.5)  # 进入紧急委托
        if not res:
            res = TomatoOcrFindRangeClick("瑶池盛会", x1=97, y1=544, x2=180, y2=1051, offsetX=40, offsetY=-40,
                                          sleep1=1.5)  # 进入紧急委托
            if not res:
                Toast('紧急委托 - 未找到活动入口')
                return

        # 领取每日礼包
        tapSleep(595, 162)  # 点击塔莎特惠
        re = TomatoOcrTap(145, 643, 200, 675, '免费')
        if re:
            tapSleep(358, 744)  # 点击购买

        tapSleep(352, 1169)  # 点击空白
        tapSleep(352, 1169)  # 点击空白

        # 选择追踪目标
        sleep(0.5)
        for i in range(3):
            point = FindColors.find("238,580,#FCF8EE|243,580,#FCF8EE|241,585,#FCF8EE|244,585,#FCF8EE",
                                    rect=[75, 511, 366, 610])
            if point:
                tapSleep(point.x, point.y)
                tapSleep(353, 722)  # 点击宝藏
                tapSleep(443, 724)  # 点击宝藏
                tapSleep(527, 721)  # 点击宝藏
                tapSleep(189, 801)  # 点击宝藏
                TomatoOcrTap(325, 928, 391, 951, '确认')
                tapSleep(352, 1169)  # 点击空白

        # 前往下一层
        sleep(0.5)
        nextLevel = False
        for l in range(3):
            re1 = imageFindClick('塔莎委托-下一层', confidence1=0.8, x1=78, y1=514, x2=645, y2=1090)
            re2 = imageFindClick('塔莎委托-下一层2', confidence1=0.8, x1=78, y1=514, x2=645, y2=1090)
            re3 = imageFindClick('塔莎委托-下一层3', confidence1=0.8, x1=78, y1=514, x2=645, y2=1090)
            re4 = FindColors.find("440,1024,#94665A|440,1018,#9A6D5B|442,1021,#95675A", rect=[83, 514, 634, 1084],
                                  diff=0.95)  # 匹配瑶池盛会下一层图标
            if re4:
                tapSleep(re4.x, re4.y)
            if re1 or re2 or re3 or re4:
                nextLevel = True
                break

        if nextLevel:
            sleep(0.5)
            TomatoOcrTap(452, 744, 510, 771, '确定')
            sleep(3)
            tapSleep(352, 1169)  # 点击空白

            sleep(0.5)

            # 选择追踪目标
            for i in range(3):
                point = FindColors.find("238,580,#FCF8EE|243,580,#FCF8EE|241,585,#FCF8EE|244,585,#FCF8EE",
                                        rect=[75, 511, 366, 610])
                if point:
                    tapSleep(point.x, point.y)
                    tapSleep(353, 722)  # 点击宝藏
                    tapSleep(443, 724)  # 点击宝藏
                    tapSleep(527, 721)  # 点击宝藏
                    tapSleep(189, 801)  # 点击宝藏
                    TomatoOcrTap(325, 928, 391, 951, '确认')
                    tapSleep(352, 1169)  # 点击空白

        # 准备剪彩
        res = TomatoOcrTap(457, 1141, 576, 1175, "准备剪彩", 10, 10)
        if res:
            res = TomatoOcrTap(457, 1141, 576, 1175, "准备剪彩", 10, 10)
            res = TomatoOcrTap(457, 1141, 576, 1175, "准备剪彩", 10, 10)
            Toast('准备剪彩')
            sleep(5)

        # 准备剪彩（瑶池盛会）
        res = TomatoOcrTap(497, 1133, 552, 1167, "吃桃", 10, 10)
        if res:
            res = TomatoOcrTap(497, 1133, 552, 1167, "吃桃", 10, 10)
            res = TomatoOcrTap(497, 1133, 552, 1167, "吃桃", 10, 10)
            Toast('准备吃桃')
            sleep(5)

        # 自动剪彩
        res = TomatoOcrTap(457, 1142, 574, 1175, "自动剪彩", 10, 10)
        if res:
            Toast('开始剪彩')
            sleep(10)

        # 自动剪彩（瑶池盛会）
        res = TomatoOcrTap(457, 1142, 574, 1175, "自动吃桃", 10, 10)
        if res:
            Toast('自动吃桃')
            sleep(10)

        tapSleep(330, 1166)  # 点击空白处
        tapSleep(330, 1166)  # 点击空白处

        任务记录["紧急委托-完成"] = 1

    # 火力全开
    def huoLiQuanKai(self):
        if 功能开关["火力全开"] == 0:
            return

        if 任务记录["火力全开-完成"] == 1:
            return

        Toast('日常 - 火力全开 - 开始')

        self.homePage()
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrFindRangeClick(x1=97, y1=544, x2=180, y2=1051, offsetX=40,
                                      offsetY=-40, keywords=[{'keyword': '火力全开', 'match_mode': 'exact'},
                                                             {'keyword': '火力', 'match_mode': 'exact'},
                                                             {'keyword': '火', 'match_mode': 'exact'},
                                                             {'keyword': '全开', 'match_mode': 'exact'}])  # 进入火力全开
        if not res:
            Toast('火力全开 - 未找到活动入口')
            return

        # 领取累计奖励
        for k in range(3):
            re = FindColors.find("270,926,#F45F42|268,924,#F46043|270,929,#EF5C3F", rect=[88, 901, 625, 1027])
            if re:
                tapSleep(re.x - 5, re.y + 5)
                tapSleep(344, 1204)  # 点击空白处

            # 等待转盘动画完成
            Toast('等待转盘动画')
            tapSleep(479, 1096)  # 点击空白处
            sleep(10)
            tapSleep(344, 1204)  # 点击空白处
            tapSleep(344, 1204)  # 点击空白处
            TomatoOcrTap(92, 1186, 127, 1218, '回')

            # 领取累计奖励
            re = FindColors.find("270,926,#F45F42|268,924,#F46043|270,929,#EF5C3F", rect=[88, 901, 625, 1027])
            if re:
                tapSleep(re.x - 5, re.y + 5)
                tapSleep(344, 1204)  # 点击空白处

        任务记录["火力全开-完成"] = 1

    # 活动 - 摸鱼
    def huoDongMoYu(self):
        if 功能开关["摸鱼时间到"] == 0:
            return

        if 任务记录["日常-摸鱼时间到-完成"] == 1:
            return

        Toast('日常 - 摸鱼时间到 - 开始')

        needCount = safe_int(功能开关["摸鱼重复次数"])
        onlyDaily = False
        if needCount == '':
            onlyDaily = True
            # 默认摸鱼5次，领取每日奖励
            needCount = 5

        for i in range(needCount):
            # res = TomatoOcrTap(566, 379, 609, 404, "摸鱼")
            res1 = TomatoOcrTap(566, 379, 609, 404, "摸鱼", 15, -20)
            res2 = TomatoOcrTap(551, 462, 622, 488, "摸鱼", 15, -20)
            res3 = TomatoOcrTap(553, 546, 620, 570, "摸鱼", 15, -20)
            res4, _ = TomatoOcrText(325, 1095, 427, 1128, "开始匹配")
            if not res1 and not res2 and not res3 and not res4:
                self.homePage()
                res1 = TomatoOcrTap(566, 379, 609, 404, "摸鱼", 15, -20)
                res2 = TomatoOcrTap(551, 462, 622, 488, "摸鱼", 15, -20)
                res3 = TomatoOcrTap(553, 546, 620, 570, "摸鱼", 15, -20)
                if not res1 and not res2 and not res3:
                    return

            # 检查是否已完成每日
            if onlyDaily or 功能开关["摸鱼重复次数"] == '':
                re, count = TomatoOcrText(126, 1011, 198, 1035, '摸鱼条数')  # 最后一格奖励
                count = count.replace('条', '')
                count = safe_int_v2(count)
                if count > 15:
                    Toast('摸鱼时间到 - 已完成每日奖励')
                    任务记录["日常-摸鱼时间到-完成"] = 1
                    tapSleep(562, 940, 0.8)  # 点击最后一个奖励
                    tapSleep(592, 1046)  # 点击空白
                    tapSleep(592, 1046)  # 点击空白
                    TomatoOcrTap(318, 738, 385, 782, '喂鱼', sleep1=1.5)
                    for k in range(3):
                        point = FindColors.find("278,236,#F56142|280,236,#F56042|280,242,#F1593E|278,241,#F15B41",
                                                rect=[208, 227, 611, 317])
                        if point:
                            tapSleep(point.x - 20, point.y + 30, 1)
                            tapSleep(102, 1074)
                    return

            res1 = TomatoOcrTap(325, 1095, 427, 1128, "开始匹配")
            res2 = TomatoOcrTap(451, 603, 505, 635, "准备")
            if not res1 and not res2:
                self.quitTeam()

            attempts = 0  # 初始化尝试次数
            maxAttempts = 6  # 设置最大尝试次数

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
        for j in range(2):
            if j == 1:
                Toast('日常 - 骑兽乐园 - 检查是否完成')
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
                    tapSleep(200, 545, 3)  # 芙芙小铺
                    isYingDi = True
                    break
            if not isYingDi:
                return

            res2 = TomatoOcrTap(510, 1134, 611, 1164, "骑兽乐园")
            if res2:
                point = FindColors.find("180,314,#767676|168,342,#A1A1A1|183,331,#A6A6A6|197,326,#C6C6C6",
                                        rect=[124, 263, 252, 448], diff=0.95)  # 已领取门票，灰色状态
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
                    for i in range(5):
                        res = TomatoOcrTap(570, 261, 645, 285, "兑换门票", 10, 10, sleep1=0.5)
                        # res, _ = TomatoOcrText(320, 372, 401, 399, "兑换门票")
                        if not res:
                            TomatoOcrFindRangeClick("兑换门票", x1=554, y1=208, x2=661, y2=296, sleep1=0.7)

                        buyCount = ""
                        for p in range(5):
                            # res, buyCount = TomatoOcrText(379, 930, 394, 947, "每日限购次数")  # 1/9
                            res, buyCount = TomatoOcrText(276, 531, 434, 571, "每日限购次数")  # 1/9
                            buyCount = (buyCount.replace("每日限购", "").replace("/9", "").
                                        replace("(", "").replace(")", "").replace("（", "").
                                        replace("）", "").replace("/", "").replace("9", "").replace(" ", ""))
                            buyCount = safe_int(buyCount)
                            Toast("已购次数：" + str(buyCount))
                            if buyCount != "":
                                break
                        if buyCount == "":
                            continue
                        if buyCount != 0 and buyCount >= needCount:
                            if buyCount >= needCount:
                                任务记录["日常-骑兽乐园-完成"] = 1
                            TomatoOcrTap(93, 1185, 127, 1220, "回", 10, 10, sleep1=0.5)  # 返回芙
                            break
                        re, ct = TomatoOcrText(336, 385, 396, 416, '准备购买次数')
                        Toast(f'准备购买{ct}次')
                        ct = safe_int(ct)
                        if ct != '' and ct < needCount:
                            tapSleep(420, 407)  # 点击+1
                        re = TomatoOcrTap(334, 462, 383, 487, "购买", 10, 10, sleep1=0.9)
                        if not re:
                            re = TomatoOcrFindRangeClick('购买', x1=123, y1=181, x2=623, y2=519, sleep1=0.9)
                        if re:
                            tapSleep(550, 1080, 0.5)  # 点击空白处关闭
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
                    sleep(1.5)
                    TomatoOcrTap(597, 28, 642, 53, "跳过")  # 跳过动画
                    sleep(1.5)
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

        for j in range(2):
            if j == 1:
                Toast('日常 - 招式创造 - 检查是否完成')
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
                    # else:
                    #     tapSleep(503,260)
                    #     tapSleep(246,219, 3)
                    #     tapSleep(185, 1024)  # 点击空白处关闭
                    #     任务记录["日常-招式创造-完成"] = 1

            # 兑换卢恩
            needCount = safe_int(功能开关["钻石兑换卢恩次数"])
            if needCount == '':
                needCount = 0
            if needCount > 0:
                for i in range(1, 5):
                    res = TomatoOcrTap(571, 261, 645, 287, "兑换卢恩", 10, 10, sleep1=0.8)
                    buyCount = ""
                    for p in range(1, 5):
                        # res, buyCount = TomatoOcrText(375, 944, 387, 960, "已购买次数")  # 1/9
                        res, buyCount = TomatoOcrText(276, 531, 434, 571, "已购买次数")  # 1/9
                        buyCount = (buyCount.replace("每日限购", "").replace("/15", "").replace("（", "").
                                    replace("）", "").replace("(", "").replace(")", "").
                                    replace("/", "").replace("15", "").replace(" ", ""))
                        buyCount = safe_int(buyCount)
                        Toast("已购次数：" + str(buyCount))
                        if buyCount != "":
                            break
                    if buyCount != 0 and (buyCount == "" or buyCount >= needCount):
                        res = TomatoOcrTap(93, 1185, 127, 1220, "回", 10, 10, sleep1=0.5)  # 返回芙芙小铺，继续
                        任务记录["日常-招式创造-完成"] = 1
                        break
                    re, ct = TomatoOcrText(336, 385, 396, 416, '准备购买次数')
                    Toast(f'准备购买{ct}次')
                    ct = safe_int(ct)
                    if ct != '' and ct < needCount:
                        tapSleep(420, 407)  # 点击+1
                    res = TomatoOcrTap(334, 462, 383, 487, "购买", 10, 10, sleep1=0.9)
                    if not res:
                        res = TomatoOcrFindRangeClick('购买', x1=123, y1=181, x2=623, y2=519, sleep1=0.9)
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
                res, _ = TomatoOcrText(317, 1054, 401, 1082, "讲述故事")
                if not res:
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
        # wait1, _ = TomatoOcrText(396, 622, 468, 650, "开启挑战")  # 队伍已满员，准备开启挑战
        # wait2 = False
        # if not wait1:
        #     wait2, _ = TomatoOcrText(240, 610, 344, 653, "队伍已满员")  # 队伍已满员，准备开启挑战
        # if wait1 or wait2:
        res5 = TomatoOcrTap(453, 727, 506, 759, "确定", 10, 10)  # 队伍已满员，准备开启挑战 - 确定

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

        Toast("摸鱼队伍发言")

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

    def checkGameStatus(self):
        try:
            if 功能开关['技能进入战斗后启动'] == 1 or 功能开关['AI进入战斗后启动'] == 1 or 功能开关[
                '暴走进入战斗后启动']:
                return

            # re1 = CompareColors.compare(
            #     "657,324,#F3EDDD|659,324,#F3EDDD|664,331,#F3EDDD|676,329,#F3EDDD|681,337,#F3EDDD|687,334,#F3EDDD")  # 战斗内队伍图标
            # if re1:
            #     Toast('战斗中-不检测游戏是否卡死')
            #     return

            diffTime = time.time() - 任务记录["首页卡死检测-倒计时"]
            if diffTime < 4 * 60:
                print(f'游戏卡死检测 - 倒计时{round((4 * 60 - diffTime) / 60, 2)}min')
                return True

            # 战斗中6分钟，强制检查是否卡死
            if 功能开关["fighting"] == 1 and diffTime < 6 * 60:
                return

            # 匹配行李图标亮着，新号为灰色，不处理
            re = CompareColors.compare("287,1224,#AC8B62|285,1218,#AC8B62|285,1199,#9F7C55|287,1210,#9F7C55")
            if not re:
                return True

            # 检测游戏是否卡死
            Toast('检测游戏是否卡死')
            任务记录["首页卡死检测-倒计时"] = time.time()

            # 避免与自动入队冲突
            功能开关["fighting"] = 1

            # 首页卡死检测（通过点击行李判断能否跳转成功）
            failCount = 0
            for i in range(10):
                return3 = TomatoOcrTap(93, 1186, 126, 1220, '回', 10, 10)  # 简单尝试返回首页
                res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击战斗失败确认
                TomatoOcrFindRangeClick('准备')  # 避免点击开始瞬间队友离队，错误点击了开始匹配，兜底准备按钮
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.7)
                if res:
                    re = CompareColors.compare(
                        "565,486,#6584B9|570,486,#6584B9|576,484,#6584B9|582,484,#6584B9|585,487,#6583B8")  # 匹配衣柜按钮
                    if re:
                        # 切换页面成功，返回首页
                        tapSleep(356, 1205)
                        tapSleep(356, 1205)
                        break
                    if not re:
                        system.open(f"{功能开关['游戏包名']}")
                        self.closeLiaoTian()
                        sleep(5)
                        Toast(f'游戏卡死，等待{i * 5}/50s')
                        res = TomatoOcrTap(233, 1205, 281, 1234, "行李")
                        res = TomatoOcrTap(233, 1205, 281, 1234, "行李")
                        if res:
                            re1 = CompareColors.compare(
                                "598,511,#6584B9|598,497,#6584B9|598,506,#6584B9|598,512,#6584B9|600,503,#6283B8")  # 匹配衣柜按钮
                            re2 = CompareColors.compare(
                                "315,1104,#FBF7EC|320,1114,#F9F4E7|331,1114,#D0C8BA|331,1114,#D0C8BA|341,1114,#F6F1E4")
                            if re1 or re2:
                                # 切换页面成功，返回首页
                                tapSleep(356, 1205)
                                tapSleep(356, 1205)
                                break
                            if not re:
                                failCount = failCount + 1
            if failCount > 4:
                # 切换页面失败，重启游戏
                Toast('游戏进程卡死，尝试重启游戏')
                # 结束应用
                # r = system.shell("am kill com.xd.cfbmf", L())
                r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
                system.open(f"{功能开关['游戏包名']}")
                功能开关["fighting"] = 0
                return False
            功能开关["fighting"] = 0
            return True
        except Exception as e:
            功能开关["fighting"] = 0
            # 处理异常
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 输出异常信息和行号
            file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
            error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
            # 显示对话框
            print(error_message)

    def closeLiaoTian(self):
        point = FindColors.find(
            "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
            rect=[61, 34, 322, 623], diff=0.93)
        if point:
            Toast('收起喊话窗口')
            tapSleep(point.x, point.y)

        point = CompareColors.compare(
            "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
