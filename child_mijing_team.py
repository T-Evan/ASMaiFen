# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关
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
            Toast('等待组队邀请')
            waitInvite()


def waitInvite():
    功能开关["fighting"] = 1
    tmpBx = 功能开关["秘境不开宝箱"]
    功能开关["秘境不开宝箱"] = 1

    res1, _ = TomatoOcrText(584, 651, 636, 678, "同意")
    res2, _ = TomatoOcrText(457, 607, 502, 631, "准备")  # 秘境准备

    fight_type = ''
    if not res1 and not res2:
        res = TomatoOcrTap(615, 558, 686, 582, "正在组队")
        sleep(1)
        res, _ = TomatoOcrText(402, 337, 442, 361, "险境")
        if res:
            fight_type = '绝境带队'
        if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
            Toast('不退出房间')
        else:
            quitTeamRe = shilianTask.quitTeam()
            功能开关["fighting"] = 0
            功能开关["秘境不开宝箱"] = tmpBx
            return

    if res1:
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
    for i in range(1, 25):
        waitTime = (i - 1) * 2
        Toast(f'等待队长开始{waitTime}/50s')

        # 未进入房间兜底
        res1 = TomatoOcrTap(584, 651, 636, 678, "同意")
        if res1:
            # 判断体力用尽提示
            res = TomatoOcrFindRangeClick("确定", sleep1=0.3, whiteList='确定', x1=105, y1=290, x2=625, y2=1013)

        # 房间 - 特殊状态识别
        if fight_type == '梦魇带队' and not findDoneStatus:
            re1, _ = TomatoOcrText(445, 375, 500, 402, "24/24")
            re2, _ = TomatoOcrText(453, 298, 510, 331, "无尽")
            if not re1 or re2:
                Toast('梦魇 - 未完成挑战 - 进入战斗后等待战斗结束')
                fight_type = '梦魇挑战'
            else:
                findDoneStatus = True
                Toast('梦魇 - 已完成挑战 - 进入战斗后自动留影')
        # 返回房间
        res1 = TomatoOcrTap(651, 559, 682, 577, "组队")
        if fight_type == '恶龙带队' and not findDoneStatus:
            # 判断是否未开宝箱
            re1 = CompareColors.compare("325,356,#F2A949|334,356,#F2A949|342,358,#F2A949")
            # 未开宝箱，不退队
            if not re1:
                Toast('恶龙 - 未完成挑战 - 进入战斗后等待战斗结束')
                fight_type = '恶龙挑战'
            else:
                findDoneStatus = True
                Toast('恶龙 - 已完成挑战 - 进入战斗后自动留影')
        waitFight = shilianTask.WaitFight(fightType=fight_type)
        if waitFight:
            break
        # 判断队友全部离队，退出房间
        allQuit, _ = TomatoOcrText(168, 804, 233, 831, "等待加入")
        if allQuit:
            Toast('队友全部离队')
            quitTeamRe = shilianTask.quitTeam()
            sleep(1)
            break
        sleep(2)
    if not waitFight:
        Toast(f'等待进入战斗超时，退出组队')

    if fight_type == '绝境带队' and 功能开关['绝境不退出房间'] == 1:
        Toast('不退出房间')
    else:
        quitTeamRe = shilianTask.quitTeam()
    功能开关["fighting"] = 0
    功能开关["秘境不开宝箱"] = tmpBx

    return
