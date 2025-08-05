# 导包
import time

from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关, 任务记录
from .shilian import ShiLianTask
from .daily import DailyTask
from .yingdi import YingDiTask
from ascript.android.screen import FindColors
import pymysql
import threading
from ascript.android.system import KeyValue

shilianTask = ShiLianTask()
dailyTask = DailyTask()
yingdiTask = YingDiTask()


# 实例方法
def main():
    global checkZBTime
    global checkQuitTeamTime
    checkZBTime = time.time()  # 兜底接收准备页面
    checkQuitTeamTime = time.time()  # 退队检查倒计时
    while True:
        if 功能开关["秘境自动接收邀请"] == 1 or 功能开关['梦魇自动接收邀请'] == 1 or 功能开关[
            '恶龙自动接收邀请'] == 1 or \
                功能开关['暴走自动接收邀请'] == 1 or 功能开关['终末战自动接收邀请'] == 1 or \
                功能开关['绝境自动接收邀请'] == 1 or 功能开关['调查队自动接收邀请'] == 1 or 功能开关[
            '斗歌会自动接收邀请'] == 1 or 功能开关['三魔头自动接收邀请'] == 1 or 功能开关[
            '桎梏之形自动接收邀请'] == 1 or 功能开关['使徒来袭自动接收邀请'] == 1:
            # res1, _ = TomatoOcrText(498,184,585,214, "离开队伍")
            # if res1:
            #     Toast('已在房间中，跳过组队邀请识别')
            #     continue

            login1 = CompareColors.compare(
                "202,419,#FCF8F0|200,426,#FCF8F0|195,460,#FCF8F0|292,426,#FCF8F0|328,438,#FCF8F0|404,421,#FCF8F0|427,467,#FCF8F0")  # 登录页 - 出发吧麦芬
            # if not login1:
            #     login1 = CompareColors.compare(
            #         "435,1201,#FABD59|424,1231,#F5AD4E|420,1215,#F7B554|296,1202,#F9BC58|295,1220,#F6B351|312,1213,#FFFFFF|328,1213,#FFFFFF|358,1216,#F7B554|382,1215,#FFFFFF")  # 角色页 - 开始冒险
            if login1:
                sleep(10)  # 等待 10 秒
                continue

            if 功能开关["fighting"] == 0:
                # 识别角色名称，做特殊逻辑
                if 任务记录["AI发言-广告开关"] == 0:
                    # if 任务记录["玩家名称"] in {'咸鱼搜麦乐芬', '养只狐狸', '那双眼动人', '风尘三尺剑', '霸王夜引弓',
                    #                             '倚仗数昏鸦', '渡渡'}:
                    任务记录["AI发言-广告开关"] = 1

                yingdiTask.HaoYouYinShen(needOpen=False)

                # 识别玩家所在旅团，做特殊逻辑
                if 功能开关["仅接收旅团成员邀请"] == 1 and (
                        任务记录["玩家-当前旅团"] == "" or time.time() - 任务记录["玩家-当前旅团-倒计时"] > 300):
                    Toast('开始识别所在旅团')
                    功能开关["fighting"] = 1
                    功能开关["needHome"] = 0
                    re = CompareColors.compare("250,99,#EDF2FB|253,101,#FFFFFF|261,104,#7CA3E0")  # 玩家右侧效果加成图标
                    if re:
                        tapSleep(49, 93, 1.3)  # 点击玩家头像
                        re = FindColors.find(
                            "442,956,#7DA2E2|453,956,#7DA2E2|445,969,#FFFFFF|437,978,#7DA2E2|448,978,#7DA2E2",
                            rect=[99, 929, 630, 1035], diff=0.95)
                        if re:
                            res, 任务记录["玩家-当前旅团"] = TomatoOcrText(409, 839, 570, 873, "旅团名称")
                            KeyValue.save('玩家-当前旅团', 任务记录["玩家-当前旅团"])
                            Toast(f'识别所在旅团-{任务记录["玩家-当前旅团"]}')
                            任务记录["玩家-当前旅团-倒计时"] = time.time()
                        tapSleep(355, 1209)  # 关闭玩家信息
                    功能开关["fighting"] = 0

                # 识别玩家当前关卡，做特殊逻辑
                if 任务记录["玩家-当前关卡"] == "" or time.time() - 任务记录["玩家-当前关卡-倒计时"] > 900:
                    Toast('开始检测最新关卡')
                    isFind = False
                    # dailyTask.checkGameStatus()
                    for k in range(3):
                        功能开关["fighting"] = 1
                        功能开关["needHome"] = 0
                        # 功能开关["noHomeMust"] = 1
                        res = TomatoOcrTap(645, 505, 691, 527, "试炼", sleep1=0.8)
                        if not res:
                            res = TomatoOcrTap(650, 522, 688, 544, "试炼", sleep1=0.8)
                        if res:
                            re = imageFindClick('秘境之间', x1=85, y1=53, x2=636, y2=700)
                            if re:
                                isFind = True
                                break
                            if not re:
                                re = TomatoOcrFindRangeClick('秘境之间', x1=374, y1=101, x2=562, y2=156)
                            if not re:
                                Toast("未找到试炼入口 - 重新尝试")
                        # else:
                        #     Toast("未找到试炼入口 - 待重新尝试")
                    if isFind:
                        shilianTask.openTreasure(noNeedOpen=1)
                        tiliPoint = FindColors.find(
                            "577,363,#F4DB77|577,358,#F3D76B|585,364,#888A93|585,356,#888992|592,356,#D9DADC|601,364,#F3F3F4",
                            rect=[72, 205, 655, 1120], diff=0.9)
                        if tiliPoint:
                            任务记录["玩家-当前关卡-倒计时"] = time.time()
                            # print(tiliPoint)
                            x1 = tiliPoint.x - 280
                            y1 = tiliPoint.y - 25
                            x2 = x1 + 235
                            y2 = y1 + 30
                            res, tmp = TomatoOcrText(x1, y1, x2, y2, "当前关卡")  # 关卡
                            if tmp != "":
                                res, nandu = TomatoOcrText(tiliPoint.x - 237, tiliPoint.y + 25, tiliPoint.x - 200,
                                                           tiliPoint.y + 45, "难度")  # 关卡难度
                                if nandu == '挑战' or nandu == '姚战':
                                    任务记录['玩家-当前关卡'] = tmp + "（挑战）"
                                else:
                                    任务记录['玩家-当前关卡'] = tmp
                                Toast(f"识别最新关卡-{任务记录['玩家-当前关卡']}-带队时自动开启宝箱")

                            # 补充体力
                            # 识别剩余体力不足40时，尝试补充
                            res2, availableTiLi = TomatoOcrText(599, 81, 632, 101, "剩余体力")  # 20/60
                            availableTiLi = safe_int(availableTiLi)
                            if 功能开关["秘境不开宝箱"] == 0 and (
                                    availableTiLi == "" or availableTiLi < 40):  # 识别剩余体力不足40时，尝试补充
                                shilianTask.tili()
                            tapSleep(98, 1212)  # 返回首页
                            tapSleep(98, 1212)  # 返回首页
                            tapSleep(98, 1212)  # 返回首页
                            sleep(1)
                    功能开关["fighting"] = 0
                    # 功能开关["noHomeMust"] = 0

            if 功能开关["fighting"] == 0 and 功能开关["home_fighting"] == 0:
                Toast('等待组队邀请')
                waitInvite()
                dailyTask.checkGameStatus()
        sleep(1)  # 等待 5 秒


