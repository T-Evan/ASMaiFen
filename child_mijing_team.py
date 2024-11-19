# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关, 任务记录
from .shilian import ShiLianTask
from ascript.android.screen import FindColors

shilianTask = ShiLianTask()


# 实例方法
def main():
    if 功能开关["秘境自动接收邀请"] == 1 or 功能开关['梦魇自动接收邀请'] == 1 or 功能开关['恶龙自动接收邀请'] == 1 or \
            功能开关['暴走自动接收邀请'] == 1 or 功能开关['终末战自动接收邀请'] == 1 or \
            功能开关['绝境自动接收邀请'] == 1 or 功能开关['调查队自动接收邀请'] == 1:
        while True:
            sleep(5)  # 等待 5 秒
            # res1, _ = TomatoOcrText(498,184,585,214, "离开队伍")
            # if res1:
            #     Toast('已在房间中，跳过组队邀请识别')
            #     continue
            if 功能开关["fighting"] == 0:
                # 识别角色名称，做特殊逻辑
                if 任务记录["自动入队-AI发言"] == 0:
                    res, name = TomatoOcrText(97, 80, 197, 102, '玩家名称')
                    if name == '咸鱼搜麦乐芬':
                        任务记录["自动入队-AI发言"] = 1
                Toast('等待组队邀请')
                waitInvite()


