# 导包
from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关
from .shilian import ShiLianTask

shilianTask = ShiLianTask()


# 实例方法
def main():
    if 功能开关["冒险总开关"] == 1 and (
            功能开关["秘境自动接收邀请"] == 1 or 功能开关['梦魇自动接收邀请'] == 1 or 功能开关['恶龙自动接收邀请'] == 1 or 功能开关['暴走自动接收邀请'] == 1):
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
    # 判断体力用尽提示
    res3, _ = TomatoOcrText(242, 598, 314, 616, "体力不足")
    if res3:
        if 功能开关["秘境无体力继续"]:
            Toast("秘境任务 - 体力不足继续挑战")
            res = TomatoOcrTap(334, 743, 385, 771, "确定")

    if not res1 and not res2:
        quitTeamRe = shilianTask.quitTeam()
        功能开关["fighting"] = 0
        功能开关["秘境不开宝箱"] = tmpBx
        return

    fight_type = '暴走带队'
    if res1:
        for i in range(1, 3):
            resMengYan1, _ = TomatoOcrText(404, 587, 480, 611, "梦魇狂潮")  # 梦魇邀请
            resMengYan2, _ = TomatoOcrText(443, 590, 481, 612, "狂潮")  # 梦魇邀请
            if resMengYan1 or resMengYan2:
                fight_type = "梦魇带队"
                break
        for i in range(1, 3):
            resELong1, _ = TomatoOcrText(405, 588, 498, 615, "恶龙大通缉")  # 恶龙邀请
            if resELong1:
                fight_type = "恶龙带队"
                break
        for i in range(1, 3):
            resMiJing1, _ = TomatoOcrText(405, 588, 480, 611, "秘境之间")  # 秘境邀请
            if resMiJing1:
                fight_type = "秘境"
                break
        for i in range(1, 3):
            resJueJing1 = TomatoOcrFindRange("绝境挑战", 0.9, 380, 583, 510, 615, match_mode='fuzzy')  # 绝境邀请
            # resJueJing1, _ = TomatoOcrText(405, 588, 483, 610, "绝境挑战")  # 绝境邀请
            if resJueJing1:
                fight_type = "绝境"
                break
        for i in range(1, 3):
            resZhongMo1 = TomatoOcrFindRange("终末战", 0.9, 380, 583, 510, 615, match_mode='fuzzy')  # 终末战邀请
            if resZhongMo1:
                fight_type = "终末战"
                break

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
        if fight_type == '绝境':
            # if 功能开关['绝境自动接收邀请'] == 0:
            Toast('绝境带队未开启，拒绝绝境组队邀请')
            功能开关["fighting"] = 0
            return
        if fight_type == '终末战':
            # if 功能开关['绝境自动接收邀请'] == 0:
            Toast('终末战带队未开启，拒绝终末战组队邀请')
            功能开关["fighting"] = 0
            return
        res1 = TomatoOcrTap(584, 651, 636, 678, "同意")

    waitFight = False
    for i in range(1, 4):
        waitTime = (i - 1) * 10
        Toast(f'等待队长开始{waitTime}/30s')
        sleep(5)
        waitFight = shilianTask.WaitFight(fightType=fight_type)
        if waitFight:
            break
        sleep(5)
    if not waitFight:
        Toast(f'等待进入战斗超时，退出组队')

    quitTeamRe = shilianTask.quitTeam()
    功能开关["fighting"] = 0
    功能开关["秘境不开宝箱"] = tmpBx

    return
