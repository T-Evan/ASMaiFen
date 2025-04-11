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
            if tryTimes < 2 and 功能开关["fighting"] == 1:
                for k in range(100):
                    if 功能开关["fighting"] == 0:
                        break
                    if k > 80:
                        Toast(f'返回首页-等待任务{k * 2}/200')
                    sleep(2)
                continue

            if tryTimes < 50:
                res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                if "等级" in teamName1:
                    for k in range(3):
                        res, teamName1 = TomatoOcrText(8, 148, 51, 163, "队友名称")
                        if "等级" in teamName1:
                            # Toast(f'返回首页-等待战斗{k * 2 * tryTimes}/60')
                            sleep(2)
                        else:
                            break
                    continue

            if tryTimes > 3:
                self.closeLiaoTian()

            if tryTimes > 5:
                system.open(f"{功能开关['游戏包名']}")
                # 暂不处理战败页启动，提高执行效率
                # 判断战败页面
                if 功能开关["fighting"] == 0:
                    Toast(f'日常-返回首页-退出组队')
                    # self.shilianTask.allQuit()
                    self.shilianTask.quitTeamFighting()
                # self.quitTeam()

            # resConnErr, _ = TomatoOcrText(292, 691, 427, 722, "尝试重新连接")
            # if resConnErr:
            #     Toast('网络断开，尝试重启游戏')
            #     # 结束应用
            #     r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
            #     # 重启游戏
            #     return self.startupTask.start_app()

            if tryTimes > 10:
                login1, _ = TomatoOcrText(287, 1019, 339, 1049, "开始")  # 开始冒险之旅
                if login1:
                    return self.startupTask.start_app()

            if tryTimes > 18:
                Toast(f'尝试返回游戏,{tryTimes}/20')
                system.open(f"{功能开关['游戏包名']}")

            if tryTimes > 20:
                res1, _ = TomatoOcrText(311, 588, 408, 637, "异地登录")
                if res1 and 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
                    return

                status = self.checkGameStatus(needForceCheck=True)
                if not status:
                    Toast('尝试重启游戏')
                    # 结束应用
                    # r = system.shell("am kill com.xd.cfbmf", L())
                    r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
                    # 重启游戏
                    return self.startupTask.start_app()
            if tryTimes > 23:
                return

            # 判断是否已在首页
            # 判断底部冒险图标
            res2 = False
            # res2 = FindColors.find(
            #     "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
            #     rect=[301, 1130, 421, 1273])
            shou_ye1 = False
            shou_ye2 = False
            if not res2:
                shou_ye1, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                if not shou_ye1:
                    shou_ye2, _ = TomatoOcrText(545, 381, 628, 404, "新手试炼")
                    if not shou_ye2:
                        shou_ye2, _ = TomatoOcrText(627, 381, 710, 403, "新手试炼")
            if not shou_ye1 and not shou_ye2:
                # 点击首页-冒险
                re = TomatoOcrTap(330, 1201, 389, 1238, '冒险', sleep1=0.2)
            if res2 or shou_ye1 or shou_ye2:
                功能开关["needHome"] = 0
                Toast('日常 - 已返回首页')
                # sleep(0.5)
                if 功能开关["fighting"] == 0 and needQuitTeam:
                    quitTeamRe = self.quitTeam()

                status = self.checkGameStatus()
                if not status:
                    # 重启游戏
                    return self.startupTask.start_app()
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
        # 兑换码领取
        self.duihuanma()
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
        # 兜底切回自动施法
        res = TomatoOcrTap(645, 882, 690, 902, "手动", 10, -10)
        if 任务记录["日常-释放1次战术技能-完成"] == 1:
            return

        if not 功能开关['释放1次战术技能']:
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
            '世界喊话4'] == "" and contentAI == "" and 功能开关['世界AI发言'] == 0:
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

        # 关闭喊话窗口
        self.closeLiaoTian()

        # AI回复世界频道发言
        if 功能开关['世界AI发言'] == 1 and contentAI == "":
            # 检查公屏发言关键词
            player_messages = shijieShoutText()
            for player, messages in player_messages.items():
                team_texts = [
                    msg.replace('元旦快乐~', '').replace('新年快乐~', '').replace('早安~', '').replace('~早安~',
                                                                                                       '').replace(
                        '~早安', '')
                    .replace('晚安~', '').replace('~晚安~', '').replace('~晚安', '').replace('午安~', '').replace(
                        '~午安~', '').replace('~午安', '').replace('~生日', '').replace('~生日~', '').replace('生日~',
                                                                                                              '') for
                    msg in messages
                    if "回环" not in msg]
                if player == '默认':
                    player = ''
                if '旅团' in player:
                    continue
                colors = generate_random_color()
                # zanList3 = ['狐巡司', '第一只']
                # contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                # if contains_zan:
                #     content = [f"<color={colors}>{player}~点开主线大地图，滑动上方找到藏匿妖怪喔~</COLOR>"]
                #     return self.shijieShout(random.choice(content))
                # zanList3 = ['火眼金睛', '找妖怪', '在哪']
                # contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                # if contains_zan:
                #     content = [f"1.大地图 2.铁匠铺 3.秘境 4.绝境 5.天赋页 6.衣柜 7.结伴 8.英雄之路"]
                #     return self.shijieShout(random.choice(content))
                # zanList3 = ['元旦快乐', '新年快乐']
                # contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                # if contains_zan:
                #     content = [f"<color={colors}>{player}~元旦快乐~</COLOR>",
                #                f"<color={colors}>{player}~新年快乐~</COLOR>", ]
                #     return self.shijieShout(random.choice(content))
                blackContent = ['其他区也收', '不想玩的', '茁', '全区收', '收耗']
                contains_zan = any(any(zan in text for zan in blackContent) for text in team_texts)
                if contains_zan:
                    res, x, y = TomatoOcrFindRange(player, x1=6, y1=781, x2=295, y2=1098, match_mode='fuzzy')
                    if res:
                        tapSleep(30, y + 30, 0.8)
                        re = TomatoOcrText(113, 819, 312, 858, player)
                        if re:
                            tapSleep(585, 1006, 0.6)
                            re = TomatoOcrTap(326, 595, 390, 625, '举报')
                            if re:
                                tapSleep(372, 531)  # 选择原因
                                tapSleep(480, 828)  # 确认举报
                                tapSleep(71, 1223)  # 返回首页
                                tapSleep(71, 1223)
                                tapSleep(71, 1223)
                                任务记录["世界喊话AI-倒计时"] = 0
                                return self.shijieShout(f"<color={colors}>已举报，{player}，请文明发言</COLOR>")

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
                zanList3 = ['生日']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    return self.shijieShout(f"<color={colors}>{player}~生日快乐~</COLOR>")
                zhanLi = int(safe_int_v2(任务记录["玩家战力"]) / 10000)
                职业映射 = {
                    '战士': '战',
                    '服事': '奶',
                    '刺客': '刺',
                    '法师': '法',
                    '游侠': '弓'
                }
                zhiye = 职业映射.get(任务记录["玩家-当前职业"], '')
                self.startupTask.zhiYeZhanLi()
                extraContent = f'{zhanLi}w{zhiye}'
                zanList3 = ['来奶', '来个奶', '有奶', '找个奶', '差个奶', '差奶', '缺奶', '缺个奶']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    if zhiye == '奶':
                        content = [f"<color={colors}>{player}~来了~{extraContent}</COLOR>",
                                   f"<color={colors}>{player}~来啦~{extraContent}</COLOR>"]
                        return self.shijieShout(random.choice(content))
                    else:
                        return
                zanList3 = ['来t', '来T', '来个t', '来个T', '挂个t', '挂个T', '有t', '有T', '找个t', '找个T', '差个t',
                            '差t', '缺t', '缺T', '缺个t', '来人', '匹配不到人']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    if zhiye == '战':
                        content = [f"<color={colors}>{player}~来了~{extraContent}</COLOR>",
                                   f"<color={colors}>{player}~来啦~{extraContent}</COLOR>"]
                        return self.shijieShout(random.choice(content))
                    else:
                        return
                zanList3 = ['来输出', '来个输出', '有输出', '找个输出', '差个输出', '差输出', '缺输出', '缺个输出']
                contains_zan = any(any(zan in text for zan in zanList3) for text in team_texts)
                if contains_zan:
                    if zhiye == '刺' or zhiye == '法' or zhiye == '弓':
                        content = [f"<color={colors}>{player}~来了~{extraContent}</COLOR>",
                                   f"<color={colors}>{player}~来啦~{extraContent}</COLOR>"]
                        return self.shijieShout(random.choice(content))
                    else:
                        return
                zanList = ['来个ai', '来个AI', '召唤ai', '召唤AI', 'ai打工', '打工ai']
                contains_zan = any(any(zan in text for zan in zanList) for text in team_texts)
                if contains_zan:
                    content = [f"<color={colors}>{player}~来了~(*^▽^*)~</COLOR>",
                               f"<color={colors}>{player}~在呢~辛苦啦~(*^▽^*)~</COLOR>"]
                    return self.shijieShout(random.choice(content))
                zanList3 = ['在哪里', '来一个', '来人', '求个', '来个', '来打工', '来黑工', '来打工', '求大佬']
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
                zanList = ['影子', '求带', '带个', '带带', '差个', '有大哥', '求个']
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

        # 避免与自动入队识别冲突
        res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
        if res6:
            Toast("世界喊话 - 已进入房间 - 等待5s")
            sleep(0.5)
            return 1
        # for p in range(5):
        #     if 功能开关["fighting"] == 1:
        #         Toast("世界喊话 - 其他任务执行中 - 等待5s")
        #         sleep(0.5)
        #         continue
        #     if 功能开关["fighting"] == 0:
        #         break
        #
        #     Toast("世界喊话 - 其他任务执行中 - 返回")
        #     return

        Toast("世界喊话 - 开始")

        need_dur_minute = safe_int(
            功能开关.get("世界喊话间隔", 0).replace("分钟", "").replace("分", "").replace("秒", "").replace("s",
                                                                                                            ""))  # 分钟
        if need_dur_minute == '':
            need_dur_minute = 1  # 默认1分钟
        if contentAI == "" and need_dur_minute > 0 and 任务记录["世界喊话-倒计时"] > 0:
            diffTime = time.time() - 任务记录["世界喊话-倒计时"]
            if diffTime < need_dur_minute * 60:
                Toast(f'日常 - 世界喊话 - 倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                return
        if contentAI != "" and 任务记录["世界喊话AI-倒计时"] > 0:
            diffTime = time.time() - 任务记录["世界喊话AI-倒计时"]
            dur_time = random.randint(60, 80)
            if diffTime < dur_time:
                Toast(f'日常 - 世界AI喊话 - 倒计时{round((dur_time - diffTime) / dur_time, 2)}min')
                return

        if not contentArr:
            return

        self.homePage()

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
                sleep(0.3)
                # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                action.input(content)
                tapSleep(360, 104, 0.2)  # 点击空白处确认输入
                shuru = TomatoOcrTap(78, 1156, 157, 1191, '点击输入')
                if shuru:
                    action.input(content)
                    tapSleep(360, 104, 0.5)  # 点击空白处确认输入
                isFaSong = False
                for k in range(4):
                    res = TomatoOcrTap(555, 1156, 603, 1188, "发送", 10, 10)
                    if not res and isFaSong:
                        break
                    isFaSong = True
                    sleep(0.3)
                if contentAI == "":
                    任务记录["世界喊话-倒计时"] = time.time()
                if contentAI != "":
                    任务记录["世界喊话AI-倒计时"] = time.time()
                # tapSleep(472, 771, 0.5)

        if 功能开关['自动切换喊话频道'] == 1 and contentAI == "":
            for i in range(3):
                # 避免与自动入队识别冲突
                if 功能开关["fighting"] == 1:
                    return

                # 关闭喊话窗口
                for j in range(3):
                    point = FindColors.find(
                        "95,88,#6483B8|104,87,#F6EFDC|109,88,#F0EBDC|112,91,#6582B8|112,94,#F9ECE0|106,100,#F4EEDE",
                        rect=[61, 34, 322, 623], diff=0.95)
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
        for i in range(2):
            point = FindColors.find(
                "107,85,#94A8C4|104,97,#8EA2C2|105,96,#6485B8|115,93,#F3EDDF|121,96,#6584B9|105,107,#6584B9",
                rect=[11, 26, 364, 489])
            if point:
                Toast('收起喊话窗口')
                tapSleep(point.x, point.y)

            point = CompareColors.compare(
                "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
            if point:
                Toast('收起喊话窗口')
                tapSleep(107, 93)
        # 功能开关["fighting"] = 0
        return 0

    def dailyTaskEnd(self):
        # 摸鱼时间到
        self.huoDongMoYu()
        # 派对大师
        self.PaiDuiDaShi()
        # 斗歌会
        if 功能开关['斗歌会'] == 1 and 功能开关['斗歌会自动接收邀请'] == 0:
            self.DouGeHui()
        # 箱庭苗圃
        self.XiangTingMiaoPu()
        # 其他签到
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
        if not res:
            res = TomatoOcrTap(627, 381, 710, 403, "新手试炼", sleep1=1)
        if res:
            Toast("日常 - 新手试炼领取 - 开始")
            # 识别黄色领取按钮
            for k in range(5):
                re, x, y = imageFind('手册-领取')
                if re:
                    tapSleep(x, y, 2)
                    tapSleep(356, 1213)  # 点击空白处关闭
                    tapSleep(356, 1213)  # 点击空白处关闭（再次点击，避免成就升级页）

            tapSleep(94, 1205, 1)  # 返回首页

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
    def newMap(self, forceCheck=False):
        if 功能开关["自动挑战首领"] == 1 and 功能开关["fighting"] == 0:
            Toast("日常 - 挑战首领 - 开始")
            self.homePage()
            sleep(1)
            res1 = TomatoOcrTap(626, 763, 702, 797, "挑战首领")
            res2 = False
            if not res1:
                res2, x, y = imageFind('挑战首领', x1=562, y1=643, x2=704, y2=838)
                if res2:
                    tapSleep(x + 25, y + 25, 1)
            if res1 or res2:
                # 功能开关["fighting"] = 1
                sleep(10)  # 等待动画
                for i in range(1, 5):
                    # res2, x, y = imageFind('首页-冒险')
                    res2 = FindColors.find(
                        "323,1210,#FCF8EE|333,1210,#FCF8ED|336,1212,#F9ECCB|336,1234,#FEF8E9|347,1231,#FCF8EE|363,1231,#FEF7EB|377,1229,#F4EFE1|372,1218,#88684E|353,1216,#9E8776",
                        rect=[301, 1130, 421, 1273])
                    # res2, _ = TomatoOcrText(626, 379, 711, 405, "冒险手册")
                    if res2:
                        break
                    else:
                        sleep(5)  # 等待动画
                # 功能开关["fighting"] = 0
                for i in range(15):
                    res1, _ = TomatoOcrText(636, 781, 691, 802, "等待中")
                    if res1:
                        Toast('挑战首领 - 等待中')
                        sleep(3)
                    res2, _ = TomatoOcrText(636, 781, 691, 802, "挑战中")
                    if res2:
                        Toast('挑战首领 - 战斗中')
                        功能开关["home_fighting"] = 1
                        sleep(3)
                    if not res1 and not res2:
                        功能开关["home_fighting"] = 0
                        # 检查是否挑战成功
                        res1, _ = TomatoOcrText(429, 542, 492, 606, "败")
                        if res1:
                            Toast('主线挑战首领 - 失败')
                        Toast('主线挑战首领 - 完成')
                        if 功能开关["优先推图到最新关卡"] == 1:
                            res = TomatoOcrTap(428, 1073, 521, 1100, "下一关卡", 10, 10)
                            if res:
                                Toast('前往下一关-快捷入口')
                        sleep(5)
                        break
                    功能开关["home_fighting"] = 0

        if 功能开关["自动换图"] == 1:
            Toast("日常 - 前往新地图 - 开始")
            self.homePage()
            # 直接点击图标切换
            newMapOK = FindColors.find(
                "603,664,#FCF8EE|612,664,#FCF8EE|618,662,#FCF8EE|607,659,#FCF8EE|615,659,#FCF8EE|612,664,#FCF8EE",
                rect=[558, 634, 661, 733])  # 匹配前往新关卡UI
            needNewMap = False
            if newMapOK:
                tapSleep(594, 689, 4)
                temp = FindColors.find(
                    "603,664,#FCF8EE|612,664,#FCF8EE|618,662,#FCF8EE|607,659,#FCF8EE|615,659,#FCF8EE|612,664,#FCF8EE",
                    rect=[558, 634, 661, 733])
                if temp:
                    tapSleep(602, 702, 4)
                # 兜底新手关卡，未开启结伴-队伍大厅时跳转逻辑
                xinShou = TomatoOcrTap(192, 359, 285, 408, '绿风原野', offsetX=25, offsetY=30)
                if xinShou:
                    tapSleep(140, 893, 0.8)  # 点击绿风原野- 1-1
                    tapSleep(361, 1046, 7)  # 点击前往

            if not newMapOK:
                newMapOK = TomatoOcrTap(589, 674, 629, 691, '前往', sleep1=4)

            res1 = False
            if newMapOK:
                res1, _ = TomatoOcrText(97, 1199, 128, 1234, "回")
            if res1:
                needNewMap = True
                tapSleep(93, 1212, 1)  # 返回
                tapSleep(93, 1212)  # 返回

            # 队员不满足时，才会不展示首页的前往下一关快速入口；因此判断开了单飞再从地图跳转下一关
            if (not newMapOK and 功能开关["队员不满足单飞"] == 1) or needNewMap:
                res1, _ = TomatoOcrText(573, 200, 694, 238, "新关卡")
                res2 = False
                if not res1:
                    res2, _ = TomatoOcrText(592, 206, 626, 225, "新地")
                    if not res2:
                        res2, _ = TomatoOcrText(592, 206, 626, 225, "新关")
                if res1 or res2:
                    功能开关["needHome"] = 0
                    功能开关["noHomeMust"] = 1
                    功能开关["fighting"] = 1
                    Toast('前往下一关-关卡大厅')
                    # if 1:
                    # 结伴入口切换
                    res = TomatoOcrTap(647, 450, 689, 474, "结伴", offsetX=10, offsetY=10, sleep1=1.5)
                    res = TomatoOcrTap(373, 1106, 471, 1141, "关卡大厅", offsetX=10, offsetY=10, sleep1=0.7)
                    for i in range(5):
                        功能开关["needHome"] = 0
                        功能开关["noHomeMust"] = 1
                        功能开关["fighting"] = 1
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

                            res = TomatoOcrTap(321, 1022, 394, 1044, "前往地图", sleep1=1)
                            res = TomatoOcrTap(330, 1027, 389, 1058, "前往", sleep1=1)
                            if res:
                                res, _ = TomatoOcrText(432, 729, 530, 760, "留在队伍")
                                if res:
                                    if 功能开关["队员不满足单飞"] == 1:
                                        res = TomatoOcrTap(187, 730, 282, 756, "离队前往")
                                    else:
                                        res = TomatoOcrTap(435, 729, 532, 759, "留在队伍")
                                    break
                                break
                            swipe(500, 800, 500, 600)
                            sleep(2)
                        else:
                            Toast('前往下一关-关卡大厅-寻找中')
                            res = TomatoOcrTap(373, 1106, 471, 1141, "关卡大厅", offsetX=10, offsetY=10, sleep1=0.7)
                            if not res:
                                break
                            swipe(500, 800, 500, 300)
                            sleep(4)

        if 功能开关["单飞后寻找结伴"] == 1 and 功能开关["fighting"] == 0 and not forceCheck:
            if 任务记录["寻找结伴-完成"] == 0:
                Toast("日常 - 寻找结伴 - 开始")
                self.homePage()
                res = TomatoOcrTap(646, 451, 689, 474, "结伴", 10, -10)
                if res:
                    isTeam, _, _ = TomatoOcrFindRange('旅伴', 0.9, 143, 257, 568, 355)
                    if not isTeam:
                        Toast("日常 - 寻找结伴 - 已有结伴")
                        任务记录["寻找结伴-完成"] = 1
                        sleep(1)
                        TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
                    else:
                        res = TomatoOcrTap(407, 1036, 513, 1070, "寻找队伍", 25, 25, sleep1=1)
                        re = TomatoOcrTap(511, 329, 555, 358, "加入", 25, 25, sleep1=1)
                        # re, x, y = imageFind('结伴-加入')
                        if re:
                            # tapSleep(x, y, 1)
                            Toast("日常 - 寻找结伴 - 加入队伍")
                            sleep(4)  # 等待动画
                            res = TomatoOcrTap(359, 741, 391, 775, "确认跟随", 10, 10)
                            任务记录["寻找结伴-完成"] = 1
        功能开关["fighting"] = 0
        功能开关["noHomeMust"] = 0

    # 斗歌会
    def DouGeHui(self):
        for p in range(3):
            if 功能开关["斗歌会"] == 0:
                return

            if 任务记录["斗歌会-完成"] == 1:
                return

            Toast('日常 - 斗歌会 - 开始')

            self.homePage()
            self.quitTeam()
            res = TomatoOcrFindRangeClick('斗歌会', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
                                          sleep1=2.5, match_mode='fuzzy')
            if not res:
                Toast('日常 - 斗歌会 - 未找到入口')
                return

            # 领取上把奖励
            re = TomatoOcrTap(332, 710, 384, 736, '开启', offsetX=10, offsetY=10, sleep1=1.5)
            if re:
                Toast('斗歌会 - 开启上一把宝箱')
                tapSleep(348, 1235)  # 空白
                tapSleep(348, 1235)  # 空白
                tapSleep(348, 1235)  # 空白

            # 领取全服榜奖励
            re = CompareColors.compare("178,263,#F36042|178,261,#F36141|178,265,#F15E40")
            if re:
                Toast('斗歌会 - 领取共享战利品')
                tapSleep(146, 280, 0.8)
                for j in range(6):
                    re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                         diff=0.9)
                    if re:
                        tapSleep(re.x, re.y)
                        tapSleep(427, 217)
                        tapSleep(427, 217)
                swipe(345, 935, 339, 337)
                sleep(2)
                for k in range(6):
                    re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                         diff=0.9)
                    if re:
                        tapSleep(re.x, re.y)
                        tapSleep(427, 217)
                        tapSleep(427, 217)
                swipe(345, 935, 339, 337)
                sleep(2)
                for k in range(6):
                    re = FindColors.find("580,266,#F05C40|583,268,#F15A41|585,265,#F35E41", rect=[481, 239, 622, 1076],
                                         diff=0.9)
                    if re:
                        tapSleep(re.x, re.y)
                        tapSleep(427, 217)
                        tapSleep(427, 217)
                tapSleep(93, 1213)  # 返回

            # 领取累积奖励
            re = CompareColors.compare("622,703,#F25E41|622,700,#F46042")
            if re:
                Toast("斗歌会 - 领取累积奖励")
                tapSleep(611, 732)
                for i in range(4):
                    res = TomatoOcrFindRangeClick("领取", sleep1=0.5, whiteList='领取', x1=108, y1=342, x2=603, y2=983)
                    if res:
                        tapSleep(350, 1010)  # 点击空白处
                    else:
                        break
                res = TomatoOcrTap(71, 1202, 124, 1231, "返回")

            # 识别目标阶段
            toLevel = safe_int_v2(功能开关['斗歌会目标阶段'])
            if toLevel == 0:
                toLevel = 1000
            if toLevel > 0:
                re, level = TomatoOcrText(132, 1013, 191, 1035, "阶段")
                level = level.replace("阶", "")
                level = safe_int_v2(level)
                if level >= toLevel:
                    Toast("斗歌会 - 已达到目标等阶")
                    sleep(1.5)
                    任务记录["斗歌会-完成"] = 1
                    return

            self.startFightDouGeHui()

    def startFightDouGeHui(self):
        # 直接开始匹配
        res = TomatoOcrTap(306, 1156, 413, 1186, "开始匹配", 40, -40)
        Toast("斗歌会 - 开始匹配")

        # 判断职业选择
        res, _ = TomatoOcrText(321, 491, 397, 514, "选择职业")
        if res:
            Toast("斗歌会 - 选择职业")
            if 功能开关["职能优先输出"] == 1:
                tapSleep(280, 665, 0.8)  # 职能输出
            elif 功能开关["职能优先坦克"] == 1 or 功能开关["职能优先治疗"] == 1:
                tapSleep(435, 665, 0.8)  # 坦克
            else:
                tapSleep(280, 665, 0.8)  # 职能输出
            res = TomatoOcrTap(332, 754, 387, 789, "确定")

        # 判断正在匹配中 - 循环等待300s
        totalWait = 150  # 30000 毫秒 = 30 秒
        elapsed = 0
        while 1:
            if elapsed > totalWait:
                # 超时取消匹配
                res = TomatoOcrTap(322, 1152, 394, 1178, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            Toast(f"斗歌会任务 - 匹配中 - 等待{elapsed}/150s")
            # 判断无合适队伍，重新开始匹配
            res = TomatoOcrTap(306, 1156, 413, 1186, "开始匹配", 40, -40)
            res, _ = TomatoOcrText(224, 617, 307, 650, "匹配超时")
            if res:
                Toast("斗歌会 - 匹配超时 - 无合适队伍 - 重新匹配")
                res = TomatoOcrTap(454, 729, 510, 7598, "确定")

            waitStatus, _ = TomatoOcrText(322, 1152, 394, 1178, "匹配中")
            if not waitStatus:
                waitStatus, _ = TomatoOcrText(325, 1156, 390, 1182, "匹配中")
                if not waitStatus:
                    res, waitTime = TomatoOcrText(334, 1184, 383, 1201, "等待时间")
                    if waitTime != "":
                        waitStatus = True

            res1 = self.shilianTask.WaitFight(fightType="斗歌会")
            if res1 == True or (waitStatus == False):  # 成功准备战斗 或 未匹配到
                # 超时取消匹配
                res = TomatoOcrTap(320, 1166, 393, 1190, "匹配中", 40, -40)
                if not res:
                    res = TomatoOcrTap(325, 1156, 390, 1182, "匹配中", 40, -40)
                    if not res:
                        res = TomatoOcrTap(321, 1151, 393, 1185, "匹配中", 40, -40)
                break

            sleep(5)
            elapsed = elapsed + 5

    # 派对大师
    def PaiDuiDaShi(self):
        for p in range(3):
            if 功能开关["派对大师"] == 0:
                return

            if 任务记录["派对大师-完成"] == 1:
                return

            Toast('日常 - 派对大师 - 开始')

            self.homePage(needQuitTeam=True)
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
                re = CompareColors.compare("517,935,#F1A949|517,942,#F1A949|520,934,#F1A949|521,943,#F1A949")  # 第五格宝箱
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
                            # print(swipeArr)
                            for p in swipeArr:
                                tapSleep(p['x'], p['y'], 0.3)
                                TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)

                        res, _ = TomatoOcrText(402, 1164, 445, 1184, '提示')
                        if not res:
                            break

                        # 兜底选取任意卡牌
                        reAll = FindColors.find_all(
                            "382,273,#C68F67|382,293,#EDBE7E|350,291,#EDBF7E|377,317,#D8A572|402,299,#EBBF7E|415,268,#D8A070",
                            rect=[97, 225, 652, 1098], diff=0.95)
                        if reAll:
                            Toast('选择未翻开卡牌')
                            for tmpPoint in reAll:
                                tapSleep(tmpPoint.x, tmpPoint.y, 0.3)
                                re = TomatoOcrTap(549, 1168, 608, 1199, '选择', sleep1=0.3)
                                if not re:
                                    break
        功能开关['fighting'] = 0

    # 踏青签到簿 - 清明活动
    def QiTaQianDaoTaQing(self):
        if 任务记录["踏青签到簿"] == 0:
            Toast('其他签到-踏青签到簿-开始')
            # 判断是否在营地页面
            res1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
            if not res1:
                hd1 = False
                hd2 = False
                for k in range(3):
                    # 返回首页
                    self.homePage()
                    res = TomatoOcrTap(125, 1202, 187, 1234, "营地")
                    # 判断是否在营地页面
                    hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
                    hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
                    if hd1 or hd2:
                        break

                if not hd1 and not hd2:
                    Toast('其他签到-踏青签到簿-未找到活动入口')
                    return

            isFind = TomatoOcrFindRangeClick('踏青', match_mode='fuzzy', x1=82, y1=61, x2=653, y2=1153)
            if not isFind:
                # -- 返回活动最后一屏
                self.huoDongSwipeDown()

                for i in range(1, 5):
                    # 上翻第二屏，继续识别
                    swipe(680, 451, 680, 804)
                    sleep(3)
                    isFind = TomatoOcrFindRangeClick('踏青', x1=82, y1=61, x2=653, y2=1153)
                    if isFind:
                        break
            if isFind:
                sleep(1.5)
                for k in range(10):
                    re = TomatoOcrTap(507, 560, 572, 586, "领取")
                    if re:
                        tapSleep(323, 1217)  # 点击空白处关闭
                        tapSleep(323, 1217)  # 点击空白处关闭
                    else:
                        break
                任务记录["踏青签到簿"] = 1
                tapSleep(98, 1194)  # 点击返回
                tapSleep(98, 1194)  # 点击返回
            return

    # 其他签到活动（简单活动合集）
    def QiTaQianDao(self):
        if 功能开关["其他签到活动"] == 0:
            return
        # 踏青签到簿 - 清明活动
        self.QiTaQianDaoTaQing()
        # 欢庆连五日
        # if 任务记录["欢庆连五日"] == 0:
        #     Toast('欢庆连五日 - 开始')
        #     # 返回首页
        #     self.homePage()
        #     res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1)
        #     # 判断是否在营地页面
        #     hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        #     hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        #     if hd1 == False and hd2 == False:
        #         return
        #
        #     isFind = TomatoOcrFindRangeClick('欢庆连五日')
        #     if not isFind:
        #         # -- 返回活动最后一屏
        #         self.huoDongSwipeDown()
        #
        #         for i in range(1, 5):
        #             # 上翻第二屏，继续识别
        #             swipe(680, 451, 680, 804)
        #             sleep(3)
        #             isFind = TomatoOcrFindRangeClick('欢庆连五日')
        #             if isFind:
        #                 break
        #     if isFind:
        #         sleep(1.5)
        #         TomatoOcrFindRangeClick(x1=454, y1=501, x2=620, y2=1136, keyword="领取")
        #         任务记录["欢庆连五日"] = 1
        #         tapSleep(36, 1123)  # 点击空白处关闭

        # # 红包传好运
        # if 任务记录["红包传好运"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('庙会开市', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=2.5, match_mode='fuzzy')
        #     if res:
        #         Toast('红包传好运 - 任务开始')
        #         tapSleep(202, 397, 3)  # 红包传好运
        #         # 领红包
        #         Toast('红包传好运 - 领红包')
        #         re = TomatoOcrTap(543, 1224, 622, 1250, '红包列表', sleep1=1.5)
        #         if re:
        #             # 点击红包
        #             for k in range(40):
        #                 re, count = TomatoOcrText(418, 1058, 471, 1079, '领取次数')
        #                 if count == '10/10':
        #                     Toast('红包传好运 - 领红包 - 完成')
        #                     任务记录["红包传好运"] = 1
        #                     break
        #                 re = FindColors.find(
        #                     "281,363,#B7C4FE|280,371,#7884FE|285,365,#E9F1FF|290,372,#A7C9EB|289,359,#EFD5DD|277,359,#DDD7FA",
        #                     rect=[221, 295, 543, 1038], diff=0.8)
        #                 if not re:
        #                     Toast('寻找钻石红包')
        #                     swipe(522, 890, 536, 651)
        #                     sleep(1)
        #                     # re = FindColors.find("413,369,#F69748|426,359,#F69A4B|432,370,#F69D4D|422,385,#F4984B")  # 普通红包
        #                 if re:
        #                     tapSleep(re.x, re.y, 1.5)
        #                     re = TomatoOcrTap(345, 814, 372, 839, '开', sleep1=1.5)
        #                     if re:
        #                         tapSleep(164, 1073)  # 空白
        #                         tapSleep(94, 1215)  # 返回
        #                 tapSleep(164, 1073)  # 空白
        #             tapSleep(94, 1215)  # 返回
        #
        #         # 发红包
        #         Toast('红包传好运 - 发红包')
        #         tapSleep(363, 1037, 2)  # 发红包
        #         re = FindColors.find(
        #             "207,1003,#FFB76E|209,1005,#F9A665|217,1000,#DE583A|224,1002,#DD5339|228,999,#E26041|236,1002,#DE5539|207,988,#E35D3F|237,963,#EB5E41",
        #             rect=[177, 947, 268, 1041], diff=0.9)  # 钻石红包
        #         if re:
        #             Toast('红包传好运 - 发红包 - 钻石')
        #             tapSleep(213, 979, 2)  # 钻石红包
        #             tapSleep(101, 1220, 2)  # 返回
        #             tapSleep(202, 397, 2)  # 红包传好运
        #             tapSleep(363, 1037, 2)  # 发红包
        #         re = FindColors.find(
        #             "207,1003,#FFB76E|209,1005,#F9A665|217,1000,#DE583A|224,1002,#DD5339|228,999,#E26041|236,1002,#DE5539|207,988,#E35D3F|237,963,#EB5E41",
        #             rect=[236, 834, 350, 945], diff=0.9)  # 猫猫糖红包
        #         if re:
        #             Toast('红包传好运 - 发红包 - 猫猫糖')
        #             tapSleep(294, 884, 2)
        #             tapSleep(101, 1220, 2)  # 返回
        #             tapSleep(202, 397, 2)  # 红包传好运
        #             tapSleep(363, 1037, 2)  # 发红包
        #         re = FindColors.find(
        #             "207,1003,#FFB76E|209,1005,#F9A665|217,1000,#DE583A|224,1002,#DD5339|228,999,#E26041|236,1002,#DE5539|207,988,#E35D3F|237,963,#EB5E41",
        #             rect=[366, 836, 476, 946], diff=0.9)  # 原材料红包
        #         if re:
        #             Toast('红包传好运 - 发红包 - 原材料')
        #             tapSleep(412, 875, 2)  # 原材料红包
        #             tapSleep(101, 1220, 2)  # 返回
        #             tapSleep(202, 397, 2)  # 红包传好运
        #             tapSleep(363, 1037, 2)  # 发红包
        #         re = FindColors.find(
        #             "207,1003,#FFB76E|209,1005,#F9A665|217,1000,#DE583A|224,1002,#DD5339|228,999,#E26041|236,1002,#DE5539|207,988,#E35D3F|237,963,#EB5E41",
        #             rect=[448, 943, 552, 1052], diff=0.9)  # 骑行鞍红包
        #         if re:
        #             Toast('红包传好运 - 发红包 - 骑行鞍')
        #             tapSleep(495, 983, 2)
        #             tapSleep(101, 1220, 2)  # 返回
        #             tapSleep(363, 1037, 2)  # 发红包
        #
        # # 祈福交好运
        # if 任务记录["祈福交好运"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('庙会开市', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=2.5, match_mode='fuzzy')
        #     if res:
        #         Toast('祈福交好运活动 - 任务开始')
        #         tapSleep(528, 367, 3)  # 祈福交好运
        #         # 领取累积奖励
        #         for k in range(4):
        #             re = FindColors.find("300,264,#F15F41|302,263,#F45E42|301,266,#ED573A", rect=[221, 243, 600, 331],
        #                                  diff=0.9)
        #             if re:
        #                 Toast('祈福交好运活动 - 领取累积奖励')
        #                 tapSleep(563, 276)
        #                 tapSleep(560, 273)
        #                 tapSleep(497, 284)
        #                 tapSleep(493, 282)
        #                 tapSleep(427, 274)
        #                 tapSleep(423, 271)
        #                 tapSleep(352, 280)
        #                 tapSleep(350, 279)
        #                 tapSleep(279, 277)
        #                 tapSleep(274, 273)
        #                 tapSleep(334, 1208)  # 空白
        #                 tapSleep(334, 1208)
        #         # 摇树
        #         for k in range(10):
        #             re, count = TomatoOcrText(541, 1153, 582, 1180, '次数')
        #             count = safe_int_v2(count)
        #             if count == 0:
        #                 任务记录["祈福交好运"] = 1
        #                 break
        #             Toast('祈福交好运活动 - 摇树')
        #             tapSleep(538, 1065, 3)  # 摇树
        #             tapSleep(334, 1208)  # 空白
        #             tapSleep(334, 1208)  # 空白
        #
        # # 摆摊奇才
        # if 任务记录["摆摊奇才签到"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('庙会开市', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=2.5, match_mode='fuzzy')
        #     if res:
        #         Toast('摆摊奇才活动 - 任务开始')
        #         tapSleep(406, 577, 3)  # 摆摊奇才
        #         tapSleep(331, 1246)  # 关闭说明
        #         # 领取币
        #         res, availableCount = TomatoOcrText(541, 1101, 617, 1125, "庙会币")
        #         if availableCount != '':
        #             Toast('摆摊奇才 - 领取庙会币')
        #             tapSleep(577, 1046)  # 领取庙会币
        #             tapSleep(331, 1246)  # 空白处
        #
        #         # 领取累积奖励
        #         res = CompareColors.compare("159,146,#F05E40|159,145,#F15F41|162,148,#F65741|157,148,#ED5B40")
        #         if res:
        #             Toast('摆摊奇才 - 领取累积奖励')
        #             tapSleep(137, 170)  # 领取等级奖励
        #             for p in range(4):
        #                 re = FindColors.find("503,410,#EB5532|503,405,#F36042|506,409,#F85242",
        #                                      rect=[109, 340, 605, 953], diff=0.95)
        #                 if re:
        #                     tapSleep(re.x - 10, re.y + 10)
        #                     tapSleep(517, 352)  # 空白处
        #                     tapSleep(517, 352)  # 空白处
        #
        #         # 判断自动向前开关
        #         re = CompareColors.compare(
        #             "320,1177,#FEFCF7|320,1175,#FEFCF7|323,1175,#FEFCF7|325,1174,#FEFCF7|330,1172,#FEFCF7|330,1177,#FEFCF7")
        #         if re:
        #             tapSleep(321, 1170)  # 开启自动向前
        #         tapSleep(363, 1056)  # 开始前进
        #         for k in range(60):
        #             # 判断自动进行
        #             re = CompareColors.compare(
        #                 "402,997,#F7FCFF|407,997,#ED5B3D|413,995,#F8FBFF|420,995,#ED5B3E|407,1010,#ED5B3E|405,989,#ED5B3E")
        #             if not re:
        #                 re = CompareColors.compare(
        #                     "320,1177,#FEFCF7|320,1175,#FEFCF7|323,1175,#FEFCF7|325,1174,#FEFCF7|330,1172,#FEFCF7|330,1177,#FEFCF7")
        #                 if re:
        #                     tapSleep(321, 1170)  # 开启自动向前
        #                 tapSleep(363, 1056)  # 开始前进
        #
        #             # 判断升级
        #             re = CompareColors.compare("420,1155,#6584B9|416,1166,#6584B9|413,1174,#6584B9")
        #             if re:
        #                 tapSleep(363, 1160)
        #
        #             # 等待游戏进行
        #             res, availableCount = TomatoOcrText(332, 1104, 392, 1125, "骰子")
        #             if availableCount == '':
        #                 Toast('摆摊奇才 - 任务中断')
        #                 break
        #             if availableCount == '0/30':
        #                 Toast('摆摊奇才 - 任务结束')
        #                 任务记录["摆摊奇才签到"] = 1
        #                 break
        #             Toast(f'摆摊奇才 - 进行中 - 剩余{availableCount}')
        #             sleep(5)
        #         TomatoOcrTap(102, 1202, 131, 1233, '回')

        # # 西行记
        # if 任务记录["西行记签到"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('西行记', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=1.5, match_mode='fuzzy')
        #     if res:
        #         Toast('西行记活动 - 任务开始')
        #         re = TomatoOcrTap(168, 470, 285, 505, '火眼金睛', sleep1=1.5)
        #         if re:
        #             for o in range(4):
        #                 re = FindColors.find("304,474,#F55F42|305,478,#F15B41|308,476,#F15D40",
        #                                      rect=[115, 440, 617, 572],
        #                                      diff=0.8)  # 累积奖励
        #                 if re:
        #                     tapSleep(re.x - 20, re.y + 20)
        #                     tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(282, 621, 330, 654, '大鹏')
        #             if re:
        #                 Toast('火眼金睛 - 大鹏金翅 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(156, 1205, 2)  # 营地
        #                 tapSleep(230, 271, 3)  # 英雄之路
        #                 swipe(374, 528, 366, 1106)  # 上划
        #                 sleep(0.5)
        #                 swipe(374, 528, 366, 1106)  # 上划
        #                 sleep(0.5)
        #                 swipe(374, 528, 366, 1106)  # 上划
        #                 sleep(0.5)
        #                 swipe(374, 528, 366, 1106)  # 上划
        #                 sleep(0.5)
        #                 swipe(374, 528, 366, 1106)  # 上划
        #                 sleep(0.5)
        #                 tapSleep(358, 441, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(273, 618, 377, 656, '黄牙老象')
        #             if re:
        #                 Toast('火眼金睛 - 黄牙老象 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(668, 437, 2.5)  # 结伴
        #                 tapSleep(547, 1126, 1)  # 收到邀请
        #                 tapSleep(225, 440, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(279, 625, 351, 653, '驮珠虫')
        #             if re:
        #                 Toast('火眼金睛 - 驮珠虫 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(258, 1202, 0.8)  # 行李
        #                 tapSleep(576, 505, 0.8)  # 衣柜
        #                 tapSleep(339, 1212, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(277, 623, 353, 653, '狸弓手')
        #             if re:
        #                 Toast('火眼金睛 - 狸弓手 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(465, 1210, 0.8)  # 旅人
        #                 tapSleep(590, 481, 1.5)  # 天赋
        #                 swipe(80, 809, 143, 323)
        #                 sleep(0.5)
        #                 swipe(80, 809, 143, 323)
        #                 sleep(0.5)
        #                 swipe(80, 809, 143, 323)
        #                 sleep(0.5)
        #                 swipe(80, 809, 143, 323)
        #                 sleep(0.5)
        #                 tapSleep(148, 1032, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(279, 620, 375, 654, '青毛狮王')
        #             if re:
        #                 Toast('火眼金睛 - 青毛狮王 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(667, 505, 0.8)  # 试炼
        #                 tapSleep(390, 374, 1.5)  # 绝境
        #                 tapSleep(94, 160, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(277, 623, 353, 653, '蓝力士')
        #             if re:
        #                 Toast('火眼金睛 - 蓝力士 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(162, 1201, 1.3)  # 营地
        #                 tapSleep(345, 421, 3)  # 铁匠铺
        #                 tapSleep(172, 329, 0.8)  # 妖怪
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #                 tapSleep(348, 1188)  # 点击空白
        #
        #             re, _ = TomatoOcrText(279, 625, 351, 653, '狐巡司')
        #             if re:
        #                 Toast('火眼金睛 - 狐巡司 - 任务开始')
        #                 tapSleep(85, 1202, 0.8)  # 返回
        #                 tapSleep(634, 164, 0.8)  # 大地图
        #                 tapSleep(311, 39, 0.8)  # 点击空白
        #                 for l in range(10):
        #                     swipe(350, 277, 380, 609)  # 上划
        #                     sleep(0.5)
        #                     if l > 5:
        #                         swipe(108, 599, 505, 577)  # 左滑
        #                     else:
        #                         swipe(505, 577, 108, 599)  # 右滑
        #                     sleep(1)
        #
        #                     find = FindColors.find(
        #                         "375,250,#F7F3EA|369,230,#F7F3EA|347,244,#836E55|363,239,#8F7D69|393,243,#F7F3EA|397,243,#F7F3EA",
        #                         rect=[11, 31, 701, 523], diff=0.93)
        #                     if find:
        #                         tapSleep(find.x - 50, find.y + 40)
        #                         任务记录["西行记签到"] = 1
        #                         Toast('火眼金睛 - 已找到任务奖励')
        #                         break
        #
        #     else:
        #         Toast('西行记活动 - 未找到活动入口')
        #
        # # 双旦联欢
        # if 任务记录["双旦联欢签到"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('双旦', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=1.5, match_mode='fuzzy')
        #     if res:
        #         Toast('双旦联欢签到 - 任务开始')
        #         任务记录["双旦联欢签到"] = 1
        #         res = CompareColors.compare("323,470,#F15D40|325,468,#F36042|326,470,#F15E41")  # 匹配红点
        #         if res:
        #             tapSleep(211, 486, 0.8)
        #             res = TomatoOcrFindRangeClick('领取', x1=459, y1=528, x2=625, y2=1150, offsetX=30, offsetY=-20,
        #                                           sleep1=0.5)
        #             tapSleep(92, 1218)  # 返回
        #             tapSleep(92, 1218)
        #             tapSleep(92, 1218)
        #     else:
        #         任务记录["双旦联欢签到"] = 1

        # # 忆战回环
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
                    tapSleep(195, 1043, 0.1)  # 点击奖励
                    tapSleep(192, 1062, 0.1)  # 点击奖励
                    tapSleep(92, 1218)  # 返回
                    tapSleep(92, 1218)
            else:
                任务记录["半周年庆典签到"] = 1
        #
        # # 半周年庆典签到
        # if 任务记录["半周年庆典签到"] == 0:
        #     self.homePage()
        #     res = TomatoOcrFindRangeClick('周年', x1=544, y1=334, x2=631, y2=623, offsetX=30, offsetY=-20,
        #                                   sleep1=0.8, match_mode='fuzzy')
        #     if res:
        #         Toast('半周年庆典签到 - 任务开始')
        #         任务记录["半周年庆典签到"] = 1
        #         res = CompareColors.compare("592,505,#F55F42|595,505,#F45F42|595,509,#F15A41")  # 匹配红点
        #         if res:
        #             TomatoOcrTap(456, 509, 565, 544, '庆典签到', sleep1=0.8)
        #             res = TomatoOcrFindRangeClick('领取', x1=7, y1=921, x2=701, y2=995, offsetX=30, offsetY=-20,
        #                                           sleep1=0.5)
        #             tapSleep(92, 1218)  # 返回
        #             tapSleep(92, 1218)
        #             tapSleep(92, 1218)
        #     else:
        #         任务记录["半周年庆典签到"] = 1

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

        # 拾光奇旅
        if 任务记录["拾光奇旅"] == 0:
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
            # 判断是否在营地页面
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if res:
                res = TomatoOcrFindRangeClick('奇旅', match_mode='fuzzy', x1=99, y1=656, x2=180, y2=1062, offsetX=30,
                                              offsetY=-20,
                                              sleep1=0.8)
                if res:
                    Toast('拾光奇旅 - 任务开始')
                    res = tapSleep(606, 296)  # 每日奖励
                    tapSleep(361, 1238)  # 空白
                    tapSleep(361, 1238)  # 空白
                    tapSleep(356, 1134)  # 一键领取
                    tapSleep(361, 1238)  # 空白
                    tapSleep(90, 1204)  # 返回
                    tapSleep(90, 1204)
                    任务记录["拾光奇旅"] = 1
                else:
                    Toast('拾光奇旅 - 未找到入口')
                    # 任务记录["拾光奇旅"] = 1

        # 黑猫虫游记
        if 任务记录["黑猫虫游记"] == 0:
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
            # 判断是否在营地页面
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if res:
                res = TomatoOcrFindRangeClick('黑猫', match_mode='fuzzy', x1=99, y1=656, x2=180, y2=1062, offsetX=30,
                                              offsetY=-20,
                                              sleep1=1.5)
                if res:
                    Toast('黑猫虫游记 - 任务开始')
                    re = FindColors.find("667,997,#EF5D40|669,995,#F45F42|672,995,#F35E41", rect=[22, 1040, 165, 1156],
                                         diff=0.95)  # 匹配带咖波回家红点
                    if re:
                        Toast('黑猫虫游记 - 带咖波回家')
                        tapSleep(91, 1095, 0.8)
                        tapSleep(363, 751, 0.8)
                        tapSleep(292, 1224)  # 空白处
                        tapSleep(292, 1224)

                    # 领取累积奖励
                    res = FindColors.find("256,146,#ED5B3E|256,144,#ED5B3E", rect=[170, 115, 634, 214], diff=0.95)
                    if res:
                        Toast('领取累积奖励')
                        tapSleep(res.x - 15, res.y + 5)  # 领取累计奖励
                        tapSleep(292, 1224)  # 空白处

                    re = CompareColors.compare("468,1109,#F25B3E|468,1106,#F55F42|470,1107,#F35E41")  # 里程任务红点
                    if re:
                        Toast('黑猫虫游记 - 领取里程奖励')
                        tapSleep(442, 1122, 1.5)
                        TomatoOcrTap(495, 301, 549, 334, '领取')
                        tapSleep(347, 1027)  # 空白处
                        tapSleep(347, 1027)  # 空白处
                        re = CompareColors.compare("598,1081,#F25A3E|598,1079,#F05D40")  # 匹配活动任务红点
                        if re:
                            tapSleep(543, 1092, 1.5)
                            TomatoOcrTap(495, 301, 549, 334, '领取')
                            tapSleep(347, 1027)  # 空白处
                            tapSleep(347, 1027)  # 空白处
                    tapSleep(292, 1224)  # 空白处

                    re = CompareColors.compare("562,1226,#4DAD3A|565,1221,#50B23A|562,1224,#4AAD39")  # 匹配未开启自动出发
                    if not re:
                        Toast('黑猫虫游记 - 开启自动出发')
                        tapSleep(557, 1226)

                    for q in range(10):
                        re, ct = TomatoOcrText(609, 82, 660, 104, '剩余前进次数')
                        TomatoOcrTap(328, 708, 390, 738, '领取')
                        Toast(f'剩余{ct}次')
                        ct = safe_int(ct)
                        if ct > 0:
                            tapSleep(596, 1092)  # 点击出发
                            tapSleep(292, 1224)  # 空白处
                            tapSleep(292, 1224)  # 空白处
                            sleep(3)
                        else:
                            break

                    # 领取累积奖励
                    res = FindColors.find("256,146,#ED5B3E|256,144,#ED5B3E", rect=[170, 115, 634, 214], diff=0.95)
                    if res:
                        Toast('领取累积奖励')
                        tapSleep(res.x - 15, res.y + 5)  # 领取累计奖励
                        tapSleep(292, 1224)  # 空白处

                    任务记录["黑猫虫游记"] = 1
                else:
                    Toast('黑猫虫游记 - 未找到入口')
                    # 任务记录["黑猫虫游记"] = 1

        # 岛屿游记
        if 任务记录["岛屿游记"] == 0:
            self.homePage()
            res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
            # 判断是否在营地页面
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if res:
                res = TomatoOcrFindRangeClick('岛屿', match_mode='fuzzy', x1=99, y1=656, x2=180, y2=1062, offsetX=30,
                                              offsetY=-20,
                                              sleep1=1.5)
                if res:
                    Toast('岛屿游记 - 任务开始')
                    re = FindColors.find("667,997,#EF5D40|669,995,#F45F42|672,995,#F35E41", rect=[22, 1040, 165, 1156],
                                         diff=0.95)  # 匹配带咖波回家红点
                    if re:
                        Toast('岛屿游记 - 带蓝猪回家')
                        tapSleep(91, 1095, 0.8)
                        tapSleep(363, 751, 0.8)
                        tapSleep(292, 1224)  # 空白处
                        tapSleep(292, 1224)

                    # 领取累积奖励
                    res = FindColors.find("256,146,#ED5B3E|256,144,#ED5B3E", rect=[170, 115, 634, 214], diff=0.95)
                    if res:
                        Toast('领取累积奖励')
                        tapSleep(res.x - 15, res.y + 5)  # 领取累计奖励
                        tapSleep(292, 1224)  # 空白处

                    re = CompareColors.compare("468,1109,#F25B3E|468,1106,#F55F42|470,1107,#F35E41")  # 里程任务红点
                    if re:
                        Toast('岛屿游记 - 领取里程奖励')
                        tapSleep(442, 1122, 1.5)
                        TomatoOcrTap(495, 301, 549, 334, '领取')
                        tapSleep(595, 1049)  # 空白处
                        tapSleep(595, 1049)  # 空白处
                        re = CompareColors.compare("595,1081,#EF5C40|596,1077,#F55F42")  # 匹配活动任务红点
                        if re:
                            tapSleep(543, 1092, 1.5)
                            TomatoOcrTap(495, 301, 549, 334, '领取')
                            tapSleep(595, 1049)  # 空白处
                            tapSleep(595, 1049)  # 空白处
                    tapSleep(292, 1224)  # 空白处

                    re = CompareColors.compare("557,1226,#50AF35|560,1229,#49B649|563,1224,#4EAD39|565,1223,#4EAD39",
                                               diff=0.8)  # 匹配未开启自动出发
                    if not re:
                        Toast('岛屿游记 - 开启自动出发')
                        tapSleep(558, 1229)

                    for q in range(10):
                        re, ct = TomatoOcrText(609, 82, 660, 104, '剩余前进次数')
                        TomatoOcrTap(328, 708, 390, 738, '领取')
                        Toast(f'剩余{ct}次')
                        ct = safe_int(ct)
                        if ct > 0:
                            tapSleep(596, 1092)  # 点击出发
                            tapSleep(292, 1224)  # 空白处
                            tapSleep(292, 1224)  # 空白处
                            sleep(3)
                        else:
                            break

                    # 领取累积奖励
                    res = FindColors.find("256,146,#ED5B3E|256,144,#ED5B3E", rect=[170, 115, 634, 214], diff=0.95)
                    if res:
                        Toast('领取累积奖励')
                        tapSleep(res.x - 15, res.y + 5)  # 领取累计奖励
                        tapSleep(292, 1224)  # 空白处

                    任务记录["岛屿游记"] = 1
                else:
                    Toast('岛屿游记 - 未找到入口')
                    # 任务记录["黑猫虫游记"] = 1

        # 大玩家
        if 任务记录["大玩家"] == 0:
            self.fuZhuangLingQu(taskName='大玩家', searchName='大玩家')
            任务记录["大玩家"] = 1

        # 繁星使者
        if 任务记录["繁星使者"] == 0:
            self.fuZhuangLingQu(taskName='繁星使者', searchName='使者')
            任务记录["繁星使者"] = 1

        # 盛大公演
        if 任务记录["盛大公演"] == 0:
            self.fuZhuangLingQu(taskName='盛大公演', searchName='公演')
            任务记录["盛大公演"] = 1

        # 逍遥大圣
        if 任务记录["逍遥大圣"] == 0:
            self.fuZhuangLingQu(taskName='逍遥大圣', searchName='大圣')
            任务记录["逍遥大圣"] = 1

        # 来富巳
        if 任务记录["来富巳"] == 0:
            self.fuZhuangLingQu(taskName='来富巳', searchName='来富')
            任务记录["来富巳"] = 1

        # 魔咒
        if 任务记录["魔咒"] == 0:
            self.fuZhuangLingQu(taskName='魔咒', searchName='魔咒')
            任务记录["魔咒"] = 1

    # 服装签到通用方法
    def fuZhuangLingQu(self, taskName='', searchName=''):
        if taskName == '':
            return False
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            self.homePage()
            TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=0.8)
        # 判断是否在营地页面
        res = TomatoOcrFindRangeClick(searchName, match_mode='fuzzy', x1=7, y1=797, x2=96, y2=1144, offsetX=30,
                                      offsetY=-20,
                                      sleep1=0.8)
        if res:
            Toast(f'{taskName} - 任务开始')
            res = TomatoOcrTap(624, 895, 713, 921, "登录奖励", sleep1=0.5)
            for p in range(3):
                res = TomatoOcrFindRangeClick('可领取', x1=101, y1=389, x2=622, y2=1068, offsetX=30, offsetY=-20,
                                              sleep1=0.5)
                tapSleep(86, 980)  # 点击空白处
                if not res:
                    break
            tapSleep(90, 1204)  # 返回活动页

            # 购买礼包
            if 功能开关['钻石购买服装币'] == 1:
                Toast(f'{taskName} - 兑换服装币')
                re, zuanShi = TomatoOcrText(593, 81, 675, 102, '钻石数量')
                zuanShi = safe_float_v2(zuanShi)
                if zuanShi >= 1800:
                    re = TomatoOcrTap(7, 896, 96, 926, '特惠活动', offsetX=20, offsetY=-40)
                    if re:
                        re = TomatoOcrTap(158, 667, 223, 696, '1800')
                        if re:
                            tapSleep(360, 738)  # 点击购买
                        tapSleep(90, 1204)  # 返回活动页
                        tapSleep(90, 1204)  # 返回活动页
            tapSleep(90, 1204)  # 返回营地
            return True
        else:
            Toast(f'{taskName} - 未找到入口')
            return False

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
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
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
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
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

    # 旅行活动翻页
    def huoDongSwipeDown(self):
        # -- 返回活动最后一屏
        for i in range(5):
            swipe(364, 1133, 680, 51, dur=400)
            sleep(2)
            re = CompareColors.compare("276,1128,#EBE4D3|296,1126,#ECE4D3|311,1125,#EBE4D3|339,1125,#EEE7D6")
            if re:
                break

    # 登录好礼
    def dengLuHaoLi(self):
        if 功能开关["登录好礼"] == 0:
            return
        if 任务记录["登录好礼-完成"] == 1:
            return
        Toast('日常 - 登录好礼 - 开始')

        # 返回首页
        self.homePage()

        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
        # 判断是否在营地页面
        hd1 = TomatoOcrTap(12, 1110, 91, 1135, "旅行活动", 40, -20)
        hd2 = TomatoOcrTap(11, 1111, 92, 1134, "旅行活动", 40, -20)
        if hd1 == False and hd2 == False:
            return

        isFind, x, y = imageFind('登录好礼')
        if not isFind:
            # -- 返回活动最后一屏
            self.huoDongSwipeDown()

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
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
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
        else:
            res = TomatoOcrTap(412, 1076, 511, 1101, "大容量充磁")
            sleep(8)  # 等待动画
            tapSleep(360, 1040)  # 点击空白处
            tapSleep(360, 1040)  # 点击空白处

            tapSleep(75, 325)  # 领取回收物进度奖励
            tapSleep(76, 335)  # 领取回收物进度奖励
            tapSleep(360, 1040)  # 点击空白处
            tapSleep(360, 1040)  # 点击空白处

        re = CompareColors.compare("682,1180,#F56043|683,1180,#F56143|682,1183,#F35E41")  # 伊尼兰特红点
        if not re:
            Toast('宝藏湖 - 伊尼兰特 - 能量不足')
            return
        if re:
            # res = TomatoOcrTap(554, 1239, 636, 1265, "伊尼兰特")
            tapSleep(660, 1227, 0.8)  # 伊尼兰特
            re1 = CompareColors.compare("123,277,#F46245|123,274,#F76246|124,279,#F16145")
            if re1:
                Toast('宝藏湖 - 领取累积奖励')
                tapSleep(90, 317, 0.8)  # 点击累积奖励
                tapSleep(363, 1019, 0.8)  # 点击领取
                tapSleep(577, 1133, 0.8)  # 点击空白处
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
        res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.5)
        # 判断是否在营地页面
        res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
        if not res:
            return

        res = TomatoOcrFindRangeClick("BBQ派对", x1=97, y1=544, x2=180, y2=1051, offsetX=40, offsetY=-40,
                                      sleep1=1.5)  # 进入BBQ派对
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
        re, level = TomatoOcrText(369, 220, 396, 255, "层数")
        Toast(f'当前层数{level} - 非大奖层')
        nextLevel = False
        for l in range(3):
            re1 = imageFindClick('塔莎委托-下一层', confidence1=0.75, x1=78, y1=514, x2=645, y2=1090)
            re2 = imageFindClick('塔莎委托-下一层2', confidence1=0.75, x1=78, y1=514, x2=645, y2=1090)
            re3 = imageFindClick('塔莎委托-下一层3', confidence1=0.75, x1=78, y1=514, x2=645, y2=1090)
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
                                        rect=[75, 511, 366, 610], diff=0.8)
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

        re, coin = TomatoOcrText(603, 80, 674, 105, "剪刀")
        coin = safe_float_v2(coin)
        if coin > 50:
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

            # 自动挖掘
            res = TomatoOcrTap(462, 1144, 573, 1177, "自动挖掘", 10, 10)
            if res:
                Toast('自动挖掘')
                sleep(10)
        else:
            Toast('自动挖掘 - 剪刀不足')

        tapSleep(330, 1166)  # 点击空白处
        tapSleep(330, 1166)  # 点击空白处

        # 兑换商店
        re, coin = TomatoOcrText(105, 287, 161, 303, "金币")
        coin = safe_float_v2(coin)
        if coin > 50:
            Toast('兑换商店')
            tapSleep(116, 247, 3)
            re, x, y = TomatoOcrFindRange('星钻', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy')
            if re:
                res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                if '已售' in tmpText:  # 兜底售罄->售馨
                    res = True
                if not res:
                    TomatoOcrFindRangeClick('星钻', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy', offsetY=80)
                    self.shopBuy()
                else:
                    Toast('星钻 - 已购买')

                re, x, y = TomatoOcrFindRange('唤兽', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy')
                if re:
                    res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                    if '已售' in tmpText:  # 兜底售罄->售馨
                        res = True
                    if not res:
                        TomatoOcrFindRangeClick('唤兽', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy', offsetY=80)
                        self.shopBuy()
                    else:
                        Toast('唤兽 - 已购买')

                re, x, y = TomatoOcrFindRange('门票', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy')
                if re:
                    res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                    if '已售' in tmpText:  # 兜底售罄->售馨
                        res = True
                    if not res:
                        TomatoOcrFindRangeClick('门票', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy', offsetY=80)
                        self.shopBuy()
                    else:
                        Toast('门票 - 已购买')

                    re, x, y = TomatoOcrFindRange('传说经验', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy')
                    if re:
                        res, tmpText = TomatoOcrText(x - 20, y + 110, x + 60, y + 150, "已售罄")
                        if '已售' in tmpText:  # 兜底售罄->售馨
                            res = True
                        if not res:
                            TomatoOcrFindRangeClick('传说经验', x1=99, y1=312, x2=630, y2=1106, match_mode='fuzzy',
                                                    offsetY=80)
                            self.shopBuy()
                        else:
                            Toast('传说经验 - 已购买')

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
                point = FindColors.find(
                    "480,266,#384458|480,273,#384458|475,273,#FDFDFD|468,273,#384458|480,282,#384458",
                    rect=[61, 72, 565, 484], diff=0.95)  # 已领取门票，灰色状态
                if point:
                    Toast('骑兽乐园 - 已领取门票')
                else:
                    Toast('骑兽乐园 - 领取门票')
                    re = FindColors.find("129,158,#C7C2FB|129,153,#A2C4F9|135,156,#A1A9DC|127,162,#DABEEF",
                                         rect=[61, 72, 565, 484], diff=0.93)
                    if re:
                        tapSleep(re.x + 20, re.y + 20, 2)
                    else:
                        tapSleep(188, 321, 2)  # 点击门票（固定位置）
                    tapSleep(540, 655, 1.5)  # 点击空白处关闭
                    tapSleep(540, 655, 1.5)  # 点击空白处关闭

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
            if 功能开关["自动讲述领取绮想妙成真"] == 0:
                needCount = safe_int(功能开关["讲述故事次数"])
                if needCount == '':
                    needCount = 0
                if needCount > 10:
                    needCount = 10  # 单次任务最多操作10次
                if needCount > 0:
                    attempt = 0
                    # 关闭批量讲述
                    res, _ = TomatoOcrText(317, 1054, 401, 1082, "讲述故事")
                    if not res:
                        tapSleep(515, 1088)
                    while attempt < needCount:
                        Toast(f'开始讲述故事{attempt}/{needCount}次')
                        res = TomatoOcrTap(319, 1062, 398, 1083, "讲述故事")
                        res = TomatoOcrTap(319, 1062, 398, 1083, "结局揭秘")
                        sleep(2)
                        res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                        res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                        tapSleep(170, 1090)  # 点击空白处
                        attempt = attempt + 1

            if 功能开关["自动讲述领取绮想妙成真"] == 1:
                # 开启批量讲述
                res, _ = TomatoOcrText(317, 1054, 401, 1082, "讲述故事")
                if res:
                    tapSleep(515, 1088)
                for k in range(10):
                    # 识别剩余可领取次数
                    res, availableCount = TomatoOcrText(91, 254, 205, 285, " 可领取次数")
                    availableCount = safe_int_v2(availableCount.replace("可领取", "").replace("次", ""))
                    if availableCount > 0:
                        Toast(f'开始讲述故事,待领取红色招式/{availableCount}次')
                        tapSleep(360, 1081, 0.8)  # 讲述故事
                        sleep(2)
                        res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取
                        res = TomatoOcrTap(359, 969, 399, 992, "收取")  # 一键收取

            任务记录["日常-招式创造-完成"] = 1

    # 兑换码领取
    def duihuanma(self):
        if 功能开关["兑换码领取"] == 0:
            return

        if 任务记录["兑换码领取-完成"] == 1:
            return

        Toast('日常 - 兑换码领取 - 开始')

        duihuanmas = []
        for duihuanma in duihuanmas:
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

            tapSleep(45, 342, 1)  # 设置
            res = TomatoOcrTap(268, 921, 326, 942, "兑换码", offsetX=10, offsetY=10, sleep1=0.7)
            if not res:
                TomatoOcrTap(101, 1188, 125, 1214, "回", 10, 10)
                return

            res = TomatoOcrTap(249, 636, 344, 667, "输入兑换码", offsetX=10, offsetY=10, sleep1=0.7)
            if res:
                action.input(duihuanma)
                tapSleep(571, 517, 0.3)  # 点击空白处确认输入
                for i in range(1, 3):
                    # 检查是否已输入
                    notInput = TomatoOcrTap(249, 636, 344, 667, "输入兑换码", offsetX=10, offsetY=10, sleep1=0.7)
                    if notInput:
                        sleep(1)
                        action.input(duihuanma)
                        sleep(1)
                        tapSleep(571, 517, 0.5)  # 点击空白处确认输入
                    if not notInput:
                        TomatoOcrTap(331, 760, 386, 787, "确定", 5, 5, sleep1=0.7)
                        break

            任务记录["兑换码领取-完成"] = 1
            tapSleep(361, 1205)  # 点击空白处
            tapSleep(361, 1205)  # 点击返回
            tapSleep(361, 1205)  # 点击冒险

    # 邮件领取
    def youJian(self):
        if 功能开关["邮件领取"] == 0:
            return

        if 任务记录["邮件领取-完成"] == 1:
            return

        Toast('日常 - 邮件领取 - 开始')

        # 判断是否在营地页面
        res = False
        for k in range(3):
            res, _ = TomatoOcrText(12, 1110, 91, 1135, "旅行活动")
            if not res:
                # 返回首页
                Toast('营地任务 - 邮件领取 - 重新寻找活动入口')
                self.homePage()
                res = TomatoOcrTap(125, 1202, 187, 1234, "营地", sleep1=1.6)
            else:
                break
        if not res:
            Toast('营地任务 - 邮件领取 - 未找到活动入口')

        # 判断邮件已完成
        re, x, y = imageFind('营地-邮箱-已领取', x1=206, y1=653, x2=367, y2=760)
        if re:
            Toast('营地任务 - 邮件领取 - 识别已完成')
            任务记录["邮件领取-完成"] = 1
            sleep(1)
            return

        tapSleep(301, 697, 4)  # 邮件
        res = TomatoOcrTap(463, 1030, 510, 1061, "领取")
        if not res:
            TomatoOcrTap(67, 1182, 121, 1221, "返回", 10, 10)
            return
        else:
            任务记录["邮件领取-完成"] = 1
        sleep(2)
        tapSleep(352, 1202)  # 点击空白处
        tapSleep(352, 1202)  # 点击空白处
        tapSleep(352, 1202)  # 点击返回冒险

    def quitTeam(self):
        if 功能开关["fighting"] == 1:
            return

        # 匹配组队中灰色底UI
        # re = FindColors.find(
        #     "610,560,#29392C|610,562,#293A2D|610,565,#293A2D|614,561,#293A2C|614,563,#29392C|613,568,#2A3A2D",
        #     rect=[592, 531, 699, 680])
        # if not re:
        #     re = CompareColors.compare("576,654,#E2DFD2|565,651,#8F9290|584,656,#344D5E|574,662,#E2DFD2")
        #     if not re:
        #         return

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
            res2 = TomatoOcrFindRangeClick('正在组队', whiteList='正在组队', x1=549, y1=340, x2=699, y2=696, sleep1=0.8)
            # res2 = TomatoOcrTap(631, 558, 699, 581, "正在组队")
            if not res2:
                # res3 = TomatoOcrFindRangeClick('匹配中', whiteList='匹配中')
                res3 = TomatoOcrTap(632, 570, 684, 598, "匹配中")
                if not res3:
                    res4 = TomatoOcrTap(311, 1156, 407, 1182, "匹配中")  # 大暴走匹配中
        res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
        if res1 or res2 or res3 or res4 or res5 or res6:
            if 功能开关["fighting"] == 1:
                return
            功能开关["needHome"] = 0
            功能开关["fighting"] = 1

            teamExist = TomatoOcrTap(500, 184, 579, 214, "离开队伍", 20, 20, sleep1=0.8)
            if not teamExist:
                teamExist = TomatoOcrFindRangeClick('离开队伍', whiteList='离开队伍', x1=416, y1=126, x2=628, y2=284)
            if teamExist:
                teamExist = TomatoOcrFindRangeClick('确定', whiteList='确定', x1=105, y1=304, x2=631, y2=953)
                if teamExist:
                    Toast('日常 - 退出组队')
                    功能开关["fighting"] = 0
                    return True

            teamStatus = TomatoOcrFindRangeClick(keyword='取消', x1=80, y1=160, x2=636, y2=1153)  # 临时兜底匹配超时未关闭确定
            if not teamStatus:
                teamStatus = TomatoOcrFindRangeClick(keyword='匹配中', x1=80, y1=160, x2=636, y2=1153)
            if teamStatus:
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
        # 功能开关["fighting"] = 0
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

    def checkGameStatus(self, needForceCheck=False):
        try:
            if 功能开关['技能进入战斗后启动'] == 1 or 功能开关['AI进入战斗后启动'] == 1 or 功能开关[
                '暴走进入战斗后启动']:
                return True

            # re1 = CompareColors.compare(
            #     "657,324,#F3EDDD|659,324,#F3EDDD|664,331,#F3EDDD|676,329,#F3EDDD|681,337,#F3EDDD|687,334,#F3EDDD")  # 战斗内队伍图标
            # if re1:
            #     Toast('战斗中-不检测游戏是否卡死')
            #     return

            diffTime = time.time() - 任务记录["首页卡死检测-倒计时"]
            if not needForceCheck and diffTime < 4 * 60:
                print(f'游戏卡死检测 - 倒计时{round((4 * 60 - diffTime) / 60, 2)}min')
                return True

            # 战斗中6分钟，强制检查是否卡死
            if not needForceCheck and 功能开关["fighting"] == 1 and diffTime < 4 * 60:
                return True

            res1, _ = TomatoOcrText(311, 588, 408, 637, "异地登录")
            if res1 and 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
                Toast('顶号等待中，跳过卡死检测')
                return True

            # 匹配行李图标亮着，新号为灰色，不处理
            if not needForceCheck:
                re = CompareColors.compare("287,1224,#AC8B62|285,1218,#AC8B62|285,1199,#9F7C55|287,1210,#9F7C55")
                if not re:
                    re = CompareColors.compare(
                        "240,1237,#191108|254,1242,#191108|255,1182,#292519|270,1177,#211C11|249,1174,#282519|279,1196,#191108")
                    if not re:
                        return True

            res1, _ = TomatoOcrText(584, 651, 636, 678, "同意")
            if res1:
                return True

            # 检测游戏是否卡死
            Toast('检测游戏是否卡死')
            任务记录["首页卡死检测-倒计时"] = time.time()

            # 避免与自动入队冲突
            功能开关["fighting"] = 1

            # 首页卡死检测（通过点击行李判断能否跳转成功）
            failCount = 0
            for i in range(6):
                # return3 = TomatoOcrTap(93, 1186, 126, 1220, '回', 10, 10)  # 简单尝试返回首页
                # res = TomatoOcrTap(326, 745, 393, 778, "确认")  # 点击战斗失败确认
                # TomatoOcrFindRangeClick('准备', x1=94, y1=276, x2=633, y2=1089)  # 避免点击开始瞬间队友离队，错误点击了开始匹配，兜底准备按钮
                res = TomatoOcrTap(233, 1205, 281, 1234, "行李", sleep1=0.7)

                re, equipNum = TomatoOcrText(498, 1042, 588, 1072, '装备数量')
                equipNum = equipNum.replace("/200", "")
                equipNum = safe_int(equipNum)
                任务记录['装备数量'] = equipNum

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
                        sleep(0.5)
                        Toast(f'游戏卡死，等待{i + 1}/6')
                        return1 = TomatoOcrTap(67, 1182, 121, 1221, '返回', 10, 10)
                        return3 = TomatoOcrTap(93, 1186, 126, 1220, '回', 10, 10)
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
                            if not re1 or not re2:
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
            rect=[61, 34, 322, 623], diff=0.95)
        if point:
            Toast('收起喊话窗口')
            tapSleep(point.x, point.y)

        point = CompareColors.compare(
            "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        if point:
            Toast('收起喊话窗口')
            tapSleep(107, 93)

    def shopBuy(self):
        re1, _ = TomatoOcrText(282, 400, 434, 459, '购买道具')
        if not re1:
            re1, _ = TomatoOcrText(330, 836, 388, 858, '购买')
        re2 = False
        if re1:
            re = TomatoOcrTap(475, 785, 513, 811, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrTap(473, 771, 514, 795, '最大', offsetX=5, offsetY=5)
            if not re:
                re = TomatoOcrTap(472, 783, 514, 807, '最大', offsetX=5, offsetY=5)
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
                    re = TomatoOcrFindRangeClick('购买', whiteList='购买', x1=93, y1=643, x2=618, y2=1004)
                # tapSleep(360, 855, 0.6)  # 购买
                if re:
                    tapSleep(101, 1065, 1)  # 点击空白处关闭
            tapSleep(101, 1065)  # 点击空白处关闭
            tapSleep(101, 1065)  # 点击空白处关闭


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