def waitInvite():
    tmpBx = 功能开关["秘境不开宝箱"]
    功能开关["秘境不开宝箱"] = 1

    global checkZBTime
    global checkQuitTeamTime
    res1, _ = TomatoOcrText(584, 651, 636, 678, "同意")
    res2 = False
    res3 = False
    if time.time() - checkZBTime > 5:
        res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备
        res3, _ = TomatoOcrText(450, 651, 506, 683, "准备")  # 恶龙准备
        checkZBTime = time.time()

    fight_type = ''
    if not res1 and not res2 and not res3:
        # res = TomatoOcrTap(615, 558, 686, 582, "正在组队")
        # sleep(1)
        # res, _ = TomatoOcrText(402, 337, 442, 361, "险境")
        # if res:
        #     fight_type = '绝境带队'
        #
        # if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
        #     Toast('不退出房间')
        # else:
        # 房间 - 关闭邀请玩家
        # re, _ = TomatoOcrText(318, 222, 401, 247, '邀请玩家')
        # if re:
        #     tapSleep(590, 1076)
        #     tapSleep(590, 1076)
        if time.time() - checkQuitTeamTime > 3:
            quitTeamRe = shilianTask.quitTeam()
            checkQuitTeamTime = time.time()
        功能开关["秘境不开宝箱"] = tmpBx
        return

    if res1:
        if 功能开关["仅接收旅团成员邀请"] == 1 or 功能开关["仅接收关注粉丝邀请"] == 1 or 功能开关[
            "仅接收互关好友邀请"] == 1:
            for p in range(3):
                isEachLike = False
                tmp = ''
                isFindInvite = False
                for o in range(4):
                    功能开关["fighting"] = 1
                    功能开关["needHome"] = 0
                    tapSleep(415, 544, 1.2)  # 点击右侧邀请玩家头像
                    re = FindColors.find(
                        "442,956,#7DA2E2|453,956,#7DA2E2|445,969,#FFFFFF|437,978,#7DA2E2|448,978,#7DA2E2",
                        rect=[99, 929, 630, 1035], diff=0.95)
                    if re:
                        # 判断点进了头像
                        isFindInvite = True
                        res, 任务记录["战斗-房主旅团"] = TomatoOcrText(413, 839, 576, 871, "旅团名称")
                        isEachLike, tmp = TomatoOcrText(147, 991, 231, 1016, "互相关注")
                        break

                if not isFindInvite:
                    Toast(f'未识别到邀请玩家信息，默认接收邀请')
                else:
                    needReject = True
                    if needReject == True and 功能开关["仅接收旅团成员邀请"] == 1:
                        if 任务记录["玩家-当前旅团"] == "":
                            任务记录["玩家-当前旅团"] = KeyValue.get('玩家-当前旅团', '')
                        if 任务记录["战斗-房主旅团"] != "" and 任务记录["玩家-当前旅团"] != "" and not has_common_chars(
                                任务记录["玩家-当前旅团"], 任务记录["战斗-房主旅团"], 2):
                            Toast(f'非旅团成员，拒绝组队邀请 - {任务记录["战斗-房主旅团"]}/{任务记录["玩家-当前旅团"]}')
                            sleep(0.5)
                        else:
                            if 任务记录["玩家-当前旅团"] == "":
                                Toast('未识别到玩家所在旅团，默认接受邀请')
                                sleep(1)
                            elif 任务记录["战斗-房主旅团"] == "":
                                Toast('未识别到房主所在旅团，默认接受邀请')
                                sleep(1)
                            else:
                                Toast('接受旅团成员组队邀请')
                            needReject = False

                    if needReject == True and 功能开关["仅接收关注粉丝邀请"] == 1:
                        res, tmp = TomatoOcrText(206, 991, 259, 1016, "回关")
                        if not res:
                            res, tmp = TomatoOcrText(206, 991, 259, 1016, "已关注")
                        if not res and tmp != "":
                            Toast('非关注粉丝，拒绝组队邀请')
                            sleep(0.5)
                        else:
                            Toast('接受关注粉丝组队邀请')
                            needReject = False

                    if needReject == True and 功能开关["仅接收互关好友邀请"] == 1:
                        if not isEachLike:
                            Toast('非互关好友，拒绝组队邀请')
                            sleep(0.5)
                        else:
                            Toast('接受互关好友组队邀请')
                            needReject = False

                    if needReject:
                        res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                        tapSleep(71, 1216)  # 点击返回
                        功能开关["秘境不开宝箱"] = tmpBx
                        return
                    if tmp != "" or 任务记录["战斗-房主旅团"] != "":
                        break

        功能开关["fighting"] = 1
        功能开关["needHome"] = 0
        resFightName, 任务记录["战斗-关卡名称"] = TomatoOcrText(374, 609, 655, 640, "关卡名称")  # 关卡名称
        resTeamName, 任务记录["战斗-房主名称"] = TomatoOcrText(456, 517, 570, 542, "房主名称")  # 房主名称
        print(f'{任务记录["战斗-关卡名称"]}-{任务记录["玩家-当前关卡"]}-{tmpBx}')
        功能开关["史莱姆选择"] = '暴走雷电大王'
        if '烈焰' in 任务记录["战斗-关卡名称"]:
            功能开关["史莱姆选择"] = '暴走烈焰大王'
        elif '水波' in 任务记录["战斗-关卡名称"]:
            功能开关["史莱姆选择"] = '暴走水波大王'
        elif '雷电' in 任务记录["战斗-关卡名称"]:
            功能开关["史莱姆选择"] = '暴走雷电大王'
        elif '深林' in 任务记录["战斗-关卡名称"]:
            功能开关["史莱姆选择"] = '暴走深林大王'
        # 判断带队为最新关卡，默认开启宝箱
        needOpen = False
        # 非挑战关卡，对比名称相同
        if "挑战" not in 任务记录["战斗-关卡名称"] and has_common_chars(任务记录["玩家-当前关卡"],
                                                                        任务记录["战斗-关卡名称"]):
            needOpen = True
        # 挑战关卡（当前仅一个），对比都有 挑战 关键字
        if "挑战" in 任务记录["玩家-当前关卡"] and "挑战" in 任务记录["战斗-关卡名称"]:
            needOpen = True
        if needOpen and tmpBx == 0:
            # 若配置要求不开宝箱，则最新关卡也不开启
            Toast(f'带队最新关卡，战斗后开启宝箱,{任务记录["玩家-当前关卡"]}-{任务记录["战斗-关卡名称"]}')
            功能开关["秘境不开宝箱"] = 0
            # 功能开关["补充体力次数"] = 3
        else:
            Toast(f'非最新关卡,不开启宝箱,{任务记录["玩家-当前关卡"]}-{任务记录["战斗-关卡名称"]}')

        fight_type = checkFightType()
        if fight_type == '':
            Toast('未识别的战斗类型，拒绝邀请')
            功能开关["fighting"] = 0
            return

        if fight_type == '梦魇带队':
            if 功能开关['梦魇自动接收邀请'] == 0:
                Toast('梦魇带队未开启，拒绝梦魇组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意梦魇组队邀请')

        if fight_type == '恶龙带队':
            if 功能开关['恶龙自动接收邀请'] == 0:
                Toast('恶龙带队未开启，拒绝恶龙组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意恶龙组队邀请')

        if fight_type == '暴走带队':
            if 功能开关['暴走自动接收邀请'] == 0:
                Toast('暴走带队未开启，拒绝暴走组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意暴走组队邀请')

        if fight_type == '秘境带队':
            if 功能开关['秘境自动接收邀请'] == 0:
                Toast('秘境带队未开启，拒绝秘境组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意秘境组队邀请')
        if fight_type == '绝境带队':
            if 功能开关['绝境自动接收邀请'] == 0:
                Toast('绝境带队未开启，拒绝绝境组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意绝境组队邀请')
        if fight_type == '终末战带队':
            if 功能开关['终末战自动接收邀请'] == 0:
                Toast('终末战带队未开启，拒绝终末战组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意终末战组队邀请')
        if fight_type == '调查队带队':
            if 功能开关['调查队自动接收邀请'] == 0:
                Toast('调查队带队未开启，拒绝调查队组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意调查队组队邀请')
        if fight_type == '忆战回环带队':
            Toast('忆战回环带队，自动拒绝')
            sleep(0.5)
            res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
            功能开关["fighting"] = 0
            return

        if fight_type == '三魔头带队':
            if 功能开关['三魔头自动接收邀请'] == 0:
                Toast('三魔头带队未开启，拒绝三魔头组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意三魔头组队邀请')

        if fight_type == '斗歌会带队':
            if 功能开关['斗歌会自动接收邀请'] == 0:
                Toast('斗歌会带队未开启，拒绝斗歌会组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意斗歌会组队邀请')

        if fight_type == '使徒来袭带队':
            if 功能开关['使徒来袭自动接收邀请'] == 0:
                Toast('使徒来袭带队未开启，拒绝使徒来袭组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意使徒来袭组队邀请')

        if fight_type == '桎梏之形带队':
            if 功能开关['桎梏之形自动接收邀请'] == 0:
                Toast('桎梏之形带队未开启，拒绝桎梏之形组队邀请')
                sleep(0.5)
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意桎梏之形组队邀请')

        # 黑名单判断
        blackList = (功能开关['秘境带队黑名单'] + '|' + 功能开关['绝境带队黑名单'] + '|'
                     + 功能开关['终末带队黑名单'] + '|' + 功能开关['恶龙带队黑名单'] + '|'
                     + 功能开关['梦魇带队黑名单'])
        blackList = blackList.split('|')
        for black in blackList:
            if black == '':
                continue
            if black in 任务记录["战斗-关卡名称"] or black in 任务记录["战斗-房主名称"]:
                Toast('命中黑名单，拒绝组队邀请')
                res1 = TomatoOcrTap(471, 654, 509, 674, "拒绝")
                功能开关["fighting"] = 0
                return

        res1 = TomatoOcrTap(584, 651, 636, 678, "同意", sleep1=0.6)
        if res1 and fight_type == '秘境带队':
            # 体力用尽不再提醒
            # 判断体力用尽提示
            res, _ = TomatoOcrText(333, 744, 385, 771, "确定")
            if res:
                tapSleep(285, 710)  # 点击不再提醒
            res = TomatoOcrTap(333, 744, 385, 771, "确定", sleep1=0.8)

    waitFight = False
    findDoneStatus = False
    teamShout = False
    totalWait = 50
    checkTreasure = time.time()  # 兜底房间宝箱检查页面
    checkYaoQingTime = time.time()  # 兜底检查邀请玩家页面
    if 功能开关["自动离房等待时间"] != "":
        totalWait = safe_int_v2(功能开关["自动离房等待时间"].replace('s', '').replace('S', ''))
    start_time = int(time.time())
    for i in range(100):
        current_time = int(time.time())
        elapsed = current_time - start_time
        if elapsed >= totalWait:
            Toast(f'等待进入战斗超时，退出组队')
            break

        # 兜底，已在队伍中时，停止返回操作
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0

        # 行李页，返回首页
        tmp = CompareColors.compare(
            "230,1202,#FCF8EE|240,1205,#FCF8EE|258,1207,#F8ECCD|271,1205,#FDF5E6|257,1223,#FAEFD5|273,1231,#FCF8EE")
        if tmp:
            Toast('行李页-返回首页')
            tapSleep(355, 1202)
        Toast(f'{fight_type}-等待队长开始{elapsed}/{totalWait}s')
        if time.time() - checkYaoQingTime > 5:
            shilianTask.openTreasure(noNeedOpen=1)
            checkTreasure = time.time()

        # 兜底，已在队伍中时，停止返回操作
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0

        # 返回房间
        failTeam = 0
        for j in range(5):
            res6, _ = TomatoOcrText(501, 191, 581, 217, "离开", match_mode='fuzzy')  # 已在队伍页面，直接退出
            if not res6:
                res6, _ = TomatoOcrText(503, 186, 582, 213, "队伍", match_mode='fuzzy')  # 已在队伍页面，直接退出
            if res6:
                break

            res5, _, _ = TomatoOcrFindRange('跳过', confidence1=0.9, x1=522, y1=17, x2=685, y2=110)
            res6, _ = TomatoOcrText(644, 782, 691, 806, '喊话')
            if res5 or res6:
                break

            res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备
            res3, _ = TomatoOcrText(450, 651, 506, 683, "准备")  # 恶龙准备
            if res2 or res3:
                break

            res1 = TomatoOcrTap(616, 613, 688, 633, "组队", match_mode='fuzzy')
            if not res1:
                res1 = TomatoOcrTap(617, 613, 690, 637, "组队", match_mode='fuzzy')
            if not res1:
                res1 = TomatoOcrTap(620, 625, 682, 650, "匹配中")
            # 兜底入队失败
            res2, _ = TomatoOcrText(584, 651, 636, 678, "同意")
            if res2:
                resFightName, 任务记录["战斗-关卡名称"] = TomatoOcrText(374, 609, 655, 640, "关卡名称")  # 关卡名称
                resTeamName, 任务记录["战斗-房主名称"] = TomatoOcrText(456, 514, 650, 546, "房主名称")  # 房主名称
                fight_type = checkFightType()
                res2 = TomatoOcrTap(584, 651, 636, 678, "同意", sleep1=0.8)
                # 判断体力用尽提示
                res = TomatoOcrTap(333, 744, 385, 771, "确定", sleep1=0.8)
                # res = TomatoOcrFindRangeClick("确定", sleep1=0.3, whiteList='确定', x1=105, y1=290, x2=625, y2=1013)

            if not res1 and not res2:
                Toast(f'未进入房间{j}/ 5')
                tapSleep(134, 1060, 0.1)
                shou_ye1, _ = TomatoOcrText(625, 363, 709, 388, "冒险手册")
                if shou_ye1:
                    failTeam = failTeam + 3
                else:
                    failTeam = failTeam + 1
            sleep(0.3)
        if failTeam >= 5:
            break

        # 房间 - 关闭邀请玩家
        if time.time() - checkYaoQingTime > 5:
            re, _ = TomatoOcrText(318, 222, 401, 247, '邀请玩家')
            if re:
                tapSleep(590, 1076)
                tapSleep(590, 1076)
            checkYaoQingTime = time.time()

        # 房间 - 特殊状态识别
        if fight_type == '梦魇带队' and not findDoneStatus:
            re1, _ = TomatoOcrText(427, 374, 489, 399, "24/24")
            re2 = False
            wujinLevel = 0
            if not re1:
                re2, _ = TomatoOcrText(431, 375, 486, 404, "24/24")
                if not re2:
                    re4, wujinLevel = TomatoOcrText(423, 374, 474, 400, "无尽层数")
                    wujinLevel = safe_int_v2(wujinLevel)
            if re1 or re2 or (wujinLevel >= 72 and 功能开关['梦魇无尽自动离队'] == 0) or (
                    功能开关['梦魇无尽自动离队'] == 1):
                findDoneStatus = True
                Toast('梦魇 - 已完成挑战 - 进入战斗后自动留影')
            else:
                Toast('梦魇 - 未完成挑战 - 进入战斗后等待战斗结束')
                fight_type = '梦魇挑战'

        if fight_type == '恶龙带队' and not findDoneStatus:
            # 判断是否为当前等级地图
            re, levelName1 = TomatoOcrText(365, 283, 440, 307, '建议职业')
            re, levelName2 = TomatoOcrText(128, 601, 264, 621, '当前职业')
            if levelName1 in levelName2:
                # 判断是否未开宝箱
                re1 = CompareColors.compare(
                    "532,358,#F4D387|535,347,#FAE69D|535,336,#D48D2F|544,334,#FDF5BC|544,348,#E7C783|555,355,#F9E79F")
                # 未开宝箱，不退队
                if not re1:
                    Toast('恶龙 - 未完成挑战 - 进入战斗后等待战斗结束')
                    fight_type = '恶龙挑战'
                else:
                    findDoneStatus = True
                    Toast('恶龙 - 已完成挑战 - 进入战斗后自动留影')
            else:
                findDoneStatus = True
                Toast('恶龙 - 已完成挑战 - 进入战斗后自动留影')

        if fight_type == '桎梏之形带队' and not findDoneStatus:
            re, level = TomatoOcrText(431, 347, 492, 375, "阶段")
            import re as rep
            level = int(rep.findall(r'\d+', level)[0]) if rep.findall(r'\d+', level) else None
            level = safe_int_v2(level)
            print(level)
            if level >= 100:
                findDoneStatus = True
                Toast("桎梏之形 - 已完成挑战 - 进入战斗后自动留影")
            else:
                Toast('桎梏之形 - 未完成挑战 - 进入战斗后等待战斗结束')
                fight_type = '桎梏之形挑战'

        # 关闭喊话窗口
        # point = CompareColors.compare(
        #     "108,94,#6884BA|102,86,#6584B9|121,89,#6584B9|107,101,#F4EEDE|105,97,#6989B9")
        # if point:
        #     Toast('收起喊话窗口')
        #     tapSleep(107, 93)

        # # 关闭未结算宝箱
        # re = CompareColors.compare("492,519,#F4E37D|491,523,#F4D86C|494,528,#EFD06E")
        # if re:
        #     Toast('关闭未结算宝箱')
        #     tapSleep(353, 1046, 0.8)
        #     tapSleep(364, 738, 0.8)

        # 判断队友全部离队，退出房间
        allQuit = False
        if fight_type == '恶龙带队' or fight_type == '恶龙挑战':
            allQuit, _ = TomatoOcrText(325, 558, 393, 585, "等待加入")
            if not allQuit:
                allQuit = CompareColors.compare(
                    "186,405,#F2C173|189,405,#F2C173|192,405,#FFF5B4|194,405,#F4C376|192,399,#FCF1B3")  # 判断是否成为房主
        else:
            hasTeam, _ = TomatoOcrText(291, 973, 427, 1008, "队长", match_mode='fuzzy')
            if not hasTeam:
                allQuit, _ = TomatoOcrText(168, 804, 233, 831, "等待加入")
                if not allQuit:
                    team4 = CompareColors.compare(
                        "217,280,#FDF3B6|221,279,#F2C274|224,280,#FFF6B5|221,276,#FFF7B6|230,287,#EBE3A7")  # 判断是否成为房主
                    team5 = CompareColors.compare(
                        "187,404,#F2C174|189,404,#F3C379|191,400,#FFF7B6|192,405,#FFF5B4|198,400,#E9DAA2")  # 终末战 - 判断是否成为房主
                    team6 = CompareColors.compare("192,406,#FFF6B5|192,403,#FFF4B3|192,400,#FFFFB6")
                    if team4 or team5 or team6:
                        allQuit = True

        if allQuit:
            Toast('队友全部离队')
            quitTeamRe = shilianTask.quitTeam()
            sleep(1)
            break

        res6, _ = TomatoOcrText(501, 191, 581, 217, "离开", match_mode='fuzzy')  # 已在队伍页面，直接退出
        if not res6:
            res6, _ = TomatoOcrText(503, 186, 582, 213, "离开", match_mode='fuzzy')  # 已在队伍页面，直接退出
        if res6:
            if not teamShout:
                count, last_time = shilianTask.daiDuiCount()
                content = f'{fight_type}-等待开始~{任务记录["战斗-房主名称"]}'
                # if count < 3:
                #     shilianTask.teamShoutAI(f'{content}-初次相遇~给个关注叭', shoutType='room')
                # else:
                #     shilianTask.teamShoutAI(f'{content}-第{count}次相遇~祝你游戏开心',
                #                             shoutType='room')
                teamShout = True
                Toast(f'{content}-第{count}次相遇')

        waitFight = shilianTask.WaitFight(fightType=fight_type)
        if waitFight:
            Toast('战斗结束 - 等待下次带队')
            # 战斗结束后不立即返回，先处理队伍中的逻辑
            功能开关["fighting"] = 1
            功能开关["needHome"] = 0
            任务记录['AI发言-上一次发言'] = []
            任务记录['AI发言-检测队友关注'] = 0
            任务记录["战斗-推荐战力"] = 0
            waitTime = 0
            start_time = int(time.time())
            teamShout = False
            # 恶龙/绝境/终末，仅挑战1次，可直接退队
            if fight_type == '恶龙带队' or fight_type == '恶龙挑战' or fight_type == '终末战带队' or fight_type == '桎梏之形带队' or fight_type == '桎梏之形挑战' or fight_type == '三魔头带队':
                Toast('退出组队')
                for z in range(2):
                    quitRes = shilianTask.quitTeam()
                    if quitRes:
                        break
                    sleep(0.5)
                break
        sleep(0.5)

    # if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
    #     Toast('不退出房间')
    # else:
    for p in range(2):
        quitTeamRe = shilianTask.quitTeam()
    功能开关["fighting"] = 0
    功能开关["秘境不开宝箱"] = tmpBx

    return