def waitInvite():
    tmpBx = 功能开关["秘境不开宝箱"]
    功能开关["秘境不开宝箱"] = 1

    res1, _ = TomatoOcrText(584, 651, 636, 678, "同意")
    res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备
    res3, _ = TomatoOcrText(450, 651, 506, 683, "准备")  # 恶龙准备

    fight_type = ''
    if not res1 and not res2 and not res3:
        res = TomatoOcrTap(615, 558, 686, 582, "正在组队")
        sleep(1)
        res, _ = TomatoOcrText(402, 337, 442, 361, "险境")
        if res:
            fight_type = '绝境带队'

        if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
            Toast('不退出房间')
        else:
            # 兜底结束战斗
            res = TomatoOcrFindRangeClick('自动准备', x1=176, y1=1167, x2=517, y2=1257, offsetY=30, match_mode='fuzzy')
            if res:
                sleep(3)

            quitTeamRe = shilianTask.quitTeam()
            功能开关["秘境不开宝箱"] = tmpBx
            return

    if res1:
        功能开关["fighting"] = 1
        if fight_type == '':
            for i in range(1, 4):
                resMengYan1, _ = TomatoOcrText(404, 587, 480, 611, "梦魇狂潮")  # 梦魇邀请
                resMengYan2, _ = TomatoOcrText(443, 590, 481, 612, "狂潮")  # 梦魇邀请
                if resMengYan1 or resMengYan2:
                    fight_type = "梦魇带队"
                    break
        if fight_type == '':
            for i in range(1, 4):
                resELong1, _ = TomatoOcrText(405, 588, 498, 615, "恶龙大通缉")  # 恶龙邀请
                if resELong1:
                    fight_type = "恶龙带队"
                    break
        if fight_type == '':
            for i in range(1, 4):
                resMiJing1, _ = TomatoOcrText(405, 588, 480, 611, "秘境之间")  # 秘境邀请
                if resMiJing1:
                    fight_type = "秘境"
                    break
        if fight_type == '':
            bitmap = screen.capture(380, 583, 510, 615)
            for i in range(1, 4):
                resJueJing1 = TomatoOcrFindRange("绝境挑战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                                                 bitmap=bitmap)  # 绝境邀请
                # resJueJing1, _ = TomatoOcrText(405, 588, 483, 610, "绝境挑战")  # 绝境邀请
                if resJueJing1:
                    fight_type = "绝境带队"
                    break
        if fight_type == '':
            bitmap = screen.capture(380, 583, 510, 615)
            for i in range(1, 4):
                resZhongMo1 = TomatoOcrFindRange("终末战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                                                 bitmap=bitmap)  # 终末战邀请
                if resZhongMo1:
                    fight_type = "终末战带队"
                    break
        if fight_type == '':
            bitmap = screen.capture(380, 583, 510, 615)
            for i in range(1, 4):
                resDiaoCha1 = TomatoOcrFindRange("调查队", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                                                 bitmap=bitmap)  # 调查队邀请
                if resDiaoCha1:
                    fight_type = "调查队带队"
                    break

        if fight_type == '':
            fight_type = '暴走带队'

        if fight_type == '梦魇带队':
            if 功能开关['梦魇自动接收邀请'] == 0:
                Toast('梦魇带队未开启，拒绝梦魇组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意梦魇组队邀请')

        if fight_type == '恶龙带队':
            if 功能开关['恶龙自动接收邀请'] == 0:
                Toast('恶龙带队未开启，拒绝恶龙组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意恶龙组队邀请')

        if fight_type == '暴走带队':
            if 功能开关['暴走自动接收邀请'] == 0:
                Toast('暴走带队未开启，拒绝暴走组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意暴走组队邀请')

        if fight_type == '秘境':
            if 功能开关['秘境自动接收邀请'] == 0:
                Toast('秘境带队未开启，拒绝秘境组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意秘境组队邀请')
        if fight_type == '绝境带队':
            if 功能开关['绝境自动接收邀请'] == 0:
                Toast('绝境带队未开启，拒绝绝境组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意绝境组队邀请')
        if fight_type == '终末战带队':
            if 功能开关['终末战自动接收邀请'] == 0:
                Toast('终末战带队未开启，拒绝终末战组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意终末战组队邀请')
        if fight_type == '调查队带队':
            if 功能开关['调查队自动接收邀请'] == 0:
                Toast('调查队带队未开启，拒绝调查队组队邀请')
                功能开关["fighting"] = 0
                return
            else:
                Toast('同意调查队组队邀请')
        res1 = TomatoOcrTap(584, 651, 636, 678, "同意")
        if res1:
            # 判断体力用尽提示
            res = TomatoOcrFindRangeClick("确定", sleep1=0.3, whiteList='确定', x1=105, y1=290, x2=625, y2=1013)

    waitFight = False
    findDoneStatus = False
    waitTime = 0
    for i in range(25):
        waitTime = waitTime + 1
        Toast(f'{fight_type}-等待队长开始{waitTime}/50s')

        # 返回房间
        failTeam = 0
        for j in range(5):
            res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
            res7, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
            if res6 or res7:
                # 兜底，已在队伍中时，停止返回操作
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                break

            res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备
            res3, _ = TomatoOcrText(450, 651, 506, 683, "准备")  # 恶龙准备
            if res2 or res3:
                break

            # 兜底结束战斗
            res = TomatoOcrFindRangeClick('自动准备', x1=176, y1=1167, x2=517, y2=1257, offsetY=30, match_mode='fuzzy')
            if res:
                sleep(3)


            res1 = TomatoOcrTap(651, 559, 682, 577, "组队")
            # 兜底入队失败
            res2 = TomatoOcrTap(584, 651, 636, 678, "同意", sleep1=0.8)
            if res2:
                # 判断体力用尽提示
                res = TomatoOcrFindRangeClick("确定", sleep1=0.3, whiteList='确定', x1=105, y1=290, x2=625, y2=1013)

            if not res1 and not res2:
                Toast(f'未进入房间{j}/ 5')
                failTeam = failTeam + 1
            sleep(0.5)
        if failTeam > 3:
            break

        # 房间 - 特殊状态识别
        if fight_type == '梦魇带队' and not findDoneStatus:
            re1, _ = TomatoOcrText(427, 374, 489, 399, "24/24")
            re2, _ = TomatoOcrText(431, 375, 486, 404, "24/24")
            re3, _ = TomatoOcrText(453, 298, 510, 331, "无尽")
            if (not re1 and not re2) or (re3 and 功能开关['梦魇无尽自动离队'] == 1):
                Toast('梦魇 - 未完成挑战 - 进入战斗后等待战斗结束')
                fight_type = '梦魇挑战'
            else:
                findDoneStatus = True
                Toast('梦魇 - 已完成挑战 - 进入战斗后自动留影')

        if fight_type == '恶龙带队' and not findDoneStatus:
            # 判断是否为当前等级地图
            re, levelName1 = TomatoOcrText(365, 283, 440, 307, '建议职业')
            re, levelName2 = TomatoOcrText(142, 602, 200, 621, '当前职业')
            if levelName1 == levelName2:
                # 判断是否未开宝箱
                re1 = CompareColors.compare(
                    "533,356,#DFB86D|533,348,#FAEAA8|536,339,#FFECB0|554,358,#EBC87E|552,350,#D79335")
                # 未开宝箱，不退队
                if not re1:
                    Toast('恶龙 - 未完成挑战 - 进入战斗后等待战斗结束')
                    fight_type = '恶龙挑战'
            else:
                findDoneStatus = True
                Toast('恶龙 - 已完成挑战 - 进入战斗后自动留影')

        res6, _ = TomatoOcrText(501, 191, 581, 217, "离开队伍")  # 已在队伍页面，直接退出
        res7, _ = TomatoOcrText(503, 186, 582, 213, "离开队伍")  # 已在队伍页面，直接退出
        if res6 or res7:
            shilianTask.teamShoutAI(f'{fight_type}-等待开始~祝你游戏开心~', type='room')

        # 判断队友全部离队，退出房间
        if fight_type == '恶龙带队' or fight_type == '恶龙挑战':
            allQuit, _ = TomatoOcrText(325, 558, 393, 585, "等待加入")
            if not allQuit:
                allQuit = CompareColors.compare(
                    "186,405,#F2C173|189,405,#F2C173|192,405,#FFF5B4|194,405,#F4C376|192,399,#FCF1B3")  # 判断是否成为房主
        else:
            allQuit, _ = TomatoOcrText(168, 804, 233, 831, "等待加入")
            if not allQuit:
                team4 = CompareColors.compare(
                    "217,280,#FDF3B6|221,279,#F2C274|224,280,#FFF6B5|221,276,#FFF7B6|230,287,#EBE3A7")  # 判断是否成为房主
                team5 = CompareColors.compare(
                    "187,404,#F2C174|189,404,#F3C379|191,400,#FFF7B6|192,405,#FFF5B4|198,400,#E9DAA2")  # 终末战 - 判断是否成为房主
                if team4 or team5:
                    allQuit = True

        if allQuit:
            Toast('队友全部离队')
            quitTeamRe = shilianTask.quitTeam()
            sleep(1)
            break

        waitFight = shilianTask.WaitFight(fightType=fight_type)
        if waitFight:
            waitTime = 0
        sleep(1)
    if waitTime > 50:
        Toast(f'等待进入战斗超时，退出组队')

    # if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
    #     Toast('不退出房间')
    # else:
    quitTeamRe = shilianTask.quitTeam()
    功能开关["fighting"] = 0
    功能开关["秘境不开宝箱"] = tmpBx

    return