def checkFightType():
    fight_type = ''
    res, fightName = TomatoOcrText(377, 582, 592, 615, "关卡类型")
    if fight_type == '' and has_common_chars("恶龙大通缉", fightName, 2):
        fight_type = "恶龙带队"
    if fight_type == '' and has_common_chars("秘境之间", fightName, 2):
        fight_type = "秘境带队"
    if fight_type == '' and has_common_chars("梦魇狂潮", fightName, 2):
        fight_type = "梦魇带队"
    if fight_type == '' and has_common_chars("绝境挑战", fightName, 2):
        fight_type = "绝境带队"
    if fight_type == '' and has_common_chars("终末战", fightName, 2):
        fight_type = "终末战带队"
    if fight_type == '' and has_common_chars("忆战回环", fightName, 2):
        fight_type = "忆战回环带队"
    if fight_type == '' and has_common_chars("大暴走", fightName, 2):
        fight_type = "暴走带队"
    if fight_type == '' and has_common_chars("斗歌会", fightName, 2):
        fight_type = "斗歌会带队"
    if fight_type == '' and has_common_chars("使徒来袭", fightName, 2):
        fight_type = "使徒来袭带队"
    if fight_type == '' and has_common_chars("莱茵幻境", fightName, 2):
        fight_type = "斗歌会带队"
    if fight_type == '' and has_common_chars("桎梏之形", fightName, 2):
        fight_type = "桎梏之形带队"
    if fight_type == '' and has_common_chars("三打三守三魔头", fightName, 2):
        fight_type = "三魔头带队"
    if fight_type == '' and has_common_chars("调查队", fightName, 2):
        fight_type = "调查队带队"

    if fight_type == '':
        for k in range(2):
            if fight_type != '':
                break
            if fight_type == '':
                resELong1, _ = TomatoOcrText(405, 588, 498, 615, "恶龙大通缉")  # 恶龙邀请
                if resELong1:
                    fight_type = "恶龙带队"
                    break
            if fight_type == '':
                resMiJing1, _ = TomatoOcrText(405, 588, 480, 611, "秘境之间")  # 秘境邀请
                if resMiJing1:
                    fight_type = "秘境带队"
                    break
            if fight_type == '':
                resMengYan1, _ = TomatoOcrText(404, 587, 480, 611, "梦魇狂潮")  # 梦魇邀请
                if not resMengYan1:
                    resMengYan1, _ = TomatoOcrText(443, 590, 481, 612, "狂潮")  # 梦魇邀请
                if resMengYan1:
                    fight_type = "梦魇带队"
                    break
            if fight_type == '':
                # bitmap = screen.capture(380, 583, 510, 615)
                # resJueJing1 = TomatoOcrFindRange("绝境挑战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                #                                  bitmap=bitmap)  # 绝境邀请
                resJueJing1, _ = TomatoOcrText(405, 589, 480, 612, "绝境挑战")  # 绝境邀请
                if resJueJing1:
                    fight_type = "绝境带队"
                    break
            if fight_type == '':
                # resZhongMo1 = TomatoOcrFindRange("终末战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                #                                  bitmap=bitmap)  # 终末战邀请
                resZhongMo1, _ = TomatoOcrText(406, 589, 461, 610, "终末战")  # 绝境邀请
                if resZhongMo1:
                    fight_type = "终末战带队"
                    break
                if fight_type == '':
                    resDiaoCha1 = TomatoOcrFindRange("调查队", 0.9, 380, 583, 510, 615, match_mode='fuzzy')  # 调查队邀请
                    if resDiaoCha1:
                        fight_type = "调查队带队"
                        break
            if fight_type == '':
                res1, _ = TomatoOcrText(404, 587, 480, 611, "忆战回环")  # 忆战回环邀请
                res2, _ = TomatoOcrText(442, 588, 480, 609, "回环")  # 忆战回环邀请
                if res1 or res2:
                    fight_type = "忆战回环带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(405, 587, 462, 611, "大暴走")  # 大暴走
                res2, _ = TomatoOcrText(460, 614, 498, 637, "大王")  # 大暴走
                if res1 or res2:
                    fight_type = "暴走带队"
                    break

            if 功能开关['斗歌会自动接收邀请'] == 1 and fight_type == '':
                res1, _ = TomatoOcrText(385, 612, 483, 637, "斗歌金元花")  # 斗歌金元花
                res2, _ = TomatoOcrText(407, 591, 461, 610, "斗歌会")  # 斗歌会
                if res1 or res2:
                    fight_type = "斗歌会带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(442, 588, 479, 609, "之形")  # 桎梏之形
                if res1:
                    fight_type = "桎梏之形带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(382, 609, 524, 639, "三打三守三魔头")  # 三魔头邀请
                res2, _ = TomatoOcrText(380, 613, 460, 640, "三打三守")  # 三魔头邀请
                if res1 or res2:
                    fight_type = "三魔头带队"
                    break

            # if fight_type == '':
            #     fight_type = '暴走带队'
    return fight_type


def has_common_chars(A, B, min_length=4):
    if A == B:
        return True

    # 将字符串转换为集合以获取唯一字符
    set_A = set(A)
    set_B = set(B)

    # 计算两个集合的交集
    common_chars = set_A.intersection(set_B)

    # 检查交集的大小是否至少为4
    return len(common_chars) >= min_length
